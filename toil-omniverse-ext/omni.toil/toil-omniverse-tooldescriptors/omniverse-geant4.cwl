#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  usd: File
  gdml_out: string
  macro: File

outputs:
  obj_output:
    type: File
    outputSource: G4GDML/obj_out
  mtl_output:
    type: File
    outputSource: G4GDML/mtl_out
  geant4_output:
    type: File
    outputSource: G4GDML/std_out
  geant4_errput:
    type: File
    outputSource: G4GDML/std_err
  # conversion_output:
  #   type: File
  #   outputSource: usdToG4/obj
  gdml_used:
    type: File
    outputSource: usdToG4/gdml
    
steps:
  usdToG4:
    run: usdToG4.cwl
    in:
      usd: usd
    out: [gdml, obj]

  G4GDML:
    run: G4GDML.cwl
    in:
      gdml_in: usdToG4/gdml
      gdml_out: gdml_out
      macro: macro
    out: [obj_out,mtl_out,std_out,std_err]
