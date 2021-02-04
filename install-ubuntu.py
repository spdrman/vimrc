#!/usr/bin/env python3

import os
import subprocess
import errno
from shutil import which

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def wch(name):
    return which(name) is not None

def ex(cmd):
    os.system(cmd)

def print_cyan(text):
    os.system('echo %s %s %s' % (bcolors.HEADER, text, bcolors.ENDC))
    #os.system("echo \e[36m#{0}\e[0m".format(text))


def print_green(text):
    os.system('echo %s %s %s' % (bcolors.OKGREEN, text, bcolors.ENDC))
    #os.system("echo \e[32m#{0}\e[0m".format(text))


def print_red(text):
    os.system('echo %s %s %s' % (bcolors.FAIL, text, bcolors.ENDC))
    #os.system("echo \e[31m#{0}\e[0m".format(text))


def path(filepath):
    os.path.abspath(filepath)


def exists(p):
    t = path(p)
    if os.path.exists(p):
        return True
    else:
        return False

def contains_text(text, file):
    if exists(file):
        with open(path(file)) as myfile:
            if text in myfile.read():
                return True
            else:
                return False

print_cyan("Updating apt before we start trying to install apps from it...")
ex("sudo apt-get update")
print_cyan("Checking if vim-plug exists...")
if exists("~/.vim/autoload/plug.vim"):
    print_green("You already have vim-plug, awesome!")
else:
    print_red("Nope, installing vim-plug")
    ex("curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim")

print_cyan("Checking if ag exists...")
if exists("/usr/local/Cellar/the_silver_searcher/"):
    print_green("You already have ag, awesome!")
else:
    print_red("Nope, installing ag")
    ex("sudo apt-get install silversearcher-ag")

print_cyan("Checking if zsh is installed")
if not wch("zsh"):
    print_red("Nope, installing zsh")
    ex("sudo apt-get install zsh")
    ex("sh -c '$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)'")
else:
    print_green("You already have zsh, awesome!")

print_cyan("Checking if honukai theme is installed")
if exists("~/.oh-my-zsh/themes/honukai.zsh-theme"):
    print_green("You already have honukai theme, awesome!")
else:
    print_red("Nope, installing honukai theme")
    ex("wget -P ~/.oh-my-zsh/themes 'https://raw.githubusercontent.com/oskarkrawczyk/honukai-iterm/master/honukai.zsh-theme'")

print_cyan("Copying .vimrc to ~/.vimrc")
ex("cp .vimrc ~/.vimrc")
print_cyan("Copying .gitconfig to ~/.gitconfig")
ex("cp .gitconfig ~/.gitconfig")
print_cyan("Copying .zsh-aliases to ~/.zsh-aliases")
ex("cp .zsh-aliases ~/.zsh-aliases")

if contains_text("zsh-aliases", "~/.zshrc"):
    print_cyan("Adding .zsh-aliases to ~/.zshrc")
    ex("echo 'source ~/.zsh-aliases' >> ~/.zshrc")
