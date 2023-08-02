import time
import ctypes
import telnetlib
from ctypes import wintypes

csgo_windows_name = 'Counter-Strike: Global Offensive - Direct3D 9'

def in_csgo():
    try:
        # Constants
        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010

        # Get a handle to the window
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        # Open the process
        process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid.value)

        # Get the process name
        buffer_size = 260  # MAX_PATH
        buffer = ctypes.create_unicode_buffer(buffer_size)
        ctypes.windll.psapi.GetModuleFileNameExW(process_handle, None, buffer, buffer_size)

        # Close the process handle
        ctypes.windll.kernel32.CloseHandle(process_handle)

        process_name = buffer.value.split('\\')[-1]

        return True if process_name == 'csgo.exe' else False
    except:
        in_csgo()

def get_window_rect(hwnd):
    # Define RECT structure
    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", ctypes.c_long),
            ("top", ctypes.c_long),
            ("right", ctypes.c_long),
            ("bottom", ctypes.c_long)
        ]

    # Call GetWindowRect function
    rect = RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))

    # Extract and return window coordinates
    return rect.left, rect.top, rect.right, rect.bottom

def main():
    # handle of csgo
    hwnd = ctypes.windll.user32.FindWindowW(None, csgo_windows_name)

    # initialization of telnet
    tn = telnetlib.Telnet('127.0.0.1', 2121)

    while True:
        try:
            data = tn.read_until(b"\n").decode("utf-8")

            if 'Started tracking Steam Net Connection to =[' in data and 'handle' in data:
                print('Match detected!')

                state = in_csgo()

                # opening csgo
                ctypes.windll.user32.ShowWindow(hwnd, 3)
                ctypes.windll.user32.SetForegroundWindow(hwnd)

                time.sleep(1)

                timer = time.time()
                while not in_csgo():
                    ctypes.windll.user32.ShowWindow(hwnd, 3)
                    ctypes.windll.user32.SetForegroundWindow(hwnd)

                    time.sleep(2)
                    if time.time() - timer > 10:
                        main()

                # get resolution of csgo
                left, top, right, bottom = get_window_rect(hwnd)
                width = right - left
                height = bottom - top
                print(f'Game resolution: {width}x{height}')

                x = int(width / 2)
                y = int(height / 2.4)

                # click to accept button
                ctypes.windll.user32.SetCursorPos(ctypes.c_long(x), ctypes.c_long(y))
                ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

                if not state:
                    # return to program you were in
                    ctypes.windll.user32.keybd_event(0x12, 0, 0, 0) # hold alt
                    time.sleep(0.1)
                    ctypes.windll.user32.keybd_event(0x09, 0, 0, 0) # hold tab
                    time.sleep(0.2)
                    ctypes.windll.user32.keybd_event(0x09, 0, 2, 0) # release tab
                    time.sleep(0.1)
                    ctypes.windll.user32.keybd_event(0x12, 0, 2, 0) # release alt
        except:
            print("failed to connect to csgo (game not open? -netconport 2121 not set?)")
            try:
                tn = telnetlib.Telnet('127.0.0.1', 2121)
                hwnd = ctypes.windll.user32.FindWindowW(None, csgo_windows_name)
            except:
                time.sleep(1)

if __name__ == '__main__':
    ctypes.windll.msvcrt.system(ctypes.c_char_p('cls'.encode())) # clear console
    ctypes.pythonapi.Py_SetRecursionLimit(100000) # without this, the code crashes after a while

    print('''
▄▀█ █░█ ▀█▀ █▀█ ▄▀█ █▀▀ █▀▀ █▀▀ █▀█ ▀█▀
█▀█ █▄█ ░█░ █▄█ █▀█ █▄▄ █▄▄ ██▄ █▀▀ ░█░

█▄▄ █▄█   █▀▀ █▀▄▀█ █▀█ █▀█ █▀█ █▄█
█▄█ ░█░   ██▄ █░▀░█ █▀▀ █▄█ █▀▄ ░█░
https://github.com/emp0ry/''')

    try:
        main()
    except:
        print('AutoAccept Crashed!!\nRestarting...')
        time.sleep(2)
