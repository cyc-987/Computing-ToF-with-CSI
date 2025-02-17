import numpy as np
from sklearn.cluster import KMeans
import scipy.io

class CSIdata():
    '''
    用于处理CSI数据的类
    '''
    def __init__(self, filepath):
        self.num_dim = 0
        self.num_waves = 0
        self.data = self.__loadData(filepath)
        
    # public funcs
    def pickUsefulData(self):
        '''
        从CSI数据中提取有用的子载波数据
        '''
        sec1 = self.data[:, 6:127]
        sec2 = self.data[:, 130:251]
        self.sec1 = sec1
        self.sec2 = sec2
        return sec1, sec2
    
    def getUnwarppedPhase(self):
        sec1, sec2 = self.pickUsefulData()
        data = np.concatenate((sec1, sec2), axis=1)
        data = np.angle(data)
        data = np.unwrap(data)
        return data
    
    def div(self):
        '''
        对CSI数据进行除法处理，得到一组omega值
        '''
        sec1, sec2 = self.pickUsefulData()
        sec1 = self.__div_process(sec1)
        sec2 = self.__div_process(sec2)
        result = np.concatenate((sec1, sec2), axis=1)
        
        return result
    
    def computeDist(self, omega, f):
        '''
        计算距离向量，omega为一维omega向量
        '''
        result = np.zeros(omega.shape)
        result = np.angle(omega) / (-2 * np.pi * f)
        result *= 3e8
        return result
    
    def computeToF(self, omega, f):
        '''
        计算距离向量，omega为一维omega向量
        '''
        result = np.zeros(omega.shape)
        result = np.angle(omega) / (-2 * np.pi * f)
        return result
    
    def convertToSmoothCSI(self, N):
        '''
        将CSI数据转换为smooth矩阵
        '''
        sec1, sec2 = self.pickUsefulData()
        self.N = N
        
        # 初始化smooth矩阵
        num_antennas = sec1.shape[0]  # 假设每一行代表一个天线
        smooth1 = []
        smooth2 = []
        
        for i in range(num_antennas):
            sec1_i = sec1[i, :]
            sec2_i = sec2[i, :]
            
            # 生成smooth矩阵
            smooth1_i = np.zeros((N, sec1_i.shape[0] - N + 1), dtype=complex)
            smooth2_i = np.zeros((N, sec2_i.shape[0] - N + 1), dtype=complex)
            
            # 填充smooth矩阵
            for j in range(sec1_i.shape[0] - N + 1):
                smooth1_i[:, j] = sec1_i[j:j + N]
            for j in range(sec2_i.shape[0] - N + 1):
                smooth2_i[:, j] = sec2_i[j:j + N]
            
            smooth1.append(smooth1_i)
            smooth2.append(smooth2_i)
        
        return np.array(smooth1), np.array(smooth2)
    
    def convertToSmoothCSI_advanced(self, N):
        sec1, sec2 = self.pickUsefulData()
        self.N = N
        dim = self.num_dim
        N_perline = int(N/4)
        
        smooth = np.zeros((N, int((sec1.shape[1]-N_perline+1)*(dim/2+1))), dtype=complex)
        
        x_shape = N_perline
        y_shape = int(dim/2)
        for i in range(y_shape+1):
            for j in range(sec1.shape[1]-N_perline+1):
                smooth[:, (i+1)*(j+1)-1] = sec1[i:i+y_shape,j:j+x_shape].reshape(-1)
        
        return smooth

    
    def buildAlpha(self, N, f):
        '''
        生成alpha函数，构建导矢向量
        '''
        def alpha(tao):
            '''
            接收一个tao值，返回一个长度为N的数组
            '''
            array = np.zeros(N, dtype=complex)
            for i in range(N):
                array[i] = np.exp(-2j * np.pi * i * f * tao)
            return array
        return alpha
    
    def buildAlpha_advanced(self, N, f, d):
        '''
        生成alpha函数，构建导矢向量
        与上一个不同，这个同时考虑了aoa和tof
        f是频率，d是天线间距占波长比例（例如1/2波长， d=1/2）
        dim是天线索引
        '''
        def alpha(theta, tao):
            '''
            接收一个theta和tao值，返回一个N的数组
            '''
            y = int(self.num_dim/2)
            x = int(N/y)
            array = np.zeros((y, x), dtype=complex)
            
            for dim in range(y):
                phi = d * np.sin(theta) * dim
                for i in range(x):
                    array[dim, i] = np.exp(-2j * np.pi * (i * f * tao + phi))
            
            array = array.reshape(-1)
            return array.T
        return alpha
    
    def computE(self, smooth):
        '''
        计算信号子空间E
        '''
        # 计算协方差矩阵
        X = smooth
        X_H = np.conj(X.T)
        R = np.dot(X, X_H)
        
        # 计算特征值和特征向量
        eigval, eigvec = np.linalg.eig(R)
        # print(eigval)
        # print(eigvec)
        
        # 对特征值进行聚类
        eigval = eigval.reshape(-1, 1) # 转换为列向量
        eigval_real = np.abs(eigval)
        kmeans = KMeans(n_clusters=2, random_state=0).fit(eigval_real)
        labels = kmeans.labels_
        # print('E labels:', labels)
        
        # 根据聚类结果提取特征向量
        large_eigvec = eigvec[:, labels == labels.max()]
        small_eigvec = eigvec[:, labels == labels.min()]
        self.Es = large_eigvec
        self.En = small_eigvec
        
        return large_eigvec, small_eigvec
    
    def buildPMUSIC(self, f):
        '''
        生成PMUSIC函数
        '''
        N = self.N
        En = self.En
        def PMUSIC(tao):
            '''
            接收一个tao值，返回一个PMUSIC值
            '''
            a = self.buildAlpha(N, f)(tao)
            a_H = np.conj(a.T)
            P = np.dot(np.dot(np.dot(a_H, En), np.conj(En.T)), a)
            return 1 / np.abs(P)
        return PMUSIC

    def buildPMUSIC_advanced(self, f, d):
        '''
        生成PMUSIC函数，与上一个不同，这个同时考虑了aoa和tof
        '''
        N = self.N
        En = self.En
        def PMUSIC(theta, tao):
            '''
            接收theta和tao值，返回一个PMUSIC值
            '''
            a = self.buildAlpha_advanced(N, f, d)(theta, tao)
            a_H = np.conj(a.T)
            P = np.dot(np.dot(np.dot(a_H, En), np.conj(En.T)), a)
            return 1 / np.abs(P)
        return PMUSIC
        
        
    
    # private funcs
    def __loadData(self, filepath):
        meta = scipy.io.loadmat(filepath)
        if 'CSI' in meta:
            sciMat = np.array(meta['CSI'])
            self.num_dim = sciMat.shape[0]
            self.num_waves = sciMat.shape[1]
        elif 'CSI_LTF1' in meta:
            sciMat = np.array(meta['CSI_LTF1'])
            self.num_dim = sciMat.shape[0]
            self.num_waves = sciMat.shape[1]
            # print(sciMat.shape)
        else:
            raise ValueError(f"failed to load data from {filepath}")
        return sciMat
    
    def __div_process(self, data):
        lenth = data.shape[1]
        result = np.zeros((self.num_dim, lenth-1), dtype=complex)
        for i in range(lenth-1):
            result[:, i] = data[:, i+1] / data[:, i]
        return result