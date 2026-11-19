import os
import viz
import vizcam
import vizact
import vizconnect


import galleryMap
from interaction_strategies import VRInteractionStrategy,DesktopInteractionStrategy



script_dir = os.path.dirname(os.path.abspath(__file__))

map = galleryMap

try:
    strategy = VRInteractionStrategy(map)
except:
    print("No VR connected, switching to PC")
    strategy = DesktopInteractionStrategy(galleryMap)
