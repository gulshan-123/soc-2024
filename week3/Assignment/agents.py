from bandits import Bandit
import numpy as np
np.random.seed(123)
# Import libraries if you need them

class Agent:
    def __init__(self, bandit: Bandit) -> None:
        self.bandit = bandit
        self.banditN = bandit.getN()

        self.rewards = 0
        self.numiters = 0
    

    def action(self) -> int:
        '''This function returns which action is to be taken. It must be implemented in the subclasses.'''
        raise NotImplementedError()

    def update(self, choice : int, reward : int) -> None:
        '''This function updates all member variables you may require. It must be implemented in the subclasses.'''
        raise NotImplementedError()

    # dont edit this function
    def act(self) -> int:
        choice = self.action()
        reward = self.bandit.choose(choice)

        self.rewards += reward
        self.numiters += 1

        self.update(choice,reward)
        return reward
    def getQN(self):
        return self.Q, self.N

class GreedyAgent(Agent):
    def __init__(self, bandits: Bandit) -> None:
        super().__init__(bandits)
        self.Q = np.zeros((bandits.getN()), dtype=np.float64) # Q-values
        self.N = np.zeros((bandits.getN()), dtype=int) # counts for each action

        # Arrays to store Q-values, returns, and actions for each episode
        # self.Qe = np.empty((n_episodes, bandits.getN()), dtype=np.float64)
        # self.returns = np.empty(n_episodes, dtype=np.float64)
        # self.actions = np.empty(n_episodes, dtype=int)
        # name = 'Greedy Agent'
        
    # implement
    def action(self) -> int:
        return np.argmax(self.Q)

    # implement
    def update(self, choice: int, reward: int) -> None:
        action=choice
        self.N[action] += 1
        self.Q[action] += (reward - self.Q[action])/self.N[action]
    
    def getQN(self):
        return self.Q, self.N

class epsGreedyAgent(Agent):
    def __init__(self, bandits: Bandit, epsilon=0.01) -> None:
        super().__init__(bandits)
        self.epsilon = epsilon
        self.Q = np.zeros((bandits.getN()), dtype=np.float64) # Q-values
        self.N = np.zeros((bandits.getN()), dtype=int) # counts for each action
    
    # implement
    def action(self) -> int:
        if np.random.uniform() > self.epsilon:
            return np.argmax(self.Q)
        else:
            return np.random.randint(len(self.Q))

    # implement
    def update(self, choice: int, reward: int) -> None:
        action =choice
        self.N[action] += 1
        self.Q[action] += (reward - self.Q[action])/self.N[action]

class UCBAAgent(Agent):
    def __init__(self, bandits: Bandit, c=2.0) -> None:
        super().__init__(bandits)
        self.c = c
        self.Q = np.zeros((bandits.getN()), dtype=np.float64) # Q-values
        self.N = np.zeros((bandits.getN()), dtype=int) # counts for each action
        # add any member variables you may require

    # implement
    def action(self, e: int) -> int:
        
        return e if e < len(self.Q) else np.argmax(self.Q + self.c * np.sqrt(np.log(e)/self.N))

    # implement
    def update(self, choice: int, reward: int) -> None:
        action =choice
        self.N[action] += 1
        self.Q[action] += (reward - self.Q[action])/self.N[action]

class GradientBanditAgent(Agent):
    def __init__(self, bandits: Bandit, alpha=0.01) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        self.Q = np.zeros(bandits.getN(), dtype=np.float64)  # Preferences
        self.N = np.zeros((bandits.getN()), dtype=int)
        self.probs = np.ones(bandits.getN(), dtype=np.float64) / bandits.getN()  # Initial equal probability
        self.average_reward = 0.0  # Average reward initialization
        self.t = 0  # Time step counter

    def action(self) -> int:
        exp_Q = np.exp(self.Q - np.max(self.Q))
        self.probs = exp_Q / np.sum(exp_Q)
        return np.random.choice(np.arange(len(self.probs)), p=self.probs)

    def update(self, choice: int, reward: int) -> None:
        self.t += 1
        self.average_reward += (reward - self.average_reward) / self.t
        baseline = self.average_reward
        one_hot = np.zeros_like(self.Q)
        one_hot[choice] = 1
        self.Q += self.alpha * (reward - baseline) * (one_hot - self.probs)
        self.N[choice] += 1

class ThompsonSamplerAgent(Agent):
    def __init__(self, bandits: Bandit, alpha=1, beta=0) -> None:
        super().__init__(bandits)
        self.Q = np.zeros((bandits.getN()), dtype=np.float64) # Q-values
        self.N = np.zeros((bandits.getN()), dtype=int) # counts for each action
        self.alpha = alpha
        self.beta = beta

    # implement
    def action(self) -> int:
        samples = np.random.normal(loc=self.Q, scale=self.alpha / (np.sqrt(self.N) + self.beta))
        return np.argmax(samples)

    # implement
    def update(self, choice: int, reward: int) -> None:
        action = choice
        self.N[action] += 1
        self.Q[action] += (reward - self.Q[action]) / self.N[action]

# Implement other subclasses if you want to try other strategies