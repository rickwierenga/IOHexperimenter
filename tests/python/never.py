import ioh
import nevergrad
import nevergrad.benchmark
import nevergrad.functions
import variables_info

submodular_problem_id = 2100
nevergrad_algorithms = [
    "OnePlusOne",
    "DiscreteLenglerFourthOnePlusOne",
    "SADiscreteLenglerOnePlusOneExp09Auto",
    "cGA",
    "TwoPointsDE",
]
budget = 1_000

submodular_problem = ioh.get_problem(submodular_problem_id, 1, 1, ioh.ProblemClass.GRAPH)

ioh_logger = ioh.logger.Analyzer(
    root="nevergrad.benchmark.Experiment",
    folder_name="das",
    algorithm_name="das",
)
ioh_logger.reset()
submodular_problem.attach_logger(ioh_logger)

class TestedFunction(nevergrad.functions.ExperimentFunction):
    def __init__(self):
        parametrization = (
            nevergrad.p.Array(init=[0] * submodular_problem.meta_data.n_variables)
            .set_bounds(0, 1)
            .set_integer_casting()
            .set_name("")
        )
        super().__init__(self.oracle_call, parametrization)

    def oracle_call(self, x):
        return -submodular_problem(x)

for nevergrad_algorithm in nevergrad_algorithms:
    # ioh_logger.folder_name = nevergrad_algorithm
    # ioh_logger.algorithm_name = nevergrad_algorithm
    nevergrad_experiment = nevergrad.benchmark.Experiment(
        TestedFunction(),
        optimizer=nevergrad_algorithm,
        budget=budget,
        num_workers=1,
    )
    nevergrad_experiment.run()
    variables_info.d(nevergrad_experiment._optimizer.current_bests)
    variables_info.d(nevergrad_experiment._optimizer.current_bests['pessimistic'].parameter.value)
    variables_info.d(submodular_problem(nevergrad_experiment._optimizer.current_bests['pessimistic'].parameter.value))
