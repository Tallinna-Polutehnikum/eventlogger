from gpiozero import Button, LED
from signal import pause
import requests
import configparser

# Setup
button1 = Button(2)  # GPIO pin 2
button2 = Button(3)  # GPIO pin 3
led = LED(17)        # GPIO pin 17

config = configparser.ConfigParser()
config.read('admins.ini')  # Update with the actual path to your config file

# Turn the LED on initially
led.on()

# Your network send function
def send_message(event):
    try:
        response = requests.post(config['DEFAULT']['server'], json={"user": config['DEFAULT']['user'], "event": event})
        if response.status_code == 200:
            led.blink(on_time=0.2, off_time=0.2, n=3)
            led.on()  # Ensure the LED stays on after blinking
        else:
            print("Error from server:", response.text)
            led.off()
            led.blink(on_time=0, off_time=2, n=1)
            led.on()  # Ensure the LED stays on after the off period
    except Exception as e:
        print("Network error:", e)

# Bind events
button1.when_pressed = lambda: send_message(config['DEFAULT']['event1'])
button2.when_pressed = lambda: send_message(config['DEFAULT']['event2'])

pause()  # Keeps the program running
