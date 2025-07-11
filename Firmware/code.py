import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.macros import Press, Release, Tap, Delay
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.macros import Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.layers import Layers
from kmk.extensions.rgb import RGB

keyboard = KMKKeyboard()

# MATRIX SETUP
keyboard.col_pins = (board.D0, board.D1, board.D2, board.D3)
keyboard.row_pins = (board.D8, board.D9, board.D10)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# MODULES
macros = Macros()
layers = Layers()
encoder_handler = EncoderHandler()

keyboard.modules.append(macros)
keyboard.modules.append(layers)
keyboard.modules.append(encoder_handler)
keyboard.modules.append(MediaKeys())
keyboard.modules.append(MouseKeys())

# EXTENSIONS
rgb = RGB(pixel_pin=board.D7, num_pixels=2, rgb_order=(1, 0, 2, 3))
keyboard.extensions.append(rgb)

# ENCODER PINS
encoder_handler.pins = [
    (board.D4, board.D5, board.D6),
]

# CYCLE LAYER HANDLER
def cycle_layer_handler(keyboard, *args, **kwargs):
    num_layers = len(keyboard.keymap)
    current_layer = keyboard.active_layers[0]
    next_layer = (current_layer + 1) % num_layers

    print(f'Cycling from layer {current_layer} to {next_layer}')
    keyboard.layers.clear_layers()
    keyboard.layers.activate_layer(next_layer)

# MACROS
Wstop = KC.MACRO(
    on_press=(Tap(KC.W),),
    on_hold=(Press(KC.W),),
    on_release=(Release(KC.W), Tap(KC.S)),
)

Sstop = KC.MACRO(
    on_press=(Tap(KC.S),),
    on_hold=(Press(KC.S),),
    on_release=(Release(KC.S), Tap(KC.W)),
)

Astop = KC.MACRO(
    on_press=(Tap(KC.A),),
    on_hold=(Press(KC.A),),
    on_release=(Release(KC.A), Tap(KC.D)),
)

Dstop = KC.MACRO(
    on_press=(Tap(KC.D),),
    on_hold=(Press(KC.D),),
    on_release=(Release(KC.D), Tap(KC.A)),
)

Arc = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.SPACE),
    Release(KC.LGUI),
    Tap(KC.A),
    Tap(KC.R),
    Tap(KC.C),
    Delay(1000),
    Tap(KC.ENTER),
)

Email = KC.MACRO(
    Press(KC.LSHIFT),
    Tap(KC.SPACE),
    Release(KC.LSHIFT),
    Delay(200),           # Fixed from 0.2 to 200 ms

    Tap(KC.W),
    Tap(KC.W),
    Tap(KC.W),
    Tap(KC.DOT),
    Tap(KC.G),
    Tap(KC.M),
    Tap(KC.A),
    Tap(KC.I),
    Tap(KC.L),
    Tap(KC.DOT),
    Tap(KC.C),
    Tap(KC.O),
    Tap(KC.M),

    Delay(200),
    Tap(KC.ENTER),
)

CycleLayer = KC.MACRO(on_press=(cycle_layer_handler,))

# KEYMAP
keyboard.keymap = [
    # Layer 0
    [
        CycleLayer, Wstop, KC.E, KC.R,
        Astop, Sstop, Dstop, KC.F,
        KC.LSHIFT, KC.NO, KC.NO, KC.BSPC,
    ],
    # Layer 1
    [
        CycleLayer, KC.NO, Email, KC.NO,
        Arc, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO, KC.NO,
    ],
    # Layer 2
    [
        CycleLayer, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO, KC.NO,
    ],
]

# ENCODER MAP
encoder_handler.map = [
    ((KC.VOLU, KC.VOLD, KC.MUTE),),
    ((KC.RGB_HUI, KC.RGB_HUD, KC.RGB_TOG),),
    ((KC.NO, KC.NO, KC.NO),),  # Add empty mapping for Layer 2 to match
]

# MAIN
if __name__ == '__main__':
    print('Keyboard firmware starting...')
    keyboard.go()
