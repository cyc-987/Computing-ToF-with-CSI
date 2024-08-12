import CSIdata
import visual
import numpy as np
from scipy.optimize import minimize_scalar

# 初始化
filepathB = './data/CSI2.mat'
filepathC = './data/CSI3.mat'
csiB = CSIdata.CSIdata(filepathB)
csiC = CSIdata.CSIdata(filepathC)

def findDistance(csi, N, f, end_dist, enablePic):
    '''
    计算距离
    '''
    smooth1, smooth2 = csi.convertToSmoothCSI(N) # 转换成smooth矩阵
    num_antennas = smooth1.shape[0]  # 天线数量
    distances = []
    
    for i in range(num_antennas):
        smooth = smooth1[i]
        csi.computE(smooth)  # 计算子空间，其中Es为信号子空间，En为噪声子空间
        P_MUSIC = csi.buildPMUSIC(f)  # 构造P_MUSIC函数（伪谱函数）
        interval = (0, float(end_dist)/3e8)  # 寻找最大值的区间
        
        result = minimize_scalar(lambda x: -P_MUSIC(x), bounds=interval, method='bounded', options={'xatol': 1e-15})
        distance = result.x * 3e8
        distances.append(distance)
    
    average_distance = np.mean(distances)
    
    # 画个图
    if enablePic:
        pic = visual.pic('P_MUSIC')
        resolution = 1e-10
        dots = 5000
        x = np.linspace(0, dots * resolution, dots)
        P_MUSIC_val = np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            P_MUSIC_val[i] = P_MUSIC(x[i])
        pic.drawData(datax=x, data=P_MUSIC_val)
        pic.end()
    return average_distance

# 计算距离
B = np.array([1.0, 1.0])
C = np.array([7.3, 1.0])

N = 60  # 重叠子载波数
f = 312500  # 频率间隔
end_distance = 30  # 寻找最大值的终止距离，单位为米

distancesB = [findDistance(csiB, N, f, end_distance, True) for _ in range(csiB.num_dim)]
distancesC = [findDistance(csiC, N, f, end_distance, False) for _ in range(csiC.num_dim)]

distB = np.mean(distancesB)
distC = np.mean(distancesC)

print(f"B 点到 A 点的估计距离为: {distB:.2f} 米")
print(f"C 点到 A 点的估计距离为: {distC:.2f} 米")

# 绘制图像
pic = visual.pic('点A的MUSIC定位结果及其候选位置', figsize=(8, 8)) 

# 设置坐标轴标签
pic.set_labels(xlabel='X 轴', ylabel='Y 轴')

# 绘制圆形
pic.drawCircle(B, distB)
pic.drawCircle(C, distC)

pic.drawScatter(B, label="点B")
pic.drawScatter(C, label="点C")

# 设置x轴和y轴刻度比例为1:1
pic.ax.set_aspect('equal', 'box')

# 找交点并绘制
def find_circle_intersections(x1, y1, r1, x2, y2, r2):
    # 计算两圆心之间的距离
    d = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # 检查是否有交点
    if d > r1 + r2 or d < abs(r1 - r2) or (d == 0 and r1 == r2):
        return None  # 没有交点
    
    # 计算交点
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h = np.sqrt(r1**2 - a**2)
    x0 = x1 + a * (x2 - x1) / d
    y0 = y1 + a * (y2 - y1) / d
    rx = -(y2 - y1) * (h / d)
    ry = (x2 - x1) * (h / d)
    
    intersection1 = (x0 + rx, y0 + ry)
    intersection2 = (x0 - rx, y0 - ry)
    
    return intersection1, intersection2

intersections = find_circle_intersections(B[0], B[1], distB, C[0], C[1], distC)
print(f"交点坐标为: A1 ({intersections[0][0]:.2f}, {intersections[0][1]:.2f}), A2 ({intersections[1][0]:.2f}, {intersections[1][1]:.2f})")


pic.drawScatter(intersections[0], label="点A1")
pic.drawScatter(intersections[1], label="点A2")

pic.end()
