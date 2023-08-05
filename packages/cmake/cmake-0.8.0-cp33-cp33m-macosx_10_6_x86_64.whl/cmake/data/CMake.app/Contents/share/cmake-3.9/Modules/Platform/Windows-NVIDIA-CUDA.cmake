include(Platform/Windows-MSVC)

set(CMAKE_CUDA_COMPILE_PTX_COMPILATION
  "<CMAKE_CUDA_COMPILER> ${CMAKE_CUDA_HOST_FLAGS} <DEFINES> <INCLUDES> <FLAGS> -x cu -ptx <SOURCE> -o <OBJECT> -Xcompiler=-Fd<TARGET_COMPILE_PDB>,-FS")
set(CMAKE_CUDA_COMPILE_SEPARABLE_COMPILATION
  "<CMAKE_CUDA_COMPILER> ${CMAKE_CUDA_HOST_FLAGS} <DEFINES> <INCLUDES> <FLAGS> -x cu -dc <SOURCE> -o <OBJECT> -Xcompiler=-Fd<TARGET_COMPILE_PDB>,-FS")
set(CMAKE_CUDA_COMPILE_WHOLE_COMPILATION
  "<CMAKE_CUDA_COMPILER> ${CMAKE_CUDA_HOST_FLAGS} <DEFINES> <INCLUDES> <FLAGS> -x cu -c <SOURCE> -o <OBJECT> -Xcompiler=-Fd<TARGET_COMPILE_PDB>,-FS")

set(__IMPLICT_LINKS )
foreach(dir ${CMAKE_CUDA_HOST_IMPLICIT_LINK_DIRECTORIES})
  string(APPEND __IMPLICT_LINKS " -LIBPATH:\"${dir}\"")
endforeach()
foreach(lib ${CMAKE_CUDA_HOST_IMPLICIT_LINK_LIBRARIES})
  string(APPEND __IMPLICT_LINKS " \"${lib}\"")
endforeach()
set(CMAKE_CUDA_LINK_EXECUTABLE
   "<CMAKE_CUDA_HOST_LINK_LAUNCHER> <CMAKE_CUDA_LINK_FLAGS> <LINK_FLAGS> <OBJECTS> /out:<TARGET> /implib:<TARGET_IMPLIB> /pdb:<TARGET_PDB> /version:<TARGET_VERSION_MAJOR>.<TARGET_VERSION_MINOR> <LINK_LIBRARIES>${__IMPLICT_LINKS}")

set(_CMAKE_VS_LINK_DLL "<CMAKE_COMMAND> -E vs_link_dll --intdir=<OBJECT_DIR> --manifests <MANIFESTS> -- ")
set(_CMAKE_VS_LINK_EXE "<CMAKE_COMMAND> -E vs_link_exe --intdir=<OBJECT_DIR> --manifests <MANIFESTS> -- ")
set(CMAKE_CUDA_CREATE_SHARED_LIBRARY
  "${_CMAKE_VS_LINK_DLL}<CMAKE_LINKER> ${CMAKE_CL_NOLOGO} <OBJECTS> ${CMAKE_START_TEMP_FILE} /out:<TARGET> /implib:<TARGET_IMPLIB> /pdb:<TARGET_PDB> /dll /version:<TARGET_VERSION_MAJOR>.<TARGET_VERSION_MINOR>${_PLATFORM_LINK_FLAGS} <LINK_FLAGS> <LINK_LIBRARIES>${__IMPLICT_LINKS} ${CMAKE_END_TEMP_FILE}")

set(CMAKE_CUDA_CREATE_SHARED_MODULE ${CMAKE_CUDA_CREATE_SHARED_LIBRARY})
set(CMAKE_CUDA_CREATE_STATIC_LIBRARY  "<CMAKE_LINKER> /lib ${CMAKE_CL_NOLOGO} <LINK_FLAGS> /out:<TARGET> <OBJECTS> ")
set(CMAKE_CUDA_LINKER_SUPPORTS_PDB ON)
set(CMAKE_CUDA_LINK_EXECUTABLE
  "${_CMAKE_VS_LINK_EXE}<CMAKE_LINKER> ${CMAKE_CL_NOLOGO} <OBJECTS> ${CMAKE_START_TEMP_FILE} /out:<TARGET> /implib:<TARGET_IMPLIB> /pdb:<TARGET_PDB> /version:<TARGET_VERSION_MAJOR>.<TARGET_VERSION_MINOR>${_PLATFORM_LINK_FLAGS} <CMAKE_CUDA_LINK_FLAGS> <LINK_FLAGS> <LINK_LIBRARIES>${__IMPLICT_LINKS} ${CMAKE_END_TEMP_FILE}")
unset(_CMAKE_VS_LINK_EXE)
unset(_CMAKE_VS_LINK_EXE)

if(CMAKE_CUDA_COMPILER_VERSION VERSION_GREATER_EQUAL "8.0.0")
  set(_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS "-Wno-deprecated-gpu-targets")
else()
  set(_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS "")
endif()

set(CMAKE_CUDA_DEVICE_LINK_LIBRARY
  "<CMAKE_CUDA_COMPILER> <CMAKE_CUDA_LINK_FLAGS> <LANGUAGE_COMPILE_FLAGS> ${_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS} -shared -dlink <OBJECTS> -o <TARGET> <LINK_LIBRARIES> -Xcompiler=-Fd<TARGET_COMPILE_PDB>,-FS")
set(CMAKE_CUDA_DEVICE_LINK_EXECUTABLE
  "<CMAKE_CUDA_COMPILER> <FLAGS> <CMAKE_CUDA_LINK_FLAGS> ${_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS} -shared -dlink <OBJECTS> -o <TARGET> <LINK_LIBRARIES> -Xcompiler=-Fd<TARGET_COMPILE_PDB>,-FS")

unset(_CMAKE_CUDA_EXTRA_DEVICE_LINK_FLAGS)

string(REPLACE "/D" "-D" _PLATFORM_DEFINES_CUDA "${_PLATFORM_DEFINES}${_PLATFORM_DEFINES_CXX}")

string(APPEND CMAKE_CUDA_FLAGS_INIT " ${PLATFORM_DEFINES_CUDA} -D_WINDOWS -Xcompiler=\"/W3${_FLAGS_CXX}\"")
string(APPEND CMAKE_CUDA_FLAGS_DEBUG_INIT " -Xcompiler=\"-MDd -Zi -Ob0 -Od ${_RTC1}\"")
string(APPEND CMAKE_CUDA_FLAGS_RELEASE_INIT " -Xcompiler=\"-MD -O2 -Ob2\" -DNDEBUG")
string(APPEND CMAKE_CUDA_FLAGS_RELWITHDEBINFO_INIT " -Xcompiler=\"-MD -Zi -O2 -Ob1\" -DNDEBUG")
string(APPEND CMAKE_CUDA_FLAGS_MINSIZEREL_INIT " -Xcompiler=\"-MD -O1 -Ob1\" -DNDEBUG")

set(CMAKE_CUDA_STANDARD_LIBRARIES_INIT "${CMAKE_C_STANDARD_LIBRARIES_INIT}")
