#!/bin/bash

# Check if a virtual environment is activated
# It will be located in an environment variable
# VIRTUAL_ENV
function check_venv()
{
    venv_active=1
    venv="${VIRTUAL_ENV:=NONE}"
    if [ $venv = 'NONE' ]
    then
        venv_active=0
    fi
}

function install() {
    cd src
    pip install -e .
    cd ..
}

function install_testing() {
    cd src
    pip install -e '.[testing]'
    cd ..
}

# If no arguments provided
if [ $# -eq 0 ] 
then

    check_venv

    # If no virtual environment activated
    if [ $venv_active -eq 0 ]
    then
        echo "It looks like your virtual environment is not active"
        echo "If you wish to install this anyways, run this: './install no-venv'"
        echo "If you do not know what a virtual environment is, use this link"
        echo "https://virtualenvwrapper.readthedocs.io/en/latest/"
    else
        echo "Installing!"
        install
    fi
else

    # If the first arg provided is not 'no-venv'
    if [ $1 = 'no-venv' ]
    then
        echo "Installing!"
        install
    elif [ $1 = 'testing' ]
    then
        echo "Installing testing packages!"
        install_testing
    else
        echo "Expected provided argument to be 'no-venv', indicating that you want to"
        echo "install this even though you do not have a virtual environment active"
        echo "OR argument should be 'testing', indicating that you want to install"
        echo "the necessary packages to run the provided tests"
    fi
fi
