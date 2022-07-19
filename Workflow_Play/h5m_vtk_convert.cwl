#!/usr/bin/env cwl-runner
# A command line tool to convert from h5m to vtk fro visualisation of CAD in paraview

cwlVersion: v1.0
class: CommandLineTool
baseCommand: mbconvert
hints:
  DockerRequirement:
    dockerPull: openmc/openmc:develop-dagmc-libmesh
inputs:
  tracks_in:
    type: File
    inputBinding:
      position: 1
outputs:
  tracks_out:
    type: File
    outputBinding:
      glob: tracks.pvtp