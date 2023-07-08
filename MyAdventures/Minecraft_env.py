import gym 
import numpy as np 
import pygetwindow
import pyautogui
import cv2 
from gym import spaces 
from Keyboard_controller import KeyboardAction
from mcpi.minecraft import Minecraft
import random

class MinecraftEnv(gym.Env):
    
    def __init__(self,verbose=False):
        self.verbose  = verbose
        self.window_title = "Minecraft 1.12"
        self.keyboard_controller = KeyboardAction(self.window_title)
        current_position_dim = 3
        goal_position_dim = 2
        pixels_dim = 1200
        current_position_space = spaces.Box(low=-1500, high=1500, shape=(current_position_dim,), dtype=float)
        goal_position_space = spaces.Box(low=-1500, high=1500, shape=(goal_position_dim,), dtype=float)
        pixels_space = spaces.Box(low=0, high=250, shape=(pixels_dim,), dtype=float)

        self.observation_space = spaces.Dict({"current_position": current_position_space,"goal_position": goal_position_space,"pixels": pixels_space})
        self.action_space =  spaces.Discrete(5)
        self.minecraft_server = Minecraft.create()
        self.initial_postion = self.minecraft_server.player.getPos()
        #print(self.initial_postion.x)
        #print(self.initial_postion.z)
        self.episode = 40
        self.current_step = 0
        self.reset()
        
    
    def create_goal(self):
        rand_x = random.randint(-850, -750)
        rand_z = random.randint(30, 100)
        return rand_x, rand_z

    def reset(self): 
        self.initialx = -808
        self.initialy = 81
        self.initialz = 60
        self.current_step = 0 
        self.xgoal,self.zgoal = self.create_goal()

        if self.verbose:
            print("Goal Position:", self.xgoal,",",self.zgoal)

        self.minecraft_server.player.setPos(self.initialx,self.initialy,self.initialz)
        self.current_position = self.minecraft_server.player.getPos()
        self.pixels = self.get_screeshot() 
        observation = {
        "current_position": np.array([self.current_position.x, self.current_position.y, self.current_position.z]),
        "goal_position": np.array([self.xgoal, self.zgoal]),
        "pixels": np.array(self.pixels)
        }
        return observation

    
    def step(self, action):
        if  action == 0:
            self.keyboard_controller.forward()
        elif action == 1:
            self.keyboard_controller.backward()
        elif action == 2:
            self.keyboard_controller.right()
        elif action == 3:
            self.keyboard_controller.left()
        elif action == 4:
            self.keyboard_controller.sprint_jump_forward()
        
        self.pixels = self.get_screeshot()
        self.current_position = self.minecraft_server.player.getPos()

        reward = self.get_reward(self.current_position)

        observation = {
        "current_position": np.array([self.current_position.x, self.current_position.y, self.current_position.z]),
        "goal_position": np.array([self.xgoal, self.zgoal]),
        "pixels": np.array(self.pixels)
        }

        if reward == 1:
            done = True
            self.reset()
        elif self.current_step >= self.episode:
            done = True
            self.reset()
        else:
            self.current_step+=1
            done = False
        info =  {}
        return observation, reward, done, info

    def get_screeshot(self):
            minecraft_window =  pygetwindow.getWindowsWithTitle(self.window_title)[0]

            new_width = 20
            new_height = 20

            left, top, width, height = minecraft_window.left, minecraft_window.top, minecraft_window.width, minecraft_window.height
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            pixel_array = np.array(screenshot)
            pixel_array = cv2.resize(pixel_array, (new_width, new_height))
            pixel_array = pixel_array.flatten()
            #print("min ", np.min(pixel_array))
            #print("max ", np.max(pixel_array))
            #print("length ", len(pixel_array))
            return pixel_array
    
    def get_reward(self,current_position):
        if (abs(current_position.x - self.xgoal) <= 2) and (abs(current_position.z - self.zgoal) <= 2):
            return 1
        elif (abs(current_position.x - self.xgoal) <= 2) or (abs(current_position.z - self.zgoal) <= 2):
            return 0.5
        else:
            return 0
        

    def close(self):
        pass

    def render(self):
        pass


