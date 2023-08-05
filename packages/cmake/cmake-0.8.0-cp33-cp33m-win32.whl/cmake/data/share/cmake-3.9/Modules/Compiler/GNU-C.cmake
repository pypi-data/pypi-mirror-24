include(Compiler/GNU)
__compiler_gnu(C)

if (NOT CMAKE_C_COMPILER_VERSION VERSION_LESS 4.5)
  set(CMAKE_C90_STANDARD_COMPILE_OPTION "-std=c90")
  set(CMAKE_C90_EXTENSION_COMPILE_OPTION "-std=gnu90")
elseif (NOT CMAKE_C_COMPILER_VERSION VERSION_LESS 3.4)
  set(CMAKE_C90_STANDARD_COMPILE_OPTION "-std=c89")
  set(CMAKE_C90_EXTENSION_COMPILE_OPTION "-std=gnu89")
endif()

if (NOT CMAKE_C_COMPILER_VERSION VERSION_LESS 3.4)
  set(CMAKE_C99_STANDARD_COMPILE_OPTION "-std=c99")
  set(CMAKE_C99_EXTENSION_COMPILE_OPTION "-std=gnu99")
endif()

if (NOT CMAKE_C_COMPILER_VERSION VERSION_LESS 4.7)
  set(CMAKE_C11_STANDARD_COMPILE_OPTION "-std=c11")
  set(CMAKE_C11_EXTENSION_COMPILE_OPTION "-std=gnu11")
elseif (NOT CMAKE_C_COMPILER_VERSION VERSION_LESS 4.6)
  set(CMAKE_C11_STANDARD_COMPILE_OPTION "-std=c1x")
  set(CMAKE_C11_EXTENSION_COMPILE_OPTION "-std=gnu1x")
endif()

__compiler_check_default_language_standard(C 3.4 90 5.0 11)
