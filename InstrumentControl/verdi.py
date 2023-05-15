import time
import serial
import traceback

ON = 1
OFF = 0
EOL = "\r\n"


class verdiLaser:
    """
    This class provides an interface to interact with a Verdi laser device over a serial port.

    The class provides methods to set and get various parameters of the laser such as the
    output power, the state of the shutter, the temperature of different components and so on.
    It also provides methods to manage the serial port connection to the laser device.

    Attributes:
        port: A `serial.Serial` object which represents the serial port connection to the laser device.
        portOK: A boolean that indicates whether the serial port connection is open and working.
    """

    def __init__(self, ioport="/dev/ttyUSB0"):
        """Initialize the verdieLaser object."""
        self.port = serial.Serial(
            port=ioport,
            baudrate=19200,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=1,
            timeout=2,
        )

        self.portOK = False
        try:
            if not self.port.is_open:
                self.port.open()
            self.portOK = True
        except:
            print("The Verdi port did not open")
            print("Please check the connection")
            self.port.close()
            traceback.print_exc()

        if self.portOK:
            self.port.write(b"E=0" + EOL.encode())
            self.port.write(b"E=0" + EOL.encode())
            time.sleep(0.1)
            self.port.write(b">=0" + EOL.encode())
            time.sleep(0.1)

            self.port.flushInput()

    def portPause(self, pause=0.1):
        """Pause before querying the port."""
        if self.portOK:
            time.sleep(pause)

    def portClear(self):
        """Clear the input buffer.  The Verdi sends back an EOL
        if it received the message successfully.  They can
        build up in the buffer, so when you read from the port,
        you get this information, and now what you wanted.  It is
        also good to not oversample the port.
        """
        if self.portOK:
            self.port.flushInput()

    def portClose(self):
        """Close the port."""
        if self.portOK:
            self.port.close()
            self.portPause()
            self.portOK = False

    def portOpen(self):
        """Open the port."""
        self.portOK = False
        try:
            self.port.open()
            self.portOK = True
        except:
            print("The Verdi port did not open")
            print("Please check the connection")
            self.port.close()
            traceback.print_exc()  # print the exception

    def laserHome(self):
        """Set the laser in a safe state for work.  This means that
        power as low as it will go (0.01 W) and the shutter closed.
        """
        if self.portOK:
            self.setShutter(0)
            self.setPower(0.01)

    def inWaiting(self):
        """See how many characters are input buffer."""
        if self.portOK:
            return self.port.inWaiting()

    #####
    def laserQuery(self, cmd):
        """ Submit a query to the Veri and return the value.
            It will try to get the return value 11 times, and
            if it fails, it will return the string '-999'.  If the
            port has an error (portOK != True), it returns '-888'
        """
        if self.portOK:
            cnt = 0
            while True:
                self.portClear()
                self.port.write(f"?{cmd}{EOL}".encode())
                self.portPause()
                returnVal = self.port.readline().decode()[:-2]
                cnt += 1
                if returnVal and returnVal[0].isdigit():
                    # first letter is a digit, readline successful
                    break
                elif cnt > 10:
                    returnVal = '-999'
            return returnVal
        else:
            return '-888'

    #####

    def shutdown(self):
        """Shutdown the laser and port."""
        if self.portOK:
            self.portClear()
            self.setShutter(0)
            self.portPause()
            self.setPower(0.01)
            self.portPause()
            self.port.close()
            self.portOK = False

    def standbyON(self):
        """Put the laser in STANDBY."""
        if self.portOK:
            self.port.write(b"L=0" + EOL.encode())

    def enableON(self):
        """ENABLE the laser."""
        if self.portOK:
            self.port.write(b"L=1" + EOL.encode())

    def getShutter(self):
        """Check the state of the shutter.
        returns an int: 0 - shutter is closed; 1 - shutter is open
        """
        return int(self.laserQuery("S"))

    def setShutter(self, state):
        """Set the shutter state."""
        if self.portOK:
            if state in (1, 0, "ON", "OFF"):
                self.port.write(f"S={state}{EOL}".encode())

    def getPower(self):
        """Check the laser output power."""
        return float(self.laserQuery("P"))

    def setPower(self, power):
        """Set the laser output power."""
        if self.portOK:
            if power <= 0:
                power = 0.01
            elif power >= 10:
                power = 10
            self.port.write(f"P={power}{EOL}".encode())

    def getDiodeCurrent(self):
        """Returns the measured diode current, as a float."""
        return float(self.laserQuery("C"))

    def getLaserDiodeCurrent(self):
        """Returns the measured laser diode current."""
        return float(self.laserQuery("D1C"))

    def getEtalonSetTemp(self):
        """Returns the set Etalon temperature."""
        return float(self.laserQuery("EST"))

    def setEtalonTemp(self, etalonTemp):
        """Set the Etalon temperature."""
        if self.portOK:
            if etalonTemp > 60:
                etalonTemp = 60
            elif etalonTemp < 30:
                etalonTemp = 30
            self.port.write(f"ET={etalonTemp}{EOL}".encode())

    def getLBOSetTemp(self):
        """Returns the LBO set temperature.
        RETURN: float nnn.nn degC
        """
        return float(self.laserQuery("LBOST"))

    def getLBOTemp(self):
        """Returns the measured LBO temperature.
        RETURN: float nnn.nn degC
        """
        return float(self.laserQuery("LBOT"))

    def getVanadateSetTemp(self):
        """Returns the Vanadate set temperature.
        RETURN: float nn.nn degC
        """
        return float(self.laserQuery("VST"))

    def getVanadateTemp(self):
        """Returns the measured Vanadate set temperature.
        RETURN: float nn.nn degC
        """
        return float(self.laserQuery("VT"))

    def setVanadateTemp(self, vanadateTemp):
        """Set the Vanadate temperature."""
        if self.portOK:
            if vanadateTemp > 45:
                vanadateTemp = 45.00
            elif vanadateTemp < 20:
                vanadateTemp = 20.00
            self.port.write(f"VT={vanadateTemp}{EOL}".encode())


if __name__ == "__main__":
    laser = verdiLaser("COM4")
    laser.enableON()
    laser.setShutter(OFF)
    laser.setPower(4.5)

    # print("")
    # print("Self-test using the Verdi module")
    # print("")
    # print("SHUTTER should be closed")
    # print("POWER should be 0.02 W")
    # print("")
    # print("Shutter test 1: %5s" % laser.getShutter())
    # print("Shutter test 2: %5s" % laser.getShutter())
    # print("Power test 1: %5s" % laser.getPower())
    # print("Power test 2: %5s" % laser.getPower())
    # print("")
    # print("End of self test.  Closing the port.")

    # laser.shutdown()
