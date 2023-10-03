

You might get this error message:
```sh
CMake Error at CMakeLists.txt:52 (add_subdirectory):
  The source directory

    /home/dimitri/Selbstgemachte_Software/IOHexperimenter/external/fmt

  does not contain a CMakeLists.txt file.
```

In this case, run:
```sh
git submodule
git submodule init
git submodule update
```

In fact, the first, of the three commands above, will give:
```sh
-32e70c1b3454a9411de2ae8d23020e08f5381f11 external/MkLandscape
-1dcb44e79a17e703e024594487b3a442d87e4741 external/cxxopts
-7df30f91aee5444a733cec0b911d21cebdeb62ae external/fmt
-6a7ed316a5cdc07b6d26362c90770787513822d4 external/googletest
-bc889afb4c5bf1c0d8ee29ef35eaaf4c8bef8a5d external/json
-80dc998efced8ceb2be59756668a7e90e8bef917 external/pybind11
```

```sh
# parentheses only work in the fish shell
sudo chown -R (id -un):(id -gn) /home/dimitri/Selbstgemachte_Software/IOHexperimenter/
sudo chmod -R 700 /home/dimitri/Selbstgemachte_Software/IOHexperimenter/
```

```sh
git clone git@github.com:Habimm/IOHexperimenter.git
git submodule
git submodule init
git submodule update
sudo chown -R (id -un):(id -gn) /home/dimitri/Selbstgemachte_Software/IOHexperimenter/
sudo chmod -R 700 /home/dimitri/Selbstgemachte_Software/IOHexperimenter/
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=./IOHexperimenter_headers ..
cd ..
sudo make install
```

To search for files under the current directory tree with a specific content:
```sh
grep -r "local_ioh"
```

To search for files under the current directory tree with a specific filename:
```sh
find . -iname "*local_ioh*"
```

To compile a file that uses the IOHexperimenter problems:
```sh
g++ -std=c++17 -I../external/fmt/include -I../include -o one_max one_max.cpp
```

```sh
set project_root /home/dimitri/code/IOHexperimenter
set fmt_include_path $project_root/external/fmt/include
set ioh_include_path $project_root/include

g++ -o one_max -g -std=c++17 -I$fmt_include_path -I$ioh_include_path one_max.cpp
./one_max
```

```sh
g++ -o one_max -g -std=c++17 -I$fmt_include_path -I$ioh_include_path one_max.cpp; and ./one_max
```

g++ version
```
g++ 9.4.0
```

Build everything:
```sh
git clone git@github.com:Habimm/IOHexperimenter.git
cd IOHexperimenter
git submodule
git submodule init
git submodule update
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=./IOHexperimenter_headers ..
cd ..
sudo make install
```

Single Objective Bound Constrained Benchmark
CEC functions
definitions
pdf
```sh
https://github.com/P-N-Suganthan/2022-SO-BO
```

Prompt for writing CEC functions
```sh
void levy_func (double *x, double *f, int nx, double *Os,double *Mr, int s_flag, int r_flag) /* Levy */
{
    int i;
  f[0] = 0.0;
  sr_func (x, z, nx, Os, Mr,1.0, s_flag, r_flag); /* shift and rotate */

  double *w;
  w=(double *)malloc(sizeof(double)  *  nx);

  double sum1= 0.0;
  for (i=0; i<nx; i++)
  {
     w[i] = 1.0 + (z[i] - 0.0)/4.0;
  }

  double term1 = pow((sin(PI*w[0])),2);
  double term3 = pow((w[nx-1]-1),2) * (1+pow((sin(2*PI*w[nx-1])),2));

  double sum = 0.0;

  for (i=0; i<nx-1; i++)
  {
    double wi = w[i];
        double newv = pow((wi-1),2) * (1+10*pow((sin(PI*wi+1)),2));
    sum = sum + newv;
  }

  f[0] = term1 + sum + term3;// - 1.442600987052770; // - 1.442600987052770
  free(w);   // ADD THIS LINE to free memory! Thanks for Dr. Janez
}
rewrite this in the style of this:
        double evaluate(const std::vector<double> &x) override
        {
            auto sum1 = 0.0, sum2 = 0.0;
            for (const auto xi : x)
            {
                sum1 += cos(2.0 * IOH_PI * xi);
                sum2 += xi * xi;
            }
            if (std::isinf(sum2)) { return sum2; }

            auto result = 10.0 * (static_cast<double>(x.size()) - sum1) + sum2;
            std::cout << "result: " << result << std::endl;

            return result;
        }
ignore sr_func, further down the line replace z with x, the f will be returned as a double rather than its memory changed with a pointer
```

lint C++-17 code
```sh
# put the .clang-format file in the same directory
clang-format -i -style=llvm functions.hpp
```

Test Python bindings
```sh
conda activate ./.conda_environment
pip install -e .
ipython3
from ioh import problem
help(problem)
```

```sh
sudo apt install doxygen

conda activate ./.conda_environment
pip install breathe xmltodict sphinx sphinx-automodapi furo

cd /home/dimitri/code/IOHexperimenter/build
cmake -DBUILD_DOCS=ON ..
make doc
cd ..
ipython3 doc/generate_docs.py
```

```sh
true
git clone git@github.com-Habimm:Habimm/IOHexperimenter.git
cd IOHexperimenter
and git submodule
and git submodule init
and git submodule update
and . INSTALL
and conda activate ./.conda_environment
and pip install .
and cd ~
and ipython3 /home/dimitri/code/IOHexperimenter/tests/python/test_cec_functions.py
```

On a freshly cloned repo:
```sh
Step 1: Clone repo.
Step 2: Update git submodules.
Step 3: Install virtual environment.
Step 4: Install ioh package.
Step 5: Create .env file with a path to the static/ folder.
Step 6: Source .env.
Step 7: Run Python script.
```

```sh
echo "IOH_RESOURCES=/home/dimitri/code/IOHexperimenter/static" > .env
for line in (cat .env)
  set -x (echo $line | cut -d '=' -f 1) (echo $line | cut -d '=' -f 2-)
end
```

```sh
true
and git clone git@github.com-Habimm:Habimm/IOHexperimenter.git
and cd IOHexperimenter
and git submodule
and git submodule init
and git submodule update
and ./INSTALL_IOH
ln -fs (pwd)/static/cec_transformations build/tests/input_data
and echo "IOH_RESOURCES=/home/dimitri/code/IOHexperimenter/static" > .env
and ./RUN
```

```sh
./INSTALL_IOH
ln -fs (pwd)/static/cec_transformations build/tests/input_data
./RUN
```




==============================================================================================================
# Über submodulare Probleme

Die MaxCoverage-Klasse erbt von der Problem-Klasse, welche ein constraints_ Objekt hat. Da drin können mehrere Constraint-Objekte untergebracht werden. Ein Constraint-Objekt kann unter anderem ein GraphConstraint-Objekt sein. Ein GraphConstraint-Objekt besteht aus Knoten und Kanten. Man kann ein GraphConstraint-Objekt evaluieren, indem man erst die GraphConstraint::compute_violation Methode aufruft und dann im Attribut violation_ nachschaut. Wenn man aufruft, bekommt einen bool-Wert, ob die gegebene Teilmenge bezüglich der Kosten ein Budget nicht überschreitet. Den Kostenwert selbst kriegt man, wenn man im violation_ Attribut nachschaut. Da drin nachschauen über Python geht, indem man sagt:
```
f.constraints[0].violation
```

Und aufrufen kann man:
```
X = [0, 0, 1]
f.constraints[0].compute_violation(X)
```

Beachte, dass wir das erste Element aus dem Constraints-Objekt herausnehmen, welches einer Liste ähnelt. Das erste Element ist das einzige Constraint, welches in dem Optimierungsproblem enthalten ist. Dieses einzige Constraint ist ein GraphConstraint.
==============================================================================================================

```sh
You can write a Python script. This script will receive a run ID as an input from the command line argument. The Python script might choose to behave differently depending on the run ID.

You can write a shell script. The shell script specifies how the PBS process will be created and which run IDs the Python script should be used with to create Python processes. The PBS process will create a Python process using a Python script and a run ID number. Then, there will be one Python process created for each run ID. Each run ID will be specified in the shell script.

There might 100 run IDs.

PBS will launch the jobs. Each Python process is called a "job". You can list the jobs by saying 'qstat'.
```
