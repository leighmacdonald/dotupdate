#!/usr/bin/python
from argparse import ArgumentParser
from logging import getLogger, basicConfig, DEBUG, INFO

from pydot import install, config, InvalidConfiguration

log = getLogger('dotupdate')

options = {
    '-s --source': {
        "help"   : "Source directory containing your dotfiles to link to.\nDefault: ./dotfiles",
        "default": None
    },
    '-d --dest' : {
        "help"    : "Where to link your dotfiles. The default is usually what you want.\nDefault: ~/",
        "default" : None
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
    },
    '-i --ignore' : {
        "help" : "Comma separated list of files and folders to ignore linking from inside your source directory",
        "action" : "store",
        "default": ""
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
    bool_opts = ['backup', 'test']
    list_opts = ['ignore']
    args.update(dict((k, v) for k, v in filter(lambda k: k[0] not in bool_opts + list_opts, config_opts)))
    for key in bool_opts:
        args[key] = config.getboolean('general', key)
    for key in list_opts:
        args[key] = filter(None, config.get('general', key).split(','))

    # Parse and merge command line options
    cli_args = arg_parser.parse_args().__dict__
    for key in filter(lambda k: k not in list_opts, cli_args.keys()):
        if cli_args[key]:
            args[key] = cli_args[key]
    for key in list_opts:
        if cli_args[key]:
            args[key] =  filter(None, cli_args[key].split(','))
    return args

def main():
    """ Setup and run the installer

    :return:
    :rtype:
    """
    args = get_args()
    log_level = DEBUG if args['debug'] else INFO
    basicConfig(level=log_level, format=":: %(name)s :: %(message)s")
    ret_val = 1
    try:
        install(source_path=args['source'], dest_path=args['dest'], dry_run=args['test'],
            ignore_list=args['ignore'])
        ret_val = 0
    except InvalidConfiguration as err:
        log.error(err)
    finally:
        return ret_val

if __name__ == "__main__":
    exit(main())
