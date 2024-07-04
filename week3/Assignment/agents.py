from bandits import Bandit
import numpy as np
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

class GreedyAgent(Agent):
    def __init__(self, bandits: Bandit) -> None:
        super().__init__(bandits)
        self.Q = np.zeros((bandits.getN), dtype=np.float64) # Q-values
        self.N = np.zeros((bandits.getN), dtype=np.int) # counts for each action

        # Arrays to store Q-values, returns, and actions for each episode
        # self.Qe = np.empty((n_episodes, bandits.getN), dtype=np.float64)
        # self.returns = np.empty(n_episodes, dtype=np.float64)
        # self.actions = np.empty(n_episodes, dtype=np.int)
        # name = 'Greedy Agent'
        
    # implement
    def action(self) -> int:
        return np.argmax(self.Q)

    # implement
    def update(self, choice: int, reward: int) -> None:
        action=choice
        self.N[action] += 1
        self.Q[action] += (reward - self.Q[action])/self.N[action]

class epsGreedyAgent(Agent):
    def __init__(self, bandits: Bandit, epsilon : float) -> None:
        super().__init__(bandits)
        self.epsilon = epsilon
        self.Q = np.zeros((bandits.getN), dtype=np.float64) # Q-values
        self.N = np.zeros((bandits.getN), dtype=np.int) # counts for each action
    
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
    def __init__(self, bandits: Bandit, c: float) -> None:
        super().__init__(bandits)
        self.c = c
        self.Q = np.zeros((bandits.getN), dtype=np.float64) # Q-values
        self.N = np.zeros((bandits.getN), dtype=np.int) # counts for each action
        # add any member variables you may require

    # implement
    def action(self, e: int) -> int:
        
        return e if e < len(self.Q) else np.argmax(self.Q + self.c * np.sqrt(np.log(e)/self.n))

    # implement
    def update(self, choice: int, reward: int) -> None:
        action =choice
        self.N[action] += 1
        self.Q[action] += (reward - self.Q[action])/self.N[action]

class GradientBanditAgent(Agent):
    def __init__(self, bandits: Bandit, alpha : float) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        # add any member variables you may require

    # implement
    def action(self) -> int:
        pass

    # implement
    def update(self, choice: int, reward: int) -> None:
        pass

class ThompsonSamplerAgent(Agent):
    def __init__(self, bandits: Bandit) -> None:
        super().__init__(bandits)
        # add any member variables you may require

    # implement
    def action(self) -> int:
        pass

    # implement
    def update(self, choice: int, reward: int) -> None:
        pass

# Implement other subclasses if you want to try other strategies