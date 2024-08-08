import numpy as np
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
        sec1 = self.data[:, 6:126]
        sec2 = self.data[:, 130:249]
        self.sec1 = sec1
        self.sec2 = sec2
        return sec1, sec2
    
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
        计算tao向量，omega为一维omega向量
        '''
        result = np.zeros(omega.shape)
        result = np.angle(omega) / (-2 * np.pi * f)
        result *= 3e8
        return result
        
    
    # private funcs
    def __loadData(self, filepath):
        meta = scipy.io.loadmat(filepath)
        if 'CSI' in meta:
            sciMat = np.array(meta['CSI'])
            self.num_dim = sciMat.shape[0]
            self.num_waves = sciMat.shape[1]
        else:
            print(f"failed to load data from {filepath}")
        return sciMat
    
    def __div_process(self, data):
        lenth = data.shape[1]
        result = np.zeros((self.num_dim, lenth-1), dtype=complex)
        for i in range(lenth-1):
            result[:, i] = data[:, i+1] / data[:, i]
        return result