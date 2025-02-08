from os import environ
from subprocess import run

from pybrary import Config

from setux.core.manage import Manager


default_script_header = '''
    #!/bin/bash
    shopt -s expand_aliases
    set -e
'''

default_config = dict(
    target = 'local',
    venv   = 'setux',
)


class Distro(Manager):
    '''Setux Config
    '''
    manager = 'config'
    config = Config('setux', default_config)

    def edit(self):
        run([
            environ.get('EDITOR','vim'),
            self.config.path,
        ])

    @property
    def script_header(self):
        return self.config.script_header or default_script_header

    def __getattr__(self, name):
        return getattr(self.config, name)

    def __iter__(self):
        return iter(self.config)

    def __getitem__(self, name):
        return self.config[name]

    def __contains__(self, name):
        return name in self.config

    def get(self, name):
        return self.config.get(name)
