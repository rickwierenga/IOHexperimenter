import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy.core.getlimits")
warnings.filterwarnings("ignore", message="Bounds are 1.0 sigma away from each other")

import greedy
import ioh
import nevergrad
import nevergrad.benchmark
import nevergrad.functions
import variables_info

submodular_problem_id = 2100
nevergrad_algorithms = [
  "DiscreteLenglerFourthOnePlusOne",
  "OnePlusOne",
  "SADiscreteLenglerOnePlusOneExp09Auto",
  "RFMetaModelOnePlusOne",
  "RLSOnePlusOne",
]
budget = 100_000

class TestedFunction(nevergrad.functions.ExperimentFunction):

  def __init__(self, submodular_problem):
    parametrization = (
      nevergrad.p.Array(init=[0] * submodular_problem.meta_data.n_variables)
      .set_bounds(0, 1)
      .set_integer_casting()
      .set_name("")
    )
    super().__init__(self.oracle_call, parametrization)
    self.submodular_problem = submodular_problem

  def oracle_call(self, x):
    return -self.submodular_problem(x)

# Generalized greedy algorithm
# =================================================================================================
ioh_logger = ioh.logger.Analyzer(
  root="nevergrad.benchmark.Experiment",
  folder_name="Generalized greedy algorithm",
  algorithm_name="Generalized greedy algorithm",
)
ioh_logger.reset()

submodular_problem = ioh.get_problem(submodular_problem_id, 1, 1, ioh.ProblemClass.GRAPH)
submodular_problem.attach_logger(ioh_logger)
greedy.generalized_greedy_algorithm(submodular_problem)
# =================================================================================================

for nevergrad_algorithm in nevergrad_algorithms:

  ioh_logger = ioh.logger.Analyzer(
    root="nevergrad.benchmark.Experiment",
    folder_name=nevergrad_algorithm,
    algorithm_name=nevergrad_algorithm,
  )
  ioh_logger.reset()

  submodular_problem = ioh.get_problem(submodular_problem_id, 1, 1, ioh.ProblemClass.GRAPH)
  submodular_problem.attach_logger(ioh_logger)

  nevergrad_experiment = nevergrad.benchmark.Experiment(
    TestedFunction(submodular_problem),
    optimizer=nevergrad_algorithm,
    budget=budget,
    num_workers=1,
  )
  nevergrad_experiment.run()
