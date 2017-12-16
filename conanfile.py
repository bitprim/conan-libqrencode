#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibqrencodeConan(ConanFile):
    name = "libqrencode"
    version = "4.0.0"
    url = "https://github.com/bincrafters/conan-libqrencode.git"
    description = "A fast and compact QR Code encoding library"
    license = "Open source: https://github.com/fukuchi/libqrencode/blob/master/COPYING"
    exports = ["sources.patch"]
    exports_sources = ["CMakeLists.txt", "COPYING"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "libiconv/1.15@bincrafters/stable", \
        "libpng/1.6.34@bincrafters/stable"

    def source(self):
        source_url = "https://github.com/fukuchi/libqrencode"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        tools.patch(base_path=extracted_dir, patch_file="sources.patch")
        #Rename to "sources" is a convention to simplify later steps
        os.rename(extracted_dir, "sources")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["WITH_TOOLS"] = False
        cmake.definitions["WITH_TESTS"] = False
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="qrencode.h", dst="include", src="sources", keep_path=False)
        with tools.chdir("sources"):
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
