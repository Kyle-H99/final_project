import gymnasium as gym
from gymnasium.utils.env_checker import check_env
from .classes.Board import MinesweeperBoard

CHANNELS: int = 10
"""
this will be implemented after we create our board object. it will wrap it.

observation space 
    - the shape is the shape of the input to the CNN. channels x rows x cols
    - each channel is a one-hot encoding. 1 channel for revealed vs unrevealed, 9 more for cell value = 0 - 9
    - action space is an int from M to N. need to convert to a coordinate with divmod()
"""

class Env(gym.Env):
    def __init__(self, rows:int, cols:int, numMines: int) -> None:

        self.Board: MinesweeperBoard = MinesweeperBoard(rows, cols, numMines)

        # spaces
        self.observation_space = gym.spaces.Box(low=0.0, high=1.0, shape=(CHANNELS, rows, cols))
        self.action_space = gym.spaces.Discrete(rows, cols)
        

env = Env(10, 10, 10)

try:
    check_env(env)
    print("Environment passes all checks!")
except Exception as e:
    print(f"Environment has issues: {e}")