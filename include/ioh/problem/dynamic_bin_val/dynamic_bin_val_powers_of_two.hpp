/**
 * @file dynamic_bin_val_powers_of_two.hpp
 * @brief Contains the declaration of the DynamicBinValPowersOfTwo class, which represents dynamic binary value
 *        problems in the context of IOH.
 */

#pragma once

#include <algorithm>
#include <iostream>
#include <math.h>
#include <random>
#include <vector>

#include "ioh/problem/single.hpp"
#include "ioh/problem/transformation.hpp"

namespace ioh::problem
{
    /**
     * @class DynamicBinValPowersOfTwo
     * @brief This class serves to represent dynamic binary value problems within the context of Iterative
     *        Optimization Heuristics (IOH).
     *
     *        DynamicBinValPowersOfTwo: takes a value among the powers 2**1, 2**2, 2**3, ..., 2**31 / n_variables for each weight at each timestep
     *
     *        Inheriting functionalities from the IntegerSingleObjective, it also integrates functionalities
     *        for automatic registration of the problem type into various data structures. This facilitates
     *        easier management and retrieval of problem instances, while encapsulating characteristics and
     *        behaviours specific to dynamic binary value problems. It holds vital data members such as
     *        timestep and weights, which are crucial in depicting the dynamic aspects and unique features
     *        of these problem instances.
     */
    class DynamicBinValPowersOfTwo : public
        IntegerSingleObjective,
        AutomaticProblemRegistration<DynamicBinValPowersOfTwo, DynamicBinValPowersOfTwo>,
        AutomaticProblemRegistration<DynamicBinValPowersOfTwo, IntegerSingleObjective>
    {
    public:

        int timestep;                   /**< The current timestep in the dynamic binary value problem scenario. */
        std::vector<int> weights;       /**< A vector of weights used in the evaluation of the problem. */
        std::mt19937 random_generator;
        std::vector<int> transformed_x;

        /**
         * @brief Constructs a new instance of DynamicBinValPowersOfTwo.
         *
         * @param n_variables The dimension of the problem, representing the size of the search space and
         *                    indicating the number of variables in the problem.
         */
        DynamicBinValPowersOfTwo(const int instance, const int n_variables) :
            IntegerSingleObjective
            (
                MetaData(10002, instance, "DynamicBinValPowersOfTwo", n_variables, common::OptimizationType::MAX),
                Bounds<int>(n_variables, 0, 1)
            ),
            random_generator(instance)
        {
            if (n_variables == 1) { return; }

            this->timestep = 0;

            // Initialize the weights vector with random numbers between 0 and 1
            this->weights.resize(n_variables);

            int subtract_bits = log2(this->weights.size());
            std::uniform_int_distribution<> uniform_int_distribution(1, 31 - subtract_bits - 1);

            // Reinitialize the weights with random numbers between 0 and 1 after shuffling
            for(size_t i = 0; i < this->weights.size(); ++i)
            {
                int exponent = uniform_int_distribution(this->random_generator);
                this->weights[i] = pow(2, exponent);
            }

            this->transformed_x = std::vector<int>(n_variables, 1);
            this->optimum_.y = transform_objectives(0);
            transform_variables(this->transformed_x);
            this->optimum_.x = this->transformed_x;
        }

        int step()
        {
            this->timestep += 1;

            int subtract_bits = log2(this->weights.size());
            std::uniform_int_distribution<> uniform_int_distribution(1, 31 - subtract_bits - 1);

            // Reinitialize the weights with random numbers between 0 and 1 after shuffling
            for(size_t i = 0; i < this->weights.size(); ++i)
            {
                int exponent = uniform_int_distribution(this->random_generator);
                this->weights[i] = pow(2, exponent);
            }

            return this->timestep;
        }

    protected:

        double evaluate(const std::vector<int> &x) override
        {
            return std::accumulate(x.begin(), x.end(), 0.0);
        }

        std::vector<int> transform_variables(std::vector<int> x) override
        {
            transformation::variables::random_flip(x, this->meta_data_.instance);
            this->transformed_x = x;
            return x;
        }

        double transform_objectives(const double y) override
        {
            double value = 0;
            for(size_t i = 0; i < this->transformed_x.size(); ++i)
            {
                value += this->transformed_x[i] * this->weights[i];
            }
            return value;
        }
    };
} // namespace ioh::problem
