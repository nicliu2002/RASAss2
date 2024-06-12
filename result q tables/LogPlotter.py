import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Function to read the log file
def read_log(file_path):
    read_csv = pd.read_csv(file_path)
    print("Data read from CSV:")
    print(read_csv.head())
    print("Column names:")
    print(read_csv.columns)
    return read_csv

# Function to plot the robot's movements with a time step based colour gradient
def plot_movements(log_data):
    # Set up the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xticks(range(7))
    ax.set_yticks(range(7))
    ax.grid(True)
    
    # Normalize the time steps for color mapping
    norm = plt.Normalize(0, len(log_data) - 1)
    cmap = plt.get_cmap('viridis')
    
    # Plot the movements
    for i in range(len(log_data) - 1):
        start = log_data.iloc[i]
        end = log_data.iloc[i + 1]
        color = cmap(norm(i))
        print(f"Plotting arrow from ({start[1]}, {start[2]}) to ({end[1]}, {end[2]}) with color {color}")
        ax.arrow(start[1], start[2], end[1] - start[1], end[2] - start[2], 
                 head_width=0.2, head_length=0.2, fc=color, ec=color)
    
    # Plot the start and end points
    start = log_data.iloc[0]
    end = log_data.iloc[-1]
    ax.plot(start[1], start[2], 'go', markersize=10, label='Start')
    ax.plot(end[1], end[2], 'ro', markersize=10, label='End')
    
    # Label the axes and add legend
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.legend()
    ax.set_title('Robot Movements in 2D Grid')
    
    # Add colorbar for the time steps
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Time Step')
    
    plt.show()

# Main function to execute the script
if __name__ == "__main__":
    log_file_path = r'C:\Users\nicli\Documents\Algorithms for RAS\Assignment 2\qlearningLog3.txt'  # Replace with your log file path
    log_data = read_log(log_file_path)
    plot_movements(log_data)
