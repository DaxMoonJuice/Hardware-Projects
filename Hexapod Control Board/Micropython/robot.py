from machine import I2C
from machine import Pin
import time
import math

class masterI2C:

    ##This is Where We Store Variables Shared Across All Class

    def __init__(self,FREQ):
        
        self.testVar='Bloorp'
        self.frequency=FREQ
        
        self.i2c=I2C(scl=Pin(13),sda=Pin(12),freq=self.frequency)


    def scanBus(self):
        print(self)
        print("The Following Buses Are In Use")
        return self.i2c.scan()
        

    def readFromBus(self,BUSNUMBER,DATALEN):

            return self.i2c.readfrom(BUSNUMBER,DATALEN)

    
    def writeToBus(self,BUSNUMBER,DATA):
            self.i2c.writeto(BUSNUMBER,DATA)

    def writeToMem(self,BUSNUMBER,START_ADDR,DATA):
            self.i2c.writeto_mem(BUSNUMBER,START_ADDR,DATA)


    def readFromMem(self,BUSNUMBER,START_ADDR,NUM_OF_BYTES):
             return self.i2c.readfrom_mem(BUSNUMBER,START_ADDR,NUM_OF_BYTES)

    def test(self):
        print(self.testVar)
    




class gyro:

    def __init__(self,MASTERI2C,BUSNUMBER):

        self.i2c=MASTERI2C
        self.busNum=BUSNUMBER


        #---Set Power Register

        #Address Number=104 (oX68)
        #Power Management Register=62 (0x3E)
        #Value To Power Up == 1(0x01)

        #How bits work

        #CLK_SEL looks at first three bits
        #Value of First Three Bits Used to Determine Setting

        #in this case dec 1 (0x01) 010 Means Setting 1 Is Selected
        

        self.i2c.writeToMem(self.busNum,62,b'\x01')


        #---Set DLPF register

        #Sets The FS_SEL Parameter In the DPLF register to 3
        #Value of 3 sets Gyro Full Scale Range to +/- 2000 degrees per second

        # ITG3200 address, 0x68(104)
        # Select DLPF register, 0x16(22)
        # 0x18(24) Gyro FSR of +/- 2000 dps

        self.i2c.writeToMem(self.busNum,22,b'\x18')
        time.sleep(0.5)
    
        
    def readRaw(self):
    # ITG3200 address, 0x68(104)
    # Read data back from 0x1D(29), 6 bytes
    # X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
        
        return self.i2c.readFromMem(self.busNum,29,6)
        #return self.i2c.readFromBus(self.busNum,6)

    def read(self):
        self.data=self.i2c.readFromMem(self.busNum,29,6)

        # Convert the data
        self.xGyro = self.data[0] * 256 + self.data[1]
        if self.xGyro > 32767 :
            self.xGyro -= 65536

        self.yGyro = self.data[2] * 256 + self.data[3]
        if self.yGyro > 32767 :
            self.yGyro -= 65536

        self.zGyro = self.data[4] * 256 + self.data[5]
        if self.zGyro > 32767 :
            self.zGyro -= 65536

        return [self.xGyro,self.yGyro,self.zGyro]

        

class magnometer:

    #Dictionaries cause problems for MicrOoPython

##    #Lets HardCode Values
##    __scales = {
##        0.88: [0, 0.73],
##        1.30: [1, 0.92],
##        1.90: [2, 1.22],
##        2.50: [3, 1.52],
##        4.00: [4, 2.27],
##        4.70: [5, 2.56],
##        5.60: [6, 3.03],
##        8.10: [7, 4.35],
##    }

    def __init__(self,MASTERI2C,BUSNUMBER):

        #Gauss Value and Declination Value (e.g. Magnetic Declination) have to set based on Location
        #Have Hardcoded mine to London
        #Values can be found with this site
        #http://www.magnetic-declination.com/
        self.gauss=4.7
        self.declination=(-2,5)
        
        self.i2c=MASTERI2C
        self.busNum=BUSNUMBER

       

        (degrees, minutes) = self.declination
        self.__declDegrees = degrees
        self.__declMinutes = minutes
        self.__declination = (degrees + minutes / 60) * math.pi / 180


        #used for setting device gain and converting two compliments to an integer
        self.__scale=2.56
        reg=5
        
     


        # Sets Data Output Rate and Measurement Configuration
        #Sending 0x70 will average 8 samples and will return average sample 15 times a second
        self.i2c.writeToMem(self.busNum,0,b'\0x70')

        #Sets Device Gain e.t.c the scale at which the results would be amplified by

        #<< IS A BITWISE OPERATOR IN THIS CASE IT WILL TAKE THE VALUE OF REG AND SHIFT BITS BY 5 PLACES TO LEF
        #In This Case The Gain Is Set To 390 (LSb/Gauss)
        self.i2c.writeToMem(self.busNum, 1, reg << 5) # Scale

        #Write to Register 2 (Mode Register) with value of 0 to set device to continuous operation mode
        #This will place a constant stream of data into chip registers which can then be read by master

        self.i2c.writeToMem(self.busNum,2,b'\0x00') #Continuous measurement



    def declination(self):
        return (self.__declDegrees, self.__declMinutes)

    def twos_complement(self, val, len):
        # Convert twos compliment to integer
        if (val & (1 << len - 1)):
            val = val - (1<<len)
        return val

    def __convert(self, data, offset):


        #float value used for conversions
        val = self.twos_complement(data[offset] << 8 | data[offset+1], 16)
        if val == -4096: return None
        return round(val * self.__scale, 4)

    def axes(self):

        #Read In Axis Data
        self.data=self.i2c.readFromBus(self.busNum,0)

        
        #print map(hex, data)
        x = self.__convert(data, 3)
        y = self.__convert(data, 7)
        z = self.__convert(data, 5)
        return (x,y,z)

    def heading(self):
        (x, y, z) = self.axes()
        headingRad = math.atan2(y, x)
        headingRad += self.__declination

        # Correct for reversed heading
        if headingRad < 0:
            headingRad += 2 * math.pi

        # Check for wrap and compensate
        elif headingRad > 2 * math.pi:
            headingRad -= 2 * math.pi

        # Convert to degrees from radians
        headingDeg = headingRad * 180 / math.pi
        return headingDeg

    def degrees(self, headingDeg):
        degrees = math.floor(headingDeg)
        minutes = round((headingDeg - degrees) * 60)
        return (degrees, minutes)

    def __str__(self):
        (x, y, z) = self.axes()
        return "Axis X: " + str(x) + "\n" \
               "Axis Y: " + str(y) + "\n" \
               "Axis Z: " + str(z) + "\n" \
               "Declination: " + self.degrees(self.declination()) + "\n" \
               "Heading: " + self.degrees(self.heading()) + "\n"

    def read(self):

        #read axis data returned from magnometer

        #returns heading measured in degrees
        return self.degrees(self.heading)
        
        
#Test Cdoe
master=masterI2C(100000)
mag=magnometer(master,13)
        
        

        

    

        
        
