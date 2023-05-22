import serial
import time
import traceback


class EDFA:
    def __init__(self, port, baudrate=19200, timeout=1, mode="APC", channel=1):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=1,
            timeout=timeout,
        )
        self.set_channel(channel)
        self.set_mode(mode)
        self.portOK = False
        try:
            if not self.ser.isOpen:
                self.ser.open()
            self.serOK = True
        except:
            print("The EDFA port did not open")
            print("Please check the connection")
            self.ser.close()
            traceback.print_exc()

        if self.serOK:
            time.sleep(0.1)
            self.ser.flushInput()

    def write(self, command):
        if self.ser.isOpen():
            self.ser.write(
                (command + "\r\n").encode()
            )  # encode the command to bytes and add newline character
            time.sleep(0.1)  # delay for the device to process the command
        else:
            print("Serial port is not open")

    def read(self):
        if self.ser.isOpen():
            return (
                self.ser.readline().decode().strip()
            )  # read the response from the device, decode it and strip newline characters
        else:
            print("Serial port is not open")
            return None

    def close(self):
        if self.ser.isOpen():
            self.ser.close()

    def set_channel(self, channel):
        self.channel = channel

    def set_mode(self, mode):
        """
        Set the mode of the EDFA. Must be in the list of modes returned by get_mode_names().
        """
        if mode not in self.get_mode_names():
            print(f"Mode must be one of {self.get_mode_names()}")
            return
        self.mode = mode
        self.write(f":MODE:SW:CH{self.channel} {mode}")

    def get_mode_names(self):
        """
        Get list of available modes.
        """
        self.write(":READ:MODE:NAMES?")
        return self.read()

    def get_mode(self):
        """
        Get current mode.
        """
        self.write(f":MODE:SW:CH{self.channel}?")
        return self.read()

    def get_num_channels(self):
        """
        Get number of switchable channels.
        """
        self.write(":READ:MODE:CH?")
        return self.read()

    def get_ch_name(self):
        """
        Get name of the channel.
        """
        self.write(f":READ:DRIV:NAME:{self.mode}:CH{self.channel}?")
        return self.read()

    def set_current(self, value):
        """
        Set current in mA if mode is ACC, and output power in mW if mode is APC.
        """
        self.write(f":DRIV:{self.mode}:CUR:CH{self.channel} {value}")

    def get_current(self):
        """
        Get current in mA if mode is ACC, and output power in mW if mode is APC.
        """
        self.write(f":DRIV:{self.mode}:CUR:CH{self.channel}?")
        return self.read()

    def set_status(self, value):
        """
        Set driving status of the EDFA. Must be one of the following:
        0: OFF
        1: ON
        """
        self.write(f":DRIV:{self.mode}:STAT:CH{self.channel} {value}")

    def get_status(self):
        """
        Get driving status of the EDFA. Will be one of the following:
        0: OFF
        1: ON
        2: BUSY
        4: LOCK
        """
        self.write(f":DRIV:{self.mode}:STAT:CH{self.channel}?")
        return self.read()

    def set_master_control(self, value):
        """
        Set master control of the EDFA. Must be one of the following:
        0: OFF
        1: ON
        """
        self.write(f":DRIV:MCTRL {value}")

    def activeON(self):
        self.set_master_control(1)

    def activeOFF(self):
        self.set_master_control(0)

    def get_master_control(self):
        """
        Get master control of the EDFA. Will be one of the following:
        0: OFF
        1: ON
        2: BUSY
        """
        self.write(":DRIV:MCTRL?")
        return self.read()

    def get_interlock(self):
        self.write(":DRIV:INTERLOCK?")
        return self.read()

    def get_driv_unit(self):
        """
        Get unit of the driving channel.
        """
        self.write(f":READ:DRIV:UNIT:{self.mode}:CH{self.channel}?")

    def get_power_in(self):
        """
        Get input power in mW.
        """
        self.write(f":SENS:POW:IN:CH{self.channel}?")
        return self.read()

    def get_power_out(self):
        """
        Get output power in mW.
        """
        self.write(f":SENS:POW:OUT:CH{self.channel}?")
        return self.read()


# Usage
if __name__ == "__main__":
    device = EDFA("COM4", timeout=1)  # change 'COM4' to your actual serial port
    device.close()
