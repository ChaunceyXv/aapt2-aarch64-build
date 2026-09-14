---
name: android-apk-build
description: Build and package Android APKs on this aarch64 proot environment using Gradle + AGP with a natively-compiled aarch64 aapt2 (natively-compiled aarch64 aapt2 (prebuilt included) or QEMU fallback; see repo prebuilt/ + README). Use when the user asks to build/package an APK, run gradle assembleDebug/assembleRelease, set up an Android project, or hits "AAPT2 Daemon startup failed" / "illegal instruction" on arm64.
---

# Android APK 打包（aarch64 proot 环境）

## 环境现状（已部署，勿重复安装）

| 组件 | 位置 | 说明 |
|---|---|---|
| JDK 21 | `java` / `javac` | AGP 运行时 |
| Gradle 9.7.1 | `/usr/local/bin/gradle` | 官方 arm64 发行版 |
| Android SDK | `/opt/android-sdk`（`ANDROID_HOME`） | cmdline-tools v12、platforms;android-35、build-tools;35.0.1，licenses 已接受 |
| **aapt2（原生，默认）** | `/opt/android-sdk/aapt2` | **aarch64 原生编译，速度快，当前默认** |
| aapt2（QEMU 回退） | `/opt/android-sdk/aapt2-qemu` | x86_64 官方二进制 + qemu 模拟，原生版坏时切回 |
| 原生 aapt2 构建树 | `/opt/aapt2-build` | 源码 + CMake（`build-clang/` 产物），可重编译 |
| 全局 Gradle 属性 | `~/.gradle/gradle.properties` | `android.aapt2FromMavenOverride=/opt/android-sdk/aapt2` |

## 核心原理

Google 官方 maven 只发布 x86_64 的 aapt2（`aapt2-<ver>-linux.jar`，无 aarch64 变体）。
两种解决路径（都已打通）：

1. **原生编译（首选）**：AOSP 源码（`platform/frameworks/base/tools/aapt2`，
   标签 `platform-tools-35.0.2`，对应 aapt2 8.5.x）+ host CMake + 系统依赖
   （protobuf 3.21 / expat / png / pcre2 / openssl），clang 19 编出 aarch64 glibc 原生
   aapt2。已构建于 `/opt/aapt2-build/build-clang/aapt2`。
2. **QEMU 模拟（回退）**：`qemu-x86_64` 用户态跑官方 x86_64 aapt2。

两条路径都通过 AGP 的 `android.aapt2FromMavenOverride` 接入。

### 切回 QEMU 版（原生版出问题/换版本不匹配时）

```sh
cp /opt/android-sdk/aapt2-qemu /opt/android-sdk/aapt2
```

QEMU 包装脚本内容（`aapt2-qemu`）：
```sh
#!/bin/sh
export QEMU_LD_PREFIX=/opt/x86_64-root
exec /usr/bin/qemu-x86_64 /opt/android-sdk/aapt2-x86_64 "$@"
```
**关键坑：必须用 `QEMU_LD_PREFIX` 环境变量，不能用 `-L` 命令行参数。**
aapt2 daemon 会 fork 后 re-exec 自身；`-L` 在 re-exec 时丢失，表现为
`qemu-x86_64: Could not open '/lib64/ld-linux-x86-64.so.2'`。
`/opt/x86_64-root` 是 Debian amd64 的 libc6+libgcc-s1 解压产物，含 `/lib64` 软链。

### 原生 aapt2 重新编译（升级 aapt2 源码/修 bug 时）

```sh
cd /opt/aapt2-build
cmake -G Ninja -S . -B build-clang -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++
cd build-clang && ninja -j$(nproc) aapt2
# 产物 build-clang/aapt2；验证: ./aapt2 version  →  "Android Asset Packaging Tool (aapt) 2.19-..."
# 部署: install -m755 build-clang/aapt2 /opt/android-sdk/aapt2
```
原生 aapt2 的 `version` 串里 build number 是 `SOONG BUILD NUMBER PLACEHOLDER`
（`soong/cc/libbuildversion` 未生成 buildversion.h 所致），**不影响功能**，AGP 只校验
协议大版本 2.19，匹配即可。

## 标准构建流程

1. 确认 JDK、Gradle、SDK 就位（`java -version && gradle --version`）
2. 项目写 `local.properties`：`sdk.dir=/opt/android-sdk`
3. `gradle assembleDebug`（或 assembleRelease）
4. 产物在 `app/build/outputs/apk/debug/`
5. 验证：`/opt/android-sdk/build-tools/35.0.1/apksigner verify <apk>`

参考最小工程：`/root/apk-test`（AGP 8.5.2，可复制为模板）。

## 排错

| 症状 | 原因 / 处理 |
|---|---|
| `AAPT2 ... Daemon startup failed` | override 没生效或二进制架构不对。`/opt/android-sdk/aapt2 version` 应正常打印；不行就 `cp /opt/android-sdk/aapt2-qemu /opt/android-sdk/aapt2` 切 QEMU |
| 二进制 `非法指令` (illegal instruction) | 误用了 x86_64 二进制。确认 `uname -m` 是 aarch64；aapt2 用原生版 |
| 原生 aapt2 与 AGP 版本不匹配 | 换 AGP 大版本后 aapt2 协议可能变，重新编译对应 AOSP 标签，或临时切 QEMU 版 |
| `qemu-x86_64: Could not open '/lib64/ld-linux-x86-64.so.2'`（QEMU 路径） | `/opt/x86_64-root` 缺失或 `/lib64` 软链坏。重做：`dpkg -x libc6_*_amd64.deb /opt/x86_64-root && ln -sfn usr/lib/x86_64-linux-gnu /opt/x86_64-root/lib64` |
| 下载中断 | 该网络偶发断流，用 `curl -sL -C -` 断点续传 |

## 把 APK 放到设备真实下载目录（安装用）

- proot-distro **不带** `--isolated`：chroot 的 `/sdcard`、`/storage/emulated` 直通真实存储，直接
  `cp app-debug.apk /sdcard/Download/` 即可
- proot-distro **`--isolated`** 模式：`/sdcard` 是私有目录（device 与 `/` 相同），拷进去文件管理器看不到；
  需在宿主侧 bind 挂载下载目录（用户已配置：仅挂载 `/sdcard/Download`）后再复制。
  鉴别真实挂载：`df -h /sdcard/Download` 显示 `/storage/emulated/0/Download`，属主 `10485:1023`(media)
- 文件管理器不显示时：root 直写 FUSE 绕过 MediaStore，等 media scanner 索引或刷新文件管理器

## 限制

- 模拟器不可用（proot 无 KVM）；打包不受影响
- adb 为 x86_64，无法在本机直接连真机调试（打包不需要）
- AGP/Gradle 版本搭配：AGP 8.5.x 实测兼容 Gradle 9.7.1；原生 aapt2 源码标签
  `platform-tools-35.0.2` ↔ aapt2 2.19 ↔ AGP 8.5.x

## 原生 aapt2 的关键构建补丁（`/opt/aapt2-build`）

复现/排查编译时注意这些 host 适配点（均已落到源码副本/CMake）：
- `host_defs.h`（`-include` 强制包含）：stub 掉 `__INTRODUCED_IN`/`__builtin_available`，
  C++ 下补 `<limits>/<memory>/<algorithm>`，C 下补 `<stdatomic.h>`，定义 `PROP_NAME_MAX`
- 必须用 **clang**（GCC 的 C++ 模式不定义 `__STDC_VERSION__`，`<stdatomic.h>` 全局原子不可用）
- `libbase/posix_strerror_r.cpp`：glibc 的 GNU `strerror_r` 语义补丁
- `liblog`（pmsg_writer/logd_writer）：`atomic_int`→`std::atomic`，去掉与 `<atomic>` 冲突的 `<stdatomic.h>`
- `libandroidfw/LoadedArsc.cpp`：`std::lower_bound` 改手写二分（incfs `map_ptr` 迭代器缺 `operator--`）
- `libziparchive`：补 `incfs_support/include` 头路径
- 新增 `libincfs`/`libselinux`/`libsepol` 静态库；SELinux 用 `host_selinux_stub.c`
  替代 Android 专用的 `android_device.c`（host 无 SELinux 内核）
- 系统库：`protobuf=3.21.12`（与 AOSP 对齐）、pcre2、openssl、expat、png、icudata

## 跨环境复用 aapt2

- 本项目（`ChaunceyXv/aapt2-aarch64-build`）自带 **预编译** `prebuilt/aapt2`（aarch64，glibc 2.41/trixie 构建），
  新环境直接：装 `ldd` 列出的运行时库 → `install` 到稳定路径 → 写 `~/.gradle/gradle.properties`
  （`android.aapt2FromMavenOverride=<path>`）→ 可用，无需再编译。步骤见仓库 `prebuilt/README.md`
- 更老 glibc 系统 / 换 AGP 大版本 / 修 bug：在目标机跑仓库 `./build_aapt2.sh`（可 `TAG=` 换 AOSP 标签）
- AGP↔aapt2 版本对照、proot-distro 隔离模式存储坑、QEMU 回退：全在仓库 README
