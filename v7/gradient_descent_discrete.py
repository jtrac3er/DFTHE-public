import numpy as np
from random import randint
from lgs import *

def oracle_norm(x, c, V):
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


def round_to_int(v):
	return np.array([int(x) for x in v])


def gradient_descent_with_oracle(
			oracle,
			n,
			max_iter=1000, 
			alpha=1, 
			alpha_decay=0.1, 
			alpha_increase=1.5,
			threshold=None):
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
	x = np.zeros(n, dtype=object)  # Start with an integer zero vector

	for iteration in range(max_iter):
		gradient = np.zeros(n, dtype=object)  # Initialize gradient

		# Estimate the gradient numerically
		for i in range(n):
			x_plus = x.copy()
			x_minus = x.copy()
			x_plus[i] += 1
			x_minus[i] -= 1

			# Query the Oracle for the finite difference approximation
			grad_estimate = (oracle(x_plus) - oracle(x_minus)) / 2
			gradient[i] = grad_estimate

		# Update x using the gradient
		x_new = round_to_int(x - alpha * gradient)
		if oracle(x) < oracle(x_new):
			# dann ist man sicher darüber gegangen, alpha zu gross
			alpha *= alpha_decay
		else:
			# ein bisschen erhöhen wieder
			alpha *= alpha_increase
			# Terminate if gradient is zero (convergence)
			if np.all(np.abs(x - x_new) < 1e-6) or (threshold and oracle(x) < threshold):
				break
			# neues x setzen
			x = x_new

		# Optional: Print progress
		#print(f"Iteration {iteration + 1}: alpha = {alpha} x = {x}, Oracle value = {oracle(x)}, Gradient = {gradient}")

	#print(f"Gradient descent found solution within {iteration} rounds")
	return x


def print_len(v): print([int.bit_length(e) for e in v])


if __name__ == "__main__":

	while True:

		# Example target vector c
		N = 1e50
		const_factor = 10

		N_half = int((N ** 0.5) // const_factor)
		N_quart = int((N ** 0.2) // const_factor)
		N_eight = int((N ** 0.01) // const_factor)

		#c = np.array([randint(-N_half,N_half), randint(-N_half,N_half), randint(-N_half,N_half)], 
		c = np.array([randint(0,N_half), randint(0,N_half), randint(0,N_half)],
				dtype=object)

		# Example correctional vectors v_i (columns of V)
		V = np.transpose(np.array([
					  [randint(0,N_quart), randint(0,N_eight), randint(0,N_eight)],
					  [randint(0,N_eight), randint(0,N_quart), randint(0,N_eight)],
					  [randint(0,N_eight), randint(0,N_eight), randint(0,N_quart)],
					  
					  #[randint(0,N_eight), randint(0,N_eight), randint(0,N_eight)],
					  #[randint(0,N_quart), randint(0,N_quart), randint(0,N_quart)],
					  
					  #[randint(0,N_quart), randint(0,N_eight), randint(0,N_quart)],
					  #[randint(0,N_quart), randint(0,N_quart), randint(0,N_eight)],
					  #[randint(0,N_eight), randint(0,N_quart), randint(0,N_quart)],
					  ], dtype=object))

		n = V.shape[0]		# cv length

		# Run gradient descent
		optimal_x = gradient_descent_with_oracle(lambda x: oracle_norm(x,c,V), n, max_iter=1000)

		if not oracle_norm(optimal_x, c, V) < N_half:
			print("\n\n\nNot found")
		else:
			print("\n\n\nFound")

		print("Optimal x (Gradient descent):", optimal_x)
		print(f"Before normalization: Norm = {oracle_norm(np.zeros(n, dtype=object), c, V)}")
		print(f"After normalization: Norm = {oracle_norm(optimal_x, c, V)}")
		print(f"nitlength of N used: N = {int.bit_length(int(N))}")
		print()
		for v in V: print_len(v)
		print()
		print_len(c)

