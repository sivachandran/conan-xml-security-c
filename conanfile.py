from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, rm, rmdir, collect_libs
from conan.tools.gnu import Autotools, AutotoolsToolchain, PkgConfigDeps
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=2.0.17"


class Libxmlsecurityc(ConanFile):
    name = "libxml-security-c"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://santuario.apache.org/cindex.html"
    license = "Apache License 2.0"
    description = "C++ library is an implementation of the XML Digital Signature and Encryption specifications, along with some additional XKMS code"
    topics = ("xml")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "disable_xkms": [True, False],
        "with_xalan": [True, False],
        "with_openssl": [True, False],
        "with_nss": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "disable_xkms": False,
        "with_xalan": True,
        "with_openssl": True,
        "with_nss": False,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        basic_layout(self, src_folder="src")

    def validate(self):
        if self.options.with_openssl == self.options.with_nss:
            raise ConanInvalidConfiguration("either OpenSSL or NSS should be enabled, not both")

    def requirements(self):
        self.requires("xerces-c/3.2.5")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        pc = PkgConfigDeps(self)
        pc.generate()

        tc = AutotoolsToolchain(self)
        if self.settings.build_type == "Debug":
            tc.configure_args.extend([ "--enable-debug" ])
        if self.options.shared:
            tc.configure_args.extend([
                "--enable-shared=yes",
                "--enable-static=no",
            ])
        else:
            tc.configure_args.extend([
                "--enable-shared=no",
                "--enable-static=yes",
            ])
        if not self.options.disable_xkms:
            tc.configure_args.extend([ "--disable-xkms" ])
        if self.options.with_xalan:
            tc.configure_args.extend([ "--with-xalan" ])
        if self.options.with_openssl:
            tc.configure_args.extend([ "--with-openssl" ])
        elif self.options.with_nss:
            tc.configure_args.extend([ "--with-nss" ])
        tc.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()
        rm(self, "*.la", os.path.join(self.package_folder, "lib"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "XmlSecurityC")
        self.cpp_info.set_property("cmake_target_name", "XmlSecurityC::XmlSecurityC")
        self.cpp_info.set_property("pkg_config_name", "xml-security-c")
        self.cpp_info.libs = collect_libs(self)
        if self.settings.os == "Macos":
            self.cpp_info.frameworks = ["CoreFoundation", "CoreServices"]
        elif self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("pthread")
