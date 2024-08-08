import matplotlib.pyplot as plt

class pic():
    def __init__(self, data):
        self.data = data
        self.num = len(data)
        self.fig, self.ax = plt.subplots()
    
    def draw(self):
        self.ax.plot(self.data)
        plt.show()