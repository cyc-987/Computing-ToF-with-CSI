import CSIdata
import visual
import numpy as np

# 加载 CSI 数据文件
filepath = './data/CSI1.mat'
csi = CSIdata.CSIdata(filepath)

# 计算 CSI 的导向矢量
omega = csi.div()

# 计算 TOF (Time of Flight)
ToF = np.mean(csi.computeToF(omega[0,:], 312500))

# 输出 TOF 估计结果
print(f"射频直连的单路径场景中估计的 TOF 时间为: {ToF:.2e} 秒")
