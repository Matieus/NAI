"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/NAI/
    Mateusz Olstowski: https://github.com/Matieus/NAI/


    
    
In ".../site-packages/rl/callbacks.py" change

from tensorflow.keras import __version__ as KERAS_VERSION

to

from keras import __version__ as KERAS_VERSION    

./env/lib/site-packages/rl/util.py#L86 -> _name to name

"""

import gym
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam


from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory


env = gym.make("ALE/Asteroids-v5", render_mode="human", obs_type="grayscale")
states = env.observation_space.shape[0]
actions = env.action_space.n
state = env.reset()

print(states, actions)

model = Sequential()
model.add(Flatten(input_shape=(1, states)))  # Poprawka w tej linii
model.add(Dense(32, activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(actions, activation="linear"))

agent = DQNAgent(
    model,
    memory=SequentialMemory(limit=50_000, window_length=1),
    policy=BoltzmannQPolicy(),
    nb_actions=actions,
    nb_steps_warmup=10,
    target_model_update=0.01,
)


agent.compile(Adam(lr=0.001), metrics=["mae"])
agent.fit(env, nb_steps=100_000, visualize=False, verbose=1)

results = agent.test(env, nb_episodes=10, visualize=True)
print(np.mean(results.history["episode_reward"]))

env.close()


"""for y in range(2000):
    env.render()
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
"""
