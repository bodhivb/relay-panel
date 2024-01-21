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
program = 0

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
    GPIO.output(pin, not state)

# Function to turn off all relay pins
def turn_off_all_relays():
    for i in range(6):
        relay_state_toggle(i, False)
        button_state[i] = False
        relay_buttons[i].bg = None

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
    while program > 0:
        if program == 0:
            time.sleep(1)
        elif program == 1:
            for i in range(6):
                relay_state_toggle(i, True)
                time.sleep(1)
                relay_state_toggle(i, False)
        elif program == 2:
            for m in range(3):
                relay_state_toggle(2, True)
                time.sleep(0.2)
                relay_state_toggle(2, False)
                time.sleep(0.2)
            for n in range(3):
                relay_state_toggle(3, True)
                time.sleep(0.2)
                relay_state_toggle(3, False)
                time.sleep(0.2)
        elif program == 3:
            for o in range(6):
                relay_state_toggle(o, True)
            time.sleep(1)
            for p in range(6):
                relay_state_toggle(p, False)
            time.sleep(1)

# Create the app
app = App(title="Relay Panel", width=1920, height=550)

# Create a new button box to switch the page box
footer = Box(app, width="fill", align="bottom")

# Button to switch to relay box
PushButton(footer, text="Relay Box", command=lambda: switch_page(relay_box))
# Button to switch to switch box
PushButton(footer, text="Program Box", command=lambda: switch_page(program_box))


# Create a box to hold the relay buttons
relay_box = Box(app, layout="grid", width="fill", height="fill")
program_box = Box(app, layout="grid", width="fill", height="fill")

# Create the relay buttons
relay_buttons = []

# LAMPEN RELAY 
# 3 LEFT LAMP turn on/off
# 3 RIGHT LAMP turn on/off
# 2 SKULL LAMP turn on/off
# 1 BAR LAMP turn on/off

# 3 LEFT LAMO SWTICH MODEL
# 3 RIGHT LAMP SWITCH MODEL
relay_buttons.append(PushButton(relay_box, text="Links lampen", grid=[0, 0], command=lambda: toggle_relay_state(2)))
relay_buttons.append(PushButton(relay_box, text="Rechts lampen", grid=[1, 0], command=lambda: toggle_relay_state(3)))

relay_buttons.append(PushButton(relay_box, text="Skull lampen", grid=[0, 2], command=lambda: toggle_relay_state(1)))
relay_buttons.append(PushButton(relay_box, text="Led bar", grid=[1, 2], command=lambda: toggle_relay_state(0)))

relay_buttons.append(PushButton(relay_box, text="Links model", grid=[0, 1], command=lambda: toggle_relay_state(4)))
relay_buttons.append(PushButton(relay_box, text="Rechts model", grid=[1, 1], command=lambda: toggle_relay_state(5)))

relay_buttons.append(PushButton(relay_box, text="Reset", grid=[0, 3], command=lambda: turn_off_all_relays()))

PushButton(program_box, text="Relax", grid=[0, 0], command=lambda: start_program(1))
PushButton(program_box, text="Politie", grid=[1, 0], command=lambda: start_program(2))
PushButton(program_box, text="Disco", grid=[2, 0], command=lambda: start_program(3))
PushButton(program_box, text="Run auto", grid=[0, 2], command=lambda: toggle_relays_periodically())
PushButton(program_box, text="Stop", grid=[2, 2], command=lambda: start_program(0))

program_box.hide()
# Function to switch the page box
def switch_page(box):
    relay_box.hide()
    program_box.hide()
    box.show()

# Function to toggle the relay state
def toggle_relay_state(index):
    print ("Button {} pressed".format(index))
    program = 0
    button_state[index] = not button_state[index]
    relay_state_toggle(index, button_state[index])
    if button_state[index]:
        relay_buttons[index].bg = "green"
    else:
        relay_buttons[index].bg = None

def start_program(index):
    print ("Button {} pressed".format(index))
    turn_off_all_relays()
    program = index
    
# Clean up GPIO after the app is closed
def on_close():
    for i in range(6):
        relay_state_toggle(i, False)
    GPIO.cleanup()
    app.destroy()

# Set the app close event handler
app.when_closed = on_close

# Start toggling the relay states periodically
# toggle_relays_periodically()

# Run the app
app.display()