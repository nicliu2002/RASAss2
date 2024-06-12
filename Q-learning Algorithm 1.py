import numpy as np 
import time
import math
import matplotlib.pyplot as plt
from spherov2 import scanner
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.types import Color
import random
import csv


# Defining the different parameters

epsilon = 0.001
max_steps = 100
alpha = 0.01
gamma = 0.95


# Defining environment:

n_states = 36
n_actions = 4
goal_state = 35
start_pos = (0,0)
goal_pos = (5,5)
current_dist = 0
last_dist = 10000
time_step = 0

# initialise Q table with zeroes

qtable_path = "Qtabletest4.csv"
Q_table = np.zeros((n_states,n_actions))

# robot parameters:

ROBOT_ID = "SB-C299"
scaleParam = 25

# observation map:

obsMap = np.zeros((6,6))
currentPosX = 0
currentPosY = 0

# Defining Actions:

action_list = [(currentPosX, currentPosY+1),
               (currentPosX, currentPosY-1),
               (currentPosX+1, currentPosY),
               (currentPosX-1, currentPosY),
                ]

# Rewards List:

rewards = {"moved" : 0,
           "blocked": -10,
           "closer": 3,
           "further" : -5,
           "goal" : 25,
           }



# start time

start_time = time.time()

def import_Qtable():
    
    global Q_table
    
    try:
        Q_table = np.loadtxt(qtable_path,delimiter=",",dtype = float)
    except:
        print("no qtable import found")
        Q_table = np.zeros((n_states,n_actions))
     
def state_to_index(x, y, grid_size=6):
    return x * grid_size + y

def index_to_state(index, grid_size=6):
    x = index // grid_size
    y = index % grid_size
    return (x, y)

def update_actionList(api):
    
    global action_list
    
    updateCurrentPos(api)
    action_list = [(currentPosX, currentPosY+1),
                   (currentPosX, currentPosY-1),
                   (currentPosX+1, currentPosY),
                   (currentPosX-1, currentPosY),
                   ]
    return

def on_collision():
    print("collided with something....")

def choose_action(state):
    action=0
    if np.random.uniform(0, 1) < epsilon:
        action = random.randint(0,3) # choice for action to choose a random from 1 - 4
    else:
        action = np.argmax(Q_table[state, :])
    return action

def execute_action(action, api):
    
    global current_dist, last_dist
    
    update_actionList(api)
    target_node = action_list[action]
    if 0 <= target_node[0] <= 5  and  0 <= target_node[1] <= 5:
        move_result = moveToNode(api, target_node[0], target_node[1])
        if move_result == "moved":
            updateCurrentPos(api)
            if (currentPosX,currentPosY) == index_to_state(goal_state):
                return rewards["goal"]
            current_dist = get_distance(currentPosX,currentPosY,goal_pos[0],goal_pos[1])
            if current_dist < last_dist:
                last_dist = current_dist
                return rewards["closer"]
            elif current_dist >= last_dist:
                last_dist = current_dist
                return rewards["further"]
        elif move_result == "blocked":
            return rewards["blocked"]
    else:
        return -2 # reward to prevent it from doing erroneous movements
    

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
    
    global currentPosX, currentPosY, obsMap
    
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
        # print("moving location data: X: " + str(progressiveX) + "     Y: " + str(progressiveY) + "   Theta: " + str(theta_error) + "    dist_error: " + str(dist_error))
        # moves until distance error is less than 5
        if dist_error < 3: 
            print("New Current Positions: " + "     X: " + str(progressiveX) + "      Y: " + str(progressiveY))
            api.set_speed(0)
            updateCurrentPos(api)
            return "moved"
            
        if timeCount > 25:
            print("Could not move")
            updateCurrentPos(api)
            obsMap[currentPosX,currentPosY] = 2
            api.set_speed(-65)
            time.sleep(1.5)
            api.set_speed(0)
            return "blocked" # negative reward for moving to a blocked or timed out square
        time.sleep(0.05)
        
#Function to learn the Q-value
def update(state, state2, reward, action, action2):
    print("updating q table: state1: " + str(state) + "      state 2: " + str(state2) + "reward: " + str(reward) )
    predict = Q_table[state, action]
    target = reward + gamma * Q_table[state2, action2]
    Q_table[state, action] = Q_table[state, action] + alpha * (target - predict)


def main():
    
    global qtable_path, time_step
    
    with open("store.txt",'r') as f: #open a file in the same folder
        a = f.readlines()            #read from file to variable a
        
    logStep = int(a[0]) 
    logStep += 1
    log_path = "qlearningLog" + str(logStep) + ".txt" 
    
    with open("store.txt",'w') as f: #open a file in the same folder
        f.write(str(logStep))   
    

    toys = scanner.find_toys(toy_names=[ROBOT_ID])
    with SpheroEduAPI(toys[0]) as droid:
        
        droid.register_event(EventType.on_collision, on_collision)
        droid.set_main_led(Color(255, 255, 255))
        time.sleep(1)
        startTime = time.time()
        
#       plt.ion()
#       fig = plt.figure()
#       ax = fig.add_subplot(111)
#       matrixPlot = ax.imshow(obsMap, cmap = "viridis", norm="linear")
                
        
        log = open(log_path, 'w')
        log.write("time, x, y, action, reward \n")
        import_Qtable()
        moveToNode(droid,start_pos[0],start_pos[1])
        state1 = state_to_index(currentPosX, currentPosY) # starts from 0,0 coords
        action1 = choose_action(state1)

        while state1 != goal_state:     
            data = str(time_step) + ", " + str(currentPosX) + ", " + str(currentPosY) + ", " + str(action1) + ", "               
            reward = execute_action(action1,droid)
            data += str(reward) + "\n"
            log.write(data) 
            updateCurrentPos(droid)
            
            state2 = state_to_index(currentPosX, currentPosY)
            
            if state2 > 35: 
                print("State 2 is larger then the size of the q table: " + str(state2) + "   X: " + str(currentPosX) + "  Y: " + str(currentPosY))                
            
            action2 = choose_action(state2)                                 
            
            update(state1, state2, reward, action1, action2)

            state1 = state2
            
            action1 = action2
                        
            print(str(Q_table))
            np.savetxt(qtable_path,Q_table,delimiter = ",")
            time_step += 1
            
        print("Epoch finished with time: " + str(time.time()-start_time) + "    in " + str(time_step) + " steps")
            
                                
                
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        np.savetxt(qtable_path,Q_table,delimiter = ",")
        print("Q table saved to: " + qtable_path)
        
        