import os
import sys
from sipconfig import Configuration, ModuleMakefile
from PyQt5.QtCore import PYQT_CONFIGURATION

# The name of the SIP build file generated by SIP and used by the build
# system.
build_file = "qcustomplot.sbf"

# Get the PyQt configuration information.
config = Configuration()
# Should be detected automatically, but if not, override here
#config.platform = "win32-msvc2008"

# Get the extra SIP flags needed by the imported PyQt modules.  Note that
# this normally only includes those flags (-x and -t) that relate to SIP's
# versioning system.
pyqt_sip_flags = PYQT_CONFIGURATION['sip_flags']
if sys.version_info[0] == 3:
    pyqt_sip_dir = '/usr/share/sip/PyQt5'
elif sys.version_info[0] == 2:
    pyqt_sip_dir = '/usr/share/python-sip/PyQt5'

# Run SIP to generate the code.  Note that we tell SIP where to find the qt
# module's specification files using the -I flag.
command = " ".join([config.sip_bin, "-c", ".", "-b", build_file, "-o", "-I", pyqt_sip_dir,  pyqt_sip_flags, "qcustomplot.sip"])
os.system(command)
print(command)

# We are going to install the SIP specification file for this module and
# its configuration module.
installs = []

installs.append(["qcustomplot.sip", os.path.join(config.default_sip_dir, "qcustomplot")])

#installs.append(["qcustomplotconfig.py", config.default_mod_dir])

# Create the Makefile.  The QtGuiModuleMakefile class provided by the
# pyqtconfig module takes care of all the extra preprocessor, compiler and
# linker flags needed by the Qt library.
makefile = ModuleMakefile(
    configuration=config,
    build_file=build_file,
    installs=installs
)

# Add the library we are wrapping.  The name doesn't include any platform
# specific prefixes or extensions (e.g. the "lib" prefix on UNIX, or the
# ".dll" extension on Windows).
if config.platform.startswith('win32'):
    libname = 'qcustomplot1'
    makefile.generator = "NMAKE"
else:
    libname = 'qcustomplot'
include_base = '/usr/include/x86_64-linux-gnu/'
makefile.extra_include_dirs = [include_base + d for d in ['', 'qt5', 'qt5/QtCore', 'qt5/QtWidgets', 'qt5/QtGui', 'qt5/QtPrintSupport']]
makefile.extra_libs = [libname]
makefile.extra_lib_dirs = ["/usr/lib/x86_64-linux-gnu"]

# Generate the Makefile itself.
makefile.generate()

# Now we create the configuration module.  This is done by merging a Python
# dictionary (whose values are normally determined dynamically) with a
# (static) template.
content = {
    # Publish where the SIP specifications for this module will be
    # installed.
    "qcustomplot_sip_dir":    config.default_sip_dir,

    # Publish the set of SIP flags needed by this module.  As these are the
    # same flags needed by the qt module we could leave it out, but this
    # allows us to change the flags at a later date without breaking
    # scripts that import the configuration module.
    "qcustomplot_sip_flags":  pyqt_sip_flags
}

# This creates the helloconfig.py module from the helloconfig.py.in
# template and the dictionary.
#sipconfig.create_config_module("qcustomplotconfig.py", "qcustomplotconfig.py.in", content)
