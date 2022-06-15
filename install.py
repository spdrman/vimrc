#!/usr/bin/env python3

import os
from sys import platform
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
#    command = cmd
#    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
#
#    while True:
#        output = p.stdout.readline()
#        if output == '' and p.poll() is not None:
#            break
#        if output:
#            yield output.strip()
    return subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, universal_newlines=True).stdout


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

def install(name, alt=None, install_cmd=None, path=None, osx=False, pkg=None):
    named = lambda n, a: a if (a is not None) else n
    cmd = named(name, alt)
    print_cyan("Installing dependency: " + named(name, alt))
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
            print_red(named(name, alt) + " is not installed on your system, installing...")
            ex(install_cmd)

    elif install_cmd is not None: # means need to use which() function instead of checking for install path
        print_red("Inside elif install_cmd")
        if wch(cmd):
            print_green("You already have " + name + ", skipping...")
        else:
            print_red(name + " is not installed on your system, installing...")
            ex(install_cmd)

    elif osx is not False:
        installed = bool(ex("if brew ls --versions '" + cmd + "' > /dev/null; then echo 'True'; else echo 'False'; fi").strip('\n'))

        if not installed:
            if pkg is not None:
                if 'brew' in pkg:
                    print_red(name + " is not installed on your system, installing...")
                    ex('brew install ' + named(cmd, pkg['brew']))
                else:
                    print_red(name + " is not installed on your system, installing...")
                    ex('brew install ' + cmd)
            else:
                print_red(name + " is not installed on your system, installing...")
                ex('brew install ' + cmd)
        else:
            print_green("You already have " + name + ", skipping...")
    elif osx is False:
        which = wch(cmd)
        check = ex("if hash " + cmd  + " 2>/dev/null; then echo 'True'; else echo 'False'; fi").strip('\n')
        installed = which or (check == 'True')
        #check = "if hash " + cmd  + " 2>/dev/null; then echo 'True'; else echo 'False'; fi"
        #check = cmd + " -v foo >/dev/null 2>&1 || { echo >&2 'False'; }"
        #res = ex(check).strip('\n')
        #installed = False
        #if res is not None:
        #    if res == 'False':
        #        installed = False
        #    else:
        #        installed = True
        if pkg is not None:
            if 'custom_check' in pkg:
                command = pkg['custom_check']
                result = ex(command).strip('\n')
                installed = result == 'True'
            elif 'apt' in pkg:
                installed = ex("if sudo apt list --installed " + pkg['apt']  + " | grep installed >> /dev/null; then echo 'True'; else echo 'False'; fi").strip('\n') == 'True'

        if not installed:
            if pkg is not None:
                if 'custom' in pkg:
                    print_red(name + " is not installed on your system, installing...")
                    ex(pkg['custom'])
                elif 'apt' in pkg:
                    print_red(name + " is not installed on your system, installing...")
                    ex('sudo apt-get install ' + named(cmd, pkg['apt']))
                else:
                    print_red(name + " is not installed on your system, installing...")
                    ex('sudo apt-get install ' + cmd)
            else:
                print_red(name + " is not installed on your system, installing...")
                ex('sudo apt-get install ' + cmd)
        else:
            print_green("You already have " + name + ", skipping...")
    else:
        raise Exception("ERROR 1000: named(name, alt) is required with (one or both of install_cmd and/or path), or with (one of brew or apt)")




#--------------------------------------------------------------------------------------------------------------------------
# Check if in OSX or Linux
ostype = "NONE"
IS_OSX = False

if platform == "linux" or platform == "linux2":
    ostype = "linux"
elif platform == "darwin":
    ostype = "osx"
    IS_OSX = True
elif platform == "win32":
    ostype = "windows"


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
BREW = ""
if IS_OSX:
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
# Update package manager
if IS_OSX:
    print_cyan("Updating BREW before we start trying to install apps from it...")
    ex("brew update")
else:
    print_cyan("Updating APT before we start trying to install apps from it...")
    ex("sudo apt update")


#--------------------------------------------------------------------------------------------------------------------------
# Install snapd on Linux
if not IS_OSX:
    install(
                name =          'snap',
                pkg =           {
                                    'apt':'snapd',
                                }
            )

#--------------------------------------------------------------------------------------------------------------------------
# Install vim-plug
install(
            name =          'vim-plug',
            install_cmd =   "curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim",
            path =          "~/.vim/autoload/plug.vim"
        )
#--------------------------------------------------------------------------------------------------------------------------
# Install curl
install(
            name =          'curl',
            osx =           IS_OSX
        )

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
            alt =           'silversearcher-ag',
            osx =           IS_OSX,
            pkg =           {
                                'apt': 'silversearcher-ag',
                            }
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
            name =          'neovim',
            alt =           'nvim',
            osx =           IS_OSX,
            pkg =           {
                                'apt': 'neovim',
                                'brew': 'neovim',
                            }
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
# Install rust-analyzer
install(
            name =          'rust-analyzer',
            osx =           IS_OSX,
            pkg =           {
                                'custom': 'sudo snap install rust-analyzer --beta',
                            }
        )

#--------------------------------------------------------------------------------------------------------------------------
# Install YouCompleteMe
print_cyan("Installing YouCompleteMe...")

if IS_OSX:
    install(
                name =          'xcode-select',
                install_cmd =   'xcode-select --install'
            )

install(
            name =          'cmake',
            osx =           IS_OSX
        )


install(
            name =          'vim-nox',
            alt =           'vim.nox',
            osx =           IS_OSX
        )

if not IS_OSX:
    install(
                name =          'pip',
                alt =           'pip3',
                pkg =           {
                                    'apt': 'python3-pip',
                                }
            )

install(
            name =          'pyenv',
            osx =           IS_OSX,
            pkg =           {
                                'custom':  "sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
                                            libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
                                            libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev && \
                                            curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash && \
                                            exec $SHELL"
                            }
        )

ex("pyenv install-latest")
#ex('''echo 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/''' + SHELL)


install(
            name =          'mono',
            osx =           IS_OSX,
            pkg =           {
                                'custom': 'sudo apt install dirmngr gnupg apt-transport-https ca-certificates software-properties-common && sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF && sudo apt-add-repository "deb https://download.mono-project.com/repo/ubuntu stable-focal main" && sudo apt-get update && sudo apt install mono-complete',
                            }
        )

install(
            name =          'golang',
            alt =           'go',
            osx =           IS_OSX,
            pkg =           {
                                'apt': 'golang',
                                'brew': 'golang',
                            }
        )

install(
            name =          'nodejs version manager',
            alt =           'nvm',
            osx =           IS_OSX,
            pkg =           {
                                'custom': 'curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash',
                                'custom_check': "if hash nvm_version >> /dev/null; then echo 'True'; else echo 'False'; fi",
                            }
        )


ex("git install-latest")
#ex('''echo 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/''' + SHELL)


install(
            name =          'git',
            osx =           IS_OSX,
        )


print_cyan("Configuring nvm to install latest NodeJS and NPM...")
if IS_OSX:
    ex("mkdir ~/.nvm")
    ex('echo \"export NVM_DIR="$HOME/.nvm" \[ -s "$(brew --prefix)/opt/nvm/nvm.sh" ] && \. "$(brew --prefix)/opt/nvm/nvm.sh" # This loads nvm \[ -s "$(brew --prefix)/opt/nvm/etc/bash_completion.d/nvm" ] && \. "$(brew --prefix)/opt/nvm/etc/bash_completion.d/nvm" # This loads nvm bash_completion\" >> ~/' + SHELL
    )
    ex('source ~/' + SHELL)
    ex('nvm install lts')
else:
    ex('source ~/' + SHELL)
    ex('nvm install lts')


install(
            name =          'java',
            osx =           IS_OSX
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
# Copy ctags info
# Function definition: Move your cursor to some function instance and type CTRL + ] (CTRL + T to go back to code)
# Function definition in split view: CTRL + W CTL + ]

print_cyan("Installing ctags...")

install(
            name =          'ctags',
            osx =           IS_OSX,
            pkg =           {
                                'apt': "exuberant-ctags"
                            }
        )

tmp = ""
if IS_OSX:
    tmp = BREW + "/bin/ctags/"
    ex('alias ctags="' + BREW + '/bin/ctags/"')
    ex('alias ctags >> ~/' + SHELL)
    ex('ln -s ~/vimrc/.ctags ~/.ctags')
else:
    tmp = "/usr/bin/ctags/"
    ex('alias ctags="/usr/bin/ctags/"')
    ex('alias ctags >> ~/' + SHELL)
    ex('ln -s ~/vimrc/.ctags ~/.ctags')


# All done
print_green("All done!")
