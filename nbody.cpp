#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cmath>
#include <iostream>
#include <vector>

namespace py = pybind11;

struct Body {
    double x, y, z;     // position
    double vx, vy, vz;  // velocity
    double m;           // mass
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
};

void compute_forces_serial(BodiesContainer& container, double dt, double G) {
    auto& bodies = container.bodies;
    int n = static_cast<int>(bodies.size());

    // Compute accelerations for each body
    for (int i = 0; i < n; ++i) {
        double ax = 0.0, ay = 0.0, az = 0.0;

        for (int j = 0; j < n; ++j) {
            if (i == j) continue;

            double dx = bodies[j].x - bodies[i].x;
            double dy = bodies[j].y - bodies[i].y;
            double dz = bodies[j].z - bodies[i].z;

            double r2 = dx*dx + dy*dy + dz*dz + 1e-10;
            double r = std::sqrt(r2);
            double invr3 = 1.0 / (r * r * r);
            double accel_coeff = G * bodies[j].m * invr3;

            ax += accel_coeff * dx;
            ay += accel_coeff * dy;
            az += accel_coeff * dz;
        }

        // update velocity from accel
        bodies[i].vx += ax * dt;
        bodies[i].vy += ay * dt;
        bodies[i].vz += az * dt;
    }

    // update positions after all velocities are updated
    for (auto& b : bodies) {
        b.x += b.vx * dt;
        b.y += b.vy * dt;
        b.z += b.vz * dt;
    }
}

PYBIND11_MODULE(nbody, m) {
    m.doc() = "N-body simulation module";

    py::class_<Body>(m, "Body")
        .def(py::init<>())
        .def_readwrite("x", &Body::x)
        .def_readwrite("y", &Body::y)
        .def_readwrite("z", &Body::z)
        .def_readwrite("vx", &Body::vx)
        .def_readwrite("vy", &Body::vy)
        .def_readwrite("vz", &Body::vz)
        .def_readwrite("m", &Body::m);
    
    py::class_<BodiesContainer>(m, "BodiesContainer")
        .def(py::init<int>())
        .def("set_body", &BodiesContainer::set_body)
        .def("get_body", &BodiesContainer::get_body)
        .def("size", &BodiesContainer::size);
    
    m.def("compute_forces_serial", &compute_forces_serial);
}