import gym


env = gym.make("ALE/Asteroids-v5", render_mode="human", obs_type="grayscale")
state = env.reset()


for y in range(2000):
    env.render()
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
