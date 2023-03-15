#%%
from instrument_class import OSA, TiSapphire
import numpy as np
import matplotlib.pyplot as plt
TiSa = TiSapphire(4)
wl_tot = 4
del_wl = 0.2
num_sweeps = int(wl_tot/del_wl)
#%%
OSA(977.5, 982.5, resolution=0.05, sensitivity='SHI1')
#%%
for i in range(num_sweeps):
    TiSa.delta_wl_nm(del_wl)
    OSA_temp = OSA(977.5, 982.5, resolution=0.05, sample=1001)
    OSA_temp.save(f'test_data/test_{i}')
TiSa.delta_wl_nm(-wl_tot)
OSA(977.5, 982.5, resolution=0.05, sample=1001)
#%%
import glob
data_folder = 'test_data/'
names = glob.glob(data_folder+'*.csv')
for idx, name in enumerate(names):
    data = np.loadtxt(name, delimiter=",")
    nan = np.where(data[:, 1] < -100)
    data[nan, 1] = np.nan
    plt.plot(data[:, 0], data[:, 1], label=f"{idx}")
plt.legend()