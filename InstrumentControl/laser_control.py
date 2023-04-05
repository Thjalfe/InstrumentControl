import numpy as np
import pyvisa as visa
import time
from pylablib.devices import Thorlabs
import copy
from .OSA_control import OSA


class laser:
    # Calibration data for the different lasers
    self_pos_array = np.array(
        [
            196140,
            198654,
            201166,
            203678,
            206191,
            208703,
            211215,
            213728,
            216240,
            218752,
            221265,
            223777,
            226289,
            228801,
            231314,
            233826,
            236339,
            238850,
            241363,
            243875,
            246387,
            248900,
            251412,
            253925,
            256436,
            258949,
            261461,
            263974,
            266486,
            268998,
            271510,
            274022,
            276535,
            279048,
            281559,
            284072,
            286584,
            289096,
            291608,
            294121,
            296633,
            299145,
            301658,
            304170,
            306682,
            309194,
            311707,
            314219,
            316731,
            319245,
            321756,
            324269,
            326781,
            329293,
            331805,
            334317,
            336830,
            339342,
            341854,
            344366,
            346879,
            349391,
            351903,
            354417,
            356928,
            359440,
            361952,
            364465,
            366977,
            369489,
            372002,
        ]
    )

    actual_peaks_thorlabs = np.array(
        [
            1510.63,
            1511.99,
            1513.17,
            1514.22,
            1515.41,
            1516.51,
            1517.65,
            1518.75,
            1519.93,
            1521.2,
            1522.44,
            1523.76,
            1525.28,
            1526.56,
            1527.61,
            1528.33,
            1529.39,
            1530.53,
            1531.65,
            1532.7,
            1533.79,
            1534.91,
            1536.11,
            1537.3,
            1538.58,
            1540.0,
            1541.32,
            1542.53,
            1543.3,
            1544.28,
            1545.34,
            1546.45,
            1547.52,
            1548.62,
            1549.65,
            1550.8,
            1552.05,
            1553.28,
            1554.49,
            1555.68,
            1557.03,
            1557.83,
            1558.79,
            1560.03,
            1561.09,
            1561.99,
            1563.19,
            1564.31,
            1565.26,
            1566.35,
            1567.47,
            1568.57,
            1569.83,
            1571.07,
            1572.33,
            1573.37,
            1574.38,
            1575.22,
            1576.29,
            1577.35,
            1578.4,
            1579.32,
            1580.49,
            1581.6,
            1582.74,
            1583.84,
            1584.94,
            1586.05,
            1587.08,
            1588.21,
            1589.21,
        ]
    )

    wavelength_array_santec = np.array(
        [
            1.521,
            1.522,
            1.523,
            1.524,
            1.525,
            1.526,
            1.527,
            1.528,
            1.529,
            1.53,
            1.531,
            1.532,
            1.533,
            1.534,
            1.535,
            1.536,
            1.537,
            1.538,
            1.539,
            1.54,
            1.541,
            1.542,
            1.543,
            1.544,
            1.545,
            1.546,
            1.547,
            1.548,
            1.549,
            1.55,
            1.551,
            1.552,
            1.553,
            1.554,
            1.555,
            1.556,
            1.557,
            1.558,
            1.559,
            1.56,
            1.561,
            1.562,
            1.563,
            1.564,
            1.565,
            1.566,
            1.567,
            1.568,
            1.569,
            1.57,
            1.571,
            1.572,
            1.573,
            1.574,
            1.575,
            1.576,
            1.577,
            1.578,
            1.579,
            1.58,
            1.581,
        ]
    )

    actual_peaks_santec = np.array(
        [
            1521.015,
            1522.18,
            1523.31,
            1524.44,
            1525.515,
            1526.593,
            1526.885,
            1528.02,
            1529.243,
            1530.385,
            1531.468,
            1532.573,
            1533.698,
            1534.77,
            1535.158,
            1536.308,
            1537.42,
            1538.48,
            1539.595,
            1540.695,
            1541.12,
            1542.238,
            1543.38,
            1544.408,
            1545.55,
            1546.675,
            1547.198,
            1548.235,
            1549.365,
            1550.468,
            1551.54,
            1552.045,
            1553.09,
            1554.288,
            1555.373,
            1556.513,
            1557.6,
            1558.683,
            1559.27,
            1560.27,
            1561.378,
            1562.51,
            1563.548,
            1564.645,
            1565.163,
            1566.3,
            1567.463,
            1568.505,
            1569.57,
            1570.263,
            1571.29,
            1572.323,
            1573.45,
            1574.52,
            1575.178,
            1576.198,
            1577.278,
            1578.355,
            1579.495,
            1580.178,
            1581.26,
        ]
    )

    wavelength_array_ando = np.array(
        [
            1521.0,
            1522.0,
            1523.0,
            1524.0,
            1525.0,
            1526.0,
            1527.0,
            1528.0,
            1529.0,
            1530.0,
            1531.0,
            1532.0,
            1533.0,
            1534.0,
            1535.0,
            1536.0,
            1537.0,
            1538.0,
            1539.0,
            1540.0,
            1541.0,
            1542.0,
            1543.0,
            1544.0,
            1545.0,
            1546.0,
            1547.0,
            1548.0,
            1549.0,
            1550.0,
            1551.0,
            1552.0,
            1553.0,
            1554.0,
            1555.0,
            1556.0,
            1557.0,
            1558.0,
            1559.0,
            1560.0,
            1561.0,
            1562.0,
            1563.0,
            1564.0,
            1565.0,
            1566.0,
            1567.0,
            1568.0,
            1569.0,
            1570.0,
            1571.0,
            1572.0,
            1573.0,
            1574.0,
            1575.0,
            1576.0,
            1577.0,
            1578.0,
            1579.0,
            1580.0,
            1581.0,
        ]
    )

    actual_peaks_ando = np.array(
        [
            1521.045,
            1522.045,
            1523.045,
            1524.043,
            1525.038,
            1526.04,
            1527.038,
            1528.035,
            1529.035,
            1530.035,
            1531.033,
            1532.033,
            1533.033,
            1534.033,
            1535.03,
            1536.035,
            1537.038,
            1538.035,
            1539.033,
            1540.038,
            1541.035,
            1542.03,
            1543.028,
            1544.028,
            1545.023,
            1546.023,
            1547.023,
            1548.023,
            1549.023,
            1550.028,
            1551.028,
            1552.023,
            1553.025,
            1554.025,
            1555.028,
            1556.028,
            1557.028,
            1558.03,
            1559.02,
            1560.025,
            1561.025,
            1562.023,
            1563.025,
            1564.025,
            1565.025,
            1566.025,
            1567.03,
            1568.033,
            1569.033,
            1570.03,
            1571.033,
            1572.03,
            1573.03,
            1574.03,
            1575.033,
            1576.033,
            1577.038,
            1578.035,
            1579.033,
            1580.043,
            1581.043,
        ]
    )

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

    def adjust_wavelength(self, OSA_GPIB_num=[0, 18]):
        """
        Adjusts the wavelength to the target wavelength using the OSA.
        """
        wavelength_target = copy.copy(self.target_wavelength)
        align_osa = OSA(
            self.target_wavelength - 0.5,
            self.target_wavelength + 0.5,
            resolution=0.01,
            GPIB_num=OSA_GPIB_num,
        )  # ,sweep_time=5)
        # align_osa = OSA(self.target_wavelength-1.0,self.target_wavelength+1.0,resolution=0.05)#,sweep_time=5)
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
        from .Newport_control import actuator

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
        Moves the Ti Sa laser by a certain number of nanometers, the measured response is not linear, but it should be in the right ballpark.
        """
        dist_1nm = -0.0678  # LGN measured response for 1 nm
        self.act.move(del_wl * dist_1nm)

    def delta_wl_arb(self, del_wl):
        """
        Moves the motor by del_wl mm, which is the Newport SMC100's native unit, but gives arbitrary response from Ti Sa.
        """
        self.act.move(del_wl)

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
                        wl_cur, wl_cur + 2 * nm_diff, resolution=res, GPIB_num=OSA_GPIB_num
                    )
                else:
                    osa = OSA(
                        wl_cur + 2 * nm_diff, wl_cur, resolution=res, GPIB_num=OSA_GPIB_num
                    )
            else:
                osa = OSA(wl_cur - 0.5, wl_cur + 0.5, resolution=res, GPIB_num=OSA_GPIB_num)
            wl_cur = osa.wavelengths[np.argmax(osa.powers)]
            nm_diff = target_wl - wl_cur
