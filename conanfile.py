from conans import ConanFile, CMake, tools
import os

class OpenColorIOConan(ConanFile):
    name = "opencolorio"
    version = "1.1.1"
    license = "BSD-3-Clause"
    description = "A color management framework for visual effects and animation."
    topics = ("graphics", "vfx", "color")
    homepage = "https://opencolorio.org/"
    url = "https://github.com/p-podsiadly/conan-opencolorio"

    settings = "os", "compiler", "build_type", "arch"
    
    options = {
        "shared": [True, False]
    }

    default_options = {
        "shared": False
    }

    generators = "cmake", "cmake_find_package"

    requires = [
        "yaml-cpp/0.6.3",
        "openexr/2.4.0"
    ]

    exports = ["ocio-*.patch"]

    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])

        os.rename("OpenColorIO-1.1.1", self._source_subfolder)

        tools.patch(
            self._source_subfolder,
            "ocio-{}.patch".format(self.version),
            strip=1)

    def _configure_cmake(self):

        cmake = CMake(self)

        cmake.definitions["OCIO_BUILD_SHARED"] = self.options.shared
        cmake.definitions["OCIO_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["OCIO_BUILD_TRUELIGHT"] = False
        cmake.definitions["OCIO_BUILD_APPS"] = False
        cmake.definitions["OCIO_BUILD_NUKE"] = False
        cmake.definitions["OCIO_BUILD_DOCS"] = False
        cmake.definitions["OCIO_BUILD_TESTS"] = False
        cmake.definitions["OCIO_BUILD_PYGLUE"] = False
        cmake.definitions["OCIO_BUILD_JNIGLUE"] = False
        cmake.definitions["OCIO_STATIC_JNIGLUE"] = False
        cmake.definitions["OCIO_USE_SSE"] = True
        cmake.definitions["OCIO_USE_BOOST_PTR"] = False
        cmake.definitions["USE_EXTERNAL_TINYXML"] = False
        cmake.definitions["TINYXML_OBJECT_LIB_EMBEDDED"] = True
        cmake.definitions["USE_EXTERNAL_LCMS"] = True

        cmake.configure(source_folder=self._source_subfolder)

        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        
        self.copy(
            pattern="*.h",
            src=os.path.join(self.source_folder, self._source_subfolder, "export/OpenColorIO"),
            dst="include/OpenColorIO")

        self.copy(
            pattern="*.h",
            src="export",
            dst="include/OpenColorIO")

        self.copy(pattern="*", src="lib", dst="lib")
        self.copy(pattern="*", src="bin", dst="bin")

        self.copy(
            pattern="LICENSE",
            src=os.path.join(self.source_folder, self._source_subfolder),
            dst="licenses")

    def package_info(self):

        self.cpp_info.names["cmake_find_package"] = "OpenColorIO"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenColorIO"

        self.cpp_info.libs = ["OpenColorIO"]

        if not self.options.shared:
            self.cpp_info.defines.append("OpenColorIO_STATIC")

