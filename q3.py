import CSIdata
import AccurateCSI
import visual
import numpy as np

# 初始化
filepathB = './data/CSI4.mat'
filepathC = './data/CSI5.mat'
csiB = CSIdata.CSIdata(filepathB)
csiC = CSIdata.CSIdata(filepathC)

f = 61.44/256.0 # 单位是MHz
processB = AccurateCSI.accurateCSI(csiB)
phaseB_average =  processB.processData()
parasB, PB = processB.estimate(f)

processC = AccurateCSI.accurateCSI(csiC)
phaseC_average =  processC.processData()
parasC, PC = processC.estimate(f)

print("parasB:\n", parasB)
print("parasC:\n", parasC)

x = np.linspace(0, phaseB_average.shape[0]-1, phaseB_average.shape[0])
y = np.zeros(x.shape[0])

# PB = lambda x: processB.buildPhaseModel(f)([80, 0.512, -0.02, -0.006, -0.02762, -0.5, 122, -0.3],x)
for i in range(x.shape[0]):
    y[i] = PB(x[i])
pic = visual.pic('B: actual vs estimated')
pic.drawData(data=phaseB_average)
pic.drawData(data=y)
pic.end()