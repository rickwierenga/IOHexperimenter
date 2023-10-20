import ioh
import numpy
import variables_info

def generalized_greedy_algorithm(problem):
  num_dimensions = problem.meta_data.n_variables
  X = [0] * num_dimensions
  V_strich = list(range(num_dimensions))
  groesser = problem.constraints[0].compute_violation
  c_dach_wert = problem.constraints[0].violation
  while V_strich:

    v_stern = None
    v_stern_wert = None
    for v in V_strich:

      X_mit_v = list(X)
      X_mit_v[v] = 1

      zaehler = problem(X_mit_v) - problem(X)

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
  max_singleton = max(singletons, key=lambda singleton: problem(singleton))

  max_singleton_func_value = problem(max_singleton)
  X_func_value = problem(X)

  if max_singleton_func_value > X_func_value:
    return max_singleton
  else:
    return X

if __name__ == '__main__':
  f = ioh.get_problem(2219, 1, 0, ioh.ProblemClass.GRAPH)
  g = generalized_greedy_algorithm(f)
  teilmenge_knoten = [index for index, value in enumerate(g) if value]
  variables_info.d(g)
  variables_info.d(f(g))
  variables_info.d(teilmenge_knoten)
