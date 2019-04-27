from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os

class NanoVGConan(ConanFile):
    name = "NanoVG"
    version = "master"
    license = "Zlib"
    author = "Mikko Mononen"
    url = "https://github.com/qno/conan-nanovg"
    description = "Antialiased 2D vector drawing library on top of OpenGL for UI and visualizations."

    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    options = {"shared": [True, False], "fons_use_freetype": [True, False]}
    default_options = dict({"shared": False,
                            "fons_use_freetype": False})

    _pkg_name = "nanovg-master"
    _libname = "nanovg"

    def source(self):
        url = "https://github.com/memononen/nanovg/archive/master.zip"
        self.output.info("Downloading {}".format(url))
        tools.get(url)
        self._createCMakeLists()

    def configure(self):
        if self._isVisualStudioBuild() and self.options.shared:
            raise ConanInvalidConfiguration("This library doesn't support dll's on Windows")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["FONS_USE_FREETYPE"] = self.options.fons_use_freetype
        cmake.configure(source_dir=self._pkg_name)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="{}{}src".format(self._pkg_name, os.sep))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self._libname]

        if not self.settings.os == "Macos":
            self.cpp_info.defines = ["NANOVG_GLEW"]
        # the defines for NANOVG_GL2_IMPLEMENTATION etc. are seem to be set by the using application ?
        # see https://github.com/memononen/nanovg/blob/1f9c8864fc556a1be4d4bf1d6bfe20cde25734b4/src/nanovg_gl.h#L37

        if self.options.fons_use_freetype:
            self.cpp_info.libs.append("freetype")

    def _isVisualStudioBuild(self):
        return self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"

    def _createCMakeLists(self):
        content = '''\
# THIS FILE WAS GENERATED BY CONAN RECIPE. DO NOT EDIT THIS FILE!
cmake_minimum_required(VERSION 3.5)
project(NanoVG)

include(${{CMAKE_BINARY_DIR}}/conanbuildinfo.cmake)
conan_basic_setup()

set(LIBNANOVG "{}")
set(SOURCES src/nanovg.c)

add_library(${{LIBNANOVG}} ${{SOURCES}})

if (MSVC)
   target_compile_definitions(${{LIBNANOVG}} PRIVATE _CRT_SECURE_NO_WARNINGS)
endif ()

if (FONS_USE_FREETYPE)
   find_package(Freetype REQUIRED)
   target_include_directories(${{LIBNANOVG}} PRIVATE ${{FREETYPE_INCLUDE_DIR_ft2build}})
   target_compile_definitions(${{LIBNANOVG}} PRIVATE FONS_USE_FREETYPE)
   target_link_libraries(${{LIBNANOVG}} PRIVATE ${{FREETYPE_LIBRARIES}})
endif ()
'''.format(self._libname)

        self.output.info("create CMakeLists.txt file")
        cmake_file = os.path.join(self._pkg_name, "CMakeLists.txt")
        f = open(cmake_file, "w+")
        f.write(content)
        f.close()
