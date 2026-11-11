import viz
import vizact
import vizinfo
import os
import vizcam

script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources')
viz.res.addPath(resources_path)

# 1. Inicjalizacja okna Vizard
viz.go()

# Bezpieczna inicjalizacja trybu VR
try:
    import openvr
    viz.window.setStereoMode(viz.STEREO_HEADSET)
    print("Tryb VR (Headset) włączony pomyślnie.")
except ImportError:
    print("Brak modułu openvr – tryb monitora (klawiatura + mysz).")

# 2. Sterowanie FPP (WASD + rozglądanie myszką)
cam = vizcam.WalkNavigate(moveScale=2.0, turnScale=1.0)
viz.MainView.setPosition([0, 1.7, 0])

# 3. Wczytanie mapy (galeria sztuki)
gallery_model = viz.addChild('maps/art_gallery/scene.gltf')

# 4. Dodanie obiektu interaktywnego (radio)
target_object = viz.addChild('items/radio/scene.gltf', pos=[0, 1.5, 3])

# 5. Wczytanie pliku dźwiękowego
music = viz.addAudio('music/music1.mp3')

# Funkcja sprawdzająca, czy kliknięty element to radio lub jego część
def is_part_of_radio(node, parent_node):
    current = node
    while current and current.valid():
        if current == parent_node:
            return True
        # W Vizard 8 używamy getParents() zamiast getParent()
        parents = current.getParents()
        if not parents:
            break
        current = parents[0]  # Pobieramy pierwszego rodzica z listy
    return False

# --- OBSŁUGA INTERAKCJI KLAWISZEM SPACJI ---
def check_interaction(*args):
    # Rzucamy promień z kamery tam, gdzie patrzy celownik na środku ekranu
    picked = viz.pick()
    print("Spojrzałeś na obiekt:", picked)
    
    # Sprawdzamy czy trafiono w radio lub dowolną część jego modelu (.gltf)
    if picked and is_part_of_radio(picked, target_object):
        music.stop()
        music.play()
        print("Sukces! Muzyka została uruchomiona!")
    else:
        print("To nie jest radio.")

# Przypisujemy zdarzenie wciśnięcia spacji (' ')
vizact.onkeydown(' ', check_interaction)