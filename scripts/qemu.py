#!/usr/bin/env python3
# parse --arm --tcg --kvm --pause
import chariot_utils
import sys
import subprocess
import os
# check if ovmf firmware exists
if not os.path.exists("edk2-ovmf"):
    r = subprocess.run("curl -L https://github.com/osdev0/edk2-ovmf-nightly/releases/latest/download/edk2-ovmf.tar.gz | gunzip | tar -xf -", shell=True)
    if r.returncode != 0:
        print("Failed to download OVMF firmware")
        exit(1)

ARCH = "x86_64"
ACCEL = "tcg"
PAUSE = False
UEFI = False
for arg in sys.argv[1:]:
    if arg == "--uefi":
        UEFI = True
    elif arg == "--arm":
        ARCH = "aarch64"
    elif arg == "--tcg":
        ACCEL = "tcg"
    elif arg == "--kvm":
        ACCEL = "kvm"
    elif arg == "--pause":
        PAUSE = True

if ARCH != "x86_64":
    UEFI = True

if chariot_utils.build(["source/kernel", "source/test_app", "source/init_system", "custom/image"], options=["-o", f"arch={ARCH}"]).returncode != 0:
    print("Build failed")
    exit(1)

qemu_cmd = [
    "qemu-system-" + ARCH,
    "-m", "512m",
    "-accel", ACCEL,
    "--no-reboot",
    "--no-shutdown",
    "-s",
    "-smp", "cpus=2",
    "-cdrom", f"{chariot_utils.path("custom/image", options=["-o", f"arch={ARCH}"]).strip()}/output.iso",
    "-d", "int,cpu_reset",
    "-D", "qemu_err.log"
]

if UEFI:
    qemu_cmd += [
        "-drive", f"if=pflash,unit=0,format=raw,file=edk2-ovmf/ovmf-code-{ARCH}.fd,readonly=on"
    ]

if ARCH == "x86_64":
    qemu_cmd += [
        "-M", "q35",
        "-debugcon", "stdio"
    ]
    if ACCEL == "kvm":    
        qemu_cmd += [
            "-accel", "kvm" ,
            "-cpu", "host,lkgs=on,fred=on,invtsc=on,x2apic=on,xsave=on,xsaveopt=on,xsavec=on,xsaves=on,avx=on,avx2=on,fma=on"
        ]
    else:
        qemu_cmd += [
            "-accel", "tcg" ,
            "-cpu", "Skylake-Client,lkgs=on,fred=on,invtsc=on,x2apic=on,xsave=on,xsaveopt=on,xsavec=on,xsaves=on,avx=on,avx2=on,fma=on"
        ]
elif ARCH == "aarch64":
    qemu_cmd += [
        "-M", "virt,gic-version=3",
        "-cpu", "cortex-a57",
        "-device", "ramfb",
        "-device", "qemu-xhci",
        "-device", "usb-kbd",
        "-device", "usb-mouse",
    ]

if PAUSE:
    qemu_cmd += ["-S"]

print(qemu_cmd)
subprocess.run(qemu_cmd)