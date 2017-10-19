# Install script for directory: /usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Debug")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin/exec_debug" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin/exec_debug")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin/exec_debug"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin/exec_debug")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin" TYPE EXECUTABLE FILES "/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/build/exec_debug")
  if(EXISTS "$ENV{DESTDIR}/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin/exec_debug" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin/exec_debug")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin/exec_debug"
         OLD_RPATH "/usr/users/iff_th2/duman/hdf5_parallel/lib:/usr/local/intel/impi/5.0.1.035/intel64/lib:/usr/local/gcc6/lib64:/usr/local/gcc6/lib/gcc/x86_64-redhat-linux/6.3.0:/usr/local/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/bin/exec_debug")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/usr/users/iff_th2/duman/Defects/Scripts/DefectAnalysis/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
