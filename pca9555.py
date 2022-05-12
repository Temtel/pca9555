
"""
PCA955
------------------------
16Bit IO Expander

GitHub: https://github.com/ldreesden/pca955
Author: L. Drees
Version: 1.0
Date:05/12/2022
Based on datasheet: https://www.nxp.com/docs/en/data-sheet/PCA9555.pdf

"""


from machine import SoftI2C, Pin
import time


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
    """PCA955 Driver
    16Bit IO extender
    i2c communication
    """



    def __init__(self, i2cBus, address=0x20):
        """
        Args:
            i2cBus: SoftI2C(Pin(*SCLpin*),Pin(*SDApin*))
            address: i2c address in hex (0x20 by default)
        """
        self.i2c = i2cBus
        self.address = address
        self.pinStats=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.pinValues=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def inputPins(self,inputPin):
        """
        Args:
            inputPin(int): 0-7 = IO0_0 - IO0_7 ; 8-15 = IO1_0-IO1_7 
        """
        self.pinStats[inputPin]=1
        stats=0
        if inputPin <= 7:
            for i in range(8):
                stats+=self.pinStats[i]<<i
            stats=int(hex(stats),0)
            self.i2c.writeto_mem(self.address,ConfigPort0,bytes([stats]))
        else:
            for i in range(8):
                stats+=self.pinStats[i+8]<<i
            stats=int(hex(stats),0)
            self.i2c.writeto_mem(self.address,ConfigPort1,bytes([stats]))
        

    def outputPins(self,outputPin):
        """
        Args:
            outputPin(int): 0-7 = IO0_0 - IO0_7 ; 8-15 = IO1_0-IO1_7 
        """
        self.pinStats[outputPin]=0
        stats=0
        if outputPin <= 7:
            for i in range(8):
                stats+=self.pinStats[i]<<i
            stats=int(hex(stats),0)
            self.i2c.writeto_mem(self.address,ConfigPort0,bytes([stats]))
        else:
            for i in range(8):
                stats+=self.pinStats[i+8]<<i
            stats=int(hex(stats),0)
            self.i2c.writeto_mem(self.address,ConfigPort1,bytes([stats]))


    def writePin(self,pin, value):
        """
        Args:
            Pin(int): 0-7 = IO0_0 - IO0_7 ; 8-15 = IO1_0-IO1_7 
            value(int): 0 = off ; 1 = on
        """
        self.pinValues[pin]=value
        vals=0
        if self.pinStats[pin]:
            print('ATTENTION Pin '+str(pin)+' at i2c address '+str(self.address)+' is configed as INPUT')
            return
        elif pin <= 7:
            for i in range(8):
                vals+=self.pinValues[i]<<i
            vals=int(hex(vals),0)
            self.i2c.writeto_mem(self.address,OutputPort0,bytes([vals]))
        else:
            for i in range(8):
                vals+=self.pinValues[i+8]<<i
            vals=int(hex(vals),0)
            self.i2c.writeto_mem(self.address,OutputPort1,bytes([vals]))
        print(vals)

        




    def readPin(self, pin):
        """Issue a measurement.
        Args:
            writeAddress (int): address to write to
        :return:
        """
        comeback = bytearray(1)
        if not self.pinStats[pin]:
            print('ATTENTION Pin '+str(pin)+' at i2c address '+str(self.address)+' is configed as OUTPUT')
            return
        elif pin <=7:
            comeback =self.i2c.readfrom_mem(self.address,InputPort0,1)
        else:
            self.i2c.readfrom_mem(self.address,InputPort1,2)
        raw = (comeback[0] >> (pin % 8)) & 1
        return raw


    def writei2c(self, writeAddress, buf):

        self.i2c.start()
        self.i2c.writeto(int(self.ADDRESS-1), int(writeAddress), int(buf))
        self.i2c.stop()

