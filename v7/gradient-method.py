import numpy as np
from random import randint

def oracle(x, c, V):
	"""
	Oracle function that calculates ||c - sum(x_i * v_i)||^2 for integer x.
	Args:
		x (np.array): Integer vector x.
		c (np.array): Target vector c.
		V (np.array): Matrix whose columns are the v_i vectors.
	Returns:
		float: Value of ||c - sum(x_i * v_i)||^2.
	"""
	residual = c - V @ x  # Compute c - sum(x_i * v_i)
	return np.dot(residual, residual)  # Return squared norm


def gradient_descent_with_oracle(c, V, 
			max_iter=1000, 
			alpha=1, 
			alpha_decay=0.1, 
			alpha_increase=1.1):
	"""
	Performs gradient descent with an Oracle that only accepts integer x values.
	Args:
		c (np.array): Target vector c.
		V (np.array): Matrix whose columns are the v_i vectors.
		max_iter (int): Maximum number of iterations.
		alpha (float): Step size for the gradient descent.
	Returns:
		np.array: Optimal integer vector x.
	"""
	n = V.shape[1]  # Number of correctional vectors
	x = np.zeros(n, dtype=np.float64)  # Start with an integer zero vector

	for iteration in range(max_iter):
		gradient = np.zeros(n, dtype=np.float64)  # Initialize gradient

		# Estimate the gradient numerically
		for i in range(n):
			x_plus = x.copy()
			x_minus = x.copy()
			x_plus[i] += 1
			x_minus[i] -= 1

			# Query the Oracle for the finite difference approximation
			grad_estimate = (oracle(x_plus, c, V) - oracle(x_minus, c, V)) / 2
			gradient[i] = grad_estimate

		# Update x using the gradient
		x_new = np.round(x - alpha * gradient)
		if oracle(x, c, V) < oracle(x_new, c, V):
			# dann ist man sicher darüber gegangen, alpha zu gross
			alpha *= alpha_decay
		else:
			# ein bisschen erhöhen wieder
			alpha *= alpha_increase
			# Terminate if gradient is zero (convergence)
			if np.all(np.abs(x - x_new) < 1e-6):
				break

			# neues x setzen
			x = x_new

		# Optional: Print progress
		#print(f"Iteration {iteration + 1}: x = {x}, Oracle value = {oracle(x, c, V)})")

	print(f"Gradient descent found solution within {iteration} rounds")
	return x

def solve_directly(c, V):
	"""
	Solves the problem directly using linear algebra for comparison.
	Args:
		c (np.array): Target vector c.
		V (np.array): Matrix whose columns are the v_i vectors.
	Returns:
		np.array: Continuous solution vector x.
	"""
	# Solve the least squares problem Vx = c
	x_continuous = np.linalg.pinv(V) @ c  # Use pseudo-inverse in case V is not square
	return np.round(x_continuous)		  # Return integer solution for comparison


if __name__ == "__main__":
	# Example target vector c
	N = 1e20
	N_half = int(N**0.5 // 10)
	N_quart = int(N**0.25 // 10)

	c = np.array([randint(0,N), randint(0,N), randint(0,N)], 
			dtype=np.float64)

	# Example correctional vectors v_i (columns of V)
	V = np.array([[randint(0,N_quart), randint(0,N_quart), randint(0,N_quart)],
				  [randint(0,N_quart), randint(0,N_quart), randint(0,N_quart)],
				  [randint(0,N_quart), randint(0,N_quart), randint(0,N_quart)]],
				  dtype=np.float64)

	# Run gradient descent
	optimal_x = gradient_descent_with_oracle(c, V)
	print("Optimal x (Gradient descent):", optimal_x, oracle(optimal_x, c, V))

	# Compute direct solution for reference
	direct_x = solve_directly(c, V)
	print("Optimal x (Direct Solution):", direct_x, oracle(direct_x, c, V))

