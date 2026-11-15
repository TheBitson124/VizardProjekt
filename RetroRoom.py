
import os
import viz
import vizfx
import vizcam
from clickable import LightButtonObject

# 1. Ścieżki do plików projektu
script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources/vr_modern_gallery_room')
viz.res.addPath(resources_path)

viz.go()
#wazne vixFx
model = vizfx.addChild('scene.osgb')
viz.phys.enable()

model.collideMesh()
cam = vizcam.WalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=2.0)
viz.cam.setHandler(cam)
viz.MainView.collision(True)
vr_active = False

# TU DO POPRAWY LEPSZA SWIATŁA NA SCENIE 
# Wyłączenie domyślnego światła kamery, żeby oświetlenie pokoju było wyraźne
viz.MainView.getHeadLight().disable()

# Stworzenie światła punktowego (oświetla modele vizfx) w centrum pokoju
room_light = vizfx.addPointLight(pos=[0, 2.5, 0]) # Dopasuj wysokość (Y=2.5) i środek (X=0, Z=0)
room_light.intensity(1.5)

interactables = []
# Konfiguracja panelu 2x2 na ścianie
# Dopasuj base_x, base_y, base_z, aby umieścić panel na odpowiedniej ścianie
base_x = 0.0
base_y = 1.5   # Wysokość na poziomie wzroku
base_z = 2.0   # Odległość od środka
offset = 0.22  # Odstęp między kwadratami

btn_red = LightButtonObject(pos=[base_x - offset/2, base_y + offset/2, base_z], 
                            color=viz.RED, light_target=room_light)
interactables.append(btn_red)

btn_green = LightButtonObject(pos=[base_x + offset/2, base_y + offset/2, base_z], 
                              color=viz.GREEN, light_target=room_light)
interactables.append(btn_green)

btn_blue = LightButtonObject(pos=[base_x - offset/2, base_y - offset/2, base_z], 
                             color=viz.BLUE, light_target=room_light)
interactables.append(btn_blue)

btn_yellow = LightButtonObject(pos=[base_x + offset/2, base_y - offset/2, base_z], 
                               color=viz.YELLOW, light_target=room_light)
interactables.append(btn_yellow)


def check_interaction(*args):
    picked = viz.pick()
    if picked:
        for obj in interactables:
            if obj.is_part(picked):
                obj.click()
                break 

# 4. Wywołanie interakcji klawiszem spacji (wyceluj środkiem ekranu w kwadrat i wciśnij spację)
vizact.onkeydown(' ', check_interaction)
