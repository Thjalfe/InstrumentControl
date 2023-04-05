import numpy as np
import pyvisa as visa
import time
import os


class OSA:
    def __init__(
        self,
        wavelength_start,
        wavelength_end,
        open=False,
        resolution=1,
        sensitivity="SMID",
        sweeptype="SGL",
        Trace="A",
        sweep_time=0,
        sample=None,
        GPIB_num=[0, 18],
    ):
        """
        Class for controlling the ANDO AQ6317B OSA.
        Args:
            wavelength_start: in nm
            wavelength_end: in nm
            open:
            resolution: 0.01-2 nm
            sensitivity: 'SMID', 'SHI1', 'SHI2', 'SHI3'
            sweeptype: 'SGL', 'RPT' (single, repeat)
            Trace: 'A', 'B', 'C', 'D'
            sweep_time: Not currently used
            sample: number of samples, default is auto

        """
        self.device_open = open
        self.wavelength_start = wavelength_start
        self.wavelength_end = wavelength_end
        self.resolution = resolution
        self.sample = sample
        self.sensitiviy = sensitivity
        self.sweeptype = sweeptype
        self.trace = Trace
        self.sweep_time = sweep_time
        self.TLS_on = 0

        rm = visa.ResourceManager()
        self.device = rm.open_resource(f"GPIB{GPIB_num[0]}::{GPIB_num[1]}::INSTR")
        self.device.timeout = 30000
        self.set_span(wavelength_start, wavelength_end)
        self.set_res(resolution)
        if sample is not None:
            self.set_sample(sample)
        self.set_sens(sensitivity)
        if self.device.query("TLSSYNC?")[0] == str(1):
            self.TLS_on = 1
            print("Warning! TLS sync is ON. Spectrum is not saved automatically!")
        else:
            self.TLS_on = 0
        self.sweep()
        self.device_open = True

    def set_sweeptype(self, sweeptype):
        self.device.write(sweeptype)

    def stop_sweep(self):
        self.device.write("STP")
        time.sleep(1)

    def set_span(self, wavelength_start, wavelength_end):
        self.device.write("STAWL" + str(wavelength_start))
        self.device.write("STPWL" + str(wavelength_end))

    def set_res(self, resolution):
        self.device.write("RESLN" + str(resolution))
        self.resolution = resolution

    def set_level(self, level):
        self.device.write("REFL" + str(level))

    def set_level_scale(self, level_scale):
        self.device.write("LSCL" + str(level_scale))

    def set_sample(self, sample_numb):
        self.device.write("SMPL" + str(sample_numb))
        self.sample = sample_numb

    def set_sens(self, sensitivity):
        self.device.write(sensitivity)
        self.sensitiviy = sensitivity

    def set_TLS(self, TLS):
        self.device.write("TLSSYNC" + str(TLS))
        if TLS == 1:
            self.TLS_on = 1
        if TLS == 0:
            self.TLS_on = 0

    def sweep(self):
        if self.TLS_on == 1:
            self.set_TLS(0)
            time.sleep(0.5)
            self.set_TLS(1)
            time.sleep(0.5)
        self.device.write(self.sweeptype)
        if self.TLS_on == 0:
            stat = 1
            while stat != 0:
                stat = int(self.device.query("SWEEP?")[:1])
                time.sleep(0.1)
            # time.sleep(self.sweep_time)
            wav = self.device.query_ascii_values(
                "WDAT" + str(self.trace), container=np.array
            )
            power = self.device.query_ascii_values(
                "LDAT" + str(self.trace), container=np.array
            )
            wav = wav[1:]
            power = power[1:]
            self.wavelengths = wav
            self.powers = power

    def get_spectrum(self):
        wav = self.device.query_ascii_values(
            "WDAT" + str(self.trace), container=np.array
        )
        power = self.device.query_ascii_values(
            "LDAT" + str(self.trace), container=np.array
        )
        wav = wav[1:]
        power = power[1:]
        self.wavelengths = wav
        self.powers = power

    def save(self, name):
        # self.device.write(self.sweeptype)
        # time.sleep(self.sweep_time)
        # wav = self.device.query_ascii_values('WDAT' + str(self.trace), container=np.array)
        # power = self.device.query_ascii_values('LDAT' + str(self.trace), container=np.array)
        # wav = wav[1:]
        # power = power[1:]
        # Avoid overwriting an existing file
        i = 1
        # parent_folder = os.path.dirname(os.path.dirname(os.getcwd()))
        while os.path.exists(os.path.join(name + ".csv")) is True:
            name = name + "_" + str(i)
            i = i + 1

        res = np.column_stack((self.wavelengths, self.powers))
        np.savetxt(os.path.join(name + ".csv"), res, fmt="%f", delimiter=",")

    def close(self):
        self.device.close()
