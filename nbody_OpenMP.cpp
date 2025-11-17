#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cmath>
#include <iostream>
#include <vector>
#include <thread>

namespace py = pybind11;

struct Body {
    double x, y, z; // Position
    double vx, vy, vz; // Velocity
    double m; // Mass
};

// Wrapper class for the vector of bodies
class BodiesContainer {
public:
    std::vector<Body> bodies;
    
    BodiesContainer(int n) : bodies(n) {}
    
    void set_body(int i, double x, double y, double z, double vx, double vy, double vz, double m) {
        if (i >= 0 && i < static_cast<int>(bodies.size())) {
            bodies[i] = {x, y, z, vx, vy, vz, m};
        }
    }
    
    Body get_body(int i) const {
        if (i >= 0 && i < static_cast<int>(bodies.size())) {
            return bodies[i];
        }
        return Body{};
    }
    
    int size() {
        return static_cast<int>(bodies.size());
    }

    void set_all(const std::vector<double>& x, const std::vector<double>& y, const std::vector<double>& z, 
    const std::vector<double>& vx, const std::vector<double>& vy, const std::vector<double>& vz, const std::vector<double>& m) {
        int n = static_cast<int>(bodies.size());
        for (int i = 0; i < n; ++i) {
            bodies[i] = {x[i], y[i], z[i], vx[i], vy[i], vz[i], m[i]};
        }
    }
};