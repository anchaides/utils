#!/usr/bin/env python3
import subprocess
import threading
import evdev
import time
import sys
import os

from enum import Enum
from evdev import ecodes, InputDevice

class TFSM_STATE(Enum):
    IDLE = 0
    TOGGLE = 1

linux_to_hid = {
    ecodes.KEY_A: 0x04, ecodes.KEY_B: 0x05, ecodes.KEY_C: 0x06, ecodes.KEY_D: 0x07,
    ecodes.KEY_E: 0x08, ecodes.KEY_F: 0x09, ecodes.KEY_G: 0x0A, ecodes.KEY_H: 0x0B,
    ecodes.KEY_I: 0x0C, ecodes.KEY_J: 0x0D, ecodes.KEY_K: 0x0E, ecodes.KEY_L: 0x0F,
    ecodes.KEY_M: 0x10, ecodes.KEY_N: 0x11, ecodes.KEY_O: 0x12, ecodes.KEY_P: 0x13,
    ecodes.KEY_Q: 0x14, ecodes.KEY_R: 0x15, ecodes.KEY_S: 0x16, ecodes.KEY_T: 0x17,
    ecodes.KEY_U: 0x18, ecodes.KEY_V: 0x19, ecodes.KEY_W: 0x1A, ecodes.KEY_X: 0x1B,
    ecodes.KEY_Y: 0x1C, ecodes.KEY_Z: 0x1D, ecodes.KEY_1: 0x1E, ecodes.KEY_2: 0x1F,
    ecodes.KEY_3: 0x20, ecodes.KEY_4: 0x21, ecodes.KEY_5: 0x22, ecodes.KEY_6: 0x23,
    ecodes.KEY_7: 0x24, ecodes.KEY_8: 0x25, ecodes.KEY_9: 0x26, ecodes.KEY_0: 0x27,
    ecodes.KEY_ENTER: 0x28, ecodes.KEY_ESC: 0x29, ecodes.KEY_BACKSPACE: 0x2A,
    ecodes.KEY_TAB: 0x2B, ecodes.KEY_SPACE: 0x2C, ecodes.KEY_MINUS: 0x2D,
    ecodes.KEY_EQUAL: 0x2E, ecodes.KEY_LEFTBRACE: 0x2F, ecodes.KEY_RIGHTBRACE: 0x30,
    ecodes.KEY_BACKSLASH: 0x31, ecodes.KEY_SEMICOLON: 0x33, ecodes.KEY_APOSTROPHE: 0x34,
    ecodes.KEY_GRAVE: 0x35, ecodes.KEY_COMMA: 0x36, ecodes.KEY_DOT: 0x37,
    ecodes.KEY_SLASH: 0x38, ecodes.KEY_CAPSLOCK: 0x39, ecodes.KEY_F1: 0x3A,
    ecodes.KEY_F2: 0x3B, ecodes.KEY_F3: 0x3C, ecodes.KEY_F4: 0x3D, ecodes.KEY_F5: 0x3E,
    ecodes.KEY_F6: 0x3F, ecodes.KEY_F7: 0x40, ecodes.KEY_F8: 0x41, ecodes.KEY_F9: 0x42,
    ecodes.KEY_F10: 0x43, ecodes.KEY_F11: 0x44, ecodes.KEY_F12: 0x45,
    ecodes.KEY_PAUSE: 0x48,
    ecodes.KEY_LEFTCTRL: 0xE0, ecodes.KEY_LEFTSHIFT:  0xE1, ecodes.KEY_LEFTALT:    0xE2,
    ecodes.KEY_LEFTMETA: 0xE3, ecodes.KEY_RIGHTCTRL:  0xE4, ecodes.KEY_RIGHTSHIFT: 0xE5,
    ecodes.KEY_RIGHTALT: 0xE6, ecodes.KEY_RIGHTMETA:  0xE7, ecodes.KEY_COMPOSE:    0x65, 
    ecodes.KEY_SYSRQ:    0x46, ecodes.KEY_SCROLLLOCK: 0x47, ecodes.KEY_DELETE:     0x4c,
    ecodes.KEY_END:      0x4d, ecodes.KEY_INSERT:     0x49, ecodes.KEY_HOME:       0x4a,
    ecodes.KEY_PAGEUP:   0x4B, ecodes.KEY_PAGEDOWN:   0x4e, ecodes.KEY_LEFT:       0x50,
    ecodes.KEY_DOWN:     0x51, ecodes.KEY_UP:         0x52, ecodes.KEY_RIGHT:      0x4F, 
    ecodes.KEY_NUMLOCK:  0x53, ecodes.KEY_KPSLASH:    0x54, ecodes.KEY_KPASTERISK: 0x55,
    ecodes.KEY_KPMINUS:  0x56, ecodes.KEY_KPPLUS:     0x57, ecodes.KEY_KPENTER:    0x58,
    ecodes.KEY_KP1:      0x59, ecodes.KEY_KP2:        0x5a, ecodes.KEY_KP3:        0x5b,
    ecodes.KEY_KP4:      0x5c, ecodes.KEY_KP5:        0x5d, ecodes.KEY_KP6:        0x5e,
    ecodes.KEY_KP7:      0x5f, ecodes.KEY_KP8:        0x60, ecodes.KEY_KP9:        0x61,
    ecodes.KEY_KP0:      0x62, ecodes.KEY_KPDOT:      0x63,

}

modifier_mask = {
    ecodes.KEY_LEFTCTRL: 0x01, ecodes.KEY_LEFTSHIFT: 0x02, ecodes.KEY_LEFTALT: 0x04,
    ecodes.KEY_LEFTMETA: 0x08, ecodes.KEY_RIGHTCTRL: 0x10, ecodes.KEY_RIGHTSHIFT: 0x20,
    ecodes.KEY_RIGHTALT: 0x40, ecodes.KEY_RIGHTMETA: 0x80,
}

IDENTITY_FILE = "~/.ssh/id_rsa"

PI_HOST_KB = "hidk@rpi02w"
REMOTE_COMMAND_KB = "cat > /dev/hidg0"
PI_HOST_M = "hidm@rpi02w"
REMOTE_COMMAND_M = "cat > /dev/hidg1"

keyboard = InputDevice('/dev/input/event8')
mouse = InputDevice('/dev/input/event4')

#remote_cursor = (0, 0)  # Start at top-left for remote
#local_cursor  = (0, 0)  # Optional: you can track local for logging or toggling

sshkb = subprocess.Popen(["ssh","-i" ,IDENTITY_FILE , PI_HOST_KB, REMOTE_COMMAND_KB], stdin=subprocess.PIPE)
sshm = subprocess.Popen(["ssh","-i" ,IDENTITY_FILE , PI_HOST_M, REMOTE_COMMAND_M], stdin=subprocess.PIPE)

class TFSM:
    def __init__(self):
        self._state = TFSM_STATE.IDLE
        self._key1 = False
        self._key2 = False
        self._grabbed = False

    @property
    def grabbed(self):
        return self._grabbed

    @grabbed.setter
    def grabbed(self, value):
        self._grabbed = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def key1(self):
        return self._key1

    @key1.setter
    def key1(self, value):
        self._key1 = value
        self.fsm()

    @property
    def key2(self):
        return self._key2

    @key2.setter
    def key2(self, value):
        self._key2 = value
        self.fsm()

    def fsm(self):
        if self.state == TFSM_STATE.IDLE:
            if self.key1 and self.key2:
                self.state = TFSM_STATE.TOGGLE

        elif self.state == TFSM_STATE.TOGGLE:
            if not (self.key1 or self.key2):
                self.state = TFSM_STATE.IDLE
                if self.grabbed:
                    print("Un-grabbing devices")
                    keyboard.ungrab()
                    mouse.ungrab()
                    self.grabbed = False
                else:
                    print("Grabbing devices")
                    keyboard.grab()
                    mouse.grab()
                    self.grabbed = True

tfsm = TFSM()
pressed_keys = set()

def keyboard_thread():
    modifiers = 0
    for event in keyboard.read_loop():
        if event.type != ecodes.EV_KEY:
            continue
        code = event.code
        value = event.value
        if code in modifier_mask:
            #print(f"Code found on modifier mask {ecodes.KEY[code]}") 
            if value == 1:
                modifiers |= modifier_mask[code]
                if code == ecodes.KEY_RIGHTSHIFT:
                    tfsm.key1 = True
            elif value == 0:
                modifiers &= ~modifier_mask[code]
                if code == ecodes.KEY_RIGHTSHIFT:
                    tfsm.key1 = False
        elif code in linux_to_hid:
            #print(f"Code found on linux_to_hdi {ecodes.KEY[code]}") 
            hid_code = linux_to_hid[code]
            if value == 1:
                pressed_keys.add(hid_code)

                if code == ecodes.KEY_PAUSE:
                    tfsm.key2 = True

            elif value == 0:
                pressed_keys.discard(hid_code)

                if code == ecodes.KEY_PAUSE:
                    tfsm.key2 = False

        else: 
            print(f"Code not found on linux_to_hdi map {ecodes.KEY[code]}")

        if tfsm.grabbed and sshkb and sshkb.stdin:
            report = bytearray(8)
            report[0] = modifiers
            for i, key in enumerate(sorted(pressed_keys)[:6]):
                report[2 + i] = key
            try: 
                sshkb.stdin.write(report)
                sshkb.stdin.flush()
            except Exception as e: 
                print("KEYBOARD WRITE FAILED,",e);
                raise RuntimeError("Mouse thread failed to write exiting") 


def mouse_thread():
    buttons = 0
    dx = dy = wheel = 0
    remote_cursor = [0, 0]
    event_counter = 0
    max_events = 5  # Change this to control smoothing/batching
    scroll_thresh = 10

    while True:
        try:
            for event in mouse.read_loop():
                if event.type == ecodes.EV_KEY:
                    wheel = 0 
                    if event.code == ecodes.BTN_LEFT:
                        buttons = buttons | 0x01 if event.value else buttons & ~0x01
                    elif event.code == ecodes.BTN_RIGHT:
                        buttons = buttons | 0x02 if event.value else buttons & ~0x02
                    elif event.code == ecodes.BTN_MIDDLE:
                        buttons = buttons | 0x04 if event.value else buttons & ~0x04

                elif event.type == ecodes.EV_REL:
                    if event.code == ecodes.REL_X:
                        dx += event.value * 7
                        wheel = 0 
                    elif event.code == ecodes.REL_Y:
                        dy += event.value * 7
                        wheel = 0 
                    elif event.code == ecodes.REL_WHEEL:
                        wheel += event.value 

                event_counter += 1

                # When threshold reached, send update
                if event_counter >= max_events and tfsm.grabbed and sshm and sshm.stdin:
                    remote_cursor[0] = max(0, min(32767, remote_cursor[0] + dx))
                    remote_cursor[1] = max(0, min(32767, remote_cursor[1] + dy))

                    wheel_byte = wheel & 0xFF if wheel >= 0 else (256 + wheel)

                    report = bytearray([
                        buttons,
                        remote_cursor[0] & 0xFF,
                        (remote_cursor[0] >> 8) & 0xFF,
                        remote_cursor[1] & 0xFF,
                        (remote_cursor[1] >> 8) & 0xFF,
                        wheel & 0xFF,
                    ])

                    try:
                        sshm.stdin.write(report)
                        sshm.stdin.flush()
                        wheel = 0 
                        print("Report (hex):", report.hex())
                        print(f"Report is Buttons = {buttons:02x} Cursor = ({remote_cursor[0]:04x},{remote_cursor[1]:04x})  wheel = {wheel:02x}")
                    except Exception as e:
                        print("Mouse write failed:", e)
                        #raise RuntimeError("Mouse thread failed to write")

                    dx = dy = wheel = 0
                    event_counter = 0

        except Exception as e:
            print("Exception in mouse_thread:", e)
            raise RuntimeError("Mouse thread crashed")


try:
    kbd_thread = threading.Thread(target=keyboard_thread, daemon=True)
    m_thread   = threading.Thread(target=mouse_thread, daemon=True)

    kbd_thread.start() 
    m_thread.start() 

    while True:
        if not kbd_thread.is_alive() or not m_thread.is_alive(): 
            print("[Fatal] One of the threads has died, Exiting with failure.")
            raise RuntimeError("Input thread died") 
            
        time.sleep(1)

except KeyboardInterrupt:
    try:
        sshkb.terminate()
        sshm.terminate()
    except Exception:
        pass 
    sys.exit(0) 

except Exception as e: 
    print(f"[ERROR] {e}") 
    sys.exit(1) 

finally:
    try:
        keyboard.ungrab()
        mouse.ungrab()
    except:
        pass
