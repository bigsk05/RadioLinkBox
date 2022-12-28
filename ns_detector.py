import threading
import win32con, win32gui
from PIL import ImageGrab

class ns_detector(object):
    def __init__(self, debug = None) -> None:
        self.RECV = False
        self.SEND = False
        self.__debug = True if debug is not None else False
        monitor = threading.Thread(target=self.monitor)
        monitor.daemon
        monitor.start()

    def get_window_pos(self, name):
        name = name
        handle = win32gui.FindWindow(0, name)
        # Get handle
        if handle == 0:
            return None
        else:
            # return position and handle
            return win32gui.GetWindowRect(handle), handle

    def monitor(self):
        while True:
            (x1, y1, x2, y2), handle = self.get_window_pos('南山对讲')
            try:
                # Set Foreground
                win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                # Highlight window
                win32gui.SetForegroundWindow(handle)
            except:
                pass
            # Grab picture
            img_ready = ImageGrab.grab((x1, y1, x2, y2))

            try:
                if img_ready.getpixel((343, 125)) == (110, 189, 83):
                    if not self.RECV and self.__debug:
                        print("RECV ON")
                    self.RECV = True
                    if self.SEND and self.__debug:
                        print("SEND OFF (Busy)")
                    self.SEND = False
                elif img_ready.getpixel((343, 125)) == (61, 67, 83):
                    if self.RECV and self.__debug:
                        print("RECV OFF")
                    self.RECV = False
                    if self.SEND and self.__debug:
                        print("SEND OFF")
                    self.SEND = False
                elif img_ready.getpixel((343, 125)) == (206, 82, 82):
                    if self.RECV and self.__debug:
                        print("RECV OFF (Busy)")
                    self.RECV = False
                    if not self.SEND and self.__debug:
                        print("SEND ON")
                    self.SEND = True
                else:
                    if self.__debug:
                        print("RECV/SEND ERROR")
                        print(img_ready.getpixel((343, 125)))
            except:
                ...