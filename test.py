import os
import viz
import vizcam


script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources/vr_gallery_house_baked')
viz.res.addPath(resources_path)

viz.go()

viz.phys.enable()


model = viz.addChild('scene.gltf')
model.collideMesh()

cam = vizcam.WalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=2.0)

viz.cam.setHandler(cam)

viz.MainView.collision(True)