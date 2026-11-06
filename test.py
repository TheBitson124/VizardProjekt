import os
import viz

script_dir = os.path.dirname(os.path.abspath(__file__))

resources_path = os.path.join(script_dir, 'resources')
viz.res.addPath(resources_path)

viz.go()

model = viz.addChild('vr_art_gallery_01.glb')