# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 18:32:41 2022

@author: Roberto

Combine and save tiff images from Lucia systems (DAPI, FITC, TXR)

HOWTO:
    1. Execute the script
    2. Open the TIFF image in Paint Shop Pro 7 (it will open as three separate files)
    3. Expand the window of the first image (the DAPI channel)
    4. press 'a' to adapt the image
    5. You can press 'v' to save the composite image
    6. Left and right arrow keys are remapped to switch between images
    7. The up arrow key can be used to quickly switch between 2 images (FITC, TXR)
    8. Press 'x' to close all the three images (composite, FITC, TXR)
    9. press 'q' to quit the script before typing in other programs!

"""

import pyautogui
# import time
from pynput import keyboard # https://stackoverflow.com/a/43106497/2962364

pyautogui.PAUSE = 0.1

def adapt():
    for i in range(3):
        
        # shift-t activates the histogram Stretch function
        pyautogui.keyDown("shift")
        pyautogui.press("t")
        pyautogui.keyUp("shift")
        # ctrl-tab to pass to the next image
        pyautogui.keyDown("ctrl")
        pyautogui.press("tab")
        pyautogui.keyUp("ctrl")
        
    # combine images as RGB
    # alt-c, m, c opens the combine window
    pyautogui.keyDown("alt")
    pyautogui.press("c")
    pyautogui.keyUp("alt")
    pyautogui.press(["m", "c"])
    # The DAPI image is already selected as the first channel, so we skip
    pyautogui.press("tab")
    # select the second image for the green channel
    pyautogui.press(["down", "tab"])
    # select the third image for the red channel, and execute
    pyautogui.press(["down", "down", "enter"])
    
    # shitf-t: histogram stretch again the RGB image
    pyautogui.keyDown("shift")
    pyautogui.press("t")
    pyautogui.keyUp("shift")
    
    
    # histogram adjustment for the blue channel, otherwise the composite image is too blue
    # ctrl-shift-h opens the histogram adjustment window
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("shift")
    pyautogui.press("h")
    pyautogui.keyUp("shift")
    pyautogui.keyUp("ctrl")
    # we go to the last channel which is blue
    pyautogui.press(["down", "down", "down", "down", "tab",
                     "2", "0", "0", "tab", # output max = 200
                     "0", "tab", # min = 0
                     "3", "0", "tab", # Low = 30
                     "0", "tab", # % = 0
                     "1", "tab", # gamma = 1.0
                     "tab", "tab", "tab", # skip the buttons
                     "2", "5", "5", "tab", # High = 255
                     "0", "enter"]) # Midtone 0 and enter
    
    # switch to the DAPI image...
    pyautogui.keyDown("ctrl")
    pyautogui.press("tab")
    pyautogui.keyUp("ctrl")
    # ...and close it
    pyautogui.keyDown("alt")
    pyautogui.press("f")
    pyautogui.keyUp("alt")
    pyautogui.press(["c", "tab", "enter"])
    
    # Resize everything to fit better on screen
    resize()
    # Colorize the FITC and TXR images
    color()


def resize():
    # resize all the three images on screen to view them better
    for i in range(3):
        # open the resize window
        pyautogui.keyDown("alt")
        pyautogui.press("i")
        pyautogui.keyUp("alt")
        pyautogui.press("e")
        # Resize to 145%
        pyautogui.press(["1", "4", "5", "enter"])
        # ctrl-tab to pass to the next image
        pyautogui.keyDown("ctrl")
        pyautogui.press("tab")
        pyautogui.keyUp("ctrl")
    

def color():
    # colorize the FITC and TXR images
    for i in range(2):
        # increase the color depth to 16 millions
        pyautogui.keyDown("alt")
        pyautogui.press("c")
        pyautogui.keyUp("alt")
        pyautogui.press(["i", "6"])
        # open the Red/Green/Blue color menu
        pyautogui.keyDown("shift")
        pyautogui.press("u")
        pyautogui.keyUp("shift")
        if i == 0:
            # Green is -100, 0, -100
            pyautogui.press(["-", "1", "0", "0", "tab", "0", "tab", "-", "1", "0", "0", "enter"])
        elif i == 1:
            # Red is 0, -100, -100
            pyautogui.press(["0", "tab", "-", "1", "0", "0", "tab", "-", "1", "0", "0", "enter"])
        # next image
        pyautogui.keyDown("ctrl")
        pyautogui.press("tab")
        pyautogui.keyUp("ctrl")
        


def save():
    # prepare to save the composite image as tiff
    #ctrl-s to save
    pyautogui.keyDown("ctrl")
    pyautogui.press("s")
    pyautogui.keyUp("ctrl")
    # as tiff
    pyautogui.press(["tab", "t"])
    # go back to the file name input box
    pyautogui.keyDown("shift")
    pyautogui.press("tab")
    pyautogui.keyUp("shift")
    
    

def closeAll(): 
    # UNBOUNDED, I just didn't want to delete it yet
    # close the saved image
    pyautogui.keyDown("alt")
    pyautogui.press("f")
    pyautogui.keyUp("alt")
    pyautogui.press("c")
    # close the modified images
    for i in range(2):
        pyautogui.keyDown("alt")
        pyautogui.press("f")
        pyautogui.keyUp("alt")
        pyautogui.press(["c", "tab", "enter"])



def close():
    # close the modified images
    for i in range(3):
        # alt-f, c to close; tab for "do you want to save?" -> no; enter
        pyautogui.keyDown("alt")
        pyautogui.press("f")
        pyautogui.keyUp("alt")
        pyautogui.press(["c", "tab", "enter"])


def goright():
    # ctrl-tab = next image
    pyautogui.keyDown("ctrl")
    pyautogui.press("tab")
    pyautogui.keyUp("ctrl")
    

def goleft():
    # ctrl-shift-tab = previous image
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("shift")
    pyautogui.press("tab")
    pyautogui.keyUp("shift")
    pyautogui.keyUp("ctrl")
    

def switch(where=["r"]): # "it's not a bug, it's a feature"(TM)
    # switch between two images
    if where[0] == "l":
        where[0] = "r"
        goleft()
    elif where[0] == "r":
        where[0] = "l"
        goright()


        
def on_press(key):
    # main schema from https://stackoverflow.com/a/43106497/2962364
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == "a":
        adapt()
    elif k == "x":
        close()
    elif k == "v":
        save()
    elif k == "left":
        goright()
    elif k == "right":
        goleft()
    elif k == "up":
        switch()
    elif k == "r":
        resize()
    elif k == "q":
        print('Key pressed: ' + k, "; bye!")
        return False  # stop listener; remove this if want more keys
    print('Key pressed: ' + k)
    


def main():
    # https://stackoverflow.com/a/43106497/2962364
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys
    
if __name__ == "__main__":
    main()
