from TicTacToe import TicTacToe
from Agent import Agent

game = TicTacToe()

agent = Agent(game, 'X',discount_factor = 0.6, episode = 20000)

agent.train_brain_x_byrandom()

agent.play_with_human()
