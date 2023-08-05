# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

if(UNIX)
  set(CMAKE_CUDA_OUTPUT_EXTENSION .o)
else()
  set(CMAKE_CUDA_OUTPUT_EXTENSION .obj)
endif()
set(CMAKE_INCLUDE_FLAG_CUDA "-I")

# Load compiler-specific information.
if(CMAKE_CUDA_COMPILER_ID)
  include(Compiler/${CMAKE_CUDA_COMPILER_ID}-CUDA OPTIONAL)
endif()

# load the system- and compiler specific files
if(CMAKE_CUDA_COMPILER_ID)
  # load a hardware specific file, mostly useful for embedded compilers
  if(CMAKE_SYSTEM_PROCESSOR)
    include(Platform/${CMAKE_SYSTEM_NAME}-${CMAKE_CUDA_COMPILER_ID}-CUDA-${CMAKE_SYSTEM_PROCESSOR} OPTIONAL)
  endif()
  include(Platform/${CMAKE_SYSTEM_NAME}-${CMAKE_CUDA_COMPILER_ID}-CUDA OPTIONAL)
endif()


if(NOT CMAKE_SHARED_LIBRARY_RUNTIME_CUDA_FLAG)
  set(CMAKE_SHARED_LIBRARY_RUNTIME_CUDA_FLAG ${CMAKE_SHARED_LIBRARY_RUNTIME_C_FLAG})
endif()

if(NOT CMAKE_SHARED_LIBRARY_RUNTIME_CUDA_FLAG_SEP)
  set(CMAKE_SHARED_LIBRARY_RUNTIME_CUDA_FLAG_SEP ${CMAKE_SHARED_LIBRARY_RUNTIME_C_FLAG_SEP})
endif()

if(NOT CMAKE_SHARED_LIBRARY_RPATH_LINK_CUDA_FLAG)
  set(CMAKE_SHARED_LIBRARY_RPATH_LINK_CUDA_FLAG ${CMAKE_SHARED_LIBRARY_RPATH_LINK_C_FLAG})
endif()

if(NOT DEFINED CMAKE_EXE_EXPORTS_CUDA_FLAG)
  set(CMAKE_EXE_EXPORTS_CUDA_FLAG ${CMAKE_EXE_EXPORTS_C_FLAG})
endif()

if(NOT DEFINED CMAKE_SHARED_LIBRARY_SONAME_CUDA_FLAG)
  set(CMAKE_SHARED_LIBRARY_SONAME_CUDA_FLAG ${CMAKE_SHARED_LIBRARY_SONAME_C_FLAG})
endif()

if(NOT CMAKE_EXECUTABLE_RUNTIME_CUDA_FLAG)
  set(CMAKE_EXECUTABLE_RUNTIME_CUDA_FLAG ${CMAKE_SHARED_LIBRARY_RUNTIME_CUDA_FLAG})
endif()

if(NOT CMAKE_EXECUTABLE_RUNTIME_CUDA_FLAG_SEP)
  set(CMAKE_EXECUTABLE_RUNTIME_CUDA_FLAG_SEP ${CMAKE_SHARED_LIBRARY_RUNTIME_CUDA_FLAG_SEP})
endif()

if(NOT CMAKE_EXECUTABLE_RPATH_LINK_CUDA_FLAG)
  set(CMAKE_EXECUTABLE_RPATH_LINK_CUDA_FLAG ${CMAKE_SHARED_LIBRARY_RPATH_LINK_CUDA_FLAG})
endif()

if(NOT DEFINED CMAKE_SHARED_LIBRARY_LINK_CUDA_WITH_RUNTIME_PATH)
  set(CMAKE_SHARED_LIBRARY_LINK_CUDA_WITH_RUNTIME_PATH ${CMAKE_SHARED_LIBRARY_LINK_C_WITH_RUNTIME_PATH})
endif()


# for most systems a module is the same as a shared library
# so unless the variable CMAKE_MODULE_EXISTS is set just
# copy the values from the LIBRARY variables
if(NOT CMAKE_MODULE_EXISTS)
  set(CMAKE_SHARED_MODULE_CUDA_FLAGS ${CMAKE_SHARED_LIBRARY_CUDA_FLAGS})
  set(CMAKE_SHARED_MODULE_CREATE_CUDA_FLAGS ${CMAKE_SHARED_LIBRARY_CREATE_CUDA_FLAGS})
endif()

# add the flags to the cache based
# on the initial values computed in the platform/*.cmake files
# use _INIT variables so that this only happens the first time
# and you can set these flags in the cmake cache
set(CMAKE_CUDA_FLAGS_INIT "$ENV{CUDAFLAGS} ${CMAKE_CUDA_FLAGS_INIT}")

foreach(c "" _DEBUG _RELEASE _MINSIZEREL _RELWITHDEBINFO)
  string(STRIP "${CMAKE_CUDA_FLAGS${c}_INIT}" CMAKE_CUDA_FLAGS${c}_INIT)
endforeach()

set (CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS_INIT}" CACHE STRING
     "Flags used by the compiler during all build types.")

if(NOT CMAKE_NOT_USING_CONFIG_FLAGS)
  set (CMAKE_CUDA_FLAGS_DEBUG "${CMAKE_CUDA_FLAGS_DEBUG_INIT}" CACHE STRING
     "Flags used by the compiler during debug builds.")
  set (CMAKE_CUDA_FLAGS_MINSIZEREL "${CMAKE_CUDA_FLAGS_MINSIZEREL_INIT}" CACHE STRING
     "Flags used by the compiler during release builds for minimum size.")
  set (CMAKE_CUDA_FLAGS_RELEASE "${CMAKE_CUDA_FLAGS_RELEASE_INIT}" CACHE STRING
     "Flags used by the compiler during release builds.")
  set (CMAKE_CUDA_FLAGS_RELWITHDEBINFO "${CMAKE_CUDA_FLAGS_RELWITHDEBINFO_INIT}" CACHE STRING
     "Flags used by the compiler during release builds with debug info.")

endif()

if(CMAKE_CUDA_STANDARD_LIBRARIES_INIT)
  set(CMAKE_CUDA_STANDARD_LIBRARIES "${CMAKE_CUDA_STANDARD_LIBRARIES_INIT}"
    CACHE STRING "Libraries linked by default with all CUDA applications.")
  mark_as_advanced(CMAKE_CUDA_STANDARD_LIBRARIES)
endif()

include(CMakeCommonLanguageInclude)

# now define the following rules:
# CMAKE_CUDA_CREATE_SHARED_LIBRARY
# CMAKE_CUDA_CREATE_SHARED_MODULE
# CMAKE_CUDA_COMPILE_WHOLE_COMPILATION
# CMAKE_CUDA_COMPILE_PTX_COMPILATION
# CMAKE_CUDA_COMPILE_SEPARABLE_COMPILATION
# CMAKE_CUDA_LINK_EXECUTABLE

if(CMAKE_CUDA_HOST_COMPILER)
  set(CMAKE_CUDA_HOST_FLAGS "-ccbin=<CMAKE_CUDA_HOST_COMPILER>")
else()
  set(CMAKE_CUDA_HOST_FLAGS "")
endif()

set(__IMPLICT_LINKS )
foreach(dir ${CMAKE_CUDA_HOST_IMPLICIT_LINK_DIRECTORIES})
  string(APPEND __IMPLICT_LINKS " -L\"${dir}\"")
endforeach()
foreach(lib ${CMAKE_CUDA_HOST_IMPLICIT_LINK_LIBRARIES})
  if(${lib} MATCHES "/")
    string(APPEND __IMPLICT_LINKS " \"${lib}\"")
  else()
    string(APPEND __IMPLICT_LINKS " -l${lib}")
  endif()
endforeach()

# create a shared library
if(NOT CMAKE_CUDA_CREATE_SHARED_LIBRARY)
  set(CMAKE_CUDA_CREATE_SHARED_LIBRARY
      "<CMAKE_CUDA_HOST_LINK_LAUNCHER> <CMAKE_SHARED_LIBRARY_CUDA_FLAGS> <LINK_FLAGS> <CMAKE_SHARED_LIBRARY_CREATE_CUDA_FLAGS> <SONAME_FLAG><TARGET_SONAME> -o <TARGET> <OBJECTS> <LINK_LIBRARIES>${__IMPLICT_LINKS}")
endif()

# create a shared module copy the shared library rule by default
if(NOT CMAKE_CUDA_CREATE_SHARED_MODULE)
  set(CMAKE_CUDA_CREATE_SHARED_MODULE ${CMAKE_CUDA_CREATE_SHARED_LIBRARY})
endif()

# Create a static archive incrementally for large object file counts.
if(NOT DEFINED CMAKE_CUDA_ARCHIVE_CREATE)
  set(CMAKE_CUDA_ARCHIVE_CREATE "<CMAKE_AR> qc <TARGET> <LINK_FLAGS> <OBJECTS>")
endif()
if(NOT DEFINED CMAKE_CUDA_ARCHIVE_APPEND)
  set(CMAKE_CUDA_ARCHIVE_APPEND "<CMAKE_AR> q  <TARGET> <LINK_FLAGS> <OBJECTS>")
endif()
if(NOT DEFINED CMAKE_CUDA_ARCHIVE_FINISH)
  set(CMAKE_CUDA_ARCHIVE_FINISH "<CMAKE_RANLIB> <TARGET>")
endif()

#Specify how to compile when ptx has been requested
if(NOT CMAKE_CUDA_COMPILE_PTX_COMPILATION)
  set(CMAKE_CUDA_COMPILE_PTX_COMPILATION
    "<CMAKE_CUDA_COMPILER> ${CMAKE_CUDA_HOST_FLAGS} <DEFINES> <INCLUDES> <FLAGS> -x cu -ptx <SOURCE> -o <OBJECT>")
endif()

#Specify how to compile when separable compilation has been requested
if(NOT CMAKE_CUDA_COMPILE_SEPARABLE_COMPILATION)
  set(CMAKE_CUDA_COMPILE_SEPARABLE_COMPILATION
    "<CMAKE_CUDA_COMPILER> ${CMAKE_CUDA_HOST_FLAGS} <DEFINES> <INCLUDES> <FLAGS> -x cu -dc <SOURCE> -o <OBJECT>")
endif()

#Specify how to compile when whole compilation has been requested
if(NOT CMAKE_CUDA_COMPILE_WHOLE_COMPILATION)
  set(CMAKE_CUDA_COMPILE_WHOLE_COMPILATION
    "<CMAKE_CUDA_COMPILER> ${CMAKE_CUDA_HOST_FLAGS} <DEFINES> <INCLUDES> <FLAGS> -x cu -c <SOURCE> -o <OBJECT>")
endif()

if(CMAKE_GENERATOR STREQUAL "Ninja")
  set(CMAKE_CUDA_COMPILE_DEPENDENCY_DETECTION
    "<CMAKE_CUDA_COMPILER> ${CMAKE_CUDA_HOST_FLAGS} <DEFINES> <INCLUDES> <FLAGS> -x cu -M <SOURCE> -MT <OBJECT> -o $DEP_FILE")
  #The Ninja generator uses the make file dependency files to determine what
  #files need to be recompiled. Unfortunately, nvcc doesn't support building
  #a source file and generating the dependencies of said file in a single
  #invocation. Instead we have to state that you need to chain two commands.
  #
  #The makefile generators uses the custom CMake dependency scanner, and thus
  #it is exempt from this logic.
  list(APPEND CMAKE_CUDA_COMPILE_PTX_COMPILATION "${CMAKE_CUDA_COMPILE_DEPENDENCY_DETECTION}")
  list(APPEND CMAKE_CUDA_COMPILE_SEPARABLE_COMPILATION "${CMAKE_CUDA_COMPILE_DEPENDENCY_DETECTION}")
  list(APPEND CMAKE_CUDA_COMPILE_WHOLE_COMPILATION "${CMAKE_CUDA_COMPILE_DEPENDENCY_DETECTION}")
endif()

# compile a cu file into an executable
if(NOT CMAKE_CUDA_LINK_EXECUTABLE)
  set(CMAKE_CUDA_LINK_EXECUTABLE
    "<CMAKE_CUDA_HOST_LINK_LAUNCHER> <CMAKE_CUDA_LINK_FLAGS> <LINK_FLAGS> <OBJECTS> -o <TARGET> <LINK_LIBRARIES>${__IMPLICT_LINKS}")
endif()

if(CMAKE_CUDA_COMPILER_VERSION VERSION_GREATER_EQUAL "8.0.0")
  set(_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS "-Wno-deprecated-gpu-targets")
else()
  set(_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS "")
endif()


#These are used when linking relocatable (dc) cuda code
if(NOT CMAKE_CUDA_DEVICE_LINK_LIBRARY)
  set(CMAKE_CUDA_DEVICE_LINK_LIBRARY
    "<CMAKE_CUDA_COMPILER> <CMAKE_CUDA_LINK_FLAGS> <LANGUAGE_COMPILE_FLAGS> ${CMAKE_CUDA_COMPILE_OPTIONS_PIC} ${_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS} -shared -dlink <OBJECTS> -o <TARGET> <LINK_LIBRARIES>")
endif()
if(NOT CMAKE_CUDA_DEVICE_LINK_EXECUTABLE)
  set(CMAKE_CUDA_DEVICE_LINK_EXECUTABLE
    "<CMAKE_CUDA_COMPILER> <FLAGS> <CMAKE_CUDA_LINK_FLAGS> ${CMAKE_CUDA_COMPILE_OPTIONS_PIC} ${_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS} -shared -dlink <OBJECTS> -o <TARGET> <LINK_LIBRARIES>")
endif()

unset(_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS)

mark_as_advanced(
CMAKE_CUDA_FLAGS
CMAKE_CUDA_FLAGS_RELEASE
CMAKE_CUDA_FLAGS_RELWITHDEBINFO
CMAKE_CUDA_FLAGS_MINSIZEREL
CMAKE_CUDA_FLAGS_DEBUG)

set(CMAKE_CUDA_INFORMATION_LOADED 1)
