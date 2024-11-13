
"""
PCA9555
------------------------
16Bit IO Expander

GitHub: https://github.com/ldreesden/pca955
Author: L. Drees
Revised by: Temtel
Version: 1.1
Date: 11/12/2024 Updated to address optimizations and fixes

Based on datasheet: https://www.nxp.com/docs/en/data-sheet/PCA9555.pdf
"""

from machine import SoftI2C, Pin
import time

# Register Definitions
InputPort0 = 0x00
InputPort1 = 0x01
OutputPort0 = 0x02
OutputPort1 = 0x03
PolInversionPort0 = 0x04
PolInversionPort1 = 0x05
ConfigPort0 = 0x06
ConfigPort1 = 0x07

#############################################################################

class PCA9555:
    """PCA9555 Driver: 16-bit I/O expander with I2C communication."""

    def __init__(self, i2cBus, address=0x20):
        """
        Args:
            i2cBus: SoftI2C(Pin(*SCLpin*), Pin(*SDApin*))
            address (hex): I2C address (default is 0x20)
        """
        self.i2c = i2cBus
        self.address = address
        self.pin_stats = [0] * 16  # Pin direction: 1 for input, 0 for output
        self.pin_values = [0] * 16 # Pin output states

    def set_pin_direction(self, pin, direction):
        """
        Set the pin direction.
        Args:
            pin (int): Pin number (0-15)
            direction (int): 1 for input, 0 for output
        """
        self.pin_stats[pin] = direction
        stats = 0
        port = ConfigPort0 if pin < 8 else ConfigPort1
        for i in range(8):
            stats += self.pin_stats[i + (8 if port == ConfigPort1 else 0)] << i
        self.i2c.writeto_mem(self.address, port, bytes([stats]))

    def input_pins(self, input_pin):
        """Configures specified pin as input (shorthand for set_pin_direction)"""
        self.set_pin_direction(input_pin, 1)

    def output_pins(self, output_pin):
        """Configures specified pin as output (shorthand for set_pin_direction)"""
        self.set_pin_direction(output_pin, 0)

    def write_pin(self, pin, value):
        """
        Write a digital value to an output pin.
        Args:
            pin (int): Pin number (0-15)
            value (int): 1 for high, 0 for low
        """
        if self.pin_stats[pin] == 1:
            print(f"Warning: Pin {pin} at address {hex(self.address)} is configured as INPUT.")
            return

        self.pin_values[pin] = value
        vals = 0
        port = OutputPort0 if pin < 8 else OutputPort1
        for i in range(8):
            vals += self.pin_values[i + (8 if port == OutputPort1 else 0)] << i
        self.i2c.writeto_mem(self.address, port, bytes([vals]))

    def read_pin(self, pin):
        """
        Read the digital state of an input pin.
        Args:
            pin (int): Pin number (0-15)
        Returns:
            int: Pin state, 1 for high, 0 for low
        """
        if self.pin_stats[pin] == 0:
            print(f"Warning: Pin {pin} at address {hex(self.address)} is configured as OUTPUT.")
            return

        port = InputPort0 if pin < 8 else InputPort1
        comeback = self.i2c.readfrom_mem(self.address, port, 1)
        return (comeback[0] >> (pin % 8)) & 1
