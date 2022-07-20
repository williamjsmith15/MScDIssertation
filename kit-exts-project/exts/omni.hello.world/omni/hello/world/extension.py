import omni.ext
import omni.ui as ui
import os

def run_workflow():
    print("Running Example Workflow")

    os.system("cwltool --no-match-user /home/williamjsmith15/dissertation_work/MScDIssertation/Workflow_Play/test_workflow.cwl /home/williamjsmith15/dissertation_work/MScDIssertation/Workflow_Play/script_loc_simple_CAD.yml")

    print("DONE!")



class MyExtension(omni.ext.IExt):


    def on_startup(self, ext_id):
        print("[omni.hello.world] MyExtension startup")

        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                ui.Label("Workflow Run From Omni")

                ui.Button("Run Test Workflow", clicked_fn=lambda: run_workflow())

    def on_shutdown(self):
        print("[omni.hello.world] MyExtension shutdown")
