FROM python:3.7

# ------------------------------------------------------------------------------
# General setup

COPY usd2g4/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libmpfr-dev libcgal-dev libgl1

# ------------------------------------------------------------------------------
# pyg4ometry setup and simple app

RUN git clone https://bitbucket.org/jairhul/pyg4ometry.git
WORKDIR /pyg4ometry
RUN git checkout develop

RUN python setup.py build_ext 
RUN pip install --editable .

COPY usd2g4/example-pyg4.py /pyg4ometry/example-pyg4.py
RUN python example-pyg4.py

RUN cat ./test.gdml

# ------------------------------------------------------------------------------
# Pixar libraries

RUN apt-get update && apt-get install -y cmake libgl1-mesa-dev libegl1-mesa-dev
RUN pip install pyside2 PyOpenGL

WORKDIR /usr/local
RUN git clone https://github.com/PixarAnimationStudios/USD
RUN python USD/build_scripts/build_usd.py /usr/local/USD

# ------------------------------------------------------------------------------
# copy main script

WORKDIR /
WORKDIR /usdToG4
COPY usd2g4/usdToG4/ ./

# ------------------------------------------------------------------------------
# Reset path for tty

WORKDIR /