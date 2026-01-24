#!/bin/zsh
KERNEL=$(chariot path custom/kernel -o arch=x86_64 --raw)/kernel.elf
gdb --ex "file $KERNEL" --ex "set substitute-path ../sources ../"