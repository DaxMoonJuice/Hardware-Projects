from machine import I2C

i2c = I2C(freq=400000)          # create I2C peripheral at frequency of 400kHz
                                # depending on the port, extra parameters may be required
                                # to select the peripheral and/or pins to use

                    # scan for slaves, returning a list of 7-bit addresses


print(i2c.scan())

##i2c.writeto(8, b'123')         # write 3 bytes to slave with 7-bit address 42
i2c.readfrom(8, 6)             # read 4 bytes from slave with 7-bit address 42

##i2c.readfrom_mem(42, 8, 3)      # read 3 bytes from memory of slave 42,
                                #   starting at memory-address 8 in the slave
##i2c.writeto_mem(42, 2, b'\x10') # write 1 byte to memory of slave 42
                                #   starting at address 2 in the slave
class masterI2C:

    ##This is Where We Store Variables Shared Across All Class

    def __init__(self,SDA,SCL,FREQ):
        from machine import IC2
        from machine import Pin
        
        self.SDA=SDA
        self.SCL=SCL
        self.FREQ=FREQ

        i2c=machine.IC2(scl=SCL,sda=SCL,freq=FREQ)


    def scan(self):
        print("Devices Found At Following Bus Addresses".join(i2c.scan()))


    def readfrom(self,BUSNUMBER,DATALEN):
        return i2c.readfrom(BUSNUMBER,DATALEN)
    

    




   

    

        
        
