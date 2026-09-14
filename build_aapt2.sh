#!/usr/bin/env bash
# Build a native aarch64 aapt2 from AOSP source for the host Linux (Debian trixie target).
# Layout: <project>/src  = AOSP source (fetched here), <project>/out = build output
#
# Usage:
#   ./build_aapt2.sh            # fetch sources + patch + build -> out/aapt2
#   TAG=android-15.0.0_r1 ./build_aapt2.sh   # pin a different AOSP tag
#
# Requirements: apt root access (installs build deps), git, python3.
# The result links against system shared libs (see README "New environment" section).
set -euo pipefail
cd "$(dirname "$0")"   # project root

TAG="${TAG:-platform-tools-35.0.2}"
GS="https://android.googlesource.com"
OUT="${OUT:-out}"

echo "==> [1/5] host dependencies (apt)"
if [ "$(id -u)" = "0" ]; then
  apt-get update -qq
  apt-get install -y -qq \
    clang ninja-build flex git python3 ca-certificates \
    libxml2-dev libexpat1-dev libpng-dev zlib1g-dev \
    libicu-dev libprotobuf-dev protobuf-compiler libfmt-dev \
    libabsl-dev libpcre2-dev libssl-dev 2>/dev/null || true
  # protobuf: must be 3.21.x (generated-code compatibility, see README)
  echo "protoc: $(protoc --version 2>/dev/null || echo MISSING)"
else
  echo "  running non-root: assuming deps already installed"
fi

echo "==> [2/5] fetch AOSP sources (tag: $TAG)"
mkdir -p src
fetch() { # name url [sparse-paths...]
  local name="$1" url="$2"; shift 2
  if [ -d "src/$name/.git" ] || [ -f "src/$name/.git" ]; then
    echo "  src/$name already present, skip"
    return
  fi
  if [ $# -gt 0 ]; then
    echo "  cloning $name (sparse: $*)"
    git clone --quiet --no-checkout --filter=blob:none --depth 1 --branch "$TAG" "$url" "src/$name"
    ( cd "src/$name" && git sparse-checkout init --no-cone && git sparse-checkout set "$@" && git checkout -q )
  else
    echo "  cloning $name"
    git clone --quiet --depth 1 --branch "$TAG" "$url" "src/$name"
  fi
}
fetch base      "$GS/platform/frameworks/base" tools/aapt2 libs/androidfw cmds/idmap2
fetch core      "$GS/platform/system/core"
fetch libbase   "$GS/platform/system/libbase"
fetch logging   "$GS/platform/system/logging"
fetch libziparchive "$GS/platform/system/libziparchive"
fetch incremental_delivery "$GS/platform/system/incremental_delivery"
fetch selinux   "$GS/platform/external/selinux"
fetch soong     "$GS/platform/build/soong"
fetch native    "$GS/platform/frameworks/native"

echo "==> [3/5] patch sources (host portability)"
python3 build/patch_sources.py src
cp -f build/sysprop/IncrementalProperties.sysprop.cpp \
      build/sysprop/IncrementalProperties.sysprop.h \
      src/incremental_delivery/sysprop/

echo "==> [4/5] configure + build"
cmake -G Ninja -S build -B "$OUT" -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ > /dev/null
ninja -C "$OUT" -j"$(nproc)" aapt2

echo "==> [5/5] done"
"$OUT/aapt2" version
echo
echo "Binary: $(pwd)/$OUT/aapt2"
echo "To use with AGP: copy it somewhere stable and set in gradle.properties:"
echo "  android.aapt2FromMavenOverride=<path-to-binary>"
