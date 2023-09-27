from ioh import get_problem, ProblemClass
import numpy
import variables_info

# This is from a paper.
def generalized_greedy_algorithm(func):
  num_dimensions = func.meta_data.n_variables
  X = [0] * num_dimensions
  V_strich = list(range(num_dimensions))
  groesser = func.constraints[0].compute_violation
  c_dach_wert = func.constraints[0].violation
  while V_strich:

    v_stern = None
    v_stern_wert = None
    for v in V_strich:

      X_mit_v = list(X)
      X_mit_v[v] = 1

      zaehler = func(X_mit_v) - func(X)

      groesser(X_mit_v)
      c_dach_mit_v = c_dach_wert()
      groesser(X)
      c_dach_ohne_v = c_dach_wert()
      nenner = c_dach_mit_v - c_dach_ohne_v

      arg_max_wert = zaehler / nenner
      if v_stern_wert is None or arg_max_wert > v_stern_wert:
        v_stern_wert = arg_max_wert
        v_stern = v

    V_strich.remove(v_stern)

    X_mit_v_stern = list(X)
    X_mit_v_stern[v_stern] = 1

    ist_kleiner_oder_gleich = not groesser(X_mit_v_stern)
    if ist_kleiner_oder_gleich:
      X = X_mit_v_stern

  # Step 1: Create a num_dimensions x num_dimensions numpy array filled with zeros
  array = numpy.zeros((num_dimensions, num_dimensions), dtype=int)

  # Step 2: Set the diagonal to ones
  numpy.fill_diagonal(array, 1)

  # Step 3: Convert each row back to a Python list
  singletons = [row.tolist() for row in array]

  singletons = [singleton for singleton in singletons if not groesser(singleton)]
  max_singleton = max(singletons, key=lambda singleton: func(singleton))

  max_singleton_func_value = func(max_singleton)
  X_func_value = func(X)

  if max_singleton_func_value > X_func_value:
    return max_singleton
  else:
    return X

# ================================================================================================

if __name__ == '__main__':
  # [2000, 2001, 2002, 2003, 2004, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2200, 2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2212, 2213, 2214, 2215, 2216, 2217, 2218, 2219, 2220, 2221, 2222, 2223, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308]
  # It could last a number of seconds to run the generalized greedy algorithm
  # on each of these instances of submodular problems.

  f = get_problem(2124, 1, 0, ProblemClass.GRAPH)
  f = get_problem(2103, 1, 0, ProblemClass.GRAPH)
  f = get_problem(2219, 1, 0, ProblemClass.GRAPH)

  # f
  # f.constraints[0].compute_violation
  # f.constraints[0].violation

  g = generalized_greedy_algorithm(f)
  teilmenge_knoten = [index for index, value in enumerate(g) if value]
  variables_info.d(g)
  variables_info.d(f(g))
  variables_info.d(teilmenge_knoten)
