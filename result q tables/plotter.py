import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV without headers
<<<<<<< HEAD
q_table_path = r'C:\Users\nicli\Documents\Algorithms for RAS\Assignment 2\result q tables\Qtabletest4result2.csv'
=======
q_table_path = r"C:\Users\nicli\Documents\Algorithms for RAS\Assignment 2\result q tables\Qtabletest4result10.csv"
>>>>>>> e852bafe8163a674c39a012dfbbc3f10e6fede53
q_table = pd.read_csv(q_table_path, header=None)

# Assign columns manually
q_table.columns = ['right', 'left', 'up', 'down']

# Reindex to the 6x6 grid
q_table.index = [(i // 6, i % 6) for i in range(len(q_table))]

# Add the missing state if necessary
if len(q_table) < 36:
    missing_state = pd.DataFrame([[0.0, 0.0, 0.0, 0.0]], columns=q_table.columns)
    q_table = pd.concat([q_table, missing_state], ignore_index=True)
    q_table.index = [(i // 6, i % 6) for i in range(36)]

# Function to plot Q-value heatmaps
def plot_q_value_heatmaps(q_table):
    actions = ['up', 'left', 'down', 'right']
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))

    for i, action in enumerate(actions):
        heatmap_data = np.zeros((6, 6))
        for index, row in q_table.iterrows():
            heatmap_data[index] = row[action]
        
        sns.heatmap(heatmap_data, ax=axes[i], annot=True, cmap='coolwarm', cbar=False)
        axes[i].set_title(f'Q-values for {action}')
        axes[i].invert_yaxis()

    plt.show()

# Function to plot the policy
def plot_policy(q_table):
    policy_arrows = np.zeros((6, 6), dtype=str)
    action_map = {'up': '↑', 'left': '←', 'down': '↓', 'right': '→'}
    
    for index, row in q_table.iterrows():
        best_action = row.idxmax()
        policy_arrows[index] = action_map[best_action]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(np.zeros((6, 6)), annot=policy_arrows, fmt='', cbar=False, cmap='viridis', ax=ax)
    ax.set_title('Optimal Policy')
    ax.invert_yaxis()
    plt.show()

# Plotting the Q-value heatmaps
plot_q_value_heatmaps(q_table)

# Plotting the policy
plot_policy(q_table)
