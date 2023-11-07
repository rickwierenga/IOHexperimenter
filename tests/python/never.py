import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy.core.getlimits")
warnings.filterwarnings("ignore", message="Bounds are 1.0 sigma away from each other")

import greedy
import ioh
import nevergrad.benchmark
import nevergrad.functions
import variables_info

# [2000, 2001, 2002, 2003, 2004, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111,
# 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2200,
# 2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2212, 2213, 2214, 2215, 2216, 2217,
# 2218, 2219, 2220, 2221, 2222, 2223, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308]
submodular_problem_ids = [2116]
nevergrad_algorithms = [
  # "DiscreteLenglerFourthOnePlusOne",
  # "OnePlusOne",
  # "SADiscreteLenglerOnePlusOneExp09Auto",
  # "RFMetaModelOnePlusOne",
  "RLSOnePlusOne",
  # "AdaptiveDiscreteOnePlusOne",
  # "Generalized greedy algorithm",
  # "AnisotropicAdaptiveDiscreteOnePlusOne",
  # "DiscreteBSOOnePlusOne",
  # "DiscreteDE",
  # "DiscreteDoerrOnePlusOne",
  # "DiscreteLengler2OnePlusOne",
  # "DiscreteLengler3OnePlusOne",
  # "DiscreteLenglerFourthOnePlusOne",
  # "DiscreteLenglerHalfOnePlusOne",
  # "DiscreteLenglerOnePlusOne",
  # "DiscreteLenglerOnePlusOneT",
  # "discretememetic",
  # "DiscreteOnePlusOne",
  # "DiscreteOnePlusOneT",
  # "DoubleFastGADiscreteOnePlusOne",
  # "MultiDiscrete",
  # "NoisyDiscreteOnePlusOne",
  # "OptimisticDiscreteOnePlusOne",
  # "PortfolioDiscreteOnePlusOne",
  # "PortfolioDiscreteOnePlusOneT",
  # "RecombiningPortfolioDiscreteOnePlusOne",
  # "RecombiningPortfolioOptimisticNoisyDiscreteOnePlusOne",
  # "SADiscreteLenglerOnePlusOneExp09",
  # "SADiscreteLenglerOnePlusOneExp099",
  # "SADiscreteLenglerOnePlusOneExp09Auto",
  # "SADiscreteLenglerOnePlusOneLin1",
  # "SADiscreteLenglerOnePlusOneLin100",
  # "SADiscreteLenglerOnePlusOneLinAuto",
  # "SADiscreteOnePlusOneExp09",
  # "SADiscreteOnePlusOneExp099",
  # "SADiscreteOnePlusOneLin100",
  # "SparseDoubleFastGADiscreteOnePlusOne",
]
budget = 1_000
num_runs = 3

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
  algorithm_name="Nevergrad + GGA",
  folder_name="NevergradAndGGA",
  root="NevergradAndGGA_Experiment",
)
ioh_logger.reset()

for nevergrad_algorithm in nevergrad_algorithms:
  for submodular_problem_id in submodular_problem_ids:

    submodular_problem = ioh.get_problem(submodular_problem_id, 1, 1, ioh.ProblemClass.GRAPH)
    submodular_problem.attach_logger(ioh_logger)

    if nevergrad_algorithm == "Generalized greedy algorithm":
      submodular_problem.attach_logger(ioh_logger)
      greedy.generalized_greedy_algorithm(submodular_problem)
    else:
      for _ in range(num_runs):
        print("run")
        nevergrad_experiment = nevergrad.benchmark.Experiment(
          TestedFunction(submodular_problem),
          optimizer=nevergrad_algorithm,
          budget=budget,
          batch_mode=False,
        )
        j = nevergrad_experiment.run()

        variables_info.d(j)
        variables_info.d(nevergrad_experiment)
        variables_info.d(nevergrad_experiment.optimsettings)
        variables_info.d(nevergrad_experiment.optimsettings.executor)
        variables_info.d(nevergrad_experiment.optimsettings.executor.check_is_done())
        variables_info.d(nevergrad_experiment.optimsettings.num_workers)
        # breakpoint()
