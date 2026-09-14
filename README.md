# aapt2-aarch64-build

在 **aarch64 Linux（glibc）** 上原生编译 Android `aapt2`，并提供可直接使用的**预编译二进制**。

解决的核心问题：Google 官方 maven 只发布 x86_64 的 aapt2（`aapt2-<ver>-linux.jar`），
aarch64 宿主（ARM 服务器、树莓派、proot-distro 等）上 Gradle/AGP 打包 APK 会卡在
`AAPT2 Daemon startup failed`。

两种用法：

1. **直接用预编译**（推荐，2 分钟）：`prebuilt/aapt2` → 见 [prebuilt/README.md](prebuilt/README.md)
2. **源码重编**（升级 AGP/修 bug 时）：`./build_aapt2.sh` 一键完成 拉源码→打补丁→CMake 编译

---

## 项目结构

```
├── prebuilt/
│   ├── aapt2                        # 预编译二进制（aarch64 / Debian trixie / glibc 2.41）
│   └── README.md                    # 快速接入步骤
├── build_aapt2.sh                   # 一键源码编译脚本
├── build/
│   ├── CMakeLists.txt               # host 编译（基于 Lzhiyong/android-sdk-tools 思路改造）
│   ├── host_defs.h                  # -include 强制包含的宏桩（__INTRODUCED_IN/原子/limits...）
│   ├── host_selinux_stub.c          # host 版 selinux_android_* 无副作用桩
│   ├── patch_sources.py             # 幂等的 host 可移植性补丁（C 原子→std::atomic 等）
│   └── sysprop/                     # soong 生成的 sysprop 文件（随 AOSP 标签配套）
└── skill/android-apk-build/SKILL.md # opencode skill（环境部署经验全文）
```

## 源码编译

```sh
# 默认：拉取 AOSP tag platform-tools-35.0.2（≈aapt2 8.5.x）
./build_aapt2.sh

# 指定其他标签（升级 AGP 时）
TAG=android-16.0.0_r1 ./build_aapt2.sh

# 产物：out/aapt2；接入 AGP：
#   android.aapt2FromMavenOverride=$(pwd)/out/aapt2   # 写入 gradle.properties
```

首次运行会自动 `apt` 安装构建依赖（clang/ninja/flex/protobuf/expat/png/ssl 等，需 root）。

## AGP ↔ aapt2 版本对照

AGP 按自身版本下载对应 aapt2（协议号 2.x）。**大版本错配可能报
`AAPT2 version mismatch / daemon error`**，选标签的原则：

| 目标 AGP | aapt2 maven 版本 | 建议 AOSP 标签 | 协议 |
|---|---|---|---|
| 8.5.x（本仓库默认） | 8.5.2-11315950 | `platform-tools-35.0.2` | 2.19 |
| 8.7 / 8.9 / 9.x | 9.x | `android-15.0.0_r*` ~ `android-16.*`（需实测） | 2.2x |
| 官方回退方案 | 任意 | 用 QEMU 模拟官方 x86_64 aapt2 | — |

> 经验：AGP 期望 aapt2 版本 ≈ 与 AGP 同小版本。不确定时先跑一次
> `gradle assembleDebug` 看日志里 AGP 实际要哪个 aapt2 maven 版本
> （`aapt2-<ver>.jar`），再选 AOSP 标签，重编后对比 `aapt2 version` 输出。

## 新环境注意事项（全总结）

1. **架构**：预编译只用于 aarch64。x86_64 机器不需要本项目（官方二进制直接可用）。
2. **glibc 前向兼容**：glibc 2.41（trixie）构建的二进制可装到 ≥2.41 的系统；
   装到 bullseye(2.31)/bookworm(2.36) 会缺符号。此时用 `./build_aapt2.sh` 在目标系统重编。
3. **protobuf 固定 3.21.12**：aapt2 生成的 pb.cc 与 protobuf 运行时强绑定。
   trixie 的 `protobuf-compiler` 恰为 3.21.12（官方上限）。Ubuntu 24.04（3.21.12）可用；
   更新系统（protobuf 4.x/5.x）需自编 3.21.12 或确认兼容后再用系统版。
4. **必须用 clang 编译**：GCC 的 C++ 模式不定义 `__STDC_VERSION__`，
   `<stdatomic.h>` 全局原子（AOSP 代码大量使用）不可用。clang ≥16 即可。
5. **系统依赖运行时库**：`ldd out/aapt2` 查看；缺的按发行版补
   （trixie：libprotobuf32 libexpat1 libpng16-16 libfmt10 libicu76 libpcre2-8-0 libssl3t64 libzstd1）。
6. **sysprop 文件随标签变**：`build/sysprop/` 里的
   `IncrementalProperties.sysprop.{cpp,h}` 对应 35.0.2 标签；换 `TAG=` 重编前
   需从新标签的 soong 生成物同步更新（参考 AOSP `soong` 的 sysprop 生成规则）。
7. **版本串占位符**：自编 aapt2 的 `version` 输出含 `SOONG BUILD NUMBER PLACEHOLDER`，
   属正常（buildversion 头由 soong 生成，这里用仓库自带桩），AGP 只校验协议主版本。

### proot-distro（Termux）专属坑

- 非隔离模式（不带 `--isolated`）：chroot 的 `/sdcard`、`/storage/emulated` 直通设备真实存储，
  产物 APK 可直接 `cp /sdcard/Download/`
- **隔离模式（`--isolated`）**：`/sdcard`、`/storage` 是 chroot 私有目录（与 `/` 同 device id），
  拷进去文件管理器看不到。要么宿主侧 bind 挂载真实 Download 目录再拷，
  要么退出 chroot 从 Termux 侧用宿主路径复制：
  `cp $PREFIX/var/lib/proot-distro/containers/<name>/rootfs/<chroot内路径> /sdcard/Download/`
- 鉴别真实挂载：`df -h <dir>` 看挂载源是否 `/storage/emulated/0/...`，属主是否 `10485:1023`（media）

### QEMU 回退方案（不想维护源码编译时）

官方 x86_64 aapt2 用 qemu-user 模拟运行（慢 5~10 倍但零维护）：

```sh
apt-get install -y qemu-user
# x86_64 glibc 根（Debian amd64 包解压）
dpkg -x libc6_*.amd64.deb /opt/x86_64-root
ln -sfn usr/lib/x86_64-linux-gnu /opt/x86_64-root/lib64
# 包装脚本（必须 QEMU_LD_PREFIX，-L 在 aapt2 daemon re-exec 时会丢）
cat > /opt/android-sdk/aapt2 <<'EOF'
#!/bin/sh
export QEMU_LD_PREFIX=/opt/x86_64-root
exec /usr/bin/qemu-x86_64 /opt/android-sdk/aapt2-x86_64 "$@"
EOF
```
aapt2-x86_64 从 gradle 缓存取：
`~/.gradle/caches/modules-2/files-2.1/com.android.tools.build/aapt2/*/` 的 jar 内，
或 `~/.gradle/caches/*/transforms/*/transformed/aapt2-*/aapt2`。

## 参考与致谢

- 社区 CMake 方案思路：[Lzhiyong/android-sdk-tools](https://github.com/Lzhiyong/android-sdk-tools)
  （Apache-2.0；其 NDK 目标版 + 本仓库 host 化改造）
- 源码：AOSP（Apache-2.0）`platform/frameworks/base`（aapt2）、`system/core`、
  `system/libbase`、`system/logging`、`system/libziparchive`、
  `system/incremental_delivery`、`external/selinux`、`build/soong`、`frameworks/native`
