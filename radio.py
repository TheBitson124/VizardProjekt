import os
import viz
import vizcam
import vizact
from clickable import RadioObject 

script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources')
viz.res.addPath(resources_path)

viz.go()

viz.phys.enable()
model = viz.addChild('vr_gallery_house_baked/scene.gltf')
model.collideMesh()
cam = vizcam.WalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=2.0)
viz.cam.setHandler(cam)
viz.MainView.collision(True)
vr_active = False

radio = RadioObject('items/radio/scene.gltf', pos=[0, 1.5, 3], audio_path='music/music1.mp3')

def check_interaction(*args):
    picked = viz.pick()
    print("Object picked", picked)
    
    if picked and radio.is_part(picked):
        radio.click()

vizact.onkeydown(' ', check_interaction)