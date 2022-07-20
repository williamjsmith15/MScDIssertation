################################################################################
## TOIL CONTAINER
################################################################################

FROM python:3.7

# ------------------------------------------------------------------------------
# General setup

COPY toil-omniverse-ext/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# ------------------------------------------------------------------------------
# CWL and Toil setup and hello world

COPY toil-omniverse-ext/omni.toil/ /toil-omniverse-ext/omni.toil

# ------------------------------------------------------------------------------
# Reset path for tty

WORKDIR /

ENTRYPOINT ["cp", "-r", "/toil-omniverse-ext/omni.toil", "/exts"]