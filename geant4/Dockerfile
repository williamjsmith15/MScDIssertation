FROM archlinux:base-devel

RUN pacman-key --init
RUN pacman -Syy --noconfirm archlinux-keyring && pacman -Su --noconfirm  

RUN pacman -Syy --noconfirm cmake \
                            xerces-c \
                            mesa \
                            libxmu \
                            wget \
                            openmpi \
                            qt5-base \
                            ospray \
                            openvr \
                            python \
                            python-pip \
                            postgresql \
                            boost \
                            boost-libs \
                            pdal \
                            libogg \
                            libtheora \
                            liblas \
                            adios2 \
                            ffmpeg \
                            gl2ps \
                            libharu \
                            cgns \
                            qt5-quick3d \
                            glew \
                            eigen \
                            fmt \
                            utf8cpp \
                            unixodbc \
                            libxtst \
                            jre-openjdk \
                            jdk-openjdk \
                            vtk \
                            cli11

RUN pip install mpi4py

##################################################
# Compile Geant4

WORKDIR Geant4

RUN wget $(echo https://github.com$(curl -Ls https://github.com/Geant4/geant4/releases/v11.0.0 | grep -e '\.tar\.gz' | grep -o '".*"' | sed 's/"//g' | cut -d' ' -f1))

RUN tar xf v*.tar.gz
RUN rm v*.tar.gz

RUN mkdir geant4-install
WORKDIR geant4-build

RUN cmake -DCMAKE_INSTALL_PREFIX=../geant4-install \   
          -DGEANT4_BUILD_MULTITHREADED=ON \
          -DGEANT4_INSTALL_DATA=ON \
          -DGEANT4_USE_GDML=ON \
          -DGEANT4_USE_OPENGL_X11=ON \
          -DGEANT4_USE_QT=ON \
          -DGEANT4_USE_VTK=ON \
          # -DGEANT4_USE_PYTHON=ON \
          # -DGEANT4_BUILD_TLS_MODEL=global-dynamic \
          ../*

RUN make -j$(nproc)
RUN make install

##################################################
# Run X spoofing server

RUN pacman -Syy --noconfirm xorg-server-xvfb

RUN sed -i 's renderWindowInteractor->Start() //renderWindowInteractor->Start() ' /Geant4/geant4-11.0.0/source/visualization/Vtk/src/G4VtkViewer.cc

RUN make -j$(nproc)
RUN make install

##################################################
# Compile GDML demo

WORKDIR /
WORKDIR /Geant4Applications/Geant4GDML

RUN cmake -DGeant4_DIR=$(find /Geant4/geant4-install/lib/ -type d -name 'Geant4*') \
          /Geant4/geant4-install/share/Geant4-*/examples/extended/persistency/gdml/G01
RUN make -j$(nproc)

COPY geant4/macros/vis.mac /Geant4Applications/Geant4GDML/vis.mac

ENTRYPOINT ["sh", "-c", "source /Geant4/geant4-install/bin/geant4.sh && \"$@\"", "-s"]
