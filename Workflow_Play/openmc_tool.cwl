#!/usr/bin/env cwl-runner
# A command line tool to run the basic openMC docker container

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
hints:
  DockerRequirement:
    dockerPull: openmc/openmc:develop-dagmc-libmesh
inputs:
  script:
    type: File
    inputBinding:
      position: 1
outputs:
  example_out:
    type: stdout
  tallies_out:
    type: File
    outputBinding:
      glob: tallies.out
  plot_out:
    type: File
    outputBinding:
      glob: pinplot.png
stdout: output.txt