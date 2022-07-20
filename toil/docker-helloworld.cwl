cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
stdout: output.txt
hints:
  DockerRequirement:
    dockerImageId: uom-omniverse-docker_usd2g4
inputs:
  switches:
    type: string
    inputBinding:
      position: 1

outputs:
  output:
    type: stdout