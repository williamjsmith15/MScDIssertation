# MScDIssertation
Colleciton of Files and Scripts that contain the work performed for a MSc Strucutral Engineering dissertation


To run:
  cwltool, needs argument --no-pass-user when using the openMC docker container as this means the CWL tool can access the root user and not userID 1000
  docker container normally: 
    docker run -it -v /home/williamjsmith15/dissertation_work/MScDIssertation/:/home/Test_Scripts/ openmc/openmc:develop-dagmc-libmesh
