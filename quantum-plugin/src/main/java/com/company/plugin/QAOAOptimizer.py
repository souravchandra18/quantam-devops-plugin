import numpy as np
from qiskit_aer import Aer
from qiskit_optimization.applications import Maxcut
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit.primitives import Sampler

# Set seed for reproducibility
np.random.seed(10598)

# Define a simple MaxCut graph
graph = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
maxcut = Maxcut(graph)
problem = maxcut.to_quadratic_program()

# Convert to QUBO
qubo_converter = QuadraticProgramToQubo()
qubo_problem = qubo_converter.convert(problem)

# Use QAOA with default sampler
qaoa = QAOA(sampler=Sampler(), reps=1)

# Minimum Eigen Optimizer
optimizer = MinimumEigenOptimizer(qaoa)

# Solve the problem
result = optimizer.solve(qubo_problem)

# Solve
result = optimizer.solve(qubo)
print("Optimal solution:", result.x)
print("Objective value:", result.fval)
print("Result:", result)

# Write output
with open("reports/final-test-suite.txt", "w") as f:
    f.write(str(result.variables))
