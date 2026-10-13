# Install script for directory: /home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/gotm_windfarm

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
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
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/gotm" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/gotm")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/gotm"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/gotm")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/gotm" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/gotm")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/gotm")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/gotmConfig.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/gotmConfig.cmake"
         "/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/CMakeFiles/Export/cmake/gotmConfig.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/gotmConfig-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/gotmConfig.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/CMakeFiles/Export/cmake/gotmConfig.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/CMakeFiles/Export/cmake/gotmConfig-release.cmake")
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/extern/gsw/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/extern/flexout/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/extern/fabm/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/airsea/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/util/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/turbulence/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/fabm/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/input/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/config/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/observations/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/meanflow/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/stokes_drift/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/seagrass/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/gotmlib/cmake_install.cmake")
  include("/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/tests/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/michael/Projects/ValMAS/Windfarm_carbon/Work_repo/scratch/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
