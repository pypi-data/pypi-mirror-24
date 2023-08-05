# compiler support for fortran CVF compiler on windows

set(CMAKE_WINDOWS_OBJECT_PATH 1)
set(CMAKE_LIBRARY_PATH_FLAG "-LIBPATH:")
set(CMAKE_LINK_LIBRARY_FLAG "")
set(WIN32 1)
if(CMAKE_VERBOSE_MAKEFILE)
  set(CMAKE_CL_NOLOGO)
else()
  set(CMAKE_CL_NOLOGO "/nologo")
endif()

set(CMAKE_Fortran_MODDIR_FLAG "-module:")

set(CMAKE_Fortran_CREATE_SHARED_LIBRARY
 "link ${CMAKE_CL_NOLOGO} ${CMAKE_START_TEMP_FILE}  /out:<TARGET> /dll  <LINK_FLAGS> <OBJECTS> <LINK_LIBRARIES> ${CMAKE_END_TEMP_FILE}")

set(CMAKE_Fortran_CREATE_SHARED_MODULE ${CMAKE_Fortran_CREATE_SHARED_LIBRARY})

# create a C++ static library
set(CMAKE_Fortran_CREATE_STATIC_LIBRARY  "lib ${CMAKE_CL_NOLOGO} <LINK_FLAGS> /out:<TARGET> <OBJECTS> ")

# compile a C++ file into an object file
set(CMAKE_Fortran_COMPILE_OBJECT
    "<CMAKE_Fortran_COMPILER>  ${CMAKE_START_TEMP_FILE} ${CMAKE_CL_NOLOGO} /object:<OBJECT> <FLAGS> /compile_only <SOURCE>${CMAKE_END_TEMP_FILE}")

set(CMAKE_Fortran_LINK_EXECUTABLE
    "<CMAKE_Fortran_COMPILER> ${CMAKE_CL_NOLOGO} ${CMAKE_START_TEMP_FILE} <FLAGS> /exe:<TARGET> <OBJECTS> /link <CMAKE_Fortran_LINK_FLAGS> <LINK_FLAGS> <LINK_LIBRARIES>${CMAKE_END_TEMP_FILE}")

set(CMAKE_CREATE_WIN32_EXE /winapp)
set(CMAKE_CREATE_CONSOLE_EXE )

if(CMAKE_GENERATOR MATCHES "Visual Studio 8")
  set (CMAKE_NO_BUILD_TYPE 1)
endif()
# does the compiler support pdbtype and is it the newer compiler

set(CMAKE_BUILD_TYPE_INIT Debug)
set (CMAKE_Fortran_FLAGS_INIT "")
set (CMAKE_Fortran_FLAGS_DEBUG_INIT "/debug:full")
set (CMAKE_Fortran_FLAGS_MINSIZEREL_INIT "/Optimize:2 /Define:NDEBUG")
set (CMAKE_Fortran_FLAGS_RELEASE_INIT "/Optimize:1 /Define:NDEBUG")
set (CMAKE_Fortran_FLAGS_RELWITHDEBINFO_INIT "/Optimize:1 /debug:full /Define:NDEBUG")

set (CMAKE_Fortran_STANDARD_LIBRARIES_INIT "user32.lib")

# executable linker flags
set (CMAKE_LINK_DEF_FILE_FLAG "/DEF:")
set (CMAKE_EXE_LINKER_FLAGS_INIT " /INCREMENTAL:YES")
if (CMAKE_COMPILER_SUPPORTS_PDBTYPE)
  set (CMAKE_EXE_LINKER_FLAGS_DEBUG_INIT "/debug /pdbtype:sept")
  set (CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO_INIT "/debug /pdbtype:sept")
else ()
  set (CMAKE_EXE_LINKER_FLAGS_DEBUG_INIT "/debug")
  set (CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO_INIT "/debug")
endif ()

set (CMAKE_SHARED_LINKER_FLAGS_INIT ${CMAKE_EXE_LINKER_FLAGS_INIT})
set (CMAKE_SHARED_LINKER_FLAGS_DEBUG_INIT ${CMAKE_EXE_LINKER_FLAGS_DEBUG_INIT})
set (CMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO_INIT ${CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO_INIT})
set (CMAKE_MODULE_LINKER_FLAGS_INIT ${CMAKE_SHARED_LINKER_FLAGS_INIT})
set (CMAKE_MODULE_LINKER_FLAGS_DEBUG_INIT ${CMAKE_SHARED_LINKER_FLAGS_DEBUG_INIT})
set (CMAKE_MODULE_LINKER_FLAGS_RELWITHDEBINFO_INIT ${CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO_INIT})
