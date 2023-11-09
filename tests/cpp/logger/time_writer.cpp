#include "../utils.hpp"

#include "ioh/logger/flatfile.hpp"
#include "ioh/problem/bbob/sphere.hpp"


using namespace ioh;


void time_writer(const std::shared_ptr<ioh::common::file::Writer> &writer)
{
    
    size_t n = 50;
    std::array<int, 50> times{};
    size_t sum_times = 0;
    for (size_t i = 0; i < n; i++)
    {
        const std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
        {
            trigger::Always always;
            watch::TransformedY transformed_y;
            auto p0 = problem::bbob::Sphere(1, 10);
            auto logger = logger::FlatFile({always}, {transformed_y}, "IOH.dat", ".");
            logger.set_writer(writer);
            common::random::seed(1);
            size_t runs = 1;
            size_t samples = 100'000;
            p0.attach_logger(logger);
            for (auto r = 0; r < runs; ++r)
            {
                for (auto s = 0; s < samples; ++s)
                {
                    p0(common::random::pbo::uniform(p0.meta_data().n_variables, s));
                }
                p0.reset();
            }
        }        
        fs::remove("./IOH.dat");
        EXPECT_TRUE(!fs::exists("./IOH.dat"));
        times[i] =
            std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - start).count();
        sum_times += times[i];
    }
    double mean = (double)sum_times / 50.0;
    double std_dev = 0.0;

    for (auto t : times)
        std_dev += std::pow(t - mean, 2);
    std_dev = sqrt(std_dev / 50.0);
    std::cout << mean << "+-" << std_dev << std::endl;
}


TEST_F(BaseTest, logger_time_writer)
{
    std::cout << "OFstream ";
    time_writer(std::make_shared<ioh::common::file::OFStream>());
    std::cout << "FWriter ";
    time_writer(std::make_shared<ioh::common::file::FWriter>());
    std::cout << "CachedFWriter ";
    time_writer(std::make_shared<ioh::common::file::CachedFWriter>());
    std::cout << "NoWriter ";
    time_writer(std::make_shared<ioh::common::file::NoWriter>());

   // 200 + 78
}

