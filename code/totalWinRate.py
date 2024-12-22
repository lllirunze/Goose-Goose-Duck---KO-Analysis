import pandas as pd

# Load the dataset to examine its structure
file_path = 'data/data - Sheet1.csv'
data = pd.read_csv(file_path)

# Mapping of roles to categories
duck_roles = {"鸭子", "间谍", "专业杀手", "刺客", "告密者", "静语者", "派对狂", "爆炸王", "身份窃贼", "忍者", "连环杀手", "小丑", "食鸟鸭", "丧葬者", "传教士", "超能力者"}
goose_roles = {"鹅", "肉汁", "通灵者", "正义使者", "警长", "加拿大鹅", "工程师", "模仿者", "侦探", "观鸟者", "政治家", "锁匠", "殡仪员", "网红", "冒险家", "复仇者", "星界行者", "说客", "生存主义者", "跟踪者", "预言家", "科学家", "流浪儿童", "追踪者"}

# Function to calculate the win rate for each player based on their selected role and the winner
def calculate_win_rate_updated(player):
    player_data = data[['胜方', player]].dropna()  # Exclude NaN rows (non-participating rounds)
    total_rounds = len(player_data)
    
    if total_rounds == 0:
        return 0, 0, 0  # If the player did not participate in any rounds
    
    wins = 0
    for _, row in player_data.iterrows():
        selected_role = row[player]
        winner = row['胜方']

        if winner == '鹅' and selected_role in goose_roles:
            wins += 1
        elif winner == '鸭子' and selected_role in duck_roles:
            wins += 1
        elif selected_role == winner:
            wins += 1
    
    # print("{}: {} ({}/{})".format(player, wins / total_rounds, wins, total_rounds))
    win_rate = wins / total_rounds
    return round(win_rate, 3), wins, total_rounds

# List to store the results
results = []

players = data.columns
for player in players[2: -1]:
    # calculate_win_rate_updated(player)
    win_rate, wins, total_rounds = calculate_win_rate_updated(player)
    results.append([player, win_rate, wins, total_rounds])

# Create a DataFrame from the results
win_rate_df = pd.DataFrame(results, columns=["玩家", "总胜率", "胜场", "总场数"])
# win_rate_df = pd.DataFrame(results, columns=["玩家", "总胜率", "胜场", "总场数", "带刀好人胜率", "普通好人胜率", "中立胜率", "鸭子胜率"])

# Sort the DataFrame by 'Win Rate' in descending order
win_rate_df_sorted = win_rate_df.sort_values(by="总胜率", ascending=False)

# Iterate through the sorted DataFrame and print each row as markdown table format
print("## 总胜率")
print()
print("| 玩家 | 总胜率 | 胜场 | 总场数 |")
print("|:-----:|:-----:|:-----:|:-----:|")
for index, row in win_rate_df_sorted.iterrows():
    print(f"| {row['玩家']} | {row['总胜率']} | {row['胜场']} | {row['总场数']} |")