#!/usr/bin/env python

import sys
import platform
import subprocess
import io
import re
import os
from distutils.command.build import build
from distutils.command.install import install

import struct

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

package_name = 'camb'
if platform.system() == "Windows":
    DLLNAME = 'cambdll.dll'
else:
    DLLNAME = 'camblib.so'
file_dir = os.path.abspath(os.path.dirname(__file__))

os.chdir(file_dir)

is32Bit = struct.calcsize("P") == 4

with open('README.rst') as f:
    long_description = f.read()


def find_version():
    version_file = io.open(os.path.join(file_dir, '%s/__init__.py' % package_name)).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def has_win_gfortran():
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        if os.path.isfile(os.path.join(path, 'gfortran.exe')):
            return True
    return False


class SharedLibrary(build):
    def run(self):
        CAMBDIR = os.path.join(file_dir, '..')
        if not os.path.exists(os.path.join(CAMBDIR, 'lensing.f90')):
            CAMBDIR = os.path.join(file_dir, 'fortran')  # pypi install
            pycamb_path = '..'
        else:
            pycamb_path = 'pycamb'
        os.chdir(CAMBDIR)
        if platform.system() == "Windows":
            COMPILER = "gfortran"
            # note that TDM-GCC MingW 5.1 does not work due go general fortran bug.
            # This works: http://sourceforge.net/projects/mingw-w64/?source=typ_redirect
            # but need to use 32bit compiler to build 32 bit dll (contrary to what is implied)
            FFLAGS = "-shared -static -cpp -fopenmp -O3 -ffast-math -fmax-errors=4"
            if is32Bit: FFLAGS = "-m32 " + FFLAGS
            SOURCES = "constants.f90 utils.f90 subroutines.f90 inifile.f90 power_tilt.f90 recfast.f90 reionization.f90" \
                      " modules.f90 bessels.f90 equations.f90 halofit_ppf.f90 lensing.f90 SeparableBispectrum.f90 cmbmain.f90" \
                      " camb.f90 camb_python.f90"
            OUTPUT = r"-o %s\camb\%s" % (pycamb_path, DLLNAME)
            scrs = os.listdir(os.getcwd())
            if not has_win_gfortran():
                print('WARNING: gfortran not in path (if you just installed you may need to log off and on again).')
                print('         You can get a Windows gfortan build from http://sourceforge.net/projects/mingw-w64/')
                print('         (get the %s version to match this python installation)' % (('x86_64', 'i686')[is32Bit]))
                print('Using pre-compiled binaries instead - any local changes will be ignored...')
                COPY = r'copy /Y %s\dlls\%s %s\camb\%s' % (
                    pycamb_path, ('cambdll_x64.dll', DLLNAME)[is32Bit], pycamb_path, DLLNAME)
                subprocess.call(COPY, shell=True)
            else:
                print(COMPILER + ' ' + FFLAGS + ' ' + SOURCES + ' ' + OUTPUT)
                subprocess.call(COMPILER + ' ' + FFLAGS + ' ' + SOURCES + ' ' + OUTPUT, shell=True)
            COPY = r"copy /Y HighLExtrapTemplate_lenspotentialCls.dat %s\camb" % (pycamb_path)
            subprocess.call(COPY, shell=True)
            scrs.append(DLLNAME)
            if not os.path.isfile(os.path.join(pycamb_path, 'camb', DLLNAME)): sys.exit('Compilation failed')
            print("Removing temp files")
            nscrs = os.listdir(os.getcwd())
            for file in nscrs:
                if not file in scrs:
                    os.remove(file)

        else:
            print("Compiling source...")
            try:
                from pkg_resources import parse_version
                try:
                    gfortran_version = subprocess.check_output("gfortran -dumpversion", shell=True).decode()
                except subprocess.CalledProcessError:
                    gfortran_version = '0.0'
                if parse_version(gfortran_version) < parse_version('4.9'):
                    raise Exception(
                        'You need gfortran 4.9 or higher to compile the python CAMB wrapper (%s).' % gfortran_version)
            except ImportError:
                pass

            subprocess.call("make camblib.so COMPILER=gfortran", shell=True)
            if not os.path.isfile(os.path.join('Releaselib', 'camblib.so')): sys.exit('Compilation failed')
            subprocess.call("chmod 755 Releaselib/camblib.so", shell=True)
            subprocess.call(r"cp Releaselib/camblib.so %s/camb" % (pycamb_path), shell=True)
            subprocess.call("cp HighLExtrapTemplate_lenspotentialCls.dat %s/camb" % (pycamb_path), shell=True)

        os.chdir(file_dir)
        build.run(self)


class CustomInstall(install):
    def run(self):
        self.run_command('build')
        install.run(self)


setup(name=package_name,
      version=find_version(),
      description='Code for Anisotropies in the Microwave Background',
      long_description=long_description,
      author='Antony Lewis',
      url="http://camb.info/",
      cmdclass={'build': SharedLibrary, 'install': CustomInstall},
      packages=['camb', 'camb_tests'],
      package_data={'camb': [DLLNAME, 'HighLExtrapTemplate_lenspotentialCls.dat',
                             'PArthENoPE_880.2_marcucci.dat', 'PArthENoPE_880.2_standard.dat']},
      test_suite='camb_tests',
      classifiers=[
          "Programming Language :: Python :: 2",
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      keywords=['cosmology', 'CAMB']
      )
