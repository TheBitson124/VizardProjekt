import viz
import vizcam
import vizact
import vizconnect

from tools import highlighter

class BaseInteractionStrategy:
    def __init__(self, map):
        pass

class VRInteractionStrategy(BaseInteractionStrategy):
    def __init__(self, map):
        if viz.hmd.getSensor() is None:
            raise Exception("Brak podlaczonego zestawu VR (HMD)")

        vizconnect.go('Config/vizConfig.py')
        # Wylaczenie chodzenia galkami (TRUE ZEBY MOZNA BYLO):
        vizconnect.getTransport('wandmagiccarpet').setEnabled(True)

        avatar = vizconnect.getAvatar('mark')
        r_controller = vizconnect.getInput('right_touch_controller')

        if avatar and r_controller:
            hand_node = avatar.getAttachmentPoint('r_hand').getNode3d()

            viz.startLayer(viz.LINES)
            viz.vertexColor(viz.RED)
            viz.vertex(0, 0, 0)
            viz.vertex(0, 0, 10)
            laser = viz.endLayer()
            laser.setParent(hand_node)
            laser.disable(viz.INTERSECTION)

            def trigger_clicked_object(hit_node):
                if hit_node and hit_node.valid():
                    for obj in map.interactables:
                        if obj.is_part(hit_node):
                            obj.click()
                            return True
                return False

            def fire_laser():
                start = hand_node.getPosition(viz.ABS_GLOBAL)
                end = hand_node.getMatrix(viz.ABS_GLOBAL).preMultVec([0, 0, 20])
                
                hits = viz.intersect(start, end, all=True)
                for hit in hits:
                    if hit.valid and trigger_clicked_object(hit.object):
                        break

            raw_ctrl = r_controller.getRaw()
            def on_button_down(e):
                if e.object == raw_ctrl:
                    fire_laser()

            viz.callback(viz.SENSOR_DOWN_EVENT, on_button_down)

            tool = vizconnect.getTool('highlighter').getRaw()
            tool.setItems([obj.node for obj in map.interactables])
            tool.setHighlightMode(highlighter.MODE_BOX)
        
            def updateHighlighter(tool):
                # Wywoluje highlight() w kazdej klatce bez koniecznosci trzymania przycisku
                tool.highlight()
        
            tool.setUpdateFunction(updateHighlighter)

class DesktopInteractionStrategy(BaseInteractionStrategy):
    def __init__(self, map):
        viz.phys.enable()
        map.model.collideMesh()
        cam = vizcam.WalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=2.0)
        viz.cam.setHandler(cam)
        viz.MainView.collision(True)

        def trigger_clicked_object(hit_node):
            if hit_node and hit_node.valid():
                for obj in map.interactables:
                    if obj.is_part(hit_node):
                        obj.click()
                        return True
                return False

        def check_interaction():
            picked = viz.pick()
            if picked:
                trigger_clicked_object(picked) 

        vizact.onkeydown(' ', check_interaction)
        
        def on_mouse_down(button):
            if button == 0:  
                check_interaction()
                
        viz.callback(viz.MOUSEDOWN_EVENT, on_mouse_down)