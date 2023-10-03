package com.lmcdasi.srtp.demo.srtp;

import java.lang.foreign.Arena;
import java.lang.foreign.FunctionDescriptor;
import java.lang.foreign.Linker;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.SymbolLookup;
import java.lang.foreign.ValueLayout;
import java.lang.invoke.MethodHandles;
import java.nio.file.Path;
import java.util.Arrays;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.BeanCreationException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.lmcdasi.srtp.demo.ApplicationProperties;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;

@Component
public class SrtpComponent {
	private final static Logger LOGGER = LoggerFactory.getLogger(SrtpComponent.class);

	private ApplicationProperties applicationProperties;
	private Arena srtpArena;
	
	@Autowired
	public void setApplicationProperties(final ApplicationProperties applicationProperties) {
		this.applicationProperties = applicationProperties;
	}
	
	@PostConstruct
	void init() {
		LOGGER.info("SrtpComponent init");
		srtpArena = Arena.ofConfined();
		final var soSrtpPath = Path.of("/usr/lib/x86_64-linux-gnu/libsrtp2.so.1");
		final var libSrtp = SymbolLookup.libraryLookup(soSrtpPath, srtpArena);
		libSrtp.find("srtp_init").ifPresentOrElse(
			memorySegment -> {
				final var linker = Linker.nativeLinker();
				final var methodHandler = linker.downcallHandle(memorySegment, 
					FunctionDescriptor.of(ValueLayout.JAVA_INT), Linker.Option.isTrivial());
				try {
					final var status = (Integer) methodHandler.invoke();
					
					LOGGER.info("srtp_init status {}.", 
							Arrays.stream(SrtpErrStatusT.values()).filter(e -> e.getValue() == status.intValue()).findFirst().get());
					
					if (applicationProperties.isSrtpDebug()) {
						try {
							setSrtpDebug(linker, libSrtp);
						} catch (final Exception e) {
							LOGGER.warn("Failed to set srtp log callback. Continue without srtp logs.", e);
						}
					}
				} catch (final Throwable e) {
					throw new BeanCreationException("Unable to init srtp library", e);
				}
			},
			() -> {
					throw new BeanCreationException("Unable to find srtp_init.");
			}
		);
	}
	
	@PreDestroy
	void unload() {
		try {
			srtpArena.close();
		} catch (final Exception e) {
			LOGGER.error("Abnormal close of srtp Arena");
		}
	}
	
	private void setSrtpDebug(final Linker linker, final SymbolLookup libSrtp) throws NoSuchMethodException, IllegalAccessException {
		final var logCallbackDescription = FunctionDescriptor.of(
				ValueLayout.ADDRESS.withTargetLayout(ValueLayout.JAVA_INT),
				ValueLayout.ADDRESS.withTargetLayout(ValueLayout.JAVA_INT),
				ValueLayout.ADDRESS.withTargetLayout(ValueLayout.ADDRESS),
				ValueLayout.ADDRESS.withTargetLayout(ValueLayout.ADDRESS)).dropReturnLayout();
		final var logCallbackHandler = MethodHandles.lookup().findStatic(SrtpLogCallback.class, "callback",
				logCallbackDescription.toMethodType());
		final var comparFunc = linker.upcallStub(logCallbackHandler, logCallbackDescription, srtpArena);
		
		libSrtp.find("srtp_install_log_handler").ifPresentOrElse(
			memorySegment -> {
				final var srtpInstallLogHandlerFuntionDesc = FunctionDescriptor.of(
							ValueLayout.JAVA_INT, 
							ValueLayout.ADDRESS,
							ValueLayout.ADDRESS);
				final var methodHandler = linker.downcallHandle(memorySegment, srtpInstallLogHandlerFuntionDesc, Linker.Option.isTrivial());
				try {
					final var status = (Integer) methodHandler.invoke(comparFunc, MemorySegment.NULL);
					LOGGER.info("srtp_install_log_handler status {}.", 
							Arrays.stream(SrtpErrStatusT.values()).filter(e -> e.getValue() == status.intValue()).findFirst().get());
				} catch (final Throwable e) {
					LOGGER.warn("Failed to invoke srtp_install_log_handler.", e);
				}
			},
			()-> {
					LOGGER.warn("No srtp_install_log_handler found. Unable to set srtp log callback.");
			}
		);
		
		libSrtp.find("srtp_set_debug_module").ifPresentOrElse(
			memorySegment -> {
				final var srtpSetDebugModuleFunctionDesc = FunctionDescriptor.of(
							ValueLayout.JAVA_INT,
							ValueLayout.ADDRESS,
							ValueLayout.JAVA_INT);
				final var methodHandler = linker.downcallHandle(memorySegment, srtpSetDebugModuleFunctionDesc, Linker.Option.isTrivial());
				final var modNameMemorySegment = srtpArena.allocateUtf8String("srtp");
				try {
					final var status = (Integer) methodHandler.invoke(modNameMemorySegment, 1);
					LOGGER.info("srtp_set_debug_module status {}.", 
							Arrays.stream(SrtpErrStatusT.values()).filter(e -> e.getValue() == status.intValue()).findFirst().get());
				} catch (final Throwable e) {
					LOGGER.warn("Failed to set srtp debug module.", e);
				}
			},
			() -> {
				LOGGER.warn("No srtp_set_debug_module found. Unable to set srtp debug module.");
			});

        //LOGGER.info("Status enabling debug srtp library {}", libSrtp.srtp_set_debug_module("srtp", 1));
	}
}
