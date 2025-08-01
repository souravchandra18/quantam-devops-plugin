from qiskit_optimization.applications import Maxcut
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

import numpy as np

# Set up graph weights
w = np.array([
    [0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 1, 1, 0]
])

# Step 1: Convert MaxCut to QUBO
maxcut = Maxcut(w)
problem = maxcut.to_quadratic_program()
qubo = QuadraticProgramToQubo().convert(problem)

# Step 2: Create QAOA with required optimizer
optimizer = COBYLA(maxiter=100)
qaoa = QAOA(optimizer=optimizer, sampler=Sampler(), reps=1)
qaoa_solver = MinimumEigenOptimizer(qaoa)

# Step 3: Solve the problem
result = qaoa_solver.solve(qubo)

# Solve
print("Optimal solution:", result.x)
print("Objective value:", result.fval)
print("Result:", result)

# Write output
with open("reports/final-test-suite.txt", "w") as f:
    f.write(str(result.variables))
