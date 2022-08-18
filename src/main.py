from sys import argv, exit
from getopt import getopt
import time
from rtmidi.midiutil import open_midiinput
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON
from pyautogui import hotkey, keyDown, keyUp, press
from yaml import safe_load, YAMLError



class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        if message[2] == 127:
            # print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
            pass
        cell = get_cell(message[1])
        print(cell["cell"])
        press_pad(message, cell["keys"], cell["color"])


def press_pad(message, action=[], defcolor=0):
    note_on = [NOTE_ON, message[1], message[2]]
    note_off = [NOTE_ON, message[1], defcolor]

    if message[2] == 127:
        midiout.send_message(note_on)  # led on

        if len(action) == 1:
            keyDown(action[0])  # press key
            time.sleep(0.01)
            keyUp(action[0])  # lift key
            print(action)
        elif len(action) > 1:
            print(*action)
            hotkey(*action)
        midiout.send_message(note_off)  # led back to default


def all_leds_off():
    for i in range(121):
        note_off = [NOTE_OFF, i, 0]
        midiout.send_message(note_off)


def initiate_leds(midiout, cell_arr):
    for cell in cell_arr:
        note_on = [NOTE_ON, cell["cell"], cell["color"]]
        midiout.send_message(note_on)


def listen(midiin, midiout):
    print("Entering main loop. Press Control-C to exit.")
    try:
        # Just wait for keyboard interrupt,
        # everything else is handled via the input callback.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("")
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin
        del midiout
        all_leds_off()


def read_config(config_path):
    with open(config_path, "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as exc:
            print(exc)


def get_cell(number):
    undefined_cell = {"cell": number, "keys": [], "color": 0}
    cell = next((item for item in cell_arr if item["cell"] == number), undefined_cell)
    return cell


def read_argv():
    argvs = argv[1:]
    opts, args = getopt(argvs,'p:c:', ['port=', 'config='])
    port = None
    config_path = 'config/config.yml'
    for o, value in opts:
        if o in ['-p', '--port']:
            port = int(value)
        elif o in ['-c', '--config']:
            config_path = value
    return {'p': port, 'c': config_path}

if __name__ == "__main__":

    # Read CLI arguments
    args = read_argv()
    port = args['p']
    config_path = args['c']

    # Prompts user for MIDI input port, unless a valid port number or name
    # is given as the first argument on the command line.
    # API backend defaults to ALSA on Linux.
    try:
        midiout, port_name = open_midioutput(port)
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        exit()
    print("Attaching MIDI input callback handler.")
    midiin.set_callback(MidiInputHandler(port_name))

    cell_arr = read_config(config_path)

    initiate_leds(midiout, cell_arr)

    listen(midiin, midiout)
