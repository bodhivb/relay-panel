from guizero import App, Box, PushButton
import RPi.GPIO as GPIO
import time

# Define the GPIO pins
RELAY_1_PIN = 17
RELAY_2_PIN = 18
RELAY_3_PIN = 27
RELAY_4_PIN = 22
RELAY_5_PIN = 23
RELAY_6_PIN = 24

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
# Set up GPIO pins for the relays
GPIO.setup(RELAY_1_PIN, GPIO.OUT)
GPIO.setup(RELAY_2_PIN, GPIO.OUT)
GPIO.setup(RELAY_3_PIN, GPIO.OUT)
GPIO.setup(RELAY_4_PIN, GPIO.OUT)
GPIO.setup(RELAY_5_PIN, GPIO.OUT)
GPIO.setup(RELAY_6_PIN, GPIO.OUT)

# State array to save which button is pressed
button_state = [False] * 6

button_effect = [False] * 6

def relay_state_toggle(index, state):
    if index == 0:
        pin = RELAY_1_PIN
    elif index == 1:
        pin = RELAY_2_PIN
    elif index == 2:
        pin = RELAY_3_PIN
    elif index == 3:
        pin = RELAY_4_PIN
    elif index == 4:
        pin = RELAY_5_PIN
    elif index == 5:
        pin = RELAY_6_PIN
    else:
        print("Invalid index")
        
    GPIO.output(pin, state)

# Function to toggle the relay state
def toggle_relay_state(index):
    print ("Button {} pressed".format(index))
    button_state[index] = not button_state[index]
    relay_state_toggle(index, button_state[index])
    
    if button_state[index]:
        relay_buttons[index].bg = "green"
    else:
        relay_buttons[index].bg = None

# Function to toggle the relay states periodically
def toggle_relays_periodically():
    while True:
        for i in range(6):
            toggle_relay_state(i)
            time.sleep(1)

# Create the app
app = App(title="Relay Panel", width=1920, height=200)

# Create a box to hold the relay buttons
relay_box = Box(app, layout="grid", width="fill", height="fill")

# Create the relay buttons
relay_buttons = []
for i in range(6):
    relay_button = PushButton(relay_box, text="Relay {}".format(i+1), grid=[i % 6, i // 6], command=lambda v=i: toggle_relay_state(v))
    relay_buttons.append(relay_button)
    
# Clean up GPIO after the app is closed
def on_close():
    GPIO.cleanup()
    app.destroy()

# Set the app close event handler
app.when_closed = on_close

# Start toggling the relay states periodically
toggle_relays_periodically()

# Run the app
app.display()