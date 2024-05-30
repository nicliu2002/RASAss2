import numpy as np 
import time
import math
import matplotlib.pyplot as plt
from spherov2 import scanner
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.types import Color
import random

#Defining the different parameters

epsilon = 0.9
epochs = 10000
max_steps = 100
alpha = 0.85
gamma = 0.95


# Defining environment:

n_states = 25
n_actions = 4
goal_state = 24

# initialise Q table with zeroes

Q_table = np.zeros((n_states, n_actions))

# robot parameters:

ROBOT_ID = ""
scaleParam = 25


# start time

start_time = time.time()

def on_collision():
    print("collided with something....")

def choose_action(state):
    action=0
    if np.random.uniform(0, 1) < epsilon:
        action = Q_table # i have no idea what to do here, ill have to figure it out
    else:
        action = np.argmax(Q_table[state, :])
    return action

def execute_action(action):
    pass   

# updates the current position on matrix based on x, y coordinate 

def updateCurrentPos(api):
    global currentPosX, currentPosY
    
    currentPosX = round(api.get_location()['x']/scaleParam)
    currentPosY = round(api.get_location()['y']/scaleParam)

# get distance function for moving to node

def get_distance(x1, y1, x2, y2):
	return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

# moving to node control function

def moveToNode(api,nodeX,nodeY):
    
    global currentPosX, currentPosY, currentDirection, obsMap

    updateCurrentPos(api)
    timeCount = 0
    x = api.get_location()['x']
    y = api.get_location()['y']
    theta = api.get_heading()
    print("current location data: X: " + str(x) + "     Y: " + str(y) + "     Theta: " + str(theta))
    target_x = scaleParam*nodeX 
    target_y = scaleParam*nodeY
    print("target data is:      target x: " + str(target_x) + "     target y: " + str(target_y))
    dist_error = get_distance(x, y, target_x, target_y) 
    while dist_error >= 2:
        timeCount += 1
        progressiveX = api.get_location()['x']
        progressiveY = api.get_location()['y']            
        dist_error = get_distance(progressiveX, progressiveY, target_x, target_y)
        theta_error = 180*math.atan2(target_x-progressiveX, target_y-progressiveY)/math.pi
        api.set_heading(int(theta_error))
        time.sleep(0.01)
        api.set_speed(35)	
        print("moving location data: X: " + str(progressiveX) + "     Y: " + str(progressiveY) + "   Theta: " + str(theta_error) + "    dist_error: " + str(dist_error))
        # moves until distance error is less than 5
        if dist_error < 3: 
            print("New Current Positions: " + "     X: " + str(progressiveX) + "      Y: " + str(progressiveY))
            api.set_speed(0)
            updateCurrentPos(api)
            obsMap[currentPosX,currentPosY] = 1
            return
        if timeCount > 25:
            print("Could not move")
            updateCurrentPos(api)
            obsMap[currentPosX,currentPosY] = 2
            currentDirection = random.randint(0,3)
            api.set_speed(-65)
            time.sleep(1.5)
            api.set_speed(0)
            return
        time.sleep(0.05)

#Function to learn the Q-value
def update(state, state2, reward, action, action2):
    predict = Q_table[state, action]
    target = reward + gamma * Q_table[state2, action2]
    Q_table[state, action] = Q_table[state, action] + alpha * (target - predict)


def get_state():
    # get the current state of the robot
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
            
            current_state = np.random.randint(0,n_states) # start from a random state/start state
            current_action = choose_action(current_state)
            start_time = time.time()
            run_time = time.time() - start_time()

            while current_state != goal_state and run_time < 10000:
                execute_action(current_action)
                
                
                
                
                
    
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')