import os
import time
import ctypes

try: from PIL import Image
except: os.system("pip install Pillow")
try: import win32gui
except: os.system("pip install win32gui"); import win32gui
try: import pyautogui
except: os.system("pip install keyboard"); import pyautogui
try: import win32ui, win32con
except: os.system("pip install pywin32"); import win32ui, win32con

# CS:GO windows name
csgo_windows_name = 'Counter-Strike: Global Offensive - Direct3D 9'

def screenshot():
    try:
        # get the window handle of the CSGO.exe window
        hwnd = win32gui.FindWindow(None, csgo_windows_name)

        # get the dimensions of the window
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        # coordinates of accept button
        x = width / 2
        y = height / 2.25

        # create a device context (DC) object for the entire window
        hdc = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(hdc)

        # create a memory DC that will be used to store the screenshot
        memDC = dcObj.CreateCompatibleDC()

        # create a bitmap object to hold the screenshot
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(dcObj, width, height)

        # select the bitmap into the memory DC
        memDC.SelectObject(screenshot)

        # copy the contents of the window into the memory DC
        memDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)

        # convert the bitmap to a numpy array
        bmpinfo = screenshot.GetInfo()
        bmpstr = screenshot.GetBitmapBits(True)
        
        # take CreateCompatibleDC
        image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        return image, x, y
    except:
        time.sleep(1)
        print('Error (def screenshot)')
        screenshot()

def main():
    while True:
        try:
            image, x, y = screenshot()

            # get pixel color from x, y coordinates
            color = image.getpixel((x, y))

            color_original = (76, 175, 80)
            # color_screenshot = (80, 175, 76)
            # color_test = (94, 203, 90)

            if color == color_original:
                print('Detected Accept Button')

                # open CS:GO
                handle = win32gui.FindWindow(None, csgo_windows_name)
                win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)
                win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)

                # click to accept button
                pyautogui.click(x, y)

                # return to program you were in
                user32 = ctypes.windll.user32
                user32.keybd_event(0x12, 0, 0, 0) # hold alt
                time.sleep(0.1)
                user32.keybd_event(0x09, 0, 0, 0) # hold tab
                time.sleep(0.2)
                user32.keybd_event(0x09, 0, 2, 0) # release tab
                time.sleep(0.1)
                user32.keybd_event(0x12, 0, 2, 0) # release alt
            time.sleep(1)
        except:
            time.sleep(1)
            print('Error (def main)')

if __name__ == '__main__':
    main()
