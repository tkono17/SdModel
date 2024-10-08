cmake_minimum_required(VERSION 3.0)
set(PROJECT_NAME SdModel)

project(${PROJECT_NAME})
set(${PROJECT_NAME} VERSION MAJOR 1)
set(${PROJECT_NAME} VERSION MAJOR 0)
set(DESTINATION $ENV{SWDIR})

set(CMAKE_INSTALL_PREFIX ${DESTINATION})

set(scriptfiles
  scripts/sdm-toJson.py)

# Installation
install(DIRECTORY ${CMAKE_SOURCE_DIR}/sdmodel
  DESTINATION python
  FILES_MATCHING PATTERN "*.py"
  )

foreach(prog ${scriptfiles})
  install(PROGRAMS ${prog} DESTINATION bin)
endforeach()

# Packaging
find_program(PYTHON python3)
if (PYTHON44)
  set(setupfiles setup.py setup.cfg)

  file(GLOB_RECURSE pyfiles RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} sdmodel/*.py)
  foreach(pyfile ${pyfiles} ${setupfiles} ${scriptfiles})
    get_filename_component(dn ${pyfile} DIRECTORY)
    file(COPY ${pyfile} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/${dn})
  endforeach()

  # Target: sdist
  # Get version from setup.cfg and set SDIST
  set(cmd "grep version setup.cfg | sed 's/.*=//g' | sed 's/ //g'")
  execute_process(COMMAND bash -c ${cmd} OUTPUT_VARIABLE version
    OUTPUT_STRIP_TRAILING_WHITESPACE)
  set(SDIST dist/sddgen-${version}.tar.gz)
  
  set(DEPS ${setupfiles} ${scriptfiles} ${pyfiles})
  add_custom_command(OUTPUT ${SDIST}
    COMMAND ${PYTHON}
    ARGS setup.py sdist
    DEPENDS ${DEPS})
  add_custom_target(sdist DEPENDS ${SDIST})

  # Target: pypi
  add_custom_target(pypi DEPENDS ${SDIST})

  # Target: testpypi
  add_custom_command(OUTPUT testpypi1
    COMMAND ${PYTHON}
    ARGS -m twine upload --repository testpypi ${SDIST}
    DEPENDS ${SDIST})
  add_custom_target(testpypi DEPENDS testpypi1 ${SDIST})
endif()
