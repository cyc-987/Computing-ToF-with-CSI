import CSIdata
import visual
import numpy as np

filepath = './data/CSI1.mat'
csi = CSIdata.CSIdata(filepath)

omega = csi.div()
distance = np.mean(csi.computeDist(omega[0,:], 312500))
print(distance)