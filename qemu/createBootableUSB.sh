#!/bin/sh

# Sample script to create an Ubuntu Linux Bootable USB
# If EFI is a requirement, install the package: 
# qemu-efi from https://packages.ubuntu.com/xenial/misc/qemu-efi

USB_DISK=/dev/sdc
ISO=/tmp/ubuntu-18.04.2-live-server-amd64.iso 

efi=$1

if [ ${efi} -eq 1 ]; then
   OVMF_CODE_OPT="-drive if=pflash,format=raw,readonly,file=/usr/share/OVMF/OVMF_CODE.fd"
   OVMF_VARS_OPT="-drive if=pflash,format=raw,file=/usr/share/OVMF/OVMF_VARS.fd"
fi

qemu-system-x86_64 -hda ${USB_DISK} -cdrom ${ISO} -boot b --enable-kvm -m 8G -machine smm=off -smp 10 ${OVMF_CODE_OPT} ${OVMF_VARS_OPT}

