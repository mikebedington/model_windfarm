#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gsw::gsw_static" for configuration "Release"
set_property(TARGET gsw::gsw_static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(gsw::gsw_static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "Fortran"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgsw.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS gsw::gsw_static )
list(APPEND _IMPORT_CHECK_FILES_FOR_gsw::gsw_static "${_IMPORT_PREFIX}/lib/libgsw.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
