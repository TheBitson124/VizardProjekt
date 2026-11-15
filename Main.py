import os
import viz
import vizcam
import vizact
import vizfx
import vizconnect

from tools import grabber
from clickable import RadioObject, PictureObject

script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources')
viz.res.addPath(resources_path)

vizconnect.go('Config/vizConfig.py')
# Wyłączenie chodzenia gałkami (TRUE ZEBY MOZNA BYLO):
vizconnect.getTransport('wandmagiccarpet').setEnabled(True)

model = vizfx.addChild('vr_gallery_house_baked/scene.osgb')

# Lista przechowująca wszystkie obiekty, w które można kliknąć
interactables = []

# Zmienna globalna przechowująca aktualnie podświetlony obiekt
current_highlighted_obj = None

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
            image_files.append(os.path.join(obrazy_dir, filename))
    image_files.sort()

# Tworzenie obrazów na podstawie znalezionych zdjęć
for i, img_path in enumerate(image_files):
    index = i + 1  
    model_path = f'vr_gallery_house_baked/Obraz{index}.osgb'
    audio_path = f'music/music{index}.mp3'
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

# Funkcja interakcji na klawiaturze (spacja)
def check_interaction(*args):
    picked = viz.pick()
    if picked:
        for obj in interactables:
            if obj.is_part(picked):
                obj.click()
                break  

vizact.onkeydown(' ', check_interaction)

# 2. LASER PRZYKLEJONY DO PRAWEJ DŁONI AWATARA
avatar = vizconnect.getAvatar('mark')
r_controller = vizconnect.getInput('right_touch_controller')

if avatar and r_controller:
    hand_node = avatar.getAttachmentPoint('r_hand').getNode3d()

    # Rysujemy laser wychodzący prosto z dłoni (na 10 metrów)
    viz.startLayer(viz.LINES)
    viz.vertexColor(viz.RED)
    viz.vertex(0, 0, 0)
    viz.vertex(0, 0, 10)
    laser = viz.endLayer()
    laser.setParent(hand_node)
    laser.disable(viz.INTERSECTION)
    
    # Funkcja sprawdzająca podświetlenie w każdej klatce
    def update_laser_highlight():
        global current_highlighted_obj
        
        start = hand_node.getPosition(viz.ABS_GLOBAL)
        end = hand_node.getMatrix(viz.ABS_GLOBAL).preMultVec([0, 0, 20])
        
        hit = viz.intersect(start, end)
        
        found_obj = None
        if hit.valid and hit.object:
            for obj in interactables:
                if obj.is_part(hit.object):
                    found_obj = obj
                    break
                    
        if found_obj != current_highlighted_obj:
            if current_highlighted_obj and hasattr(current_highlighted_obj, 'highlight'):
                current_highlighted_obj.highlight(False)
                
            current_highlighted_obj = found_obj
            if current_highlighted_obj and hasattr(current_highlighted_obj, 'highlight'):
                current_highlighted_obj.highlight(True)

    # Uruchamiamy pętlę podświetlenia co klatkę
    vizact.ontimer(0, update_laser_highlight)

    # Funkcja wywoływana przy kliknięciu spustu kontrolera
    def fire_laser():
        global current_highlighted_obj
        
        # 1. Jeśli obiekt jest aktualnie podświetlony przez laser, kliknij go!
        if current_highlighted_obj:
            current_highlighted_obj.click()
            print("Kliknięto podświetlony obiekt za pomocą lasera.")
            return True
            
        # 2. Awaryjne sprawdzenie kolizji, gdyby current_highlighted_obj był pusty
        start = hand_node.getPosition(viz.ABS_GLOBAL)
        end = hand_node.getMatrix(viz.ABS_GLOBAL).preMultVec([0, 0, 20])
        
        hits = viz.intersect(start, end, all=True)
        for hit in hits:
            if hit.valid and trigger_clicked_object(hit.object):
                return True
        return False

    # Poprawione podpięcie zdarzenia kontrolera (bezpieczne dla wizconnect)
    raw_ctrl = r_controller.getRaw()
    def on_button_down(e):
        # Sprawdzamy czy zdarzenie pochodzi z prawego kontrolera
        if hasattr(e, 'object') and e.object == raw_ctrl:
            fire_laser()
        elif not hasattr(e, 'object'): 
            # Czasami vizconnect wyzwala zdarzenie bez obiektu 'e.object' ale z prawego kontrolera
            fire_laser()

    viz.callback(viz.SENSOR_DOWN_EVENT, on_button_down)