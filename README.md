# PCA9555
Micropython driver for PCA9555
This fork is updated, optimized to support ESP32-S3, and makes use of the
interrupt pin for optimal non-blocking input functioning.

The PCA 9555 is an 16Bit IO Expander via i2c with a single shared interrupt pin.
possible with 8 PCA955 in one i2c bus.
Addresses from 0x20 to 0x28

For the IO0_* the Pins are 0-7 and for IO1_* they are  8-15

Usage:
---------
### Imports
<pre>
from machine import I2C, Pin
import time
from pca9555 import PCA9555
</pre>

### Initialize I2C and PCA9555
<pre>i2c_bus = I2C(1, scl=Pin(6), sda=Pin(7))  # Adjust pin numbers as needed
expander = PCA9555(i2c_bus, address=0x21)
</pre>
       
### Configure pins 0-8 as inputs (for buttons)
<pre>
for pin in range(9):  # Now correctly handling pins 0-8
    expander.input_pins(pin)
</pre>
        
### Define the interrupt callback function
<pre>
def interrupt_handler(pin):
    # Optional debounce to prevent noise from triggering multiple interrupts
    time.sleep_ms(50)  # Adjust debounce delay as necessary

    # Debug message to confirm interrupt activation
    print("Interrupt detected on GPIO", pin)

    # Poll the expander for the current button states for pins 0-8
    button_states = [expander.read_pin(p) for p in range(9)]
    print("Button States:", button_states)

    # Additional handling logic can be added here based on button states
</pre>

### Set up the ESP32 interrupt pin on GPIO 5 to trigger the interrupt handler
<pre>
interrupt_pin = Pin(5, Pin.IN, Pin.PULL_UP)
interrupt_pin.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_handler)
</pre>

### Main loop (no need to continuously poll)
<pre>
while True:
    # Optional: Add any non-blocking code here
    time.sleep(0.1)  # Small delay to allow for other processing
</pre>
