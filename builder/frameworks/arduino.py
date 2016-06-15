# Copyright 2014-present Ivan Kravets <me@ikravets.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.DevPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinointel")
FRAMEWORK_VERSION = platform.get_package_version("framework-arduinointel")
assert isdir(FRAMEWORK_DIR)

# USB flags
ARDUINO_USBDEFINES = [
    "ARDUINO=10608",
    "ARDUINO_FRAMEWORK=%s" % FRAMEWORK_VERSION.split(".")[1]
]
if "build.usb_product" in env.BoardConfig():
    ARDUINO_USBDEFINES += [
        "USB_VID=%s" % env.BoardConfig().get("build.hwids")[0][0],
        "USB_PID=%s" % env.BoardConfig().get("build.hwids")[0][1],
        'USB_PRODUCT=\\"%s\\"' % (
            env.BoardConfig().get("build.usb_product", "").replace('"', "")),
        'USB_MANUFACTURER=\\"%s\\"' % (
            env.BoardConfig().get("vendor", "").replace('"', ""))
    ]

env.Prepend(
    CPPDEFINES=ARDUINO_USBDEFINES,
    CPPPATH=[
        join(FRAMEWORK_DIR, "system", "libarc32_arduino101", "drivers"),
        join(FRAMEWORK_DIR, "system", "libarc32_arduino101", "common"),
        join(FRAMEWORK_DIR, "system", "libarc32_arduino101", "framework",
             "include"),
        join(FRAMEWORK_DIR, "system", "libarc32_arduino101", "bootcode"),
        join("$BUILD_DIR", "IntelDrivers"),
        join("$BUILD_DIR", "FrameworkArduino")
    ],

    LIBPATH=[
        join(
            FRAMEWORK_DIR, "variants",
            env.BoardConfig().get("build.variant")
        ),
        join(
            FRAMEWORK_DIR, "variants",
            env.BoardConfig().get("build.variant"),
            "linker_scripts"
        )
    ]
)

env.Append(
    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries", "__cores__",
             env.BoardConfig().get("build.core", "")),
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join("$BUILD_DIR", "FrameworkArduinoVariant")
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
    ))

envsafe = env.Clone()

if env.subst("$BOARD") == "genuino101":
    libs.append("libarc32drv_arduino101")

libs.append(envsafe.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores", env.BoardConfig().get("build.core"))
))

env.Prepend(LIBS=libs)
