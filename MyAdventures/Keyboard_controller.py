import pyautogui
import pygetwindow
import time 
import PIL
import io
import numpy as np 

# target_window = pygetwindow.getWindowsWithTitle("Minecraft 1.12")[0]
# target_window.activate()


# pyautogui.press('esc')
# time.sleep(3)

# left, top, width, height = target_window.left, target_window.top, target_window.width, target_window.height
# screenshot = pyautogui.screenshot(region=(left, top, width, height))
# pixel_array = np.array(screenshot)

# print(pixel_array.flatten())

# screenshot.save("screenshot.png", "PNG")

class KeyboardAction:
    def __init__(self, window_title): 
        self.target_window = pygetwindow.getWindowsWithTitle(window_title)[0]
        self.target_window.activate()
        pyautogui.press('esc')
        

    def forward(self):
        pyautogui.keyDown("w")
        time.sleep(2)
        pyautogui.keyUp("w")

    def backward(self):
        pyautogui.keyDown("s")
        time.sleep(2)
        pyautogui.keyUp("s")
    
    def right(self):
        pyautogui.keyDown("d")
        time.sleep(2)
        pyautogui.keyUp("d")

    def left(self):
        pyautogui.keyDown("a")
        time.sleep(2)
        pyautogui.keyUp("a")
    
    def jump(self):
        pyautogui.keyDown("space")
        time.sleep(2)
        pyautogui.keyUp("space")
    
    def jump_forward(self):
        pyautogui.keyDown("space")
        pyautogui.keyDown("w")
        time.sleep(3)
        pyautogui.keyUp("space")
        pyautogui.keyUp("w")

    def sprint_jump_forward(self):
        pyautogui.keyDown("space")
        pyautogui.keyDown("w")
        pyautogui.keyDown("ctrl")
        time.sleep(3)
        pyautogui.keyUp("space")
        pyautogui.keyUp("w")
        pyautogui.keyUp("ctrl")

if __name__ == '__main__':
    window_title = "Minecraft 1.12"
    keyboard_controller = KeyboardAction(window_title)
    keyboard_controller.sprint_jump_forward()




