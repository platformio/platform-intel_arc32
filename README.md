# Intel ARC32: development platform for [PlatformIO](http://platformio.org)
[![Build Status](https://travis-ci.org/platformio/platform-intel_arc32.svg?branch=develop)](https://travis-ci.org/platformio/platform-intel_arc32)
[![Build status](https://ci.appveyor.com/api/projects/status/o2mw4111t1yjqch7/branch/develop?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-intel_arc32/branch/develop)

ARC embedded processors are a family of 32-bit CPUs that are widely used in SoC devices for storage, home, mobile, automotive, and Internet of Things applications.

* [Home](https://registry.platformio.org/platforms/platformio/intel_arc32) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/intel_arc32.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = intel_arc32
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-intel_arc32.git
board = ...
...
```

# Configuration

Please navigate to [documentation](https://docs.platformio.org/page/platforms/intel_arc32.html).
