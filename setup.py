#!/usr/bin/env python

from Cython.Distutils import build_ext
from distutils.errors import DistutilsExecError
from glob import glob
import os
import setuptools
from setuptools import find_packages, setup
import shutil
from subprocess import check_call

# discover the path to this setup.py file
thisScriptDir = os.path.dirname(os.path.realpath(__file__))

class ProtocCommand(setuptools.Command):
    user_options = [
        ('protoc=', 'p', "(default: 'protoc') path to protoc compiler. The default value can be set via the PROTOC environment variable"),
        ('raises=', 'r', '(default: True) if true, raise error on protobuf compilation error'),
    ]

    def initialize_options(self):
        self.protoc = os.environ['PROTOC'] if 'PROTOC' in os.environ else 'protoc'
        self.raises = True

    def finalize_options(self):
        print(f'searching for protoc executable at: {self.protoc}...')
        self.protoc = shutil.which(self.protoc)
        if self.protoc is None:
            if self.raises:
                raise DistutilsExecError('Could not find protoc executable.')
            else:
                print('Could not find protoc executable. Skipping protobuf compilation.')
        else:
            print(f'Found. Using protoc at: {self.protoc}')

    def run(self):
        if self.protoc is None:
            # bail if self.raises is False and protoc isn't found
            return

        protoDir = os.path.join(thisScriptDir, 'npbuf', 'protobuf')
        protoOutDir = os.path.join(thisScriptDir, 'npbuf', 'protobuf_py')
        protoSrcs = glob(os.path.join(protoDir, '*.proto'))

        # clean up any existing compiled protobufs
        shutil.rmtree(protoOutDir, ignore_errors=True)
        # create a new module for the compiled protobufs, including an `__init__.py`
        os.mkdir(protoOutDir)
        with open(os.path.join(protoOutDir, '__init__.py'), 'w') as f: pass

        # compile protobuf files to .py python modules
        protoc_python_cmd = [
            self.protoc,
            '--proto_path=%s' % protoDir,
            '--python_out=%s' % protoOutDir,
            ]
        protoc_python_cmd.extend(protoSrcs)

        check_call(protoc_python_cmd)

class DevelopCommand(setuptools.command.develop.develop):
    def run(self):
        # pass options to the protoc command and run it
        protocCommand = self.distribution.get_command_obj('protoc')
        protocCommand.database = self.database
        self.run_command('protoc')

        # run the normal develop command
        super().run(self)

setup(
    author = 'Max Klein',
    cmdclass = {'build_ext': build_ext,
                'develop': DevelopCommand,
                'protoc': ProtocCommand
    },
    description = 'provides Python protobuf types that can be used to serialize/deserialize Numpy arrays',
    license = 'Apache License, Version 2.0',
    name = 'numpy-protobuf',
    packages = find_packages(where='.', exclude=('npbuf.protobuf'))
)
