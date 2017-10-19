cmake_minimum_required(VERSION 3.5.1)  
project(DefectAnalysis)

########## Version information ########## 

set (DefectAnalysis_version_major 0)
set (DefectAnalysis_version_minor 1)
set (DefectAnalysis_version_patch 0)
set (CF_PACKAGE_VERSION ${DefectAnalysis_version_major}.${DefectAnalysis_version_minor}.${DefectAnalysis_version_patch})

### Echo an empty line and program version

message("")
message(STATUS "configuring DefectAnalysis version " ${DefectAnalysis_version_major} . ${DefectAnalysis_version_minor} . ${DefectAnalysis_version_patch})

### Set cmake module directory

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake-modules/" ${CMAKE_MODULE_PATH})
set(CMAKE_INCLUDE_DIRECTORIES_BEFORE ON)

### Set compiler flags

add_definitions(-O3)
if(UNIX)
		add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)
endif()

### Set include directories

include_directories(include) 
include_directories($ENV{HOME}/hdf5_parallel/include 
  $ENV{HOME}/Eigen
  /usr/local/intel/impi/5.0.1.035/intel64/include)
if(UNIX)
		include_directories(/usr/local/gcc6/include/c++/6.3.0)
endif()

### Set link directories

link_directories($ENV{HOME}/hdf5_parallel/lib
  /usr/local/intel/impi/5.0.1.035/intel64/lib)
if(UNIX)
		link_directories(/usr/local/gcc6/lib64)
		link_directories(/usr/local/gcc6/lib/gcc/x86_64-redhat-linux/6.3.0)
    link_directories(/usr/local/lib)
endif()

### Executable 

if(CMAKE_BUILD_TYPE STREQUAL "Release")
  set(exec_name "exec_run")
elseif(CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(exec_name "exec_debug")
else()
  set(exec_name "exec_run")
endif()

add_executable(${exec_name} 
  src/misc_tools.cpp
  src/read_write.cpp
  src/find_defects_multi.cpp 
  src/compute_defect.cpp)
target_link_libraries(${exec_name} hdf5 mpi)
if(UNIX)
		target_link_libraries(${exec_name} stdc++ supc++ gcc_s)
endif()
  
install(TARGETS ${exec_name} DESTINATION ${CMAKE_SOURCE_DIR}/bin)

