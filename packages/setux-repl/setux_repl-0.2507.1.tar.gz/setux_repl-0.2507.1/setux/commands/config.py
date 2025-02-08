from pybrary.command import Command

from setux.targets import Local


local_config = Local().config
config_dict = local_config.config.config


class ConfigCmd(Command):
    '''Setux Configuration.

    Edit the Setux Config file.
    '''
    def run(self):
        local_config.edit()

