1. Anaconda package manager

        MINICONDA_URL="https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        export MINICONDA=$HOME/miniconda
        export PATH="$MINICONDA/bin:$PATH"
        hash -r
        echo $MINICONDA_URL
        wget $MINICONDA_URL -O miniconda.sh;
        bash miniconda.sh -b -f -p $MINICONDA;
        conda config --set always_yes yes
        conda update conda
        conda info -a

2. [Optional] Linux specific libraries that are very often pre-installed in a linux distro.
    
        sudo apt install gcc make make-guile git zlib1g-dev libncurses5-dev libbz2-dev
        sudo apt update
