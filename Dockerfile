FROM openmc/openmc:develop-dagmc-libmesh

# Move the cross section files to an accessbile folder and change the path (circumvents the issue with UserID not being root)
RUN cp -r ~/nndc_hdf5/ /home
RUN export OPENMC_CROSS_SECTIONS=/home/nndc_hdf5/cross_sections.xml


RUN pip install vtk