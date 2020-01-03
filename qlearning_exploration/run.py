import numpy as np
import random

gamma = 0.8

#For matrices reward and q_matrix columns are in order (U, D, L, R, N)

# here the states are 0, 1, 2, 3 for convenience
# 0 is the startinf state 
# 1 is state to the right of 0
# 2 is the snake-pit state 
# 3 is the treasure(goal state)

reward = np.array([[0, -10, 0, -1, -1],
		 [0, 10, -1, 0, -1],
		 [-1, 0, 0, 10, -1],
		 [-1, 0, -10, 0, 10]])

q_matrix = np.zeros((4,5))

# -1 represent invalid transitions
transition_matrix = np.array([[-1, 2, -1, 1, 0],
			      [-1, 3, 0, -1, 1],
			      [0, -1, -1, 3, 2],
			      [1, -1, 2, -1, 3]])

# for valid actions 
# encode up as 0, down as 1, left as 2, right as 3, no action as 4
# the rows are the states
valid_action = np.array([[1, 3, 4],
			 [1, 2, 4],
			 [0, 3, 4],
			 [0, 2, 4]])

for i in range(10): # 10 episodes
	start_state = 0
	current_state = start_state
	while current_state != 3:
		action = random.choice(valid_action[current_state])
		next_state = transition_matrix[current_state][action]
		future_rewards =[]
		for action_nxt in valid_action[next_state]:
			future_rewards.append(q_matrix[next_state][action_nxt])
		q_state = reward[current_state][action] + gamma*max(future_rewards)
		q_matrix[current_state][action] = q_state
		print(q_matrix)
		print('Q-matrix is updated')
		current_state = next_state
		if current_state == 3:
			print('goal state reached')

print('final q-matrix : ')
print(q_matrix)