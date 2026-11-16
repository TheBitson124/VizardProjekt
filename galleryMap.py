import os
import viz
import vizfx
from clickable import RadioObject, PictureObject


script_dir = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(script_dir, 'resources')
viz.res.addPath(resources_path)

model = vizfx.addChild('vr_gallery_house_baked/scene.osgb')
music_dir = os.path.join(resources_path, 'music')

interactables = []


audio_data = [
    ("music/radio/music_radio.mp3", 1.0),
    ("music/radio/music_radio2.mp3", 1.0)
    ]
radio = RadioObject(f'items/marshall_bluetooth_speaker/radio.osgb', pos=[0, 0, 0], audio_data=audio_data)
interactables.append(radio)


obrazy_dir = os.path.join(resources_path, 'vr_gallery_house_baked', 'Obrazy')

# Funkcja pomocnicza szukajaca pliku z danym prefiksem i rozszerzeniami
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
    
    # Jesli brakuje ZDJECIA -> pomijamy (nawet jesli istnieje sam plik audio)
    if not img_path:
        print(f"Pominieto Obraz {index} (prefiks {prefix}) - brak zdjecia.")
        continue

    model_rel_path = f'vr_gallery_house_baked/Obraz{index}.osgb'
    model_full_path = os.path.join(resources_path, 'vr_gallery_house_baked', f'Obraz{index}.osgb')
    
    if not os.path.exists(model_full_path):
        print(f"Pominieto Obraz {index} - brak pliku modelu {model_rel_path}.")
        continue
        
    position = [0, 0, 0] 
    
    try:
        picture = PictureObject(model_rel_path, pos=position, audio_path=audio_path, image_path=img_path)
        interactables.append(picture)
        audio_info = os.path.basename(audio_path) if audio_path else "BRAK (tylko obraz)"
        print(f"Zaladowano: Obraz{index}.osgb | Zdjecie: {os.path.basename(img_path)} | Audio: {audio_info}")
    except Exception as e:
        print(f"Blad podczas ladowania zestawu dla indeksu {index}: {e}")
