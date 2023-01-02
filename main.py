"""
    main file for command_led project
    useage: sudo python3 main.py
    must use sudo to access GPIO pins
    @authors: Alec Parfitt, Josh Gmys, Philip Colen, Josh Gmys
"""

import speech_recognition as sr

from light_functions import *

import multiprocessing as mp

def stop_check(other_process):
    while True:
        r2 = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say stop to stop the animation")
            audio = r2.listen(source)
        try:
            command = r.recognize_google(audio)
            print("You said: " + command)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            continue
        if command == "stop":
            other_process.terminate()
            break


func_dict = {"red": turn_red, "green": turn_green, "purple" : turn_purple, "lights off" : lights_off, 
"Christmas" : christmas, "party" : party , "brightness up"  : increaseBrightNess, "brightness down" : lowerBrightness ,
"invert color" : invertColors, "Steelers": steelers, "yellow" : turn_yellow, "sky blue" : turn_skyblue, "Orange" : turn_orange }
# Create NeoPixel object with appropriate configuration.
cb = LED_BRIGHTNESS
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
prev_cmd = None
lights_off(strip)

if __name__ == '__main__':
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak a command!")
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio)
            print("You said: " + command)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            continue
        
        
        if command in func_dict:
            if "brightness" in command:
                cb = func_dict[command](strip, cb, prev_cmd)
            elif command == "Christmas":
                p = mp.Process(target=func_dict[command], args=(strip,))
                p.start()
                stop_check(p)
                lights_off(strip)
                prev_cmd = func_dict["purple"]
            elif command == "party":
                p = mp.Process(target=func_dict[command], args=(strip,))
                p.start()
                stop_check(p)
                lights_off(strip)
                prev_cmd = func_dict["purple"]
            else:
                func_dict[command](strip)
                prev_cmd = func_dict[command]
