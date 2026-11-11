import viz

class ClickableObject:
    def __init__(self, model_path, pos=[0, 0, 0]):
        # Wczytanie modelu 3D na podstawie ścieżki
        self.node = viz.addChild(model_path, pos=pos)
        self.node.collideMesh()

    def is_part(self, picked_node):
        """Check if element is in object hierachy (glTF management)."""
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
        print("Music played")
        
class PictureObject(ClickableObject):
    def __init__(self, model_path, pos, audio_path, image_path):
        super().__init__(model_path, pos)

        self.audio = viz.addAudio(audio_path)
        #do edycji?
        self.image = viz.addTexture(image_path)
    
    def click(self):
        self.music.stop()
        self.music.play()
        print("Audio played")