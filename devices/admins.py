from gpiozero import Button, LED
from signal import pause
import requests
import configparser

# Setup
config = configparser.ConfigParser()
config.read('admins.ini')  # Update with the actual path to your config file

button1 = Button(20)
button2 = Button(21)
ledRed = LED(24) #18
ledGreen = LED(23) #23
ledBlue = LED(18) #24

# Turn the LED on initially
ledBlue.on()

# Your network send function
def send_message(event):
    try:
        print("send "+event)
        ledBlue.blink(on_time=0.2, off_time=0.2, background=True)
        response = requests.post(config['DEFAULT']['server'], json={"user": config['DEFAULT']['user'], "event": event})
        if response.status_code == 200:
            print("sent")
            ledBlue.off()
            ledRed.off()
            ledGreen.blink(on_time=2, off_time=0, n=1)
            ledGreen.off()
            ledBlue.on()
        else:
            print("Error from server:", response.text)
            ledBlue.off()
            ledRed.blink(on_time=0, off_time=2, n=1)
            ledBlue.on()  # Ensure the LED stays on after the off period
    except Exception as e:
        print("Network error:", e)

# Bind events
button1.when_pressed = lambda: send_message(config['DEFAULT']['event1'])
button2.when_pressed = lambda: send_message(config['DEFAULT']['event2'])

print("Running...")

pause()  # Keeps the program running
