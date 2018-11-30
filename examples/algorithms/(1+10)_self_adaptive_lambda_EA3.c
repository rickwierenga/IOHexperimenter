/**
 * This file implements an evolutionary algorithm with a self-adaptive lambda rule:
 *   If there is not a solution with fitness is not smaller than the parent's is found, lambda is doubled.
 *   Otherwise lambda is divided by s, where s is the number of offsrings with fitnesses are not smaller than the parent's.
 * Mutation rate (fixed): 1/dimension
 * Size of parents: 1
 * Size of offsprings: originally set as 10
 */

/**
 * The maximal budget for evaluations done by an optimization algorithm equals dimension * BUDGET_MULTIPLIER.
 * Increase the budget multiplier value gradually to see how it affects the runtime.
 */
static const size_t BUDGET_MULTIPLIER = 50;

/**
 * The maximal number of independent restarts allowed for an algorithm that restarts itself.
 */
static const size_t INDEPENDENT_RESTARTS = 100;

/**
 * The random seed. Change it if needed.
 */
static const uint32_t RANDOM_SEED = 1;

/**
 * To generate individuals randomly. Elements of a bit-string is generated by a standard Uniform distribution. 
 */
void generatingIndividual(int * individuals,
                            const size_t dimension, 
                            IOHprofiler_random_state_t *random_generator){
  size_t i;
  for(i = 0; i < dimension; ++i){
    individuals[i] = (int)(IOHprofiler_random_uniform(random_generator) * 2);
  }
}

/**
 * To copy an individual "old" to "new", the length of the bit-string is given by "dimension".
 */
void CopyIndividual(int * old, int * new, const size_t dimension){
  size_t i;
  for(i = 0; i < dimension; ++i){
    new[i] = old[i];
  }
}

/**
 * To sample a random value by a Binomial distribution with "n" trials and a given "probability".
 */
size_t randomBinomial(size_t n, double  probability,IOHprofiler_random_state_t *random_generator)
{
    size_t r, i;
    r = 0;
    for(i = 0; i < n; ++i){
        if(IOHprofiler_random_uniform(random_generator) < probability)
        {
            ++r;
        }
    }
    return r;
}

/**
 * Mutation Operator.
 * "l" is the number of bits to be flipped, which is sample by Binomial distribution.
 * "l" positions are randomly selected by a uniform distribution.
 * A resampling strategy is applied to make sure that "l" is larger than 0. 
 */
size_t mutateIndividual(int * individual, 
                      const size_t dimension, 
                      double mutation_rate, 
                      IOHprofiler_random_state_t *random_generator){
  size_t i,h, l;
  int flag,temp;
  int * flip;

  l = randomBinomial(dimension,mutation_rate,random_generator);
  while(l == 0){
    l = randomBinomial(dimension,mutation_rate,random_generator);
  }
  
  flip = IOHprofiler_allocate_int_vector(l);
  for(i = 0; i < l; ++i){
    while(1){
      flag = 0;
      temp = (int)(IOHprofiler_random_uniform(random_generator) * dimension);
      for(h = 0; h < i; ++h)
      {
        if(temp == flip[h]){
          flag = 1;
          break;
        }
      }
      if(flag == 0)
        break;
    }
    flip[i] = temp;
  }

  for(i = 0; i < l; ++i){
    individual[flip[i]] =  ((int)(individual[flip[i]] + 1) % 2);
  }
  IOHprofiler_free_memory(flip);
  return l;
}

/**
 * An user defined algorithm.
 *
 * @param "evaluate" The function for evaluating variables' fitness. Invoking the 
 *        statement "evaluate(x,y)", then the fitness of 'x' will be stored in 'y[0]'.
 * @param "dimension" The dimension of problem.
 * @param "number_of_objectives" The number of objectives. The default is 1.
 * @param "lower_bounds" The lower bounds of the region of interested (a vector containing dimension values). 
 * @param "upper_bounds" The upper bounds of the region of interested (a vector containing dimension values). 
 * @param "max_budget" The maximal number of evaluations. You can set it by BUDGET_MULTIPLIER in "config" file.
 * @param "random_generator" Pointer to a random number generator able to produce uniformly and normally
 * distributed random numbers. You can set it by RANDOM_SEED in "config" file
 */
void User_Algorithm(evaluate_function_t evaluate,
                      const size_t dimension,
                      const size_t number_of_objectives,
                      const int *lower_bounds,
                      const int *upper_bounds,
                      const size_t max_budget,
                      IOHprofiler_random_state_t *random_generator) {

  int *parent = IOHprofiler_allocate_int_vector(dimension);
  int *offspring = IOHprofiler_allocate_int_vector(dimension);
  int *best = IOHprofiler_allocate_int_vector(dimension);
  double best_value,current_best_value;
  double *y = IOHprofiler_allocate_vector(number_of_objectives);
  
  size_t i, j, l, s;
  size_t number_of_parameters = 3;
  double *p = IOHprofiler_allocate_vector(number_of_parameters);
  int hit_optimal = 0;
  int lambda = 10;
  double mutation_rate = 1/(double)dimension;

  generatingIndividual(parent,dimension,random_generator);

  /* Call the evaluate function to evaluate x on the current problem (this is where all the IOHprofiler logging
   * is performed) */
  p[0] = (double)lambda; p[1] = 0.0; p[2] = 0.0;
  set_parameters(number_of_parameters,p);
  evaluate(parent,y);
  
  CopyIndividual(parent,best,dimension);
  best_value = y[0];
  
  for (i = 1; i < max_budget; ) {
    
    current_best_value = best_value;
    s = 0;
    
    for(j = 0; j < lambda; ++j){
      CopyIndividual(parent,offspring,dimension);
      l = mutateIndividual(offspring,dimension,mutation_rate,random_generator);
      p[0] = (double)lambda; p[1] = mutation_rate; p[2] = (double)l;

      set_parameters(number_of_parameters,p);
      evaluate(offspring, y);
      
      ++i;
      if(i == max_budget) {
        break;
      }

      if(if_hit_optimal()) {
        hit_optimal = 1;
        break;
      }
      
      if(y[0] > best_value){
        best_value = y[0];
        CopyIndividual(offspring,best,dimension);
      }

      if(y[0] >= current_best_value){
        s++;
      }
    }

    if(hit_optimal) {
      break;
    }   
    CopyIndividual(best,parent,dimension);
    
    /* The self-adaptive rule.
     */
    if(s == 0){ 
      lambda = lambda *2;
    }
    else{
      lambda = lambda / s; 
      if(lambda < 1) {
        lambda = 1;
      }
    }
  }

  IOHprofiler_free_memory(parent);
  IOHprofiler_free_memory(offspring);
  IOHprofiler_free_memory(best);
  IOHprofiler_free_memory(p);
  IOHprofiler_free_memory(y);
}