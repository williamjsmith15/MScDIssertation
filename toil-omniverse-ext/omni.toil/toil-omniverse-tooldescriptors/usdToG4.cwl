#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [python, /usdToG4/readUSD_makePYG4.py]
hints:
  DockerRequirement:
    dockerImageId: uom-omniverse-docker_usd2g4
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONPATH: /usr/local/USD/lib/python
inputs:
  usd:
    type: File
    inputBinding:
      position: 1
outputs:
  gdml:
    type: File
    outputBinding:
      glob: test.gdml
  obj:
    type: File
    outputBinding:
      glob: test.obj
