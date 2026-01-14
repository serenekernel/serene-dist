#!/bin/zsh
set -e
chariot build source/kernel
chariot build source/test_app
chariot build source/init_system
chariot build custom/image

# parse args
# --tgc
# --kvm
# --pause
ARGS=()
ACCEL="tcg"
for arg in "$@"; do
    case $arg in
        --tcg)
            ACCEL="tcg"
            ;;
        --kvm)
            ACCEL="kvm"
            ;;
        --pause)
            ARGS+=("-S")
            ;;
        *)
            echo "Unknown argument: $arg"
            exit 1
            ;;
    esac
done


ARGS+=("-cdrom" "$(chariot path custom/image)/output.iso")
ARGS+=("-d" "int,cpu_reset" "-D" "qemu_err.log")


if [ "$ACCEL" = "kvm" ]; then
    ARGS+=("-accel" "kvm" "-cpu" "host,invtsc=on,x2apic=on,xsave=on,xsaveopt=on,xsavec=on,xsaves=on,avx=on,avx2=on,fma=on,smm=off")
elif [ "$ACCEL" = "tcg" ]; then
    ARGS+=("-accel" "tcg" "-cpu" "Skylake-Client,invtsc=on,x2apic=on,xsave=on,xsaveopt=on,xsavec=on,xsaves=on,avx=on,avx2=on,fma=on")
fi

qemu-system-x86_64 -m 512M --no-reboot --no-shutdown -s -smp cpus=2 -M q35 -debugcon stdio "${ARGS[@]}"