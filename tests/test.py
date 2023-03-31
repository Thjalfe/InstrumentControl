import pyvisa as visa
# from InstrumentControl.OSA_control import OSA
from OSA_control_test import OSA
from InstrumentControl.laser_control import laser, TiSapphire
import numpy as np
import matplotlib.pyplot as plt
rm = visa.ResourceManager("C:/Windows/System32/visa32.dll")
print(rm.list_resources())

# TiSa = TiSapphire(3)
wl_tot = 4
del_wl = 0.2
num_sweeps = int(wl_tot / del_wl)
# |%%--%%| <44kq2ARlHO|xktV1QPeAQ>
osa = OSA(978.5, 982.5, GPIB_num=19)
# |%%--%%| <xktV1QPeAQ|cPEHpCSHBc>
for i in range(num_sweeps):
    TiSa.delta_wl_nm(del_wl)
    OSA_temp = OSA(977.5, 982.5, resolution=0.05, sample=1001)
    OSA_temp.save(f"test_data/test_{i}")
TiSa.delta_wl_nm(-wl_tot)
OSA(977.5, 982.5, resolution=0.05, sample=1001)
# |%%--%%| <cPEHpCSHBc|2NML2wCucO>
import glob

data_folder = "test_data/"
names = glob.glob(data_folder + "*.csv")
for idx, name in enumerate(names):
    data = np.loadtxt(name, delimiter=",")
    nan = np.where(data[:, 1] < -100)
    data[nan, 1] = np.nan
    plt.plot(data[:, 0], data[:, 1], label=f"{idx}")
plt.legend()
