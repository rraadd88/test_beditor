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
