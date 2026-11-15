import os
import viz
import vizfx
from clickable import RadioObject, PictureObject


script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources')
viz.res.addPath(resources_path)

model = vizfx.addChild('vr_gallery_house_baked/scene.osgb')

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
