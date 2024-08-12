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
processB = AccurateCSI.accurateCSI(csiB) # 初始化
phaseB_average =  processB.processData() # 处理数据，得到平均相位
parasB, PB = processB.estimate(f)

processC = AccurateCSI.accurateCSI(csiC)
phaseC_average =  processC.processData()
parasC, PC = processC.estimate(f)

print("parasB:\n", parasB)
print("parasC:\n", parasC)

# 打印相位平均值的形状
print("PhaseB average shape:", phaseB_average.shape)
print("PhaseC average shape:", phaseC_average.shape)

# 绘制CSI4的实际相位图
picB = visual.pic('CSI4.mat数据解缠后对应实际相位图', figsize=(8, 8))
picB.set_labels(xlabel='子载波索引', ylabel='相位（弧度）')
picB.drawData(data=phaseB_average, color='tab:blue', linewidth=2.5)  # 蓝色线条，线宽为2.5
picB.end()

# 绘制CSI5的实际相位图
picC = visual.pic('CSI5.mat数据解缠后对应实际相位图', figsize=(8, 8))
picC.set_labels(xlabel='子载波索引', ylabel='相位（弧度）')
picC.drawData(data=phaseC_average, color='tab:orange', linewidth=2.5)  # 红色线条，线宽为2.5
picC.end()

# PB = lambda x: processB.buildPhaseModel(f)([80, 0.512, -0.02, -0.006, -0.02762, -0.5, 122, -0.3],x)

x = np.linspace(0, phaseB_average.shape[0]-1, phaseB_average.shape[0])
y = np.zeros(x.shape[0])
for i in range(x.shape[0]):
    y[i] = PB(x[i])
# 计算每个子载波的相对误差
relative_errors = np.abs(phaseB_average - y) / np.abs(phaseB_average)
# 计算平均相对误差
average_relative_error = np.mean(relative_errors)
print(f'CSI4.mat数据的实际数据和估计数据的平均相对误差: {average_relative_error:.4f}')
# 创建对比图的绘制对象
pic = visual.pic('CSI4.mat数据的实际相位与估计相位对比', figsize=(8, 8))
pic.set_labels(xlabel='子载波索引', ylabel='相位（弧度）')
pic.drawData(data=phaseB_average, color='#9FC9DF',  marker='o',linewidth=15, markersize=15, label='实际相位')
pic.drawData(data=y, color='tab:blue',  linewidth=4, marker='D',markersize=4,label='估计相位')
pic.end()


x = np.linspace(0, phaseC_average.shape[0]-1, phaseC_average.shape[0])
y = np.zeros(x.shape[0])
for i in range(x.shape[0]):
    y[i] = PC(x[i])
# 计算每个子载波的相对误差
relative_errors = np.abs(phaseC_average - y) / np.abs(phaseC_average)
# 计算平均相对误差
average_relative_error = np.mean(relative_errors)
print(f'CSI5.mat数据的实际数据和估计数据的平均相对误差: {average_relative_error:.4f}')
# 创建对比图的绘制对象
pic = visual.pic('CSI5.mat数据的实际相位与估计相位对比', figsize=(8, 8))
pic.set_labels(xlabel='子载波索引', ylabel='相位（弧度）')
pic.drawData(data=phaseC_average, color='#ECC97F',  marker='o',linewidth=15, markersize=15, label='实际相位')
pic.drawData(data=y, color='tab:orange',  linewidth=4, marker='D',markersize=4,label='估计相位')
pic.end()
