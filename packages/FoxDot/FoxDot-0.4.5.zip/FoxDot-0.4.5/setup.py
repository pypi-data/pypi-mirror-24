#!/usr/bin/env python

from distutils.core import setup   

setup(name='FoxDot',
      version='0.4.5',
      description='Live Coding with SuperCollider',
      author='Ryan Kirkbride',
      author_email='sc10rpk@leeds.ac.uk',
      url='http://foxdot.org/',
      packages=['FoxDot',
                'FoxDot.lib',
                'FoxDot.lib.Code',
                'FoxDot.lib.Custom',
                'FoxDot.lib.Workspace',
                'FoxDot.lib.Patterns',
                'FoxDot.lib.SCLang',
                'FoxDot.lib.Settings',
                'FoxDot.lib.Utils'],
      package_data = {'FoxDot': ['snd/*/*/*.*',
                                 'snd/_loop_/foxdot.wav',
                                 'snd/_loop_/drums130.wav',
                                 'snd/_loop_/dirty120.wav',
                                 'osc/*.scd',
                                 'osc/sceffects/*.scd',
                                 'osc/scsyndef/*.scd'],
                      'FoxDot.lib.Workspace': ['img/*'],
                      'FoxDot.lib.Settings' : ['conf.txt']})
