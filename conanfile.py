from conans import ConanFile, CMake
from conans import tools
from conans.tools import os_info, SystemPackageTool
import os, sys
import sysconfig

class DiscruptorConan(ConanFile):
    name = "disruptor"
    version = "1.0"

    description = "LDMAX Disruptor Pattern"
    url = "https://github.com/ulricheck/Disruptor-cpp"
    license = "APL"

    short_paths = True
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "virtualrunenv"

    options = {
    }

    requires = (
        "Boost/1.72.0@camposs/stable",
        )

    default_options = {
        "Boost:shared": True,
        "Boost:fPIC": True,
    }

    # all sources are deployed with the package
    exports_sources = "Disruptor/*", "Disruptor.PerfTests/*", "DisruptorTestTools/*", "googletest-release-1.8.0/*", "msvc/*", "cmake_uninstall.cmake.in", "CMakeLists.txt", "Disruptor.cmake"

    def requirements(self):
        pass

    def configure(self):
        pass

    def imports(self):
        self.copy(src="bin", pattern="*.dll", dst="./bin") # Copies all dll files from packages bin folder to my "bin" folder
        self.copy(src="lib", pattern="*.dll", dst="./bin") # Copies all dll files from packages bin folder to my "bin" folder
        self.copy(src="lib", pattern="*.dylib*", dst="./lib") # Copies all dylib files from packages lib folder to my "lib" folder
        self.copy(src="lib", pattern="*.so*", dst="./lib") # Copies all so files from packages lib folder to my "lib" folder
        self.copy(src="lib", pattern="*.a", dst="./lib") # Copies all static libraries from packages lib folder to my "lib" folder
        self.copy(src="bin", pattern="*", dst="./bin") # Copies all applications


    def _configure_cmake(self):
        cmake = CMake(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            cmake.definitions[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        cmake.configure()

        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
