import os
import viz

script_dir = os.path.dirname(os.path.abspath(__file__))

resources_path = os.path.join(script_dir, 'resources')
viz.res.addPath(resources_path)

viz.mouse.setVisible(True)

viz.go()

model = viz.addChild('/maps/art_gallery/scene.gltf')
