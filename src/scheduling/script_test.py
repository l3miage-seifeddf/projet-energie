import time
from src.scheduling.instance.instance import Instance
from src.scheduling.optim.constructive import Greedy, NonDeterminist
from src.scheduling.optim.local_search import FirstNeighborLocalSearch, BestNeighborLocalSearch
from src.scheduling.optim.neighborhoods import MachineSwitchNeighborhood, OperationOrderNeighborhood

N_RUNS = 10
instance = Instance.from_file("src/scheduling/tests/data/jsp_easy")

# Greedy
start = time.time()
greedy = Greedy()
sol_greedy = greedy.run(instance)
greedy_time = time.time() - start
greedy_obj = sol_greedy.objective

# FirstNeighborLocalSearch
best_fnls_obj = float('inf')
fnls_time = 0
for _ in range(N_RUNS):
    start = time.time()
    fnls = FirstNeighborLocalSearch()
    sol = fnls.run(instance, NonDeterminist(), MachineSwitchNeighborhood(instance))
    fnls_time += time.time() - start
    if sol.is_feasible and sol.objective < best_fnls_obj:
        best_fnls_obj = sol.objective
fnls_time /= N_RUNS

# BestNeighborLocalSearch
best_bnls_obj = float('inf')
bnls_time = 0
for _ in range(N_RUNS):
    start = time.time()
    bnls = BestNeighborLocalSearch()
    sol = bnls.run(instance, NonDeterminist(), OperationOrderNeighborhood(instance), MachineSwitchNeighborhood(instance))
    bnls_time += time.time() - start
    if sol.is_feasible and sol.objective < best_bnls_obj:
        best_bnls_obj = sol.objective
bnls_time /= N_RUNS

print(f"Greedy: obj={greedy_obj}, time={greedy_time:.4f}s")
print(f"FirstNeighborLocalSearch: best obj={best_fnls_obj}, avg time={fnls_time:.4f}s")
print(f"BestNeighborLocalSearch: best obj={best_bnls_obj}, avg time={bnls_time:.4f}s")