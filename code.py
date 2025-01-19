import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 加载角色数据
roles_path = 'data/roles.json'
with open(roles_path, 'r', encoding='utf-8') as roles_file:
    roles = json.load(roles_file)

duck_roles = set(roles["duck_roles"])
goose_roles = set(roles["goose_roles"])

# Function to calculate the win rate for each player based on their selected role and the winner
def calculate_win_rate_curve(player):
    player_data = data[["time", '胜方', player]]
    player_data['time'] = pd.to_datetime(player_data['time'])  # 转换为日期时间格式
    player_data['day'] = player_data['time'].dt.date          # 提取日期部分

    total_rounds = 0
    wins = 0
    date = str(player_data.iloc[0]['day'])

    winRateCurve = []
    winsCurve = []
    totalCurve = []

    for _, row in player_data.iterrows():
        selected_role = row[player]
        winner = row['胜方']
        today = str(row['day'])

        if today != date:
            if total_rounds == 0:
                winRateCurve.append(0)
            else:
                winRateCurve.append(wins / total_rounds)
            date = today

        if pd.isna(selected_role):
            continue

        if winner == '鹅' and selected_role in goose_roles:
            wins += 1
        elif winner == '鸭子' and selected_role in duck_roles:
            wins += 1
        elif selected_role == winner:
            wins += 1
        total_rounds += 1

    if total_rounds == 0:
        winRateCurve.append(0)
    else:
        winRateCurve.append(wins / total_rounds)

    return winRateCurve

# 加载数据
file_path = 'data/data - Sheet1.csv'
data = pd.read_csv(file_path)

# 获取日期列表
days = sorted(pd.to_datetime(data['time']).dt.date.unique())  # 确保日期按时间排序
players = data.columns[2:-1]  # 去掉非玩家列

# 创建动画
fig, ax = plt.subplots(figsize=(20, 12))
num_lines = len(players)
colors = plt.cm.get_cmap('tab20', num_lines)  # 使用 'tab20' 调色盘
lines = {player: ax.plot([], [], marker='o', linestyle='-', label=player, color=colors(i))[0] for i, player in enumerate(players)}

def init():
    """初始化动画，清空所有曲线"""
    ax.set_xlim(days[0], days[-1])
    ax.set_ylim(0, 0.6)
    ax.set_xlabel('Days', fontsize=14)
    ax.set_ylabel('Win Rate', fontsize=14)
    ax.legend(fontsize=12)
    return list(lines.values())

def update(frame):
    """更新动画帧"""
    current_day = days[:frame + 1]
    for player, line in lines.items():
        win_rate = calculate_win_rate_curve(player)[:frame + 1]
        line.set_data(current_day, win_rate)
    return list(lines.values())

ani = FuncAnimation(fig, update, frames=len(days), init_func=init, blit=True, interval=200)

# 保存或展示动画
ani.save("image/winCurve.gif", writer='pillow')  # 保存为 GIF
# plt.show()