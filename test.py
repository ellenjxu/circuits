import math

from solve import solve

# N=2 -> 5/7
result_2 = solve(2)
expected_2 = 5/7
assert math.isclose(result_2, expected_2, rel_tol=1e-9), f"Test failed for N=2: got {result_2}, expected {expected_2}"

# N=3 -> 331/495
result_3 = solve(3)
expected_3 = 331/495
assert math.isclose(result_3, expected_3, rel_tol=1e-9), f"Test failed for N=3: got {result_3}, expected {expected_3}"

print("All tests passed!")