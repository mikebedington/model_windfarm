
####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was PackageConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

#gsw-config.cmake
#
# Valid Find COMPONENTS:
#  * SHARED - Find shared libraries.
#  * STATIC - Find static libraries.
#
# Output variables set:
#  * gsw_LIBRARIES  - set to static libs if available, shared libs otherwise
#  * gsw_SHARED_LIBRARIES - shared libaries if availible
#  * gsw_STATIC_LIBRARIES - static libaries if availible
#  * gsw_BUILD_TYPES - build types provided
#
# Imported interface targets provided:
#  * gsw::gsw_static - static library target
#  * gsw::gsw_shared - shared library target:

#Include targets file.  This will create IMPORTED target gsw
include("${CMAKE_CURRENT_LIST_DIR}/gsw-targets.cmake")
set(gsw_SHARED_LIBRARIES)
set(gsw_STATIC_LIBRARIES)
set(gsw_SHARED_FOUND 0)
set(gsw_STATIC_FOUND 0)
if(ON)
    set(gsw_STATIC_LIBRARIES gsw::gsw_static)
    set(gsw_LIBRARIES gsw::gsw_static)
    set(gsw_STATIC_FOUND 1)
    if(OFF)
        set(gsw_SHARED_LIBRARIES gsw::gsw_shared)
        set(gsw_SHARED_FOUND 1)
    endif()
elseif(OFF)
    #Only shared libraries are build.  Set gsw_LIBRARIES to point to shared target.
    set(gsw_SHARED_LIBRARIES gsw::gsw_shared)
    set(gsw_LIBRARIES gsw::gsw_shared)
    set(gsw_SHARED_FOUND 1)
else()
    set(gsw_FOUND 0)
    set(gsw_NOT_FOUND_MESSAGE "Neither GSW_BUILD_SHARED_LIBS nor GSW_BUILD_STATIC_LIBS was set.  Unable to find any libraries.")
endif()

if(ON)
    get_target_property(gsw_BUILD_TYPES gsw::gsw_static IMPORTED_CONFIGURATIONS)
elseif(OFF)
    get_target_property(gsw_BUILD_TYPES gsw::gsw_shared IMPORTED_CONFIGURATIONS)
endif()

check_required_components("gsw")
