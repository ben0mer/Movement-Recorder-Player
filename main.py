import win32api
import win32con
import time,threading

class recordKeyboard(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.keyEvents = []
        self.stop_event = threading.Event()
        self.wPressed = False
        self.aPressed = False
        self.sPressed = False
        self.dPressed = False
        self.spacePressed = False
        self.ctrlPressed = False
    def run(self):
        self.record()
    def on_press(self, key):
        self.pressStartTime = time.time()
        print('{0} pressed'.format(key))
       
    def on_release(self, key):
        self.pressEndTime = time.time()
        self.pressDuration = self.pressEndTime - self.pressStartTime
        print('{0} release'.format(key))
        info = {'key': key, 'pressDuration': self.pressDuration, 'pressStartTime': self.pressStartTime, 'pressEndTime': self.pressEndTime}
        self.keyEvents.append(info)
    def stop(self):
        self.stop_event.set()
    def record(self):
        while not self.stop_event.is_set():
            w = win32api.GetAsyncKeyState(ord('W'))
            a = win32api.GetAsyncKeyState(ord('A'))
            s = win32api.GetAsyncKeyState(ord('S'))
            d = win32api.GetAsyncKeyState(ord('D'))
            space = win32api.GetAsyncKeyState(win32con.VK_SPACE)
            ctrl = win32api.GetAsyncKeyState(win32con.VK_LCONTROL)
            esc = win32api.GetAsyncKeyState(win32con.VK_ESCAPE)
            if w == -32767:
                if not self.wPressed:
                    self.wPressed = True
                    self.on_press('W')
            if a == -32767:
                if not self.aPressed:
                    self.aPressed = True
                    self.on_press('A')
            if s == -32767:
                if not self.sPressed:
                    self.sPressed = True
                    self.on_press('S')
            if d == -32767:
                if not self.dPressed:
                    self.dPressed = True
                    self.on_press('D')
            if ctrl == -32767:
                if not self.ctrlPressed:
                    self.ctrlPressed = True
                    self.on_press(win32con.VK_LCONTROL)
            if space == -32767:
                if not self.spacePressed:
                    self.spacePressed = True
                    self.on_press(win32con.VK_SPACE)
            if esc == -32767:
                self.on_press(win32con.VK_ESCAPE)
                self.stop()
                break
            else:
                if self.wPressed:
                    self.wPressed = False
                    self.on_release('W')
                if self.aPressed:
                    self.aPressed = False
                    self.on_release('A')
                if self.sPressed:
                    self.sPressed = False
                    self.on_release('S')
                if self.dPressed:
                    self.dPressed = False
                    self.on_release('D')
                if self.ctrlPressed:
                    self.ctrlPressed = False
                    self.on_release(win32con.VK_LCONTROL)
                if self.spacePressed:
                    self.spacePressed = False
                    self.on_release(win32con.VK_SPACE)
            time.sleep(0.05)
        for i in range(len(self.keyEvents)):
            if i == 0:
                self.keyEvents[i]['delay'] = 0
            else:
                delay = self.keyEvents[i]['pressStartTime'] - self.keyEvents[i-1]['pressEndTime']
                self.keyEvents[i]['delay'] = delay
class playKeyboard(threading.Thread):
    def __init__(self, keyEvents):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.keyEvents = keyEvents
        self.length = len(keyEvents)
        self.index = 0
    def run(self):
        self.play()
    def press_and_hold_key(self, key):
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        self.release_key(key)
    def release_key(self, key):
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)

    def play(self):
        while self.index < self.length:
            key = self.keyEvents[self.index]['key']
            if key == 'W':
                self.press_and_hold_key(ord('W'))
            elif key == 'A':
                self.press_and_hold_key(ord('A'))
            elif key == 'S':
                self.press_and_hold_key(ord('S'))
            elif key == 'D':
                self.press_and_hold_key(ord('D'))
            elif key == win32con.VK_SPACE:
                self.press_and_hold_key(win32con.VK_SPACE)
            elif key == win32con.VK_LCONTROL:
                self.press_and_hold_key(win32con.VK_LCONTROL)
            time.sleep(self.keyEvents[self.index]['delay'])
            self.index += 1
        print('done')

class recordMouse(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mouseEvents = []
        self.stop_recording = threading.Event()
    def run(self):
        self.record()
    def on_move(self, x, y):
        print('Pointer moved to {0}'.format((x, y)))
        self.now = time.time()
        info = {'x': x, 'y': y, 'time': self.now}
        self.mouseEvents.append(info)
    def stop(self):
        self.stop_recording.set()
    def record(self):
        previous_pos = win32api.GetCursorPos()
        while not self.stop_recording.is_set():
            current_pos = win32api.GetCursorPos()
            if current_pos != previous_pos:
                x, y = win32api.GetCursorPos()
                self.on_move(x, y)
                previous_pos = current_pos
            if win32api.GetAsyncKeyState(win32con.VK_ESCAPE) == -32767:
                self.stop()
                break
            time.sleep(0.01)
        for i in range(len(self.mouseEvents)):
            if i == 0:
                self.mouseEvents[i]['delay'] = 0
            else:
                delay = self.mouseEvents[i]['time'] - self.mouseEvents[i-1]['time']
                self.mouseEvents[i]['delay'] = delay
        print('done')
        print(self.mouseEvents)
class playMouse(threading.Thread):
    def __init__(self, mouseEvents):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.mouseEvents = mouseEvents
        self.length = len(mouseEvents)
        self.index = 0
    def run(self):
        self.play()
    def play(self):
        while self.index < self.length:
            x = self.mouseEvents[self.index]['x']
            y = self.mouseEvents[self.index]['y']
            win32api.SetCursorPos((x, y))
            time.sleep(self.mouseEvents[self.index]['delay'])
            self.index += 1
        print('done')

# ESC'ye basana kadar Klavye ve Mouse aktivitelerini kaydeder daha sonra oynatır.
keyboard_recorder = recordKeyboard()
mouse_recorder = recordMouse()
keyboard_recorder.start()
mouse_recorder.start()

keyboard_recorder.join()
mouse_recorder.join()

keyboard_player = playKeyboard(keyboard_recorder.keyEvents)
mouse_player = playMouse(mouse_recorder.mouseEvents)
keyboard_player.start()
mouse_player.start()

keyboard_player.join()
mouse_player.join()

# # Mouse hareketlerini kaydetme ve oynatma
# deneme = recordMouse()
# deneme.record()
# play = playMouse(deneme.mouseEvents)
# play.play()

# # Klavye hareketlerini kaydetme ve oynatma
# deneme = recordKeyboard()
# deneme.record()
# play = playKeyboard(deneme.keyEvents)
# play.play()



