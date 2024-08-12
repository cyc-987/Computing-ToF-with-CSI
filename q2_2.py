import CSIdata
from tqdm import tqdm
import numpy as np
from scipy.optimize import minimize_scalar

from matplotlib import pyplot as plt
from matplotlib import cm
# plt.style.use('_mpl-gallery')

# 初始化
filepathB = './data/CSI2.mat'
filepathC = './data/CSI3.mat'
csiB = CSIdata.CSIdata(filepathB)
csiC = CSIdata.CSIdata(filepathC)

def drawPic(csi: CSIdata.CSIdata, N, f, d, resolution_tao, points):
    smooth = csi.convertToSmoothCSI_advanced(N) # 转换成smooth矩阵
    print(smooth.shape)
    
    csi.computE(smooth)  
    P_MUSIC = csi.buildPMUSIC_advanced(f, d)  # 构造P_MUSIC函数（伪谱函数）
    
    theta_resolution = np.pi/1000
    xx = np.linspace(0, theta_resolution*points, num=points)
    yy = np.linspace(0, resolution_tao*points, num=points)
    X, Y = np.meshgrid(xx.copy(), yy.copy())
    try:
        Z = np.load('Z500.npy')
        print("found existing data")
    except:
        print("no existing data, computing...")
        Z = np.zeros((points, points), dtype=float)
        for i in tqdm(range(points), desc='Computing(rows)'):
            for j in range(points):
                Z[i][j] = P_MUSIC(xx[i], yy[j])
            # Z[i,:] = P_MUSIC(xx[i], yy)
        np.save('Z500.npy', Z)
    
    fig=plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(False)
    # print(X.shape, Y.shape, Z.shape)
    ax.plot_surface(X, Y, Z, cmap=cm.Blues)
    ax.set_title('P_MUSIC_with_AoA&ToF')
    ax.set_xlabel('theta/rad')
    ax.set_ylabel('tau/s')
    plt.show()
    
drawPic(csiB, 268, 312500, 0.5, 3e-11, 500)
