set(CMAKE_SHARED_LIBRARY_CREATE_C_FLAGS "-shared")

# no optimization in tcc:
string(APPEND CMAKE_C_FLAGS_INIT " ")
string(APPEND CMAKE_C_FLAGS_DEBUG_INIT " -g")
string(APPEND CMAKE_C_FLAGS_MINSIZEREL_INIT " -DNDEBUG")
string(APPEND CMAKE_C_FLAGS_RELEASE_INIT " -DNDEBUG")
string(APPEND CMAKE_C_FLAGS_RELWITHDEBINFO_INIT " -g -DNDEBUG")
