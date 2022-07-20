################################################################################
## Import system essentials

import os, datetime, pathlib, sys, shutil, tarfile, tempfile, tarfile, io

import omni
import omni.ui as ui
import omni.kit.asset_converter

import carb

import asyncio

import docker

sep = os.sep

################################################################################
## Import extension dependancies


# def resolveDeps():
#     print("[omni.hello.world] Resolving dependancies") 
  
#     deps = ["docker", "wheel", "pypiwin32", "pywin32[win32]"]
#     for dep in deps:
#         success = omni.kit.pipapi.install(dep, 
#                                           use_online_index=True, 
#                                           extra_args=["--upgrade"])
#         print("[omni.hello.world] Installed: " + dep + " with result : "  + str(success))
        
#     print("[omni.hello.world] Finished resolving dependancies")

#resolveDeps()


################################################################################
## Set paths and create tmp folders

tmp       = tempfile.gettempdir()
extension = os.path.abspath(carb.tokens.acquire_tokens_interface().resolve("${omni.toil}"))
kit       = os.path.abspath(carb.tokens.acquire_tokens_interface().resolve("${kit}"))

paths = {
    "tmp"               : tmp,
    "extension"         : extension,
    "kit"               : kit,
    "share"             : f"{tmp}{sep}share",
    "usdTmp"            : f"{tmp}{sep}usd",
    "usdDestination"    : "/usdToG4",
    "cwlSource"         : f"{extension}{sep}toil-omniverse-tooldescriptors",
    "cwlDestination"    : "/omniverse",
    "geant4Macro"       : f"{extension}{sep}examples{sep}macros",
    "geant4Tmp"         : f"{tmp}{sep}geant4",
    "geant4Destination" : "/geant4",
    "geant4OutputTmp"   : f"{tmp}{sep}geant4_out",
}

pathlib.Path(paths["share"]).mkdir(parents=True, exist_ok=True)
pathlib.Path(paths["usdTmp"]).mkdir(parents=True, exist_ok=True)
pathlib.Path(paths["geant4Tmp"]).mkdir(parents=True, exist_ok=True)
pathlib.Path(paths["geant4OutputTmp"]).mkdir(parents=True, exist_ok=True)

################################################################################
## Helper functions


def make_tarfile(source_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        print(f"{source_dir} contains: {os.listdir(source_dir)}")
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return tar


def send_files(container, source, temp, destination):
    make_tarfile(source, temp)
    with open(temp, 'rb') as bundle:
        ok = container.put_archive(path=destination, data=bundle)
        if not ok:
            raise Exception(f'Put {source} to {destination} failed')
        else:
            print(f'Uploaded {source} ({os.path.getsize(temp)} B) to {destination} successfully')


def toil_on_click(outputText, macroText):

    print(f"PATHS: {paths['extension']}")
    print(f"PATHS: {paths['kit']}")

    client = docker.from_env()
    toilContainer = client.containers.get("uom-omniverse-docker-toil-1")

    var = toilContainer.exec_run(["find", "/geant4/", "-mindepth", "1", "-delete"])

    # --------------------------------------------------
    # Copy CWL files to toil container

    send_files(toilContainer,                       # container
               f'{paths["cwlSource"]}/',            # source directory 
               f'{paths["share"]}/cwl_bundle.tar',  # temp directory
               paths["cwlDestination"]              # container location
               )

    # --------------------------------------------------
    # Copy USD file to toil container

    stage = omni.usd.get_context().get_stage()
    stage.Export(f'{paths["usdTmp"]}/export.usd')

    send_files(toilContainer,                      # container
               f'{paths["usdTmp"]}/',              # source directory 
               f'{paths["share"]}/usdbundle.tar',  # temp directory
               paths["cwlDestination"]             # container location
               )

    # --------------------------------------------------
    # Copy Geant4 macro to toil container

    with open(f'{paths["geant4Tmp"]}/run.mac', "w") as macroFile:
        macroFile.write(macroText)

    send_files(toilContainer,                        # container
               f'{paths["geant4Tmp"]}/',             # source directory 
               f'{paths["share"]}/macroBundle.tar',  # temp directory
               paths["geant4Destination"]            # container location
               )

    # --------------------------------------------------
    # Run toil

    var = toilContainer.exec_run(["toil-cwl-runner",
                                  "--disableProgress",
                                  "/omniverse/omniverse-geant4.cwl",
                                  "/omniverse/usdToG4-job.yml"
                                  ])
    print(var)
    outputText.set_value(str(var.output.decode("utf-8")))

    # --------------------------------------------------
    # Get output file

    archive_path = f'{paths["geant4OutputTmp"]}/'
    bitstream, stat = toilContainer.get_archive("/geant4/",)
    filelike = io.BytesIO(b"".join(b for b in bitstream))
    tar = tarfile.open(fileobj=filelike)
    tar.extractall(path=archive_path)

    target_files = [f'{paths["geant4OutputTmp"]}/geant4/g4.obj']
    asyncio.ensure_future(
        convert_asset_to_usd(target_files)
    )
    
    omni.usd.get_context().open_stage(f'{paths["geant4OutputTmp"]}/geant4/g4.usd')

    print(str(var.output.decode("utf-8")))
    return


def get_converter_context():
    converter_context = omni.kit.asset_converter.AssetConverterContext()

    #                                                                   default
    converter_context.ignore_materials                         = True   # False
    converter_context.ignore_animations                        = False  # False
    converter_context.ignore_camera                            = False  # False
    converter_context.ignore_light                             = False  # False
    converter_context.single_mesh                              = True   # True
    converter_context.smooth_normals                           = True   # True
    converter_context.export_preview_surface                   = False  # False
    converter_context.support_point_instancer                  = False  # False
    converter_context.embed_mdl_in_usd                         = True   # True
    converter_context.use_meter_as_world_unit                  = False  # False
    converter_context.create_world_as_default_root_prim        = True   # True
    converter_context.embed_textures                           = False  # False
    converter_context.convert_fbx_to_y_up                      = False  # False
    converter_context.convert_fbx_to_z_up                      = False  # False
    converter_context.keep_all_materials                       = False  # False
    converter_context.merge_all_meshes                         = False  # False
    converter_context.use_double_precision_to_usd_transform_op = False  # False
    converter_context.ignore_pivots                            = False  # False
    return converter_context


async def convert_asset_to_usd(target_files):
    import omni.kit.asset_converter

    def progress_callback(progress, total_steps):
        pass

    print("Conversion process launching")
    for input_obj in target_files:
        basename = os.path.splitext(input_obj)[0]
        output_usd = f"{basename}.usd"

        converter_context = get_converter_context()
        instance = omni.kit.asset_converter.get_instance()
        task = instance.create_converter_task(input_obj,
                                              output_usd,
                                              progress_callback,
                                              get_converter_context())
        success = await task.wait_until_finished()
        if not success:
            print(f"Failed to convert {input_obj}")
            #carb.log_error(task.get_status(), task.get_detailed_error())
        else:
            print(f"Converting {input_obj} done. Wrote out {output_usd}")
    print("Conversion process finished")

            
def check_ver(outputText):
    omni.usd.get_context().open_stage(f'{paths["geant4OutputTmp"]}/geant4/g4.usd')

    
    #asyncio.run(main(target_files))

    # client = docker.from_env()

    # toilContainer = client.containers.get("uom-omniverse-docker-toil-1")

    # testScript = "for i in {1..10}; do echo hello $RANDOM; sleep 1; done"
    # with open(f'{paths["geant4Tmp"]}/runtest', "w") as macroFile:
    #     macroFile.write(testScript)

    # send_files(toilContainer,                        # container
    #            f'{paths["geant4Tmp"]}/',             # source directory 
    #            f'{paths["share"]}/testBundle.tar',   # temp directory
    #            paths["geant4Destination"]            # container location
    #            )

    # print("Running!")
    # import time as t
    # for n in range(0,20):
    #     print("Read " + str(n))
    #     outputText.model.set_value("Read " + str(n) )
    #     t.sleep(1)
    # return


def on_end(macroText):
    print("I am box " + str(macroText.get_value_as_string()))
    macroText = "RUN"


class MyExtension(omni.ext.IExt):
    macroText = ""
    
    def on_startup(self, ext_id):
        self._window = ui.Window("Toil")
        with self._window.frame:
            with ui.VStack():
                macroFile = f'{paths["geant4Macro"]}{sep}run.mac'
                macroFileString = pathlib.Path(macroFile).read_text()
                macroFileStringModel = ui.SimpleStringModel(macroFileString)

                editorModel = ui.StringField(macroFileStringModel, multiline=True).model
                editorModel.add_end_edit_fn(lambda m, macroText=macroFileStringModel: on_end(macroText))

                outputFieldStringModel = ui.SimpleStringModel("")
                outputField = ui.StringField(outputFieldStringModel, multiline=True).model
                
                ui.Button("Run Toil", clicked_fn=lambda outputText=outputField: toil_on_click(outputText,macroFileString))
                ui.Button("Check ver", clicked_fn=lambda outputText=outputField: check_ver(outputText))


    def on_shutdown(self):
        print("[omni.hello.world] MyExtension shutdown")


