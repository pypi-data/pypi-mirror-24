set(CMAKE_C_COMPILE_OPTIONS_PIC -K PIC)
set(CMAKE_C_COMPILE_OPTIONS_PIE "")
set(CMAKE_SHARED_LIBRARY_C_FLAGS "-K PIC")
set(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "-Wl,-Bexport")
include(Platform/UnixPaths)
