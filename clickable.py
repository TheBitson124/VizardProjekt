import viz

class ClickableObject:
    def __init__(self, model_path, pos=[0, 0, 0]):
        self.node = viz.addChild(model_path, pos=pos)
        self.node.collideMesh()

    def is_part(self, picked_node):
        current = picked_node
        while current and current.valid():
            if current == self.node:
                return True
            parents = current.getParents()
            if not parents:
                break
            current = parents[0]
        return False

    def click(self):
        pass

class RadioObject(ClickableObject):
    def __init__(self, model_path, pos, audio_path):
        super().__init__(model_path, pos)
        self.music = viz.addAudio(audio_path)

    def click(self):
        self.music.stop()
        self.music.play()
        print("Radio played")
        
class PictureObject(ClickableObject):
    def __init__(self, model_path, pos, audio_path, image_path):
        super().__init__(model_path, pos)

        self.audio = viz.addAudio(audio_path)
        self.image = viz.addTexture(image_path)
        

        geom_node = self.node
   
                
        # Nałożenie tekstury (diffuse) na docelową geometrię
        geom_node.texture(self.image)
        
        # --- DODANY KOD: Obrót tekstury o 180 stopni ---
        mat = viz.Matrix()
        mat.postTrans(-0.5, -0.5, 0) # Przesunięcie środka obrotu na środek obrazu
        mat.postEuler(0, 0, 180)     # Obrót o 180 stopni wokół osi Z (w przestrzeni UV)
        mat.postTrans(0.5, 0.5, 0)   # Przesunięcie z powrotem na właściwe miejsce
        geom_node.texmat(mat)        # Przypisanie transformacji do materiału
    
    def click(self):
        self.audio.stop()
        self.audio.play()
        print("Obraz kliknięty - muzyka gra")