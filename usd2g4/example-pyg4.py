# ------------------------------------------------------------------------------
# Load pyg4ometry
import pyg4ometry as pyg4
import os

# ------------------------------------------------------------------------------
# Registry to store gdml data
registry = pyg4.geant4.Registry()

# ------------------------------------------------------------------------------
# world solid and logical
worldSolid   = pyg4.geant4.solid.Box("worldSolid",
                                           50,
                                           50,
                                           50,
                                           registry)

worldLogical   = pyg4.geant4.LogicalVolume(worldSolid,
                                                 "G4_Galactic",
                                                 "worldLogical",
                                                 registry)

registry.setWorld(worldLogical.name)

# ------------------------------------------------------------------------------
# box placed at origin

box   = pyg4.geant4.solid.Box("box",
                                    10,
                                    10,
                                    10,
                                    registry)

box_logical = pyg4.geant4.LogicalVolume(box,
                                              "G4_Fe",
                                              "box_logical",
                                              registry)

box_physical = pyg4.geant4.PhysicalVolume([0,0,0],
                                                [0,0,0],
                                                box_logical,
                                                "box_physical",
                                                worldLogical,
                                                registry)

# ------------------------------------------------------------------------------
# Writeout to GDML file

gdmlWriter = pyg4.gdml.Writer()
gdmlWriter.addDetector(registry)
gdmlWriter.write(os.path.join(os.path.dirname(__file__), "test.gdml"))


