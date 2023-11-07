#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <filesystem>
#include <iostream>
#include <string>
#include <vector>

namespace fs = std::filesystem;


const size_t PAGE_SIZE = sysconf(_SC_PAGESIZE);

struct CachedFile
{
    fs::path path;
    FILE *file_ptr;
    std::vector<char> buffer;

    CachedFile() : file_ptr(NULL) {}

    CachedFile(const fs::path &path) : path(path), file_ptr(fopen(path.c_str(), "a")), buffer{}
    {
        if (file_ptr == NULL)
        {
            std::cout << strerror(errno) << std::endl;
        }
    }

    ~CachedFile()
    {
        if (is_open())
        {
            std::cout << path << " closing buffer size: " << buffer.size() << std::endl;
            auto ret = fwrite(buffer.data(), sizeof(char), buffer.size(), file_ptr);
            if (ret != buffer.size())
            {
                std::cout << strerror(errno) << std::endl;
            }
            std::cout << ret << " bytes written\n";
            fclose(file_ptr);
            buffer.clear();
        }
    }

    bool is_open() const { return file_ptr != NULL; }

    void operator()(const char *data, const size_t size)
    {
        buffer.insert(buffer.end(), data, data + size);
        if (buffer.size() >= PAGE_SIZE)
        {
            const size_t size = (buffer.size() / PAGE_SIZE) * PAGE_SIZE;
            auto ret = fwrite(buffer.data(), sizeof(char), size, file_ptr);
            if (ret != buffer.size())
            {
                std::cout << strerror(errno) << std::endl;
            }
            buffer.erase(buffer.begin(), buffer.begin() + size);
        }
    }

    void operator()(const std::string &s)
    {
        // std::cout << path << ": " << s << std::endl;
        operator()(s.data(), s.size());
    }
};


int main()
{
    CachedFile f("a.dat");
    std::string s = "hallo\n";


    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
    f(s);
}