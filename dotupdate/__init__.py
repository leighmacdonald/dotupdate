from glob import glob
from os.path import isfile, isdir, islink

def install(source_path="./", source_filter="*", dest_path="~/"):
    filter_txt = "{0}/{1}".format(source_path, source_filter)
    potential_links = glob(filter_txt)
    for link in potential_links:
        print(link)
