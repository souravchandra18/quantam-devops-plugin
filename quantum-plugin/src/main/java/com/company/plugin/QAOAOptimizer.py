from qiskit_optimization.applications import Maxcut
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.primitives import Estimator
from qiskit import Aer
from qiskit.utils import algorithm_globals
import numpy as np

# Set random seed for reproducibility
algorithm_globals.random_seed = 123

# Example problem: Optimize test case execution order
# (This would be generated dynamically based on test cost/coverage)
w = np.array([
    [0.0, 1.0, 2.0],
    [1.0, 0.0, 1.0],
    [2.0, 1.0, 0.0]
])

# Build MaxCut QUBO
maxcut = Maxcut(w)
problem = maxcut.to_quadratic_program()
qp2qubo = QuadraticProgramToQubo()
qubo = qp2qubo.convert(problem)

# Use Estimator backend and new-style QAOA
qaoa = QAOA(optimizer=None, reps=1, estimator=Estimator())
optimizer = MinimumEigenOptimizer(qaoa)

# Solve
result = optimizer.solve(qubo)
print("Result:", result)

# Write output
with open("reports/final-test-suite.txt", "w") as f:
    f.write(str(result.variables))
