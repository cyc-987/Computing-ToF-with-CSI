import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

class pic():
    def __init__(self, title):
        self.fig, self.ax = plt.subplots()
        plt.ion()
        self.refreshTime = 0.1
        self.ax.set_title(title)
        self.ax.grid()
        self.height = [-1, 1]
        self.width = [-1, 1]
        
        config = {
            "font.family": ['Times New Roman', 'STZhongsong'],
            "font.size": 12,
            "mathtext.fontset": 'stix',
            'axes.unicode_minus': False
        }
        # rcParams.update(config)
    
    def drawData(self, datax=-1, data=any):
        if np.all(datax == -1):
            datax = np.linspace(0, data.shape[0]-1, data.shape[0])
        self.ax.plot(datax, data)
        self.update()
    
    def drawScatter(self, point):
        self.ax.scatter(point[0], point[1])
        
        annotation = f"{point[0]:.2f}, {point[1]:.2f}"
        self.ax.text(point[0], point[1]+ 0.5, annotation, ha='center', va='bottom')
        self.update()
        
    def drawCircle(self, center, radius):
        circle = plt.Circle(center, radius, fill=False)
        self.drawScatter(center)
        self.ax.add_patch(circle)
        
        x, y = center
        self.height = [min(self.height[0], y - radius - 1), max(self.height[1], y + radius + 1)]
        self.width = [min(self.width[0], x - radius - 1), max(self.width[1], x + radius + 1)]
        maxrange = max(self.height[1] - self.height[0], self.width[1] - self.width[0])
        self.ax.set_xlim(self.width[0], self.width[0]+maxrange)
        self.ax.set_ylim(self.height[0], self.height[0]+maxrange)
        
        annotation = f"Center: {center}, Radius: {radius:.2f}"
        self.ax.text(x, y + radius + 0.5, annotation, ha='center', va='bottom')
        
        self.update()

    def update(self):
        plt.pause(self.refreshTime)
    def clear(self):
        self.ax.cla()
    def end(self):
        plt.ioff()
        plt.show()