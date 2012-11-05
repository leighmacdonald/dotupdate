from glob import glob
from os.path import abspath, lexists, exists, join, expanduser, dirname
from os import symlink
from logging import getLogger

log = getLogger('pydot')
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

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
    full_source_path = abspath(source_path)
    if not exists(full_source_path):
        err = "Source dotfiles path does not exist {0}, cannot continue!".format(full_source_path)
        raise InvalidConfiguration(err)
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
        if link in ignore_list:
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
            pass
        except LinkExists:
            pass

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
