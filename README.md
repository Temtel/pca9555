# PCA9555
Micropython driver vor PCA9555

The PCA 9555 is an 16Bit IO Expander via i2c.
possible with 8 PCA955 in one i2c bus.
Addresses from 0x20 to 0x28

For the IO0_* the Pins are 0-7 and for IO1_* they are  8-15
---------

# Imports

To use the i2c from your µC:

        from machine import SoftI2C, Pin
        from pca955 import PCA955

For recent Micropython firmwares is SoftI2C neccesary, for older version will I2C work.

# Init PCA955

        i2c=SoftI2C(scl=Pin(22),sda=Pin(21))
        pca=PCA9555(i2c, address = 0x20)

The i2c address is by default 0x20, if need to adjust the address take a look on the datasheet


Set pins to input or output
-------
________

After the initialisation the pins have to be set

for Input:

        pca.inputPins(0)


for Output:

        pca.outputPins(8)

# Read pins

        pca.readPin(0)

will return 0 if low and 1 if high at IO0_0

# Write pins

        pca.writePin(8,1)

will turn IO1_0 to high