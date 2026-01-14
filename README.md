# serene-dist

Build system and distribution configuration for Serene.

## Overview

This directory contains the [Chariot](https://github.com/elysium-os/chariot) build configuration for building and packaging the complete Serene distribution, including the kernel and userspace applications.
## Structure

- `recipes/` - Build recipes for all components
  - `image.chariot` - Disk image generation
  - `packages/` - Userspace package recipes
  - `system/` - Kernel and system component recipes
  - `tools/` - Build tool recipes

- `scripts/` - Helper scripts for building and testing

## Usage

Build and install [Chariot](https://github.com/elysium-os/chariot) if you haven't already.
Clone the Serene distribution repository and run 
```bash
chariot build custom/kernel (builds just the kernel)
chariot build package/init_system (build just the init_system)
chariot build package/test_app (builds just the test_app)
chariot build custom/image (builds a full iso with the default packages)

```

## Configuration

Architecture and build type can be configured in [config.chariot](config.chariot).
While x86_64 is the primary supported architecture, *hopefully* other architectures will be supported in the future.
