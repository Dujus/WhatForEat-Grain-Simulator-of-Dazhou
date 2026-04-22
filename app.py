import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
c_img_path = os.path.join(os.path.dirname(__file__), "image", "吃什么.jpg")
# 设置页面配置
st.set_page_config(page_title="《大周列国志》粮食结余模拟器", layout="wide")

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False # 中文显示


# 我用的核心算法，在main.py中也可见
def calculate_tax(t, params):
    # 农田随时间的变化
    farm = params['farm_base'] + params['rate_of_c'] * t


    X = params['pop_ratio']
    if X < 1:
        Y = 0.5 + 0.5 * X
    else:
        Y = 2.5 - (1.5 / X)

    # 综合税收公式
    tax_val = (farm * params['tax_rate'] * params['tan_factor'] * (1 + params['irrigation']) * Y * (
                1 + params['profit']) * (1 - params['disorder']) * (1 + params['stability']) * (
                           1 + params['expansion']) * params['yield_rate'] / 100 +
               params['donations'])
    return tax_val


# Streamlit 界面侧边栏，进行参数输入
st.sidebar.header("存档参数配置")
st.sidebar.text('注意，在这里粮食的’单位‘是万，其中涉及到的直接加减粮食的参数（如属国贡赋）需换算为万。百分比加成参数则直接输入加成即可。')
with st.sidebar.expander("农业产出参数", expanded=True):
    farm_base = st.number_input("当前基础农田 (注意填’农田‘原数值即可，不用换算)", value=60000)
    rate_of_c = st.number_input("农田年变化（由玩家估计，正、负和0均可）", value=60)
    yield_rate = st.slider("粮种质量 (亩产)", 1.0, 5.0, 2.09)
    expansion = st.slider("粮食产量 (温暖期算在这里)", 0.0, 2.0, 1.225)
    profit = st.number_input("地利加成，即各个地形加成乘以各形所占比例。详见taptap解释", value=2.45)

with st.sidebar.expander(" 人口与政策参数", expanded=True):
    pop_ratio = st.number_input("庶民人口与所需农人之比 (X)", value=2.85)
    tax_rate = st.slider("基础税率", 0.0, 1.0, 0.1)# 使用滑块功能实现
    tan_factor = st.selectbox("国君心性加成 (是否为贪？)", [1.0, 1.3], index=1)
    stability = st.number_input("财政收入", value=0.1)
    irrigation = st.slider("水利等级加成", 0, 1, 1)
    disorder = st.slider("骚乱度 (扣减)", 0.0, 1.0, 0.0)
    donations = st.number_input("属国贡赋和士绅献粮 (万)", value=1020)

with st.sidebar.expander("仓储与消耗", expanded=True):
    initial_food = st.number_input("当前总粮食 (万)", value=11400)
    capacity = st.number_input("仓库理论总量 (万)", value=3324)
    consumption = st.number_input("年预计总消耗 (万)（由玩家估计1年内平均消耗及年终结算）", value=1500)
    corruption_rate = st.slider("仓储腐败率", 0.0, 1.0, 0.54)
    years = st.slider("模拟年限", 3, 200, 120)

    with st.sidebar.expander("目标监测", expanded=False):
        target_value = st.number_input("设定预期目标 (万)", value=15000.0)

# 主界面显示
st.title("吃什么：《大周列国志》动态粮食与财政模拟器")

left_po, cent_po, right_po = st.columns([2, 3, 1])

with cent_po:
    st.image(c_img_path)
with st.expander("查看模拟公式", expanded=False):
    st.write("本模拟器基于以下公式：")

    # 显示税收公式
    st.latex(r'''
    Tax_{t} = \frac{Farm_{t} \cdot Rate \cdot Tan \cdot (1+Irr) \cdot Y \cdot (1+Profit) \cdot (1-Dis) \cdot (1+Stab) \cdot (1+Exp) \cdot Yield}{100} + Donation
    ''')
    st.write("Farm为农田，Rate为税率，'Tan‘为国君心性，profit为地利，Dis为骚乱，Stab为’财政加成‘，Exp为’粮食产量‘，yield为粮种。")

    st.write("其中，人口与所需农人之比： $Y$ 采用：")
    st.latex(r'''
    Y = \begin{cases} 
    0.5 + 0.5X & \text{if } X < 1 \\
    2.5 - \frac{1.5}{X} & \text{if } X \geq 1 
    \end{cases}
    ''')

    st.info("更新后的腐败我计算的有些简单粗暴，只分出了不满库和满库的情况。所以可能更适合中后期的宏观模拟：中后期粮食普遍多，满仓常见")
st.markdown("---")

# 运行模拟逻辑
params = {
    'farm_base': farm_base, 'rate_of_c': rate_of_c, 'yield_rate': yield_rate,
    'expansion': expansion, 'profit': profit, 'pop_ratio': pop_ratio,
    'tax_rate': tax_rate, 'tan_factor': tan_factor, 'stability': stability,
    'irrigation': irrigation, 'disorder': disorder, 'donations': donations
}

food_history = [initial_food]
times = list(range(years + 1))
n = initial_food

for t in range(1, years + 1):
    m = n if n <= capacity else capacity  # 倘若说总量比理论可存储量小，就替换。这很简单粗暴，但没有办法细化之。
    n = n - ((n - m) * corruption_rate) - consumption + calculate_tax(t, params) # 原公式在main.py在更清楚看到
    food_history.append(n)

# 结果展示
col1, col2 = st.columns(2)
with col1:
    st.metric("第一年预期税收", f"{round(calculate_tax(0, params), 2)} 万")
    st.metric("预测峰值储粮", f"{round(max(food_history), 2)} 万")

with col2:
    st.metric("预测最低储粮", f"{round(min(food_history), 2)} 万")
    st.metric("最终年度结余", f"{round(food_history[-1], 2)} 万")

# 绘图逻辑
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(times, food_history, color='#e67e22', linewidth=2, label="储粮趋势")
ax.fill_between(times, food_history, alpha=0.2, color='#e67e22')

# 添加预定值的横线
ax.axhline(y=target_value, color='red', linestyle='--', alpha=0.7, label=f"目标值: {target_value}万")

# 找到第一个大于或等于目标值的索引
food_array = np.array(food_history)
# 针对上升趋势找第一个达标点，或者针对下降趋势找第一个'跌出’的点
if target_value > initial_food:
    idx = np.where(food_array >= target_value)[0]
else:
    idx = np.where(food_array <= target_value)[0]

if len(idx) > 0:
    first_hit_year = idx[0]
    # 在图表上标出那个点
    ax.plot(first_hit_year, food_history[first_hit_year], "ro")
    ax.annotate(f"第 {first_hit_year} 年达标",
                xy=(first_hit_year, food_history[first_hit_year]),
                xytext=(first_hit_year + 5, food_history[first_hit_year] + (max(food_history) * 0.05)),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))


ax.set_xlabel("年份")
ax.set_ylabel("储粮总量 (万)")
ax.set_title("未来储粮变动趋势及目标监测")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.4)
st.pyplot(fig)