#!/usr/bin/python
from argparse import ArgumentParser
from logging import getLogger, basicConfig, DEBUG, INFO
from glob import glob
from os.path import abspath, lexists, exists, join, expanduser, dirname
from os import symlink

try:
    from configparser import ConfigParser
except ImportError:
    #noinspection PyUnresolvedReferences
    from ConfigParser import SafeConfigParser as ConfigParser

try:
    from argparse import ArgumentParser

    parser = True
except ImportError:
    parser = False

log = getLogger('dotupdate')

class InvalidConfiguration(Exception):
    """Used when a user configures bad paths"""


class LinkExists(OSError):
    pass


class FileExists(OSError):
    pass


def install(source_path=".", source_filter="*", dest_path="~/", backup=True, dry_run=True,
            ignore_list=None):
    """ Install a set of files from the specified source path into the dest_path.

    An example of the transformation that will take place:

    initial_path: ~/
                  ~/.bashrc (v0)

    source path : ./my_dot_files
                  ./my_dot_files/bashrc (v1)
                  ./my_dot_files/vim (v0)

    dest_path   : ~/
                  ~/.bashrc (v1)
                  ~/.vim (v0)


    :param source_path:
    :type source_path:
    :param source_filter:
    :type source_filter:
    :param dest_path:
    :type dest_path:
    :return:
    :rtype:
    """
    full_source_path = abspath(expanduser(source_path))
    if not exists(full_source_path):
        err = "Source dotfiles path does not exist {0}, cannot continue!".format(full_source_path)
        raise InvalidConfiguration(err)
    dest_path = expanduser(dest_path)
    if not exists(dest_path):
        raise InvalidConfiguration("Dest path does not exist {0}".format(dest_path))
    full_dest_path = abspath(expanduser(dest_path))
    filter_txt = "{0}/{1}".format(source_path, source_filter)
    potential_links = glob(filter_txt)
    if not potential_links:
        error_msg = "No potential candidates for linking found at {0}".format(source_path)
        raise InvalidConfiguration(error_msg)

    for link in potential_links:
        cut_size = len(source_path)
        if link[0:2] == "./":
            link = link[2:]
            cut_size -= 2
        link = link[cut_size:]
        if link[0] == "/":
            link = link[1:]
        if ignore_list and link in ignore_list:
            log.debug("Skipped ignored file {0}".format(link))
            continue
        dest_link = join(full_dest_path, '.' + link)
        source_link = join(full_source_path, link)
        try:
            if lexists(dest_link):
                raise LinkExists("Link exists {0}".format(dest_link))
            if exists(dest_link):
                raise FileExists("File exists already {0}".format(dest_link))
        except FileExists:
            log.warn("File already exists {0}".format(dest_link))
        except LinkExists:
            log.warn("Symlink already exists {0}".format(dest_link))
        else:
            if dry_run:
                log.info("dryrun :: ln -s {0} {1}".format(source_link, dest_link))
            else:
                try:
                    symlink(source_link, dest_link)
                except OSError as err:
                    log.exception(err)

config = None
if not config:
    config = ConfigParser()
    config_file = join(dirname(dirname(__file__)), 'config.ini')
    if exists(config_file):
        log.debug("Reading config file {0}".format(config_file))
        read_ok = config.read(config_file)
        if not read_ok:
            log.warn("Failed to read configuration file {0}".format(config_file))

options = {
    '-s --source': {
        "help": "Source directory containing your dotfiles to link to.\nDefault: ./dotfiles",
        "default": None
    },
    '-d --dest': {
        "help": "Where to link your dotfiles. The default is usually what you want.\nDefault: ~/",
        "default": None
    },
    '-b --backup': {
        "help": "Perform a backup of files that already exist",
        "action": "store_true"
    },
    '--version': {
        'action': 'version',
        'version': "git@github.com:leighmacdonald/dotfiles.git"
    },
    '-t --test': {
        'help': "Do a dry run printing what would have taken place",
        'action': "store_true"
    },
    '--debug': {
        'help': "Enable debug output level",
        "action": "store_true"
    },
    '-i --ignore': {
        "help": "Comma separated list of files and folders to ignore linking from inside your source directory",
        "action": "store",
        "default": ""
    }
}

def parse_args():
    """ Parse the options from the config file if they are available. Then parse
    the command line options, which will override any options also defined in the
    configuration file

    :return: Dictionary of configuration options defined under "general" in config.ini of the \
             current directory
    :rtype: dict
    """
    # Parse config file options
    args = dict()
    config_opts = config.items('general')
    bool_opts = ['backup', 'test']
    list_opts = ['ignore']
    args.update(dict((k, v) for k, v in filter(lambda k: k[0] not in bool_opts + list_opts, config_opts)))
    for key in bool_opts:
        args[key] = config.getboolean('general', key)
    for key in list_opts:
        args[key] = filter(None, config.get('general', key).split(','))

    if parser:
        arg_parser = ArgumentParser(description="Utility for managing dotfiles")
        for option_name, args in options.items():
            arg_parser.add_argument(*option_name.split(' '), **args)
            # Parse and merge command line options
        cli_args = arg_parser.parse_args().__dict__
        for key in filter(lambda k: k not in list_opts, cli_args.keys()):
            if cli_args[key]:
                args[key] = cli_args[key]
        for key in list_opts:
            if cli_args[key]:
                args[key] = filter(None, cli_args[key].split(','))
    return args


def main():
    """ Setup and run the installer

    :return:
    :rtype:
    """
    args = parse_args()
    log_level = DEBUG if args['debug'] else INFO
    basicConfig(level=log_level, format=":: %(name)s :: %(message)s")
    ret_val = 1
    try:
        install(source_path=args['source'], dest_path=args['dest'], dry_run=args['test'],
            ignore_list=args['ignore'])
    except InvalidConfiguration as err:
        log.error(err)
    else:
        ret_val = 0
    finally:
        return ret_val

if __name__ == "__main__":
    exit(main())
