/**
 * Feedback for the CEC functions:
 * So what you did was indeed make a copy of the BBOB function.
 * While the code that performs the function evaluation, the code in the evaluate method
 * is indeed exactly the same for both the BBOB suite and the CEC suite, the stuff that happens in
 * transform_variables is different.
 *
 * For your information, how a problem is evaluated in iohexperimenter is as follows:
 *
 * problem(x_raw)
 *  1. x_transformed = transform_variables(x_raw)
 *  2. y_raw = evaluate(y_raw)
 *  3. y_transformed = transform_objectives(y_raw)
 *  4. return y_transformed
 *
 * For BBOB, the code in transform_variables is based on "randomly" generated transformations,
 * while for CEC, these transformation matrices/vectors are defined in a set of flat files.
 * This also means that for BBOB problems in theory we can generate any number of transformations,
 * while for the CEC problems there is only one officially defined transformation set for a given
 * function.
 *
 * What I would suggest, since most of the file parsing code is shared amongst all CEC functions,
 * is that you make a shared parent class for all CEC functions, which only performs such shared
 * tasks, and put the function specific code, i.e. the rastrigin evaluation/transformation code
 * in the function class. Take a look at the bbob_problem.hpp for an idea on how to this.
 *
 * Below I give an example of such a structure. This is not complete, nor fully working, but hope you get the idea.
 */

#include <string>
#include <vector>

namespace ioh::problem::cec2022
{

    // ************************ Parent class *************************** //

    // Class which implements the methods shared for all cec functions
    class CEC : public RealSingleObjective
    {
    public:
        /**
         * @brief Construct a new CEC object
         *
         * @param problem_id The id of the problem (should be unique)
         * @param instance The instance of the problem (ignored for cec for now)
         * @param n_variables the dimension of the problem (the size of the search space, how many x varables)
         * @param name the name of the problem (should be unique)
         * @param path the transformation file (just an example, maybe you want to do this differently)
         */
        CEC(const int problem_id, const int instance, const int n_variables, const std::string &name,
            const std::string &path) :
            RealSingleObjective(MetaData(problem_id, instance, name, n_variables),
                                Bounds<double>(n_variables, -5 /*Lower bound*/, 5 /*Upper bound*/))
        {
            read_transformation_files(path);
            set_optimum();
        }

        //! Method to set the value for the global optimum correctly. 
        void set_optimum();

        //! Handler for reading all static data
        void read_transformation_files(const std::string path);

        //! Method for applying the cec transformations. 
        std::vector<double> apply_cec_transformation(const std::vector<double> &x);

    protected:
        //! The method which should be override in RealSingleObjective for applying the actual transformation correctly
        std::vector<double> transform_variables(std::vector<double> x) override { return apply_cec_transformation(x); }
    };


    // CRTP class for CEC problems. Inherit from this class when defining new CEC problems. This is needed for 
    // storing stuff in the hash maps. 
    template <template <typename> class ProblemType>
    struct CECProblem : AutomaticProblemRegistration<ProblemType<CEC>, CEC>,
                        AutomaticProblemRegistration<ProblemType<CEC>, RealSingleObjective>
    {
    };


    // ************************ Specific functions (other files) *************************** //
    class Rastrigin final : public CECProblem<Rastrigin>
    {
    protected:
        //! Evaluation method
        double evaluate(const std::vector<double> &x) override { 
            auto sum1 = 0.0, sum2 = 0.0;

            for (const auto xi : x)
            {
                sum1 += cos(2.0 * IOH_PI * xi);
                sum2 += xi * xi;
            }
            if (std::isinf(sum2))
                return sum2 ;

            return 10.0 * (static_cast<double>(x.size()) - sum1) + sum2;
        }

    public:
        /**
         * \brief Construct a new Rastrigin object. 
         *
         * \param instance The instance number of a problem, which controls the transformation
         * performed on the original problem. This is ignored on the CEC problems, but
         * required by the interface. 
         * \param n_variables The dimensionality of the problem to created, 4 by default.
         **/
        Rastrigin(const int instance, const int n_variables) : 
            CECProblem(100 /*Should be unique*/, instance, n_variables, "RastriginCEC2022", "/a/path/to/a/file")
        {
           
        }
    };


} // namespace ioh::problem::cec2022
