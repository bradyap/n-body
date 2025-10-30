CXX = g++
CXXFLAGS = -g -std=c++20 -fPIC -Wall -Wextra -Wpedantic -Wshadow 

all: libnbody.so

libnbody.so: nbody.cpp
	$(CXX) $(CXXFLAGS) -shared nbody.cpp -o libnbody.so

clean:
	rm -f libnbody.so