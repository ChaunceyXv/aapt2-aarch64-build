#pragma once
#ifndef __INTRODUCED_IN
#define __INTRODUCED_IN(x)
#define __INTRODUCED_IN_NDA(x)
#define __UNINTENDEDLY_EXPOSED(x)
#endif
#if !defined(__APPLE__)
#undef __builtin_available
#define __builtin_available(...) 0
#endif
#if defined(__cplusplus)
#include <limits>
#include <memory>
#include <algorithm>
#include <string.h>
#else
#include <string.h>
#endif
#include <limits.h>
#if !defined(__cplusplus)
#include <stdatomic.h>
#endif
#if !defined(PROP_NAME_MAX)
#define PROP_NAME_MAX 32
#endif
#if !defined(PROP_VALUE_MAX)
#define PROP_VALUE_MAX 92
#endif
