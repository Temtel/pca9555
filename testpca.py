from pca9555 import PCA9555
from machine import I2C,Pin
from time import sleep

i2c=I2C(1, scl=Pin(6), sda=Pin(7))
devices = i2c.scan()
print("i2c devices found:",devices)
pca = PCA9555(i2c)

pca.inputPins(0)
pca.outputPins(8)


while True:
    if pca.readPin(0) == 1:
        pca.writePin(8,1)
    else:
        pca.writePin(8,0)
        


