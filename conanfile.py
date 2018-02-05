#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibqrencodeConan(ConanFile):
    name = "libqrencode"
    version = "4.0.0"
    url = "https://github.com/bitprim/conan-libqrencode"
    description = "A fast and compact QR Code encoding library"
    license = "LGPL-2.1, LGPL-3.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "sources.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    options = {
                "shared": [True, False], 
                "fPIC": [True, False]
    }

    default_options = "shared=False", "fPIC=True"


    build_policy = "missing"
    
    requires = (
        "libiconv/1.15@bitprim/stable", 
        "libpng/1.6.34@bitprim/stable"
    )

    @property
    def msvc_mt_build(self):
        return "MT" in str(self.settings.compiler.runtime)

    @property
    def fPIC_enabled(self):
        if self.settings.compiler == "Visual Studio":
            return False
        else:
            return self.options.fPIC

    @property
    def is_shared(self):
        # if self.options.shared and self.msvc_mt_build:
        if self.settings.compiler == "Visual Studio" and self.msvc_mt_build:
            return False
        else:
            return self.options.shared

    def configure(self):
        del self.settings.compiler.libcxx #Pure-C 

    def config_options(self):
        self.output.info('*-*-*-*-*-* def config_options(self):')
        if self.settings.compiler == "Visual Studio":
            self.options.remove("fPIC")

            if self.options.shared and self.msvc_mt_build:
                self.options.remove("shared")


    def source(self):
        source_url = "https://github.com/fukuchi/libqrencode"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        tools.patch(base_path=extracted_dir, patch_file="sources.patch")
        #Rename to "sources" is a convention to simplify later steps
        os.rename(extracted_dir, "sources")

    def build(self):
        cmake = CMake(self)
        
        cmake.verbose = True

        cmake.definitions["WITH_TOOLS"] = False
        cmake.definitions["WITH_TESTS"] = False

        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.fPIC_enabled

        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="qrencode.h", dst="include", src="sources", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
