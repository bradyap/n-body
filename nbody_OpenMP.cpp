#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "nbody_OpenMP.h"

#include <cmath>
#include <iostream>
#include <vector>
#include <thread>
#include <omp.h>

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

void compute_forces_serial(BodiesContainer& container, double dt, double G) {
    auto& bodies = container.bodies;
    int n = static_cast<int>(bodies.size());

    // Compute accelerations for each body
    for (int i = 0; i < n; ++i) { // Iterate through each body
        double ax = 0.0, ay = 0.0, az = 0.0; // Stores accel temporarily

        for (int j = 0; j < n; ++j) { // Iterate through all other bodies (not i)
            if (i == j) continue;

            // Distance components between bodies i and j 
            double dx = bodies[j].x - bodies[i].x;
            double dy = bodies[j].y - bodies[i].y;
            double dz = bodies[j].z - bodies[i].z;

            // Compute gravitational acceleration on body i due to body j
            double r2 = dx*dx + dy*dy + dz*dz + 1e-10;
            double r = std::sqrt(r2);
            double invr3 = 1.0 / (r * r * r);
            double accel_coeff = G * bodies[j].m * invr3;

            // Apply acceleration components
            ax += accel_coeff * dx;
            ay += accel_coeff * dy;
            az += accel_coeff * dz;
        }

        // Update velocity from accel
        bodies[i].vx += ax * dt;
        bodies[i].vy += ay * dt;
        bodies[i].vz += az * dt;
    }

    // Update positions after all velocities are updated
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        bodies[i].x += bodies[i].vx * dt;
        bodies[i].y += bodies[i].vy * dt;
        bodies[i].z += bodies[i].vz * dt;
    }

}

void compute_forces_open_mp(BodiesContainer& container, double dt, double G, int number_threads) {
    auto& bodies = container.bodies;
    int n = static_cast<int>(bodies.size());

    #pragma omp parallel num_threads(number_threads)
    {
        #pragma omp for
        for (int i = 0; i < n; ++i) { // Iterate through each body
            double ax = 0.0, ay = 0.0, az = 0.0; // Stores accel temporarily

            for (int j = 0; j < n; ++j) { // Iterate through all other bodies (not i)
                if (i == j) continue;

                // Distance components between bodies i and j 
                double dx = bodies[j].x - bodies[i].x;
                double dy = bodies[j].y - bodies[i].y;
                double dz = bodies[j].z - bodies[i].z;

                // Compute gravitational acceleration on body i due to body j
                double r2 = dx*dx + dy*dy + dz*dz + 1e-10;
                double r = std::sqrt(r2);
                double invr3 = 1.0 / (r * r * r);
                double accel_coeff = G * bodies[j].m * invr3;

                // Apply acceleration components
                ax += accel_coeff * dx;
                ay += accel_coeff * dy;
                az += accel_coeff * dz;
            }

        // Update velocity from accel
        bodies[i].vx += ax * dt;
        bodies[i].vy += ay * dt;
        bodies[i].vz += az * dt;
        }
    }
    for (auto& b : bodies) {
        b.x += b.vx * dt;
        b.y += b.vy * dt;
        b.z += b.vz * dt;
    }

}

PYBIND11_MODULE(nbody_OpenMP, m) {
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
        .def("size", &BodiesContainer::size)
        .def("set_all", &BodiesContainer::set_all);

    m.def("compute_forces_serial", &compute_forces_serial, "Computes gravitational forces serially");
    m.def("compute_forces_OpenMP", &compute_forces_open_mp, "Computes gravitational forces using OpenMP");
}