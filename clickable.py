import viz
import vizfx
import vizshape

class ClickableObject:
    def __init__(self):
        pass
        
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
    def __init__(self, model_path, pos, audio_data):
        self.node = vizfx.addChild(model_path, pos=pos)
        self.node.collideMesh()

        self.tracks =[]

        for path, volume in audio_data:
            audio = viz.addAudio(path)
            audio.volume(volume)
            self.tracks.append(audio)

        self.current_track = -1

    def click(self):
        for track in self.tracks:
            track.stop()

        self.current_track +=1

        if self.current_track >= len(self.tracks):
            self.current_track = -1
            print("Radio stoped")
        else:
            self.tracks[self.current_track].play()
            print("Radio played")
        
class PictureObject(ClickableObject):
    def __init__(self, model_path, pos, audio_path, image_path):
        self.node = viz.addChild(model_path, pos=pos)
        self.node.collideMesh()

        self.audio = viz.addAudio(audio_path)
        self.image = viz.addTexture(image_path)
        

        geom_node = self.node
   
        geom_node.texture(self.image)
        
        # --- Obrót tekstury o 180 stopni ---
        mat = viz.Matrix()
        mat.postTrans(-0.5, -0.5, 0) 
        mat.postEuler(0, 0, 180)     
        mat.postTrans(0.5, 0.5, 0)   
        geom_node.texmat(mat)        
    
    def click(self):
        self.audio.stop()
        self.audio.play()
        print("Obraz kliknięty - muzyka gra")
        
        
class LightButtonObject(ClickableObject):
    def __init__(self, pos, color, light_target, size=(0.2, 0.2)):
        self.node = vizshape.addQuad(size=size, pos=pos)
        self.node.collideMesh()
        
        self.node.color(color)
        
        self.node.disable(viz.LIGHTING)
        
        self.color = color
        self.light_target = light_target
        
    def click(self):
        self.light_target.color(self.color)
        print(f"Światło zmienione na: {self.color}")