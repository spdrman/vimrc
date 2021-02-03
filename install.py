#!/usr/bin/env python3

import os
import subprocess

def which(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

def ex(cmd):
    os.system(cmd)

def print_cyan(text):
    os.system("\e[36m#{text}\e[0m")


def print_green(text):
    os.system("\e[32m#{text}\e[0m")


def print_red(text):
    os.system("\e[31m#{text}\e[0m")

def path(filepath):
    os.path.abspath(filepath)
    
def exists(p):
    t = path(p)
    if path.exists(d):
        return true
    else:
        return false

def contains_text(text, file):
    if exists(file):
        with open(path(file)) as myfile:
            if text in myfile.read():
                return true
            else:
                return false
            
            
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
    ex("brew install the_silver_searcher"

print_cyan("Checking if zsh is installed")
if not which(zsh):
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

if contains_text("zsh-aliases", "~/.zshrc")
    print_cyan("Adding .zsh-aliases to ~/.zshrc")
    ex("echo 'source ~/.zsh-aliases' >> ~/.zshrc")
