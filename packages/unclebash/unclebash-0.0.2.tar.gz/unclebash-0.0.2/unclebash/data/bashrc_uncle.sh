#!/usr/bin/env bash

###########################
# user-defined paths
###########################

# mycommand --> deprecated
# export PATH="~/mycommand:$PATH"

# Anaconda2
# export PATH="~/anaconda2/bin:$PATH"

# added by Anaconda3 4.2.0 installer
export PATH="~/anaconda3/bin:$PATH"

# added by PyCharm
export PATH="~/mysoftware/pycharm/pycharm-community-2017.2/bin/:$PATH"

# STELLA
export PATH=~/bin:$PATH


###########################
# user-defined commands
###########################

# softwares
alias topcat="java -jar ~/mysoftware/topcat-full.jar &"
alias pycharm="bash ~/mysoftware/pycharm/pycharm-community-2017.2/bin/pycharm.sh &"
alias jupyter-font="jupyter-qtconsole --ConsoleWidget.font_size=13 &"

# ssh
alias ssh-zen="ssh -X zb@10.0.10.94"
alias ssh-t7610="ssh -X cham@10.25.1.131"
alias ssh-chenxy="ssh -X cham@10.25.1.131"
# ssh to ali VM
alias ssh-ali-root="ssh -X -Y root@101.201.56.181 -p 9990"
alias ssh-ali="ssh -X -Y cham@101.201.56.181 -p 9990"

# python profile
alias kernprof="~/.local/lib/python2.7/site-packages/kernprof.py"

# zen nodes
alias ssh1="ssh -X -Y zen-0-1"
alias ssh2="ssh -X -Y zen-0-2"
alias ssh3="ssh -X -Y zen-0-3"
alias ssh4="ssh -X -Y zen-0-4"
alias ssh5="ssh -X -Y zen-0-5"
alias ssh6="ssh -X -Y zen-0-6"
alias ssh7="ssh -X -Y zen-0-7"
alias ssh8="ssh -X -Y zen-0-8"
alias ssh9="ssh -X -Y zen-0-9"
alias ssh10="ssh -X -Y zen-0-10"
alias ssh11="ssh -X -Y zen-0-11"
alias ssh12="ssh -X -Y zen-0-12"
alias ssh13="ssh -X -Y zen-0-13"
alias ssh14="ssh -X -Y zen-0-14"
alias ssh15="ssh -X -Y zen-0-15"
alias ssh16="ssh -X -Y zen-0-16"


###########################
# UREKA
###########################
ur_setup() {
    eval `~/.ureka/ur_setup -sh $*`
}
ur_forget() {
    eval `~/.ureka/ur_forget -sh $*`
}
#ur_setup


# ################
# T7610
####################

# Montage
export PATH="$PATH:~/mysoftware/montage/Montage/bin"

# open MPI
export LD_LIBRARY_PATH=/usr/lib/openmpi/lib/
export PATH=$PATH:$HOME/.openmpi/bin

# LIBSVM
export PATH="~/mysoftware/svm/libsvm:$PATH"
export PYTHONPATH="~/mysoftware/svm/libsvm/python:$PYTHONPATH"

# Julia
export JULIA_HOME="~/juliapro/JuliaPro-0.5.1.1/Julia/bin"

# github oauth
export GITHUB_CLIENT_ID=c8c94e4c16c8a2afddc2
export GITHUB_CLIENT_SECRET=3d5bf163bb3a35567edab29c2a3cd8de2d105cfc
export OAUTH_CALLBACK_URL=https://hypergravity.jupyter.org/hub/oauth_callback
