#!/usr/bin/env python3

import os
import subprocess
import errno
from shutil import which



#--------------------------------------------------------------------------------------------------------------------------
class bcolors:
    HEADER = '\033[33m' #yellow
    OKBLUE = '\033[44m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[31m' #white
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''




#--------------------------------------------------------------------------------------------------------------------------
def wch(name):
    return which(name) is not None


def ex(cmd):
#    os.system(cmd)
#    os.popen(cmd)
    return subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE).stdout


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


def install(name, install_cmd=None, path=None, brew=False):
    print_cyan("Installing dependency: " + name)
    print_cyan("Checking if " + name + " exists...")

    if path is not None:
        if '~/' in path:
            path = path.replace('~', HOME)
        if 'brew --prefix' in path:
            path = path.replace('brew --prefix ', BREW)

    if install_cmd is not None:
        if '~/' in install_cmd:
            install_cmd = install_cmd.replace('~', HOME)

    if path is not None and install_cmd is not None:
        if exists(path):
            print_green("You already have " + name + ", skipping...")
        else:
            print_red(name + " is not installed on your system, installing...")
            ex(install_cmd)

    elif install_cmd is not None: # means need to use which() function instead of checking for install path
        if wch(name):
            print_green("You already have " + name + ", skipping...")
        else:
            print_red(name + " is not installed on your system, installing...")
            ex(install_cmd)

    elif brew is True:
        installed = bool(ex("if brew ls --versions '" + name  + "' > /dev/null; then echo 'True'; else echo 'False'; fi").strip('\n'))

        if not installed:
            print_red(name + " is not installed on your system, installing...")
            ex('brew install ' + name)
        else:
            print_green("You already have " + name + ", skipping...")
    else:
        raise Exception("ERROR 1000: install_cmd and path, or name and brew=True not set for " + name)




#--------------------------------------------------------------------------------------------------------------------------
# Checking current environment $SHELL
sh = os.path.basename(os.environ['SHELL'])
if sh is not None:
    SHELL = '.' + str(sh) + 'rc'
else:
    raise Exception("ERROR 1001: Couldn't determine which SHELL we are in via echo $SHELL")

# Checking current environment $HOME
# HOME = os.path.basename(os.environ['HOME'])
HOME = os.environ['HOME']
if HOME is not None:
    HOME = HOME.strip('\n')
else:
    raise Exception("ERROR 1002: Couldn't determine which HOME folder to use via echo $HOME")

# Set env path of brew installs
BREW = ex("brew --prefix")
if BREW is not None:
    BREW = BREW.strip('\n')
else:
    raise Exception("ERROR 1003: Couldn't determine which BREW folder to use via brew --prefix")


#--------------------------------------------------------------------------------------------------------------------------
#
#           BEGIN CONFIGURATION & INSTALLATION
#
#--------------------------------------------------------------------------------------------------------------------------
# Update bREW
print_cyan("Updating BREW before we start trying to install apps from it...")
ex("brew update")


#--------------------------------------------------------------------------------------------------------------------------
# Install vim-plug
install(
            name =          'vim-plug',
            install_cmd =   "curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim",
            path =          "~/.vim/autoload/plug.vim"
        )

#--------------------------------------------------------------------------------------------------------------------------
# Install Ag / silver searcher
install(
            name =          'the_silver_searcher',
            brew =          True
        )

#--------------------------------------------------------------------------------------------------------------------------
# Install  Honukai Theme
install(
            name =          'Honukai Theme',
            path =          "~/.oh-my-zsh/themes/honukai.zsh-theme",
            install_cmd =   "wget -P ~/.oh-my-zsh/themes 'https://raw.githubusercontent.com/oskarkrawczyk/honukai-iterm/master/honukai.zsh-theme'"
        )

#--------------------------------------------------------------------------------------------------------------------------
# Install NeoVim
install(
            name =          'Neovim',
            brew =          True
        )

#--------------------------------------------------------------------------------------------------------------------------
# Install link to vimrc
print_cyan("Backing up your .vimrc file and making symlink to the one in this package")
ex("cp ~/.vimrc ~/.vimrc.bkp")
ex("rm ~/.vimrc")
ex("ln -s $HOME/vimrc/.vimrc ~/.vimrc")

#--------------------------------------------------------------------------------------------------------------------------
# Install all plugins in the .vim.plugins file
print_cyan("Install all vim plugins")
ex("vim -E -s -u '$HOME/.vimrc' +PlugInstall +qall")

print_cyan("Configuring neovim...")
ex("pip3 install pynvim")


#--------------------------------------------------------------------------------------------------------------------------
# Install YouCompleteMe
print_cyan("Installing YouCompleteMe...")
install(
            name =          'xcode-select',
            install_cmd =   'xcode-select --install'
        )


install(
            name =          'cmake',
            brew =          True
        )


install(
            name =          'vim-nox',
            brew =          True
        )

# install Python as part of YouCompleteMe
install(
            name =          'pyenv',
            brew =          True
        )

ex("pyenv install-latest")
ex('''echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/''' + SHELL)


install(
            name =          'mono',
            brew =          True
        )

install(
            name =          'golang',
            brew =          True
        )

install(
            name =          'nodejs',
            brew =          True
        )

install(
            name =          'java',
            brew =          True
        )
#ex("sudo ln -sfn /usr/local/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk")

#install(
#            name =          'YouCompleteMe',
#            path =          "~/.vim/plugged/YouCompleteMe/install.pipi", #wrong name -- so this always gets run
#            install_cmd =   "python3 ~/.vim/plugged/YouCompleteMe/install.py --rust-completer --js-completer --go-completera"
#        )

print_cyan("Configuring YouCompleteMe...")
ex("python3 ~/.vim/plugged/YouCompleteMe/install.py --all")

print_green("YouCompleteMe has now been installed and configured.")


#--------------------------------------------------------------------------------------------------------------------------
# Install rust-analyzer
install(
            name =          'rust-analyzer',
            brew =          True
        )

#--------------------------------------------------------------------------------------------------------------------------
# Copy ctags info
# Function definition: Move your cursor to some function instance and type CTRL + ] (CTRL + T to go back to code)
# Function definition in split view: CTRL + W CTL + ]

print_cyan("Installing ctags...")

install(
            name =          'ctags',
            brew =          True
        )

tmp = BREW + "/bin/ctags/"
ex('alias ctags="' + BREW + '/bin/ctags/"')
ex('alias ctags >> ~/' + SHELL)
ex('ln -s ~/vimrc/.ctags ~/.ctags')


# All done
print_green("All done!")
