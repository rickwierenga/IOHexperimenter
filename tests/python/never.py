import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy.core.getlimits")
warnings.filterwarnings("ignore", message="Bounds are 1.0 sigma away from each other")

import greedy
import ioh
import nevergrad.benchmark
import nevergrad.functions
import variables_info

submodular_problem_ids = [2100]
nevergrad_algorithms = [
  "AdaptiveDiscreteOnePlusOne",
  # "DiscreteLenglerFourthOnePlusOne",
  # "Generalized greedy algorithm",
  # "OnePlusOne",
  # "RFMetaModelOnePlusOne",
  # "RLSOnePlusOne",
  # "SADiscreteLenglerOnePlusOneExp09Auto",
]
budget = 1_000
num_runs = 10

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



for nevergrad_algorithm in nevergrad_algorithms:

  ioh_logger = ioh.logger.Analyzer(
    # [ioh.logger.trigger.ALWAYS],
    additional_properties = [
      # ioh.logger.property.EVALUATIONS,
      # ioh.logger.property.RAWY,
      ioh.logger.property.RAWYBEST,
      ioh.logger.property.TRANSFORMEDY,
      ioh.logger.property.TRANSFORMEDYBEST,
      # ioh.logger.property.CURRENTBESTY,
      # ioh.logger.property.CURRENTY,
      # ioh.logger.property.PENALTY,
      # ioh.logger.property.VIOLATION,
    ],
    algorithm_name = nevergrad_algorithm,
    folder_name = nevergrad_algorithm,
    root = "nevergrad.benchmark.Experiment",
  )
  ioh_logger.reset()

  for submodular_problem_id in submodular_problem_ids:

    submodular_problem = ioh.get_problem(submodular_problem_id, 1, 1, ioh.ProblemClass.GRAPH)
    submodular_problem.attach_logger(ioh_logger)

    if nevergrad_algorithm == "Generalized greedy algorithm":

      submodular_problem.attach_logger(ioh_logger)
      greedy.generalized_greedy_algorithm(submodular_problem)

      # Do a second time to make it clear that GGA can produce only one run on a given problem.
      submodular_problem.reset()
      greedy.generalized_greedy_algorithm(submodular_problem)

    else:
      for run in range(num_runs):
        nevergrad_experiment = nevergrad.benchmark.Experiment(
          TestedFunction(submodular_problem),
          optimizer=nevergrad_algorithm,
          budget=budget, # seems to actually use budget + 1 function evaluations, so 1_001 instead of 1_000.
          batch_mode=False,
        )
        nevergrad_experiment.run()
        submodular_problem.reset()
