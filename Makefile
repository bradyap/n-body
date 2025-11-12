CXX = g++
CXXFLAGS = -g -std=c++20 -fPIC -Wall -Wextra -Wpedantic -Wshadow -shared -undefined dynamic_lookup
PYINCLUDES = $(shell python3 -m pybind11 --includes)
PYSUFFIX = $(shell python3-config --extension-suffix)

all:
	$(CXX) $(CXXFLAGS) $(PYINCLUDES) nbody.cpp -o nbody$(PYSUFFIX)

clean:
	rm -f nbody$(PYSUFFIX)