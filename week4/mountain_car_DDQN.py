import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from decay_schedule import decay_schedule
from tqdm import tqdm_notebook as tqdm
np.random.seed(85)
'''
The first task to work with a gym env is to initialise it using gym.make(name_of_env) and reset it using .reset() function. This resets the env to a starting position, with some noise in state. It returns a tuple of the initial state of environment and a dictionary containing info (Not important for the moment).

Just as a environment in RL, you can take action based on current state. This is done using env.step(action), and it returns the following 5 values:

1. Next State: The state the environment transitioned to after taking the step.

2. Reward: Reward received for taking the action

3. Terminated: A boolean which is true if the environment terminated after taking the action. The condition for this termination is provided in the documentation of the environment.

4. Truncated: A boolean which is true if the environment was truncated after taking the action, usually because we cannot run a environment for infinite time, and hence every environment has a truncation period. More details in the documentation

Note: You must call env.reset() after either termination or truncation.

5. Info: A dictionary containing information of env.

The observation space of Mountation Car is an array of two variables: Position of car(x - coordinate) and velocity of cart. 

Three actions are possible, as mentioned in documentation
'''
def double_q_learning(env,
                      gamma=1.0,
                      init_alpha=0.5,
                      min_alpha=0.01,
                      alpha_decay_ratio=0.5,
                      init_epsilon=1.0,
                      min_epsilon=0.1,
                      epsilon_decay_ratio=0.9,
                      n_episodes=30_000):
    nS, nA = env.observation_space.n, env.action_space.n
    pi_track = []
    Q1 = np.zeros((nS, nA), dtype=np.float64)
    Q2 = np.zeros((nS, nA), dtype=np.float64)
    Q_track1 = np.zeros((n_episodes, nS, nA), dtype=np.float64)
    Q_track2 = np.zeros((n_episodes, nS, nA), dtype=np.float64)
    select_action = lambda state, Q, epsilon: np.argmax(Q[state]) \
        if np.random.random() > epsilon \
        else np.random.randint(len(Q[state]))
    alphas = decay_schedule(init_alpha, 
                           min_alpha, 
                           alpha_decay_ratio, 
                           n_episodes)
    epsilons = decay_schedule(init_epsilon, 
                              min_epsilon, 
                              epsilon_decay_ratio, 
                              n_episodes)
    for e in tqdm(range(n_episodes), leave=False):
        state, done = env.reset(), False
        while not done:
            action = select_action(state, (Q1 + Q2)/2, epsilons[e])
            next_state, reward, done, _ = env.step(action)

            if np.random.randint(2):
                argmax_Q1 = np.argmax(Q1[next_state])
                td_target = reward + gamma * Q2[next_state][argmax_Q1] * (not done)
                td_error = td_target - Q1[state][action]
                Q1[state][action] = Q1[state][action] + alphas[e] * td_error
            else:
                argmax_Q2 = np.argmax(Q2[next_state])
                td_target = reward + gamma * Q1[next_state][argmax_Q2] * (not done)
                td_error = td_target - Q2[state][action]
                Q2[state][action] = Q2[state][action] + alphas[e] * td_error
            state = next_state

        Q_track1[e] = Q1
        Q_track2[e] = Q2        
        pi_track.append(np.argmax((Q1 + Q2)/2, axis=1))

    Q = (Q1 + Q2)/2.
    V = np.max(Q, axis=1)    
    pi = lambda s: {s:a for s, a in enumerate(np.argmax(Q, axis=1))}[s]
    return Q, V, pi, (Q_track1 + Q_track2)/2., pi_track

env=gym.make('MountainCar-v0')
Q, V, pi, Q_track, pi_track=double_q_learning(env=env)
np.save('Q.npy',Q)