import pandas as pd

# Load the dataset to examine its structure
file_path = 'data/data - Sheet1.csv'
data = pd.read_csv(file_path)

role_results = data['胜方'].value_counts()

# Convert the result into a DataFrame
role_rate_df = role_results.reset_index()

print("## 各阵营胜场")
print()
print("| 阵营 | 胜利次数 |")
print("|:-----:|:-----:|")
for index, row in role_rate_df.iterrows():
    print(f"| {row['index']} | {row['胜方']} |")