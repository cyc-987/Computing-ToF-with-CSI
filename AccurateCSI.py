import CSIdata
import numpy as np
from scipy.optimize import leastsq

class accurateCSI():
    '''
    处理单条路径的CSI数据，去除IQ不平衡导致的相位偏差
    '''
    def __init__(self, csi: CSIdata.CSIdata):
        self.csi = csi
        
    def processData(self):
        phase = self.csi.getUnwarppedPhase()
        self.phase = phase
        phase_average = np.mean(phase, axis=0)
        self.phase_average = phase_average
        return phase_average
    
    def buildPhaseModel(self, f):
        '''
        建立相位模型，其中f是频率间隔
        '''
        def P(p, x): # p是参数，x是自变量
            tol, xia, xi, epsilon, tof, beta, xb, xscale= p
            numerator = np.sin(2*np.pi*f*xscale*(x-xb)*xi + epsilon)
            denominator = np.cos(2*np.pi*f*xscale*(x-xb)*xi)
            bias = -2*np.pi*f*xscale*(x-xb)*tof + beta
            return tol * (np.arctan(xia * numerator/denominator) + bias)
        return P
    
    def buildErrorFunc(self, P):
        '''
        建立误差函数
        '''
        def error(p, x, y):
            # numerator = denominator = 0
            # x = np.int_(x)
            # for i in range(self.csi.num_dim):
            #     numerator += (self.phase[i,x] - y) ** 2
            #     denominator += (self.phase[i,x] - P(p, x)) ** 2
                
            # return 1 - numerator/denominator
            return abs(P(p, x) - y)
        return error
    
    def estimate(self, f):
        '''
        估计相位模型的参数, f是频率间隔
        返回估计的参数和确定的函数
        '''
        self.processData()
        x = np.linspace(0, self.phase_average.shape[0]-1, self.phase_average.shape[0])
        y = self.phase_average
        initial_guess = [80, 0.512, -0.02, -0.006, -0.02762, -0.5, 122, -0.3]
        paras, ier = leastsq(self.buildErrorFunc(self.buildPhaseModel(f)), initial_guess, args=(x, y), maxfev=30000)
        P = lambda x: self.buildPhaseModel(f)(paras, x)
        
        return paras, P
