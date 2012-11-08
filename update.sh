#!/bin/sh
# This is a simple script which will just update the git submodules
# used in the dotfiles tree

echo [+] Updating git submodules
pushd dotfiles
git submodule foreach git pull origin master
popd
echo [+] Update complete
