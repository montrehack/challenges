cmake_minimum_required(VERSION 3.4)
project(fastcoll)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp block0.cpp block1.cpp block1stevens00.cpp block1stevens01.cpp block1stevens10.cpp block1stevens11.cpp block1wang.cpp md5.cpp)
add_executable(fastcoll ${SOURCE_FILES})

find_package(Boost)
if (Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIR})
    set (Boost_USE_STATIC_LIBS OFF) # enable dynamic linking
    set (Boost_USE_MULTITHREAD ON)  # enable multithreading
    find_package (Boost COMPONENTS REQUIRED filesystem program_options system)
    target_link_libraries(fastcoll ${Boost_LIBRARIES})
endif ()

