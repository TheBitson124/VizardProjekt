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
    ("music/radio/music_radio.mp3", 1.0),
    ("music/radio/music_radio2.mp3", 1.0)
    ]
radio = RadioObject(f'items/marshall_bluetooth_speaker/radio.osgb', pos=[0, 0, 0], audio_data=audio_data)
interactables.append(radio)

# Ścieżka do folderu ze zdjęciami
# Ścieżki do folderów ze zdjęciami i muzyką
obrazy_dir = os.path.join(resources_path, 'vr_gallery_house_baked', 'Obrazy')
music_dir = os.path.join(resources_path, 'music')

# Funkcja pomocnicza szukająca pliku z danym prefiksem i rozszerzeniami
def find_file_with_prefix(directory, prefix, extensions):
    if not os.path.exists(directory):
        return None
    for filename in sorted(os.listdir(directory)):
        if filename.startswith(prefix) and filename.lower().endswith(extensions):
            return os.path.join(directory, filename)
    return None

MAX_OBRAZY = 20

for index in range(1, MAX_OBRAZY + 1):
    prefix = f"{index:02d}_"
    
    img_path = find_file_with_prefix(obrazy_dir, prefix, ('.png', '.jpg', '.jpeg'))
    audio_path = find_file_with_prefix(music_dir, prefix, ('.mp3', '.wav', '.ogg'))
    
    # Jeśli brakuje ZDJĘCIA -> pomijamy (nawet jeśli istnieje sam plik audio)
    if not img_path:
        print(f"Pominięto Obraz {index} (prefiks {prefix}) - brak zdjęcia.")
        continue

    model_rel_path = f'vr_gallery_house_baked/Obraz{index}.osgb'
    model_full_path = os.path.join(resources_path, 'vr_gallery_house_baked', f'Obraz{index}.osgb')
    
    if not os.path.exists(model_full_path):
        print(f"Pominięto Obraz {index} - brak pliku modelu {model_rel_path}.")
        continue

    position = [0, 0, 0]
    
    try:
        picture = PictureObject(model_rel_path, pos=position, audio_path=audio_path, image_path=img_path)
        interactables.append(picture)
        
        audio_info = os.path.basename(audio_path) if audio_path else "BRAK (tylko obraz)"
        print(f"Załadowano: Obraz{index}.osgb | Zdjęcie: {os.path.basename(img_path)} | Audio: {audio_info}")
    except Exception as e:
        print(f"Błąd podczas ładowania zestawu dla indeksu {index}: {e}")


from tools import highlighter
tool = vizconnect.getTool('highlighter').getRaw()
#tool.setItems([radio.node,Obraz1.node,Obraz2.node,Obraz3.node,Obraz4.node,Obraz5.node,Obraz6.node,Obraz7.node,Obraz8.node,Obraz9.node,Obraz10.node,Obraz11.node,Obraz12.node,Obraz13.node])
tool.setItems([obj.node for obj in interactables])
tool.setHighlightMode(highlighter.MODE_BOX)

def updateHighlighter(tool):
    # Wywołuje highlight() w każdej klatce bez konieczności trzymania przycisku
    tool.highlight()

tool.setUpdateFunction(updateHighlighter)

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




# 2. LASER PRZYKLEJONY DO PRAWEJ DŁONI AWATARA (porusza się razem z Tobą)
avatar = vizconnect.getAvatar('mark')
r_controller = vizconnect.getInput('right_touch_controller')

if avatar and r_controller:
    # Pobieramy fizyczny węzeł prawej dłoni awatara (ten, który idzie razem z postacią)
    hand_node = avatar.getAttachmentPoint('r_hand').getNode3d()

    # Rysujemy laser wychodzący prosto z dłoni (na 10 metrów)
    viz.startLayer(viz.LINES)
    viz.vertexColor(viz.RED)
    viz.vertex(0, 0, 0)
    viz.vertex(0, 0, 10)
    laser = viz.endLayer()
    laser.setParent(hand_node)
    laser.disable(viz.INTERSECTION)

    # Funkcja sprawdzająca, w co celuje dłoń w aktualnym miejscu pokoju
    def fire_laser():
        start = hand_node.getPosition(viz.ABS_GLOBAL)
        end = hand_node.getMatrix(viz.ABS_GLOBAL).preMultVec([0, 0, 20])
        
        hits = viz.intersect(start, end, all=True)
        for hit in hits:
            if hit.valid and trigger_clicked_object(hit.object):
                break

    # Podpięcie kliknięcia pod prawy kontroler (spust / przyciski)
    raw_ctrl = r_controller.getRaw()
    def on_button_down(e):
        if e.object == raw_ctrl:
            fire_laser()

    viz.callback(viz.SENSOR_DOWN_EVENT, on_button_down)


