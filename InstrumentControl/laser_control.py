import numpy as np
import pyvisa as visa
import time
from pylablib.devices import Thorlabs
import copy
import os
from OSA_control import OSA
script_dir = os.path.dirname(os.path.abspath(__file__))
calibration_file = os.path.join(script_dir, "calibration_data", "laser_calibration.npz")
calibration_data = np.load(calibration_file)


class laser:
    # Calibration data for the different lasers
    self_pos_array = calibration_data["self_pos_array"]
    actual_peaks_thorlabs = calibration_data["actual_peaks_thorlabs"]
    wavelength_array_santec = calibration_data["wavelength_array_santec"]
    actual_peaks_santec = calibration_data["actual_peaks_santec"]
    wavelength_array_ando = calibration_data["wavelength_array_ando"]
    actual_peaks_ando = calibration_data["actual_peaks_ando"]

    def __init__(
        self, type, target_wavelength, power="default", wl_interp=False, GPIB_num=0
    ):
        self.type = type
        self.target_wavelength = target_wavelength
        self.actual_wavelength = 0
        self.wl_interp = wl_interp
        rm = visa.ResourceManager()

        if power == "default":
            if type == "santec":
                self.power = 115
            elif type == "ando" or self.type == "ando2":
                self.power = 6
            elif type == "agilent":
                self.power = 0

        if self.type == "thorlabs":
            self.device = Thorlabs.KinesisMotor("27000677")
            self.device.home()
            self.device.wait_for_home()
        if self.type == "santec":
            self.device = rm.open_resource(f"GPIB{GPIB_num}::3::INSTR")
        if self.type == "ando":
            self.device = rm.open_resource(f"GPIB{GPIB_num}::24::INSTR")
        if self.type == "ando2":
            self.device = rm.open_resource(f"GPIB{GPIB_num}::23::INSTR")
        if self.type == "agilent":
            self.device = rm.open_resource(f"GPIB{GPIB_num}::10::INSTR")
        self.set_wavelength(target_wavelength)
        self.set_power(power)

    def set_wavelength(self, wavelength):
        """
        Sets the wavelength using the calibration data given in the start of the class.
        """
        if self.type == "thorlabs":
            self.wavelength_device_argument = np.round(
                np.interp(
                    wavelength, laser.actual_peaks_thorlabs, laser.self_pos_array
                ),
                0,
            )
            self.device.move_to(self.wavelength_device_argument)
            self.device.wait_move()
            self.target_wavelength = wavelength
        if self.type == "santec":
            if self.wl_interp:
                self.wavelength_device_argument = np.round(
                    np.interp(
                        wavelength,
                        laser.actual_peaks_santec,
                        laser.wavelength_array_santec,
                    ),
                    4,
                )
            else:
                self.wavelength_device_argument = wavelength
            self.device.write("WA:" + str(self.wavelength_device_argument))
            self.target_wavelength = wavelength
        if self.type == "ando" or self.type == "ando2":
            if self.wl_interp:
                self.wavelength_device_argument = np.round(
                    np.interp(
                        wavelength, laser.actual_peaks_ando, laser.wavelength_array_ando
                    ),
                    3,
                )
            else:
                self.wavelength_device_argument = wavelength
            self.device.write("TWL" + str(self.wavelength_device_argument))
            self.target_wavelength = wavelength
        if self.type == "agilent":
            self.wavelength_device_argument = wavelength
            self.device.write(
                "SOURCE1:CHAN1:WAV " + str(self.wavelength_device_argument) + "NM"
            )
            self.target_wavelength = wavelength

    def set_power(self, power):
        if self.type == "thorlabs":
            pass
        if self.type == "santec":
            if power >= 50 and power <= 118:
                self.device.write("CU:" + str(power))  # Set santec current
                self.power = power
            else:
                print("Power must be between 50 and 118")
        if self.type == "ando" or self.type == "ando2":
            if power >= -10 and power <= 8:
                self.device.write("TPDB" + str(power))  # Set ando power
                self.power = power
            else:
                print("Power must be between -10 and 8")
        if self.type == "agilent":
            if power >= -10 and power <= 6:
                self.device.write("SOURCE1:CHAN1:POW " + str(power))
                self.power = power
            else:
                print("Power must be between -10 and 6")

    def adjust_wavelength(self, res=0.01, sens="SMID", OSA_GPIB_num=[0, 18]):
        """
        Adjusts the wavelength to the target wavelength using the OSA.
        """
        wavelength_target = copy.copy(self.target_wavelength)
        align_osa = OSA(
            self.target_wavelength - 0.5,
            self.target_wavelength + 0.5,
            resolution=res,
            sensitivity=sens,
            GPIB_num=OSA_GPIB_num,
        )  # ,sweep_time=5)
        align_osa.set_sample(10001)
        peak = np.argmax(align_osa.powers)
        align_peak = align_osa.wavelengths[peak]
        error = align_peak - wavelength_target
        if (
            self.type == "thorlabs"
            or self.type == "ando"
            or self.type == "agilent"
            or self.type == "ando2"
        ):
            while abs(error) >= 0.005:
                self.set_wavelength(self.target_wavelength - error)
                time.sleep(1)
                align_osa.sweep()
                peak = np.argmax(align_osa.powers)
                align_peak = align_osa.wavelengths[peak]
                error = align_peak - wavelength_target

        if self.type == "santec":
            set_wl_list = []
            while abs(error) >= 0.1:
                if np.abs(error) <= 0.5:
                    self.set_wavelength(self.target_wavelength - 0.1 * np.sign(error))
                else:
                    self.set_wavelength(self.target_wavelength - error)
                time.sleep(1)
                align_osa.sweep()
                peak = np.argmax(align_osa.powers)
                align_peak = align_osa.wavelengths[peak]
                error = align_peak - wavelength_target
                if self.target_wavelength in set_wl_list:
                    break
                else:
                    set_wl_list = np.append(set_wl_list, self.target_wavelength)
                    # print(error_list)
        self.target_wavelength = wavelength_target
        self.actual_wavelength = align_peak

    def close(self):
        self.device.close()

    def toggle_laser(self):
        if self.type == "ando" or self.type == "ando2":
            state = int(self.device.query("L?")[0])
            if state == 0:
                toggle_signal = 1
            else:
                toggle_signal = 0
            self.device.write("L" + str(toggle_signal))
        else:
            print("Only works for ando")


class TiSapphire:
    """
    The Ti Sa laser is controlled externally by a Newport SMC100 motor, so it has a different class.
    """

    def __init__(self, com_port, NSL=10, PSL=10):
        from Newport_control import actuator

        # Set up parameters for Ti Sa control, this file is installed automatically when the Newport SMC100 software is installed
        SMC_file_loc = (
            "C:/Windows/Microsoft.NET/assembly/GAC_64/"
            + "Newport.SMC100.CommandInterface/"
            + "v4.0_2.0.0.3__d9d722840772240b/"
        )

        self.act = actuator(SMC_file_loc, com_port)
        self.act.initialize(PSL, NSL)

    def delta_wl_nm(self, del_wl):
        """
        Moves the Ti Sa laser by a certain number of nanometers.
        """
        # dist_1nm = -0.0678  # LGN measured response for 1 nm
        dist_1nm = (
            -0.08297
        )  # Thjalfe measured response for 1 nm (960-990 nm, R^2 = 0.99974)
        self.act.move(del_wl * dist_1nm)

    def delta_wl_arb(self, del_wl):
        """
        Moves the motor by del_wl mm, which is the Newport SMC100's native unit, but gives arbitrary response from Ti Sa.
        """
        self.act.move(del_wl)

    def get_pos(self):
        result, response, errString = self.act.SMC.TP(1, 00, "")
        return response

    def set_wavelength(
        self, target_wl, error_tolerance=0.1, OSA_GPIB_num=[0, 18], res=0.05
    ):
        """
        Sets the wavelength of the TiSa laser.
        Args:
            target_wl: self explanatory
            error_tolerance: Error tolerated from the OSA to target wl

        """
        osa = OSA(target_wl - 10, target_wl + 10, resolution=res, GPIB_num=OSA_GPIB_num)
        peak_val = np.max(osa.powers)
        counter = 1
        while peak_val < -65:  # Keeps expanding sweep size until TiSa is visible
            counter += 1
            osa = OSA(
                target_wl - 10 * counter,
                target_wl + 10 * counter,
                resolution=res,
                GPIB_num=OSA_GPIB_num,
            )
            peak_val = np.max(osa.powers)
        wl_cur = osa.wavelengths[np.argmax(osa.powers)]
        nm_diff = target_wl - wl_cur
        if counter > 1:  # If TiSa started far from target, do one rough step first
            self.delta_wl_nm(nm_diff)
            time.sleep(2)
            osa.sweep()
            wl_cur = osa.wavelengths[np.argmax(osa.powers)]
            nm_diff = target_wl - wl_cur
        while np.abs(nm_diff) > error_tolerance:
            self.delta_wl_nm(nm_diff)
            if np.abs(nm_diff) > 0.5:
                if nm_diff > 0:
                    osa = OSA(
                        wl_cur,
                        wl_cur + 2 * nm_diff,
                        resolution=res,
                        GPIB_num=OSA_GPIB_num,
                    )
                else:
                    osa = OSA(
                        wl_cur + 2 * nm_diff,
                        wl_cur,
                        resolution=res,
                        GPIB_num=OSA_GPIB_num,
                    )
            else:
                osa = OSA(
                    wl_cur - 0.5, wl_cur + 0.5, resolution=res, GPIB_num=OSA_GPIB_num
                )
            wl_cur = osa.wavelengths[np.argmax(osa.powers)]
            nm_diff = target_wl - wl_cur
