#!/usr/bin/env cwl-runner
# A command line tool to convert from h5 to pvtp fro visualisation of tracks in paraview

cwlVersion: v1.0
class: CommandLineTool
baseCommand: openmc-track-to-vtk
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