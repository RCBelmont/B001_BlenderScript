import math
import matplotlib.pyplot as plt


def func(n: int, keys: list, width: int):
    retList = []
    refList = []
    for i in range(0, n):
        refList.append(i)
        weight = 0
        dis = 0
        for j in keys:
            dis = abs(j - i)
            weightC = max(width - dis, 0) / width
            weight = max(weightC, weight)
        retList.append(math.pow(weight, 0.5))
    plt.plot(refList, retList)
    plt.show()


if __name__ == '__main__':
    func(100, [10, 20, 25, 65, 90], 5)
