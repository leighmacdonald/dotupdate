#!/usr/bin/python
from argparse import ArgumentParser
from logging import getLogger, basicConfig, DEBUG, INFO

from pydot import install, config, InvalidConfiguration

log = getLogger('dotupdate')

options = {
    '-s --source': {
        "help"   : "Source directory containing your dotfiles to link to.\nDefault: ./dotfiles",
        "default": "./dotfiles"
    },
    '-d --dest' : {
        "help"    : "Where to link your dotfiles. The default is usually what you want.\nDefault: ~/",
        "default" : "~/"
    },
    '-b --backup' : {
        "help" : "Perform a backup of files that already exist",
        "action" : "store_true"
    },
    '--version' : {
        'action'  : 'version',
        'version' : "git@github.com:leighmacdonald/dotfiles.git"
    },
    '-t --test' : {
        'help'   : "Do a dry run printing what would have taken place",
        'action' : "store_true"
    },
    '--debug' : {
        'help' : "Enable debug output level",
        "action" : "store_true"
    }
}

def get_args():
    """ Parse the options from the config file if they are available. Then parse
    the command line options, which will override any options also defined in the
    configuration file

    :return: Dictionary of configuration options defined under "general" in config.ini of the \
             current directory
    :rtype: dict
    """
    # Parse config file options
    arg_parser = ArgumentParser(description="Utility for managing dotfiles")
    for option_name, args in options.items():
        arg_parser.add_argument(*option_name.split(' '), **args)
    args = dict()
    config_opts = config.items('general')
    bool_opts = ('backup', 'test')
    args.update(dict((k, v) for k, v in filter(lambda k: k[0] not in bool_opts, config_opts)))
    for key in bool_opts:
        args[key] = config.getboolean('general', key)
    # Parse and merge command line options
    args.update(arg_parser.parse_args().__dict__)
    return args

def main():
    args = get_args()
    log_level = DEBUG if args['debug'] else INFO
    basicConfig(level=log_level, format=":: %(name)s :: %(message)s")
    try:
        install(source_path=args['source'], dest_path=args['dest'], dry_run=args['test'])
    except InvalidConfiguration as err:
        log.exception(err)

if __name__ == "__main__":
    main()
