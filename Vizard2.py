import viz
import vizact
import vizshape

viz.setMultiSample(4)
viz.fov(60)
viz.go()
viz.mouse(viz.OFF)

# Settings
MOVE_SPEED = 3.0        # meters per second
SPRINT_MULT = 2.0       # hold Shift to sprint
MOUSE_SENS = 0.15       # degrees per pixel

# Start position (eye height ~1.8 m)
viz.MainView.setPosition([0, 1.8, 0])

yaw = 0.0
pitch = 0.0

def updateMovement():
    dt = viz.getFrameElapsed()
    speed = MOVE_SPEED * (SPRINT_MULT if viz.key.isDown(viz.KEY_SHIFT_L) else 1.0)

    x = z = 0.0
    if viz.key.isDown('w'): z += 1
    if viz.key.isDown('s'): z -= 1
    if viz.key.isDown('d'): x += 1
    if viz.key.isDown('a'): x -= 1

    # Normalize so diagonal movement isn't faster
    length = (x*x + z*z) ** 0.5
    if length > 0:
        x, z = x / length, z / length
        # BODY_ORI = move relative to yaw only, so you stay on the ground
        viz.MainView.move([x * speed * dt, 0, z * speed * dt], viz.BODY_ORI)

vizact.ontimer(0, updateMovement)   # run every frame

# Mouse look
viz.mouse.setVisible(viz.OFF)
viz.mouse.setTrap(viz.ON)

def onMouseMove(e):
    global yaw, pitch
    yaw += e.dx * MOUSE_SENS
    pitch -= e.dy * MOUSE_SENS
    pitch = max(-89, min(89, pitch))   # clamp so you can't flip over
    viz.MainView.setEuler([yaw, 0, 0], viz.BODY_ORI)
    viz.MainView.setEuler([0, pitch, 0], viz.HEAD_ORI)

viz.callback(viz.MOUSE_MOVE_EVENT, onMouseMove)

# Press Esc-alternative to release the mouse
def toggleMouse():
    trapped = not viz.mouse.getTrap()
    viz.mouse.setTrap(trapped)
    viz.mouse.setVisible(not trapped)

vizact.onkeydown('m', toggleMouse)

# Optional: Set the camera's initial starting position [X, Y, Z]
viz.MainView.setPosition([0, 1.8, -5])
# Add a model/environment to walk around in
viz.MainView.move([0,0,-1])
viz.MainView.getHeadLight().disable()
sky_light = viz.addLight(euler=(0,90,0))
sky_light.position(0,0,-1,0)
sky_light.color(viz.WHITE)
sky_light.ambient([0.9,0.9,1])
gallery = viz.addChild('vr_gallery_house_baked.osgb')
