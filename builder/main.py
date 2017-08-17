# Copyright 2014-present PlatformIO <contact@platformio.org>
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

from os.path import join

from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default,
                          DefaultEnvironment)

env = DefaultEnvironment()


def BeforeUpload(target, source, env):  # pylint: disable=W0613,W0621
    env.AutodetectUploadPort()
    if env.BoardConfig().get("upload.use_1200bps_touch", False):
        env.TouchSerialPort("$UPLOAD_PORT", 1200)


env.Replace(
    AR="arc-elf32-ar",
    AS="arc-elf32-as",
    CC="arc-elf32-gcc",
    CXX="arc-elf32-g++",
    GDB="arc-elf32-gdb",
    OBJCOPY="arc-elf32-objcopy",
    RANLIB="arc-elf32-ranlib",
    SIZETOOL="arc-elf32-size",

    ARFLAGS=["rcs"],

    ASFLAGS=["-x", "assembler-with-cpp"],

    CFLAGS=["-std=gnu11"],

    CCFLAGS=[
        "-g",
        "-Os",
        "-ffunction-sections",
        "-fdata-sections",
        "-Wall",
        "-mlittle-endian",
        "-mcpu=" + env.BoardConfig().get("build.cpu"),
        "-fno-reorder-functions",
        "-fno-asynchronous-unwind-tables",
        "-fno-omit-frame-pointer",
        "-fno-defer-pop",
        "-Wno-unused-but-set-variable",
        "-Wno-main",
        "-ffreestanding",
        "-fno-stack-protector",
        "-mno-sdata",
        "-fsigned-char"
    ],

    CXXFLAGS=[
        "-fno-rtti",
        "-std=c++11",
        "-fno-exceptions",
        "-fcheck-new"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU"),
        "ARDUINO_ARC32_TOOLS",
        "__CPU_ARC__",
        ("CLOCK_SPEED",
         int(int(env.BoardConfig().get(
            "build.f_cpu").replace("L", "")) / 1000000)),
        "CONFIG_SOC_GPIO_32",
        "CONFIG_SOC_GPIO_AON",
        "INFRA_MULTI_CPU_SUPPORT",
        "CFW_MULTI_CPU_SUPPORT",
        "HAS_SHARED_MEM"
    ],

    LINKFLAGS=[
        "-Os",
        "-Wl,--gc-sections",
        "-Wl,-X",
        "-Wl,-N",
        "-Wl,-mcpu=" + env.BoardConfig().get("build.cpu"),
        "-Wl,-marcelf",
        "-static",
        "-nostdlib",
        "-nodefaultlibs",
        "-nostartfiles",
        "-Wl,--whole-archive",
        "-larc32drv_arduino101",
        "-Wl,--no-whole-archive"
    ],

    LIBS=["nsim", "c", "m", "gcc"],

    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    UPLOADER="arduino101load",
    UPLOADERFLAGS=[
        ("-dfu", join(env.PioPlatform().get_package_dir(
                 "tool-arduino101load") or "", "dfu-util")),
        ("-bin", "$SOURCES"),
        ("-port", '"$UPLOAD_PORT"'),
        ("-ble_fw_str", '\"ATP1BLE00R-1631C4439\"'),
        ("-ble_fw_pos", 169984),
        ("-rtos_fw_str", '\"\"'),
        ("-rtos_fw_pos", 0),
        ("-core", "2.0.0"),
        "-v"
    ],
    UPLOADCMD='$UPLOADER $UPLOADERFLAGS',

    PROGNAME="firmware",
    PROGSUFFIX=".elf"
)

env.Append(
    ASFLAGS=env.get("CCFLAGS", [])[:],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-S",
                "-O",
                "binary",
                "-R",
                ".note",
                "-R",
                ".comment",
                "-R",
                "COMMON",
                "-R",
                ".eh_frame",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".bin"
        ),
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-S",
                "-O",
                "binary",
                "-R",
                ".note",
                "-R",
                ".comment",
                "-R",
                "COMMON",
                "-R",
                ".eh_frame",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".hex"
        )
    )
)

#
# Target: Build executable and linkable firmware
#

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_firm = join("$BUILD_DIR", "firmware.bin")
else:
    target_elf = env.BuildProgram()
    target_firm = env.ElfToBin(join("$BUILD_DIR", "firmware"), target_elf)

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload firmware
#

target_upload = env.Alias(
    "upload", target_firm,
    [env.VerboseAction(BeforeUpload, "Looking for upload port..."),
     env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")])
AlwaysBuild(target_upload)

#
# Default targets
#

Default([target_buildprog, target_size])
