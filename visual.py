import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

config = {
            "font.family": ['Times New Roman', 'STZhongsong'],
            "font.size": 12,
            "mathtext.fontset": 'stix',
            'axes.unicode_minus': False
        }
rcParams.update(config)

class pic():
    def __init__(self, title,figsize=(8, 6)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        plt.ion()
        self.refreshTime = 0.1
        self.title = title
        self.ax.grid()
        self.height = [-1, 1]
        self.width = [-1, 1]

        # 设置标题位置在图下方，使用相对大小调整
        relative_position = 0.08  # 相对于底部的相对位置
        self.fig.subplots_adjust(bottom=relative_position + 0.1)  # 增加图形底部空白区域
        self.fig.text(0.5, relative_position, self.title, ha='center', va='center', fontsize=14)
        
    def set_labels(self, xlabel=None, ylabel=None):
        '''
        设置坐标轴标签
        '''
        if xlabel:
            self.ax.set_xlabel(xlabel)
        if ylabel:
            self.ax.set_ylabel(ylabel)
    
    def drawData(self, datax=-1, data=None, color='tab:blue', linewidth=2, linestyle='-', marker=None, markersize=6, label=None):
        """
        绘制数据，并指定线条颜色、宽度、线型、标记点、标记点大小和图例标签。

        参数：
        - datax: X轴数据（可选），如果为 -1 则自动生成。
        - data: Y轴数据，必须提供。
        - color: 线条颜色，默认为 'tab:blue'。
        - linewidth: 线条宽度，默认为 2。
        - linestyle: 线条样式，默认为实线 ('-')。可以是 '--' (虚线)、':' (点线) 等。
        - marker: 标记点样式，默认为 None。可以设置为 'o', 'x', '^' 等。
        - markersize: 标记点大小，默认为 6。
        - label: 图例标签，默认为 None。用于显示图例。
        """
        if data is None:
            raise ValueError("参数 'data' 不能为 None")
        
        if np.all(datax == -1):
            datax = np.linspace(0, data.shape[0] - 1, data.shape[0])
        
        self.ax.plot(datax, data, color=color, linewidth=linewidth, linestyle=linestyle, marker=marker, markersize=markersize, label=label)
        self.update()

    def drawScatter(self, point, label=None):
        self.ax.scatter(point[0], point[1], label=label)
        
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
         # 添加图例
        self.ax.legend(loc='best')
        plt.ioff()
        plt.show()