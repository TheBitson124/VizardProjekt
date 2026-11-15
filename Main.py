import os
import viz
import vizcam
import vizact
import vizfx
import vizconnect

from tools import highlighter
from clickable import RadioObject, PictureObject

script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources')
viz.res.addPath(resources_path)

vizconnect.go('Config/vizConfig.py')
# Wyłączenie chodzenia gałkami (TRUE ZEBY MOZNA BYLO):
vizconnect.getTransport('wandmagiccarpet').setEnabled(True)

model = vizfx.addChild('vr_gallery_house_baked/scene.osgb')


##CHODZENIE NA KLAWIATURZE##
#viz.phys.enable()
#model.collideMesh()
#cam = vizcam.WalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=2.0)
#viz.cam.setHandler(cam)
#viz.MainView.collision(True)

# Lista przechowująca wszystkie obiekty, w które można kliknąć
interactables = []

# Dodanie radia
audio_data = [
    ("music/radio/music_radio.mp3", 0.1),
    ("music/radio/music_radio2.mp3", 0.1)
    ]
radio = RadioObject(f'items/marshall_bluetooth_speaker/radio.osgb', pos=[0, 0, 0], audio_data=audio_data)
interactables.append(radio)

# Ścieżka do folderu ze zdjęciami
obrazy_dir = os.path.join(resources_path, 'vr_gallery_house_baked', 'Obrazy')

# Dynamiczne wyszukiwanie plików zdjęć
image_files = []
if os.path.exists(obrazy_dir):
    for filename in os.listdir(obrazy_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Dodajemy pełną ścieżkę do pliku
            image_files.append(os.path.join(obrazy_dir, filename))
    # Sortowanie gwarantuje, że pliki zawsze będą przypisywane w tej samej kolejności
    image_files.sort()

# Tworzenie obrazów na podstawie znalezionych zdjęć
for i, img_path in enumerate(image_files):
    index = i + 1  # Numeracja plików od 1
    model_path = f'vr_gallery_house_baked/Obraz{index}.osgb'
    audio_path = f'music/music{index}.mp3'
    
    # Przykładowe pozycjonowanie. Modele w osgb mogą mieć własne transformacje, 
    # więc pos=[0,0,0] może być odpowiednie, jeśli obrazy są już wypalone w odpowiednich miejscach.
    position = [0, 0, 0] 
    
    try:
        picture = PictureObject(model_path, pos=position, audio_path=audio_path, image_path=img_path)
        interactables.append(picture)
        print(f"Załadowano: Obraz{index}.osgb | Zdjęcie: {os.path.basename(img_path)} | Audio: music{index}.mp3")
    except Exception as e:
        print(f"Nie udało się załadować zestawu dla indeksu {index}: {e}")






def trigger_clicked_object(hit_node):
    if hit_node and hit_node.valid():
        for obj in interactables:
            if obj.is_part(hit_node):
                obj.click()
                return True
    return False





# Zaktualizowana funkcja interakcji sprawdzająca wszystkie obiekty z listy
def check_interaction(*args):
    picked = viz.pick()
    if picked:
        for obj in interactables:
            if obj.is_part(picked):
                obj.click()
                break 

vizact.onkeydown(' ', check_interaction)


avatar = vizconnect.getAvatar('mark')
r_controller = vizconnect.getInput('right_touch_controller')

if avatar and r_controller:
    hand_node = avatar.getAttachmentPoint('r_hand').getNode3d()
    
    tool = highlighter.Highlighter(highlightMode=highlighter.MODE_OUTLINE)

    all_mesh_nodes = [obj.node for obj in interactables if hasattr(obj, 'node')]
    tool.setItems(all_mesh_nodes)
    
    viz.link(hand_node, tool)

    current_target_node = None
    
    def onHighlight(e):
        global current_target_node
        current_target_node = e.new
        
    viz.callback(highlighter.HIGHLIGHT_EVENT, onHighlight)
    
    vizact.ontimer(0, tool.highlight)
    
    raw_ctrl = r_controller.getRaw()
    
    def on_button_down(e):
        if e.object == raw_ctrl:
            fire_laser()

    def on_vr_button_down(e):
        if e.object == raw_ctrl and current_target_node:
            for obj in interactables:
                if obj.is_part(current_target_node):
                    obj.click()
                    break

    viz.callback(viz.SENSOR_DOWN_EVENT, on_vr_button_down)


