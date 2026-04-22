《大周列国志》粮食结余模拟器

基于游戏内国家财政公式的宏观粮仓推演工具。输入存档数据，获得未来储粮变化曲线及目标值预警。

## ✨ 由来

2024 年底大周曾出现粮食溢出 bug，当时刚学 Python 的我写了个脚本算粮仓何时回落。这堪称是我python编程的’首战‘。如今 bug 早已修了，我把代码重构并做成了这个 Streamlit 可视化模拟器。

⚠️ 注意更适合中后期种田档“观其大略”。

## 🚀 快速上手

👉 [点击打开在线模拟器](https://whatforeat-grain-simulator-of-dazhou-fnsciiuxwdd7fjeu6maamz.streamlit.app/)

左侧输入存档参数，右侧查看趋势图与达标年份。所有粮食单位均为万。关于参数的详细指导，详见taptap https://www.taptap.cn/moment/796128174508344223

## 📁 项目结构

- `streamlit_app.py` —— 网页版主程序
- `main.py` —— Streamlit 化前的原始脚本（可本地运行）
- `image/` —— 页面展示图片

🙇‍致谢

税收公式参考了 @鴥彼飞隼 大佬的攻略《收入计算和城邑特性汇总》，特此感谢。
📜 许可

MIT License
