#!/usr/bin/env python3
"""Host-portability patches for building aapt2 (AOSP) on Linux glibc host.

All replacements are idempotent: if the original text is not found
(already patched) the step is skipped.

Usage: python3 build/patch_sources.py <src-dir>
"""
import sys
from pathlib import Path

SRC = Path(sys.argv[1])

def patch(relpath, pairs):
    p = SRC / relpath
    text = p.read_text(encoding="utf-8", errors="replace")
    changed = False
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new)
            changed = True
    if changed:
        p.write_text(text, encoding="utf-8")
        print(f"patched {relpath}")
    else:
        print(f"skip    {relpath} (already patched)")

# --- 1. proto imports: "frameworks/base/tools/aapt2/X.proto" -> "X.proto"
for f in sorted((SRC / "base/tools/aapt2").glob("*.proto")):
    t = f.read_text()
    if "frameworks/base/tools/aapt2/" in t:
        f.write_text(t.replace("frameworks/base/tools/aapt2/", ""))
        print(f"patched {f.name} (proto imports)")
    else:
        print(f"skip    {f.name} (proto imports)")

# --- 2. libbase: glibc GNU/XSI strerror_r has different signature
patch("libbase/posix_strerror_r.cpp", [
    (
        "#ifdef _WIN32\n"
        "  return strerror_s(buf, buflen, errnum);\n"
        "#else\n"
        "  return strerror_r(errnum, buf, buflen);\n"
        "#endif\n",
        "#ifdef _WIN32\n"
        "  return strerror_s(buf, buflen, errnum);\n"
        "#else\n"
        "#if defined(__GLIBC__)\n"
        "  // glibc GNU/XSI strerror_r both write into buf; discard the return value.\n"
        "  ::strerror_r(errnum, buf, buflen);\n"
        "  return 0;\n"
        "#else\n"
        "  return strerror_r(errnum, buf, buflen);\n"
        "#endif\n"
        "#endif\n",
    ),
])

# --- 3. liblog: C-style global atomics don't have C++ member functions in host
# libstdc++/libc++; convert the few uses to std::atomic.
patch("logging/liblog/pmsg_writer.cpp", [
    ("#include <time.h>\n", "#include <time.h>\n#include <atomic>\n#include <cstdint>\n"),
    ("static atomic_int pmsg_fd;", "static std::atomic<int> pmsg_fd{0};"),
])
patch("logging/liblog/logd_writer.cpp", [
    ("#include <stdatomic.h>\n", ""),
    ("#include <time.h>\n", "#include <time.h>\n#include <atomic>\n#include <cstdint>\n"),
    ("  atomic_int sock_ = kUninitialized;", "  std::atomic<int> sock_{kUninitialized};"),
    ("  static atomic_int dropped;", "  static std::atomic<int> dropped{0};"),
    ("int32_t snapshot = atomic_exchange_explicit(&dropped, 0, memory_order_relaxed);",
     "int32_t snapshot = dropped.exchange(0, std::memory_order_relaxed);"),
    ("atomic_fetch_add_explicit(&dropped, snapshot, memory_order_relaxed);",
     "dropped.fetch_add(snapshot, std::memory_order_relaxed);"),
    ("atomic_fetch_add_explicit(&dropped, 1, memory_order_relaxed);",
     "dropped.fetch_add(1, std::memory_order_relaxed);"),
])
patch("logging/liblog/pmsg_reader.cpp", [
    ("#include <errno.h>\n", "#include <errno.h>\n#include <limits.h>\n"),
])

# --- 4. libandroidfw: incfs::map_ptr iterator lacks operator--; std::lower_bound
# (libstdc++) requires bidirectional. Replace with manual binary search.
patch("base/libs/androidfw/LoadedArsc.cpp", [
    (
        "    auto result = std::lower_bound(sparse_indices, sparse_indices_end, entry_index,\n"
        "                                   [&error](const incfs::map_ptr<ResTable_sparseTypeEntry>& entry,\n"
        "                                            uint16_t entry_idx) {\n"
        "      if (UNLIKELY(!entry)) {\n"
        "        return error = true;\n"
        "      }\n"
        "      return dtohs(entry->idx) < entry_idx;\n"
        "    });\n",
        "    // Manual binary search (libstdc++ std::lower_bound requires bidirectional iterators,\n"
        "    // but incfs::map_ptr::const_iterator does not support operator-- on host).\n"
        "    auto lo = sparse_indices, hi = sparse_indices_end;\n"
        "    while (lo != hi) {\n"
        "      auto mid = lo + static_cast<int>((hi - lo) / 2);\n"
        "      const auto& mid_entry = *mid;\n"
        "      if (UNLIKELY(!mid_entry)) {\n"
        "        error = true;\n"
        "        lo = mid + 1;\n"
        "      } else if (dtohs(mid_entry->idx) < entry_index) {\n"
        "        lo = mid + 1;\n"
        "      } else {\n"
        "        hi = mid;\n"
        "      }\n"
        "    }\n"
        "    auto result = lo;\n",
    ),
])

print("all patches applied")
