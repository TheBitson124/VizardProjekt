import os
import viz
import vizfx
import vizcam

# 1. Ścieżki do plików projektu
script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources/vr_art_gallery_01_gltf')
viz.res.addPath(resources_path)

viz.go()
#wazne vixFx
model = vizfx.addChild('scene.gltf')
viz.phys.enable()

model.collideMesh()
cam = vizcam.WalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=2.0)
viz.cam.setHandler(cam)
viz.MainView.collision(True)
vr_active = False
