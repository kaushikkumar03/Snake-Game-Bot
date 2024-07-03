#This is the main executable file

import pygame
import numpy as np
from snake_game import Game
from dqn_agent import DQNAgent


def train_agent(episodes, batch_size):
    env = SnakeGameEnv()
    agent = DQNAgent(env.state_size, env.action_space)

    for e in range(episodes):
        state = env.reset()
        total_reward = 0

        while True:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

            if done:
                print(f"Episode: {e}/{episodes}, Score: {env.game.snake.length}, Total Reward: {total_reward}")
                break

    return agent


def run_trained_agent(agent, episodes=10):
    env = SnakeGameEnv()
    for e in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.act(state, exploit=True)
            state, _, done = env.step(action)
            env.render()
            pygame.time.wait(100)

        print(f"Episode {e + 1} finished with score: {env.game.snake.length}")


class SnakeGameEnv:
    def __init__(self):
        self.game = Game()
        self.action_space = 4  # up, down, left, right
        self.max_snake_length = 18*12  # To constrain state size in _get_state_size
        self.state_size = self._get_state_size()

    def _get_state_size(self):
        # 2 for head position, 2 for apple position, 4 for direction, 2 * max_snake_length for body
        return 8 + (2 * self.max_snake_length)

    def reset(self):
        self.game.reset()
        return self._get_state()

    def get_score(self):
        return self.game.snake.length

    def step(self, action):
        # Map action (0, 1, 2, 3) to game actions
        if action == 0:
            self.game.snake.move_up()
        elif action == 1:
            self.game.snake.move_down()
        elif action == 2:
            self.game.snake.move_left()
        elif action == 3:
            self.game.snake.move_right()

        done = self.game.play()

        reward = 0
        if done:
            reward = -10  # Penalty for losing
        elif Game.is_collision(self.game.snake.x[0], self.game.snake.y[0], self.game.apple.x, self.game.apple.y):
            reward = 10  # Reward for eating apple

        return self._get_state(), reward, done

    def _get_state(self):
        state = [
            self.game.snake.x[0] / 720,  # Normalize head x position
            self.game.snake.y[0] / 480,  # Normalize head y position
            self.game.apple.x / 720,  # Normalize apple x position
            self.game.apple.y / 480,  # Normalize apple y position
        ]
        state.extend(self.game.snake.get_direction_vector())

        # Add snake body positions and pad with zeros
        for i in range(1, self.max_snake_length + 1):
            if i < self.game.snake.length:
                state.extend([self.game.snake.x[i] / 720, self.game.snake.y[i] / 480])
            else:
                state.extend([0, 0])  # Padding for consistent state size

        return np.array(state, dtype=np.float32)  # Updated array type to avoid matrix multiplication error

    def render(self):
        self.game.render_background()
        self.game.snake.draw()
        self.game.apple.draw()
        self.game.display_score()
        pygame.display.flip()


if __name__ == "__main__":
    trained_agent = train_agent(episodes=1000, batch_size=32)
    run_trained_agent(trained_agent)
