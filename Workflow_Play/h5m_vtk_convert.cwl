#!/usr/bin/env cwl-runner
# A command line tool to convert from h5m to vtk fro visualisation of CAD in paraview

cwlVersion: v1.0
class: CommandLineTool
baseCommand: mbconvert
hints:
  DockerRequirement:
    dockerPull: openmc/openmc:develop-dagmc-libmesh
inputs:
  CAD_in:
    type: File
    inputBinding:
      position: 1
outputs:
  CAD_out:
    type: File
    outputBinding:
      glob: dagmc.vtk