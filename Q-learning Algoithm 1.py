import numpy as np 
import time
import math
import matplotlib.pyplot as plt
from spherov2 import scanner
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.types import Color
import random

# Define parameters

learning_rate = 0.5
discount_factor = 0.95
exploration_rate = 1.0
exploration_decay = 0.995
min_exploration = 0.01
exploration_prob = 0.2
epochs = 1000


# Defining environment:

n_states = 25
n_actions = 4
goal_state = 24

# initialise Q table with zeroes

Q_table = np.zeros((n_states, n_actions))

# robot parameters:

ROBOT_ID = ""

def get_state():
    # get the current state of the robot
    pass

def take_action(action):
    # execute given action and return new state and reward
    pass

def main():
    
    toys = scanner.find_toys(toy_names=[ROBOT_ID])
    with SpheroEduAPI(toys[0]) as droid:
        
        droid.register_event(EventType.on_collision, on_collision)
        droid.set_main_led(Color(255, 255, 255))
        time.sleep(1)
        startTime = time.time()
        
        # plt.ion()
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # matrixPlot = ax.imshow(obsMap, cmap = "viridis", norm="linear")
        # log = open("alg2log2", 'w')
        # log.write("time, x, y, currentPosX, currentPosY, currentDirection")
        
        for epoch in range(epochs):
            
            current_state = np.random.randint(0,n_states) # start from a random state/start from this explicit state
            
            while current_state != goal_state:
                if np.random.rand() < exploration_prob:
                    pass
                
    
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')