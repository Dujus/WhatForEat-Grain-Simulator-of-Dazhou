import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体（msyh)
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块问题
def tax(time):
    rate_of_c = 60 # 变化率
    farm = 6*10000+rate_of_c*time
    disorder = 0  # 骚乱
    rate = 0.1  # 征税比例
    expansion = 0.975+0.25  # 粮食产量，温暖期
    yeild_rate = 2.09  # ‘亩产’（即粮种质量）
    profit = 3.6*0.1386 + 2.6*0.1392 + 2.5*0.3423 + 1.9*0.3732 + (-0) * 0.0025  # 地形？
    constellation = 1  # 星象 纳入加成当中。
    Population_benefit = 2   # 人口比例
    X = 839.94/294.04  # 人口与所需农人之比,替代了原来的Population_benefit
    if X < 1:
        Y = 0.5 + 0.5*X
    elif X >= 1:
        Y = 2.5 - (1.5/X)
    irrigation = 1 # 水利
    stability_benefit = 0.15  # include some local officials' efforts # 财政收入及地方杂项加成.
    tan = 1.3  # 0.3是国君’贪‘心性
    donate_of_squires = 1020 #贡赋
    # 1 单位代表1万
    tax = farm*rate*tan*(1+irrigation)*Y*(1+profit)*(1-disorder)*(1+stability_benefit)*(1+expansion)*yeild_rate/100+donate_of_squires
    # print(f'tax is {tax}')

    return tax


def attenuation_withtax(x, m, capacity, years, lower= None,upper = None):

    # x是原储存粮食，y是目标结果，m是粮食中入库的。capacity是库理论上可存储总量。中后期粮食极多通常这两个值基本是一致的。但初期就不一致了。
    n = x
    time = 0
    lower_hit = None
    upper_hit = None
    times = [time]
    food = [n]
    corruption_rate = 0.54
    consumption = 1500 # 消耗量，包括玩家自己估计一年内大约消耗量和年终结算
    print(f"第一年税收约为{tax(0)}")
    '''
    current_civilian_food = 3.92*10000
    civilian_food = [current_civilian_food]
    population = 900
    culture = 1800

    luxury = 300-20000000/(population*10000)+(60-900/(current_civilian_food/population))-culture*0.03-10-(current_civilian_food/(population*100))+2

    current_civilian_food=(tax(time)-90)*9+current_civilian_food-(1+luxury*0.01)*population-2000 # some sold for money, unknown number
    civilian_food.append(current_civilian_food)'''
    for time in range(1, years+1):
        if n <= capacity:
            m = n
        else:
            m = capacity

        n = n - (m * 0 + (n - m) * corruption_rate) - consumption + tax(time)  # 温暖期腐败率亦上升

        times.append(time)
        food.append(n)

        if (lower_hit is None) and (lower is not None) and n <= lower:
            lower_hit = time
            print(f'第一次到达预期低阈值{lower}万是在第{lower_hit}年')
        if (upper_hit is None) and (upper is not None) and n >= upper:
            upper_hit = time
            print(f'第一次到达预期高阈值{upper}万是在第{upper_hit}年')
    if lower_hit is None and lower is not None:
        print('从未到达预期低阈值')
    if upper_hit is None and upper is not None:
        print('从未到达预期高阈值')
    print(f"预测的仓储最大值是{max(food)},最小值是{min(food)}")
    plt.plot(times, food)
    plt.xlabel('Time')
    plt.ylabel('n')
    plt.title('储粮随时间变化 ')
    plt.show()
    return time


d = attenuation_withtax(1.14*10000, 3324, 3324, 120,0, 1.3*10000 )
print(d)
