import CSIdata
import visual
import numpy as np
from scipy.optimize import minimize_scalar

# 初始化
filepathB = './data/CSI2.mat'
filepathC = './data/CSI3.mat'
csiB = CSIdata.CSIdata(filepathB)
csiC = CSIdata.CSIdata(filepathC)

# omegaC = csiC.div()
# distanceC = np.mean(csiC.computeDist(omegaC[0,:], 312500))
# dataC = csiC.computeDist(omegaC[0,:], 312500)
# print(distanceC)

def findDistance(csi, N, f, end_dist, enablePic):
    '''
    计算距离懒人包
    '''
    smooth1, smooth2 = csi.convertToSmoothCSI(N) # 转换成smooth矩阵
    # 备注：smooth1和2结果相同，我都算过了
    csi.computE(smooth1) # 计算子空间，其中Es为信号子空间，En为噪声子空间
    P_MUSIC = csi.buildPMUSIC(f) # 构造P_MUSIC函数（伪谱函数）
    end_distance =  end_dist# 寻找最大值的终止距离，单位为米
    intervel = (0, float(end_distance)/3e8) # 寻找最大值的区间
    result = minimize_scalar(lambda x: -P_MUSIC(x), bounds=intervel, method='bounded', options={'xatol': 1e-15}) # 寻找最大值
    distance = result.x*3e8
    
    # 画个图
    if enablePic:
        pic = visual.pic('P_MUSIC')
        resolution = 1e-10
        dots = 5000
        x = np.linspace(0, dots*resolution, dots)
        P_MUSIC_val = np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            P_MUSIC_val[i] = P_MUSIC(x[i])
        pic.drawData(datax=x, data=P_MUSIC_val)
        pic.end()
    return distance


N = 60 # 重叠子载波数
f = 312500 # 频率间隔
end_distance = 30 # 寻找最大值的终止距离，单位为米
distB = findDistance(csiB, N, f, end_distance, False)
distC = findDistance(csiC, N, f, end_distance, False)
print('B:', distB)
print('C:', distC)

# 计算点
B = np.array([1.0, 1.0])
C = np.array([7.3, 1.0])

pic = visual.pic('q2')
pic.drawCircle(B, distB)
pic.drawCircle(C, distC)

# 找交点
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
print('交点:', intersections)

pic.drawScatter(intersections[0])
pic.drawScatter(intersections[1])
pic.end()