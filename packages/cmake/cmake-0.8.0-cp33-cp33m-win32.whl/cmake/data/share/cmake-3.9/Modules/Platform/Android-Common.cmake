# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

# This module is shared by multiple languages; use include blocker.
if(__ANDROID_COMPILER_COMMON)
  return()
endif()
set(__ANDROID_COMPILER_COMMON 1)

if(CMAKE_ANDROID_NDK)
  # <ndk>/build/core/definitions.mk

  set(_ANDROID_STL_TYPES
    none
    system
    c++_static
    c++_shared
    gabi++_static
    gabi++_shared
    gnustl_static
    gnustl_shared
    stlport_static
    stlport_shared
    )

  if(CMAKE_ANDROID_STL_TYPE)
    list(FIND _ANDROID_STL_TYPES "${CMAKE_ANDROID_STL_TYPE}" _ANDROID_STL_TYPE_FOUND)
    if(_ANDROID_STL_TYPE_FOUND EQUAL -1)
      string(REPLACE ";" "\n  " _msg ";${_ANDROID_STL_TYPES}")
      message(FATAL_ERROR
        "The CMAKE_ANDROID_STL_TYPE '${CMAKE_ANDROID_STL_TYPE}' is not one of the allowed values:${_msg}\n"
        )
    endif()
    unset(_ANDROID_STL_TYPE_FOUND)
  else()
    set(CMAKE_ANDROID_STL_TYPE "gnustl_static")
  endif()

  unset(_ANDROID_STL_TYPES)

  # Forward Android-specific platform variables to try_compile projects.
  list(APPEND CMAKE_TRY_COMPILE_PLATFORM_VARIABLES
    CMAKE_ANDROID_STL_TYPE
    )
endif()

if(CMAKE_ANDROID_STL_TYPE)
  if(CMAKE_ANDROID_NDK)

    macro(__android_stl_inc lang dir req)
      if(EXISTS "${dir}")
        list(APPEND CMAKE_${lang}_STANDARD_INCLUDE_DIRECTORIES "${dir}")
      elseif(${req})
        message(FATAL_ERROR
          "Android: STL '${CMAKE_ANDROID_STL_TYPE}' include directory not found:\n"
          "  ${dir}"
          )
      endif()
    endmacro()

    macro(__android_stl_lib lang lib req)
      if(CMAKE_ANDROID_ARCH_ABI MATCHES "^armeabi" AND NOT CMAKE_ANDROID_ARM_MODE)
        get_filename_component(_ANDROID_STL_LIBDIR "${lib}" DIRECTORY)
        get_filename_component(_ANDROID_STL_LIBNAME "${lib}" NAME)
        set(_ANDROID_STL_LIBTHUMB "${_ANDROID_STL_LIBDIR}/thumb/${_ANDROID_STL_LIBNAME}")
        unset(_ANDROID_STL_LIBDIR)
        unset(_ANDROID_STL_LIBNAME)
      else()
        set(_ANDROID_STL_LIBTHUMB "")
      endif()

      if(_ANDROID_STL_LIBTHUMB AND EXISTS "${_ANDROID_STL_LIBTHUMB}")
        string(APPEND CMAKE_${lang}_STANDARD_LIBRARIES " \"${_ANDROID_STL_LIBTHUMB}\"")
      elseif(EXISTS "${lib}")
        string(APPEND CMAKE_${lang}_STANDARD_LIBRARIES " \"${lib}\"")
      elseif(${req})
        message(FATAL_ERROR
          "Android: STL '${CMAKE_ANDROID_STL_TYPE}' library file not found:\n"
          "  ${lib}"
          )
      endif()

      unset(_ANDROID_STL_LIBTHUMB)
    endmacro()

    include(Platform/Android/ndk-stl-${CMAKE_ANDROID_STL_TYPE})
  else()
    macro(__android_stl lang)
    endmacro()
  endif()
else()
  macro(__android_stl lang)
  endmacro()
endif()

# The NDK toolchain configuration files at:
#
#   <ndk>/[build/core/]toolchains/*/setup.mk
#
# contain logic to set TARGET_CFLAGS and TARGET_LDFLAGS (and debug/release
# variants) to tell their build system what flags to pass for each ABI.
# We need to produce the same flags here to produce compatible binaries.
# We initialize these variables here and set them in the compiler-specific
# modules that include this one.  Then we use them in the macro below when
# it is called.
set(_ANDROID_ABI_INIT_CFLAGS "")
set(_ANDROID_ABI_INIT_CFLAGS_DEBUG "")
set(_ANDROID_ABI_INIT_CFLAGS_RELEASE "")
set(_ANDROID_ABI_INIT_LDFLAGS "")
set(_ANDROID_ABI_INIT_EXE_LDFLAGS "")

macro(__android_compiler_common lang)
  if(_ANDROID_ABI_INIT_CFLAGS)
    string(APPEND CMAKE_${lang}_FLAGS_INIT " ${_ANDROID_ABI_INIT_CFLAGS}")
  endif()
  if(_ANDROID_ABI_INIT_CFLAGS_DEBUG)
    string(APPEND CMAKE_${lang}_FLAGS_DEBUG_INIT " ${_ANDROID_ABI_INIT_CFLAGS_DEBUG}")
  endif()
  if(_ANDROID_ABI_INIT_CFLAGS_RELEASE)
    string(APPEND CMAKE_${lang}_FLAGS_RELEASE_INIT " ${_ANDROID_ABI_INIT_CFLAGS_RELEASE}")
    string(APPEND CMAKE_${lang}_FLAGS_MINSIZEREL_INIT " ${_ANDROID_ABI_INIT_CFLAGS_RELEASE}")
    string(APPEND CMAKE_${lang}_FLAGS_RELWITHDEBINFO_INIT " ${_ANDROID_ABI_INIT_CFLAGS_RELEASE}")
  endif()
  if(_ANDROID_ABI_INIT_LDFLAGS)
    foreach(t EXE SHARED MODULE)
      string(APPEND CMAKE_${t}_LINKER_FLAGS_INIT " ${_ANDROID_ABI_INIT_LDFLAGS}")
    endforeach()
  endif()
  if(_ANDROID_ABI_INIT_EXE_LDFLAGS)
    string(APPEND CMAKE_EXE_LINKER_FLAGS_INIT " ${_ANDROID_ABI_INIT_EXE_LDFLAGS}")
  endif()

  if(DEFINED _ANDROID_STL_EXCEPTIONS)
    if(_ANDROID_STL_EXCEPTIONS)
      string(APPEND CMAKE_${lang}_FLAGS_INIT " -fexceptions")
    else()
      string(APPEND CMAKE_${lang}_FLAGS_INIT " -fno-exceptions")
    endif()
  endif()

  if("x${lang}" STREQUAL "xCXX" AND DEFINED _ANDROID_STL_RTTI)
    if(_ANDROID_STL_RTTI)
      string(APPEND CMAKE_${lang}_FLAGS_INIT " -frtti")
    else()
      string(APPEND CMAKE_${lang}_FLAGS_INIT " -fno-rtti")
    endif()
  endif()

  if("x${lang}" STREQUAL "xCXX")
    __android_stl(CXX)
  endif()

  # <ndk>/build/core/definitions.mk appends the sysroot's include directory
  # explicitly at the end of the command-line include path so that it
  # precedes the toolchain's builtin include directories.  This is
  # necessary so that Android API-version-specific headers are preferred
  # over those in the toolchain's `include-fixed` directory (which cannot
  # possibly match all versions).
  #
  # Do not do this for a standalone toolchain because it is already
  # tied to a specific API version.
  if(CMAKE_ANDROID_NDK)
    if(NOT CMAKE_ANDROID_NDK_DEPRECATED_HEADERS)
      list(APPEND CMAKE_${lang}_STANDARD_INCLUDE_DIRECTORIES
        "${CMAKE_SYSROOT_COMPILE}/usr/include"
        "${CMAKE_SYSROOT_COMPILE}/usr/include/${CMAKE_ANDROID_ARCH_HEADER_TRIPLE}"
        )
    else()
      list(APPEND CMAKE_${lang}_STANDARD_INCLUDE_DIRECTORIES "${CMAKE_SYSROOT}/usr/include")
    endif()
  endif()
endmacro()
