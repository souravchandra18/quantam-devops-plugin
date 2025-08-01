# from qiskit_optimization.applications import Maxcut
# from qiskit_optimization.converters import QuadraticProgramToQubo
# from qiskit_optimization.algorithms import MinimumEigenOptimizer

# from qiskit_algorithms.minimum_eigensolvers import QAOA
# from qiskit_algorithms.optimizers import COBYLA
# from qiskit.primitives import Sampler

# import numpy as np
# import os

# # Set up graph weights
# w = np.array([
#     [0, 1, 1, 0, 0],
#     [1, 0, 1, 1, 0],
#     [1, 1, 0, 1, 1],
#     [0, 1, 1, 0, 1],
#     [0, 0, 1, 1, 0]
# ])

# # Step 1: Convert MaxCut to QUBO
# maxcut = Maxcut(w)
# problem = maxcut.to_quadratic_program()
# qubo = QuadraticProgramToQubo().convert(problem)

# # Step 2: Create QAOA with required optimizer
# optimizer = COBYLA(maxiter=100)
# qaoa = QAOA(optimizer=optimizer, sampler=Sampler(), reps=1)
# qaoa_solver = MinimumEigenOptimizer(qaoa)

# # Step 3: Solve the problem
# result = qaoa_solver.solve(qubo)

# # Solve
# print("Optimal solution:", result)
# print("Objective value:", result.fval)
# print("Result:", result)

# # Make sure the reports directory exists
# os.makedirs("reports", exist_ok=True)

# # Write output to a file
# with open("reports/final-test-suite.txt", "w") as f:
#     f.write(f"Optimal solution: {result}\n")
#     f.write(f"Objective value: {result.fval}\n")
#     f.write(f"Result: {result}\n")


import numpy as np
from qiskit_optimization.problems import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit.primitives import Sampler
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_utils import algorithm_globals
from qiskit_optimization.translators import from_docplex_mp
from docplex.mp.model import Model
from qiskit_algorithms.optimizers import COBYLA

import os

# Set random seed for reproducibility
algorithm_globals.random_seed = 123

# 🧪 Test names aligned with variable order in the QAOA model
test_names = [
    "com.company.tests.UserServiceTest",
    "com.company.tests.ClaimsServiceTest",
    "com.company.tests.PolicyServiceTest",
    "com.company.tests.PaymentServiceTest",
    "com.company.tests.NotificationServiceTest"
]

# Create an optimization model
mdl = Model(name="TestCaseSelection")
x = [mdl.binary_var(name=f"x_{i}") for i in range(len(test_names))]

# Objective: Minimize total cost (simulate test runtime as weights)
weights = [2, 1, 1, 2, 2]  # arbitrary cost per test
mdl.minimize(mdl.sum(weights[i] * x[i] for i in range(len(test_names))))

# Constraint: At least 2 tests should be selected to maintain confidence
mdl.add_constraint(mdl.sum(x) >= 2, "min_coverage")

# Convert to Qiskit QUBO
qp = from_docplex_mp(mdl)

# Convert to QUBO
converter = QuadraticProgramToQubo()
qubo = converter.convert(qp)

# Run QAOA optimizer
qaoa = QAOA(optimizer=COBYLA(), reps=1, sampler=Sampler())
optimizer = MinimumEigenOptimizer(qaoa)

# Solve problem
result = optimizer.solve(qubo)

# 📌 Extract selected test names
selected_tests = [
    test_names[i] for i, v in enumerate(result.x) if v == 1
]

# ✅ Ensure reports dir exists
os.makedirs("reports", exist_ok=True)

# Write selected test classes to final-test-suite.txt
with open("reports/final-test-suite.txt", "w") as f:
    for test in selected_tests:
        f.write(test + "\n")

# Print for debug
print("Optimal solution:", result)
print("Selected test classes:")
for test in selected_tests:
    print(test)
