#include "../utils.hpp"

#include "ioh/logger/flatfile.hpp"
#include "ioh/problem/bbob/sphere.hpp"
#include "ioh/problem/bbob/attractive_sector.hpp"

using namespace ioh;

size_t test_for_writer(const std::shared_ptr<ioh::common::file::Writer>& writer)
{
    auto p0 = problem::bbob::Sphere(1, 2);
    auto p1 = problem::bbob::Sphere(1, 4);
    auto p2 = problem::bbob::AttractiveSector(1, 4);

    trigger::Always always;
    watch::TransformedY transformed_y;
    {
        auto logger = logger::FlatFile({always}, {transformed_y}, "IOH.dat", ".");

        logger.set_writer(writer);
        common::random::seed(1);
        const int runs = 3;
        const int samples = 30;

        for (auto pb : std::array<problem::BBOB *, 3>({&p0, &p1, &p2}))
        {
            pb->attach_logger(logger);
            for (auto r = 0; r < runs; ++r)
            {
                for (auto s = 0; s < samples; ++s)
                {
                    (*pb)(common::random::pbo::uniform(pb->meta_data().n_variables, s));
                }
                pb->reset();
            }
        }
    }
    EXPECT_TRUE(fs::exists("./IOH.dat"));
    auto data = ioh::common::file::as_string("./IOH.dat");
    //std::cout << data << std::endl;
    EXPECT_GT(data.size(), 0);
    fs::remove("./IOH.dat");
    EXPECT_TRUE(!fs::exists("./IOH.dat"));
    return data.size();
}

TEST_F(BaseTest, logger_flatfile) { 
    auto n1 = test_for_writer(std::make_shared<ioh::common::file::OFStream>());
    auto n2 = test_for_writer(std::make_shared<ioh::common::file::FWriter>());
    auto n3 = test_for_writer(std::make_shared<ioh::common::file::CachedFWriter>());
    auto n4 = test_for_writer(std::make_shared<ioh::common::file::FWriter>(4096));
    auto n5 = test_for_writer(std::make_shared<ioh::common::file::AsyncWriter>());
    auto n6 = test_for_writer(std::make_shared<ioh::common::file::AsyncWriter>(4096));
    auto n7 = test_for_writer(std::make_shared<ioh::common::file::AsyncWriter>(128, true));
    auto n8 = test_for_writer(std::make_shared<ioh::common::file::DirectIOWriter>(4096));
     
    EXPECT_TRUE(n1 == n2 && n2 == n3 && n3 == n4 && n4 == n5 && n5 == n6 && n6 == n7 && n7 == n8)
        << n1 << " " << n2 << " " << n3 << " " << n4 << " " << n5 << " " << n6 << " " << n7 << " " << n8;
}
