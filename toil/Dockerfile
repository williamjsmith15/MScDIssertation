################################################################################
## TOIL CONTAINER
################################################################################

FROM python:3.7

# ------------------------------------------------------------------------------
# General setup

COPY toil/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN curl -sSL https://get.docker.com/ | sh

# ------------------------------------------------------------------------------
# CWL and Toil setup and hello world

WORKDIR /toil
COPY toil/example.cwl /toil/example.cwl
COPY toil/example-job.yaml /toil/example-job.yaml

RUN toil-cwl-runner example.cwl example-job.yaml
RUN cat ./output.txt

# ------------------------------------------------------------------------------
# Reset path for tty

WORKDIR /omniverse
WORKDIR /geant4