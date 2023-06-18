# -*- coding: utf-8 -*-
from turtle import left, top, right, bottom
import cv2
import numpy as np
import gym
from gym import spaces
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
import win32gui, win32ui, win32con, win32api
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from typing import Tuple, Any, Dict, Union, Optional, List, Generator, Iterable


def detect_edges(image: np.ndarray, edge_threshold: int) -> np.ndarray:
    """Apply a Canny filter for edge detection"""
    return cv2.Canny(image, edge_threshold, edge_threshold * 2)


class ZeepkistEnv(gym.Env):
    def __init__(self, edge_threshold: int):
        super(ZeepkistEnv, self).__init__()
        self.action_space = spaces.Discrete(4)  # 4 actions: left, right, up, down
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 1), dtype=np.uint8)
        self.edge_threshold = edge_threshold
        self.action_meanings = ["left", "right", "up", "down"]
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.canvas.pack()
        self.image = None
        self.render()
        self.root.update()


    def get_game_state(self) -> np.ndarray:
        """Capture the game screen as an image"""
        game_screen = capture_game_screen()
        return cv2.cvtColor(game_screen, cv2.COLOR_BGR2GRAY)

    def process_game_state(self, game_state: np.ndarray) -> np.ndarray:
        """Process the game state using edge detection"""
        return detect_edges(game_state, self.edge_threshold)

    def reset(self) -> np.ndarray:
        """Reset the environment and return the initial state"""
        game_state = self.get_game_state()
        return self.process_game_state(game_state)

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        """Execute the action in the game and return the next state, reward, and done status"""
        game_state = self.get_game_state()
        processed_state = self.process_game_state(game_state)
        agent_position = get_agent_position(processed_state)
        target_position = get_target_position(processed_state)
        distance_to_target = calculate_distance(agent_position, target_position)
        reward = 1.0 / distance_to_target if distance_to_target > 0 else 0.0
        done = distance_to_target < 10  # Arbitrary threshold for reaching the target
        return processed_state, reward, done, {}

    def render(self, mode="human") -> None:
        """Render the game screen if the 'Render Game' checkbox is checked"""
        if mode == "human" and render_checkbox.var.get():
            game_state = self.get_game_state()
            processed_state = self.process_game_state(game_state)
            img = Image.fromarray(processed_state)
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            if self.image is None:
                self.image = self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            else:
                self.canvas.itemconfig(self.image, image=img_tk)
            self.root.update()

    def close(self) -> None:
        self.root.destroy()


def get_agent_position(processed_state: np.ndarray) -> Optional[Tuple[int, int]]:
    """Return the position of the agent in the processed game state"""
    circles = cv2.HoughCircles(processed_state, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=30)
    return tuple(map(int, circles[0][0][:2])) if circles is not None else None


def get_target_position(processed_state: np.ndarray) -> Optional[Tuple[int, int]]:
    """Return the position of the target in the processed game state"""
    contours = cv2.findContours(processed_state, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if contours:
        contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)
        return x + w//2, y + h//2
    else:
        return None


def calculate_distance(position1: Tuple[int, int], position2: Tuple[int, int]) -> float:
    """Calculate the Euclidean distance between two positions"""
    return np.sqrt((position2[0] - position1[0])**2 + (position2[1] - position1[1])**2)


def grab_screen(region=None):
    #faster screengrab https://pythonprogramming.net/next-steps-python-plays-gta-v/
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


def capture_game_screen() -> np.ndarray:
    """Capture the game screen as an image"""
    screen = grab_screen(region=(left, top, right, bottom))
    return cv2.cvtColor(screen, cv2.COLOR_BGRA2RGB)


def start_training() -> None:
    """Start the RL training loop"""
    learning_rate = float(lr_scale.get()) / 10000
    num_epochs = int(epochs_scale.get())
    edge_threshold = int(edge_threshold_scale.get())
    rl_algorithm = rl_algorithm_var.get()
    env = ZeepkistEnv(edge_threshold=edge_threshold)
    model = PPO("MlpPolicy", env, learning_rate=learning_rate, n_epochs=num_epochs)
    model.learn(total_timesteps=10000)
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    print("Mean reward:", mean_reward, "Std reward:", std_reward)
    
    # Save the trained model to a file
    model.save("trained_model.zip")



root = tk.Tk()

# Learning rate slider
lr_label = tk.Label(root, text="Learning Rate:")
lr_label.grid(row=0, column=0)
lr_scale = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL)
lr_scale.grid(row=0, column=1)

# Number of epochs slider
epochs_label = tk.Label(root, text="Number of Epochs:")
epochs_label.grid(row=1, column=0)
epochs_scale = tk.Scale(root, from_=1, to=500, orient=tk.HORIZONTAL)
epochs_scale.grid(row=1, column=1)

# Edge detection threshold slider
edge_threshold_label = tk.Label(root, text="Edge Detection Threshold:")
edge_threshold_label.grid(row=2, column=0)
edge_threshold_scale = tk.Scale(root, from_=1, to=255, orient=tk.HORIZONTAL)
edge_threshold_scale.grid(row=2, column=1)

# RL algorithm selection dropdown
rl_algorithm_label = tk.Label(root, text="RL Algorithm:")
rl_algorithm_label.grid(row=3, column=0)

rl_algorithm_var = tk.StringVar()
rl_algorithm_dropdown = ttk.Combobox(root, textvariable=rl_algorithm_var, state="readonly")
rl_algorithm_dropdown["values"] = ("PPO", "DQN", "SAC")
rl_algorithm_dropdown.current(0)
rl_algorithm_dropdown.grid(row=3, column=1)

# Add a check box to the GUI
render_checkbox = tk.Checkbutton(root, text="Render Game")
render_checkbox.grid(row=5, column=0, columnspan=2)

# Start training button
train_button = tk.Button(root, text="Start Training", command=start_training)
train_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
