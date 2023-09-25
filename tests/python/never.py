import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import ioh
import nevergrad
import variables_info

nevergrad_optimizers = [
    # 'SADiscreteLenglerOnePlusOneExp09',
    # 'OnePlusOne',
    'RLSOnePlusOne',
    # 'DiscreteLenglerHalfOnePlusOne',
    # 'SADiscreteLenglerOnePlusOneLin100',
    # 'Carola3',
    # 'DiscreteDoerrOnePlusOne',
    # 'LBFGSB',
    # 'MicroSQP',
    # 'NGOptBase',
    # 'NoisyDE',
    # 'pysot',
    # 'RescaledCMA',
    # 'SQORealSpacePSO',
    # 'TinyCMA',
]

class NevergradOptimizer:

    def __init__(self, optimizer):
        optimizer = f'nevergrad.optimization.optimizerlib.{optimizer}'
        self.optimizer = eval(optimizer)
        variables_info.d(optimizer)
        variables_info.d(self.optimizer)
    
    def __call__(self, func):
        parametrization = nevergrad.p.Choice([0, 1], repetitions=func.meta_data.n_variables)
        instance_of_optimizer = self.optimizer(parametrization=parametrization, budget=100_000)

        # Remember the greedy point in the state of the IOHexperimenter function.
        generalized_greedy_algorithm_point = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # func(generalized_greedy_algorithm_point)

        instance_of_optimizer.minimize(func)
        
# [2000, 2001, 2002, 2003, 2004, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2200, 2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2212, 2213, 2214, 2215, 2216, 2217, 2218, 2219, 2220, 2221, 2222, 2223, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308]
submodular_function_ids = []
for function_id in range(2000, 2400):
    try:
        p = ioh.get_problem(function_id, 1, 1, ioh.ProblemClass.GRAPH)
        submodular_function_ids.append(function_id)
    except:
        continue

# Function ID 2124:
#   example_graphs/example_graph0
#   example_graphs/example_graph0_c_linear

submodular_function_ids = [2124]
submodular_function_ids = [2120]
variables_info.d(submodular_function_ids)

for nevergrad_optimizer in nevergrad_optimizers:
    ioh_experiment = ioh.Experiment(
        algorithm = NevergradOptimizer(nevergrad_optimizer),
        fids = submodular_function_ids,
        iids = [1] * len(submodular_function_ids),
        dims = [1] * len(submodular_function_ids),
        problem_class = ioh.ProblemClass.GRAPH,
        folder_name = nevergrad_optimizer,
        algorithm_name = nevergrad_optimizer,
        output_directory = 'ioh_experiments',
        reps = 1,
        njobs = 1,
        logged = True,
        store_positions = False,
        merge_output = True,
        zip_output = True,
        remove_data = True,
    )
    ioh_experiment()
