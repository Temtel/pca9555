from pca9555 import PCA9555
from machine import SoftI2C,Pin
from time import sleep

i2c=SoftI2C(Pin(22),Pin(21))
pca = PCA9555(i2c)

pca.inputPins(0)
pca.outputPins(8)


while True:
    if pca.readPin(0) == 1:
        pca.writePin(8,1)
    else:
        pca.writePin(8,0)
        


