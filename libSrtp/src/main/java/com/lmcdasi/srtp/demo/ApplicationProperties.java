package com.lmcdasi.srtp.demo;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import lombok.Getter;
import lombok.Setter;


@Configuration
@ConfigurationProperties(prefix = "application")
public class ApplicationProperties {
	@Getter @Setter
	private boolean srtpDebug;
}
