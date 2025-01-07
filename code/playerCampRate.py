import pandas as pd
import json

# Load the dataset to examine its structure
file_path = 'data/data - Sheet1.csv'
data = pd.read_csv(file_path)

roles_path = 'data/roles.json'
with open(roles_path, 'r', encoding='utf-8') as roles_file:
    roles = json.load(roles_file)

duck_roles = set(roles["duck_roles"])
goose_roles = set(roles["goose_roles"])
knife_roles = set(roles["knife_roles"])

# Mapping of roles to categories
# duck_roles = {"鸭子", "间谍", "专业杀手", "刺客", "告密者", "静语者", "派对狂", "爆炸王", "身份窃贼", "忍者", "连环杀手", "小丑", "食鸟鸭", "丧葬者", "传教士", "超能力者", "雇佣杀手", "变形者"}
# goose_roles = {"鹅", "肉汁", "通灵者", "正义使者", "警长", "加拿大鹅", "工程师", "模仿者", "侦探", "观鸟者", "政治家", "锁匠", "殡仪员", "网红", "冒险家", "复仇者", "星界行者", "说客", "生存主义者", "跟踪者", "预言家", "科学家", "流浪儿童", "追踪者", "保镖"}
# knife_roles = {"鸭子", "间谍", "专业杀手", "刺客", "告密者", "静语者", "派对狂", "爆炸王", "身份窃贼", "忍者", "连环杀手", "正义使者", "警长", "鹈鹕", "猎鹰", "雇佣杀手", "变形者"}

# Function to calculate the win rate for each player based on their selected role and the winner
def calculate_role_rate_updated(player):
    player_data = data[['胜方', player]].dropna()  # Exclude NaN rows (non-participating rounds)
    total_rounds = len(player_data)
    
    if total_rounds == 0:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0  # If the player did not participate in any rounds
    
    geese = 0
    ducks = 0
    knives = 0
    neutrality = 0

    for _, row in player_data.iterrows():
        selected_role = row[player]
        winner = row['胜方']

        if selected_role in goose_roles:
            geese += 1
        elif selected_role in duck_roles:
            ducks += 1
        else:
            neutrality += 1
        
        if selected_role in knife_roles:
            knives += 1

        # if winner == '鹅' and selected_role in goose_roles:
        #     wins += 1
        # elif winner == '鸭子' and selected_role in duck_roles:
        #     wins += 1
        # elif selected_role == winner:
        #     wins += 1
    
    # print("{}: {} ({}/{})".format(player, wins / total_rounds, wins, total_rounds))
    return total_rounds, round(geese/total_rounds, 3), geese, round(ducks/total_rounds, 3), ducks, round(neutrality/total_rounds, 3), neutrality, round(knives/total_rounds, 3), knives 

# List to store the results
results = []

players = data.columns
for player in players[2: -1]:
    # calculate_win_rate_updated(player)
    total, geese_rate, geese, ducks_rate, ducks, neutrality_rate, neutrality, knives_rate, knives = calculate_role_rate_updated(player)
    results.append([player, total, geese_rate, geese, ducks_rate, ducks, neutrality_rate, neutrality, knives_rate, knives])

role_rate_df = pd.DataFrame(results, columns=["玩家", "总场数", "好人概率", "好人数", "狼人概率", "狼人数", "中立概率", "中立数", "带刀概率", "带刀数"])

# Iterate through the sorted DataFrame and print each row as markdown table format
print("## 玩家选中阵营概率")
print()
print("| 玩家 | 好人概率 | 狼人概率 | 中立概率 | 中立及以下概率 | 带刀概率 |")
print("|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|")
for index, row in role_rate_df.iterrows():
    print(f"| {row['玩家']} | {row['好人概率']} ({row['好人数']}/{row['总场数']}) | {row['狼人概率']} ({row['狼人数']}/{row['总场数']}) | {row['中立概率']} ({row['中立数']}/{row['总场数']}) | {round(row['中立概率'] + row['狼人概率'], 3)} ({row['中立数'] + row['狼人数']}/{row['总场数']}) | {row['带刀概率']} ({row['带刀数']}/{row['总场数']}) |")