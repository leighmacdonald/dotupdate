dotupdate
=================

Small tool & library to updated users dotfiles using symlinks to an alternate configuration root path.

Requirements
-------------------

- Python 2.7 or Python 3.x, 2.6 is not supported

Installation & Usage
-----------------------------

Below is a demonstration of how to intall the tool and install files from a dotfiles repo hosted on github.

    # Change to the directory you want to store the dotupdate utility
    $ cd ~/

    # Clone the symlinker tool
    $ git clone https://github.com/leighmacdonald/dotupdate

    # Change directory into the checked out symlinker source tree
    $ cd dotupdate

    # Do 1 of the following 2 steps depending on your setup

    # A: Clone your existing dotfiles repo
    $ git clone https://github.com/leighmacdonald/dotfiles

    # B: Create a new empty dotfiles tree
    $ mkdir dotfiles

    # Create a new config file from the example one
    $ cp config_dist.ini config.ini

    # Edit your default config settings
    $ vim config.ini

    # Run the tool in test mode to verify what will happen
    $ ./dotupdate.py -t

    # Update your symlinks if all looks good
    $ ./dotupdate.py


MIT License
-------------------------

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.