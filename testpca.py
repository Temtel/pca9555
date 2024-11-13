from pca9555 import PCA9555
from machine import I2C,Pin
from time import sleep

#initialize second i2c bus on ESP32-S3 (i2c1)
i2c1=I2C(1, scl=Pin(6), sda=Pin(7))
devices = i2c1.scan()
print("i2c1 devices found:",devices)

#initialize the pca9555 gpio expander on the i2c1 bus
pca = PCA9555(i2c1)

#set inputs and outputs
pca.inputPins(0)
pca.outputPins(8)

# poll pins for changes?
while True:
    if pca.readPin(0) == 1:
        pca.writePin(8,1)
    else:
        pca.writePin(8,0)
        


