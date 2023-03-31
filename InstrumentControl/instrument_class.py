# %%
import numpy as np
import pyvisa as visa
import time
import serial
from ThorlabsPM100 import ThorlabsPM100


class EDFA:
    def __init__(self):
        rm = visa.ResourceManager()
        self.device = rm.open_resource("GPIB0::5::INSTR")
        self.device.read_termination = "\x00"
        self.device.write_termination = "\x00"
        self.power = float(self.device.query("CPU?")[4:]) / 10

    def set_power(self, power):
        power_str = str(np.round(10 * power, 0))[:-2]
        self.device.write("CPU=" + power_str)
        time.sleep(1)
        # print(self.device.query('CPU?'))
        self.power = float(self.device.query("CPU?")[4:]) / 10

    def turn_off(self):
        self.device.write("K0")

    def turn_on(self):
        self.device.write("K1")


class SignalGenerator:
    def __init__(self):
        rm = visa.ResourceManager()
        self.device = rm.open_resource("GPIB0::15::INSTR")
        self.device.read_termination = "\r\n"
        self.device.write_termination = "\r\n"

    def set_delay(self, delay):
        self.device.write("DT 3,2," + str(delay))

    def set_offset(self, offset):
        self.device.write("DT 2,1," + str(offset))

    def set_rate(self, rate):
        self.device.write("TR 0," + str(rate))

    def check_RATE_led(self):
        stat_array = np.array([])
        for indx in range(100):
            status = int(self.device.query("IS 4"))
            time.sleep(0.01)
            stat_array = np.append(stat_array, status)
        check = np.sum(stat_array)
        return check


class oscilloscope:
    def __init__(self):
        rm = visa.ResourceManager()
        self.device = rm.open_resource("GPIB0::7::INSTR")
        self.device.read_termination = "\n"
        self.device.write_termination = "\n"
        self.device.timeout = 30000

    def saveWaveform(self, channel):
        self.device.write(":DATA:SOURCE CH" + str(channel))
        self.device.write(":data:encdg sribinary")
        self.device.write("CURVe?")

        raw = self.device.read_raw()
        # print(len(raw))
        # print(len(raw[13:-1]))
        waveform = np.fromstring(raw[13:-1], dtype=np.int16)
        # waveform = self.device.query_binary_values('CURVe?', datatype='b', is_big_endian=True)
        settings = self.device.query("WFMOutpre?").split(";")
        x_increment = float(settings[9].split(" ")[-1])
        x_origin = float(settings[10].split(" ")[-1])

        y_increment = float(settings[13].split(" ")[-1])
        y_origin = float(settings[15].split(" ")[-1])
        y_reference = float(settings[14].split(" ")[-1])

        voltage = np.zeros(len(waveform))
        time_val = np.zeros(len(waveform))
        for i in range(len(waveform)):
            # assumes time is shared
            time_val[i] = x_origin + (i * x_increment)
            voltage[i] = ((waveform[i] - y_reference) * y_increment) + y_origin
        return time_val, voltage

    def trigger(self, channel):
        self.device.write(":DATA:SOURCE CH" + str(channel))
        self.device.write(":TRIGGER:B:EDGE:SLOPE RISE")

    def singleAcq(self):
        self.device.write(":ACQuire:STOPAFTER SEQUENCE")
        self.device.write(":ACQuire:NUMACq 1")
        self.device.write(":ACQuire:STATE 1")

    def repeatAcq(self):
        self.device.write(":ACQuire:STOPAFTER RUNSTOP")
        self.device.write(":ACQuire:REPEt 1")
        self.device.write(":ACQuire:STATE 1")

    def stopAcq(self):
        self.device.write("ACQuire:STATE 0")


class piezo:
    def __init__(
        self,
        port="COM3",
        baudrate=115200,
        timeout=1,
        stage1=[0, 0, 0],
        stage2=[0, 0, 0],
    ):
        # Establish serial connection
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        if self.ser.is_open is False:
            self.ser.open()
        self.stage1 = stage1
        self.stage2 = stage2
        self.set_duty(1, "X", stage1[0])
        self.set_duty(1, "Y", stage1[1])
        self.set_duty(1, "Z", stage1[2])
        self.set_duty(2, "X", stage2[0])
        self.set_duty(2, "Y", stage2[1])
        self.set_duty(2, "Z", stage2[2])

    def close(self):
        self.ser.close()

    def read_buf(self):
        return self.ser.read(self.ser.inWaiting())

    def set_stage(self, stage_no, configuration):
        # configuration: [duty_x, duty_y, duty_z]
        self.set_duty(stage_no, "X", configuration[0])
        self.set_duty(stage_no, "Y", configuration[1])
        self.set_duty(stage_no, "Z", configuration[2])

    def set_duty(self, stage_no, dimension, duty_cycle, sleep=True):
        if duty_cycle < 0:
            duty_cycle = 0
            print("Duty cycle must be between 0 and 1! Input changed to 0.")
        if duty_cycle > 1:
            duty_cycle = 1
            print("Duty cycle must be between 0 and 1! Input changed to 1.")
        # voltage: 0-5 V
        # dimension: 'X', 'Y' or 'Z'
        # stage_no: '1' or '2'
        stage_no = str(stage_no)
        pwm_byte = duty_cycle * 255
        msg = dimension + stage_no + str(int(pwm_byte))
        msg = msg.encode("ascii")
        self.ser.write(msg)
        if stage_no == str(1):
            if dimension == "X":
                self.stage1[0] = duty_cycle
            if dimension == "Y":
                self.stage1[1] = duty_cycle
            if dimension == "Z":
                self.stage1[2] = duty_cycle
        if stage_no == str(2):
            if dimension == "X":
                self.stage2[0] = duty_cycle
            if dimension == "Y":
                self.stage2[1] = duty_cycle
            if dimension == "Z":
                self.stage2[2] = duty_cycle
        if sleep:
            time.sleep(0.05)

    def optimize(self):
        opt_PM = PM()
        prev_power = opt_PM.read()


class PM:
    """
    Thorlabs PM100D power meter.
    """

    def __init__(self):
        rm = visa.ResourceManager()
        self.device = rm.open_resource(
            "USB0::0x1313::0x8078::P0009779::INSTR", timeout=1
        )
        self.PM = ThorlabsPM100(inst=self.device)

    def read(self, scale="dBm", sleep=True):
        if sleep:
            time.sleep(0.1)
        if scale == "dBm":
            return 10 * np.log10(self.PM.read * 1e3)
        if scale == "W":
            return self.PM.read
