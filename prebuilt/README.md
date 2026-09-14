# 预编译 aapt2（aarch64 / Debian 13 trixie glibc 2.41）

- 文件：`prebuilt/aapt2`（~3.7 MB，动态链接）
- 源码：AOSP `platform-tools-35.0.2` 标签（aapt2 8.5.x 时代，协议版本 **2.19**，匹配 **AGP 8.5.x**）
- 依赖：见下方 `apt` 列表（trixie 包名；其他发行版按库名对应）

## 快速接入（2 分钟）

```sh
# 1. 安装运行库（trixie 包名；缺哪个装哪个）
apt-get install -y libprotobuf32 libexpat1 libpng16-16 zlib1g libfmt10 \
    libicu76 libpcre2-8-0 libssl3t64 libstdc++6 libzstd1

# 2. 放到稳定路径
install -m 755 prebuilt/aapt2 /opt/android-sdk/aapt2-native

# 3. 验证
/opt/android-sdk/aapt2-native version
# → Android Asset Packaging Tool (aapt) 2.19-...

# 4. 接入 AGP（全局，所有工程生效）
mkdir -p ~/.gradle
echo 'android.aapt2FromMavenOverride=/opt/android-sdk/aapt2-native' >> ~/.gradle/gradle.properties
```

之后 `gradle assembleDebug` 即用此 aapt2，无需 QEMU。

## 注意事项（新环境）

| 项 | 说明 |
|---|---|
| 架构 | 仅 aarch64；x86_64 机器直接不可用 |
| glibc | 在 glibc 2.41（trixie）构建。**只能往更新系统装**，装到更老系统会 `GLIBC_2.xx not found` |
| 库缺失 | `ldd prebuilt/aapt2` 列出全部依赖，按发行版补包 |
| AGP 匹配 | 2.19 ↔ AGP 8.5.x。AGP 8.7/8.9/9.x 期望更新的 aapt2 协议，可能不匹配——见根目录 README「AGP ↔ aapt2 版本对照」 |
| 版本串 | `version` 输出里的 build number 是 `SOONG BUILD NUMBER PLACEHOLDER`，正常，不影响功能 |
