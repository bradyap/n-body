# What os?
UNAME_S := $(shell uname -s)

# Py flags and suffix
PYINCLUDES := $(shell python3 -m pybind11 --includes)
PYSUFFIX := $(shell python3-config --extension-suffix)

CXX := c++
CXXFLAGS := -g -std=c++20 -fPIC -Wall -Wextra -Wpedantic -shared -fopenmp

# If macos specify dynamic lookup
ifeq ($(UNAME_S),Darwin)
    CXXFLAGS += -undefined dynamic_lookup
endif

TARGET := nbody_OpenMP$(PYSUFFIX)
SRC := nbody_OpenMP.cpp

all:
	$(CXX) $(CXXFLAGS) $(PYINCLUDES) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)