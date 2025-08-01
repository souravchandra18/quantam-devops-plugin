from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit.primitives import Sampler
from qiskit import Aer
from qiskit.utils import algorithm_globals

algorithm_globals.random_seed = 123
qp = QuadraticProgram()
qp.binary_var("UserServiceTest")
qp.binary_var("ClaimsServiceTest")
qp.maximize(linear={"UserServiceTest": 1, "ClaimsServiceTest": 1}, quadratic={("UserServiceTest", "ClaimsServiceTest"): -2})
backend = Aer.get_backend("aer_simulator")
qaoa = QAOA(sampler=Sampler(), reps=1)
optimizer = MinimumEigenOptimizer(qaoa)
result = optimizer.solve(qp)

with open("../reports/final-test-suite.txt", "w") as f:
    for var, val in result.samples[0].x.items():
        if val > 0.5:
            f.write(var + "\n")
