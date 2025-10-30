#include <vector>
#include <cmath>
#include <iostream>

extern "C" { // Use plain c linkage so we can call from py with ctypes

const double G = 1; // Gravitational constant
// 6.674e-11

void step(double* mass, double* pos, double* vel, int n, double dt, double G) {
    // pos and vel are flattened arrays of size 3*n
    std::vector<double> accel(n * 3, 0.0); // Temporary accelerations array

    // Compute accelerations for each body
    for (int i = 0; i < n; ++i) {
        // Position of body i
        double xi = pos[3*i];
        double yi = pos[3*i + 1];
        double zi = pos[3*i + 2];

        // These will store accel as we calculate them
        double ax = 0.0;
        double ay = 0.0;
        double az = 0.0;

        for (int j = 0; j < n; ++j) {
            if (i != j) { // Iterating through all other bodies
                // Position of body j
                double xj = pos[3*j];
                double yj = pos[3*j + 1];
                double zj = pos[3*j + 2];

                // 3d dist components
                double dx = xj - xi;
                double dy = yj - yi;
                double dz = zj - zi;

                double distSqr = dx*dx + dy*dy + dz*dz + 1e-10; // r^2, adding a small term to avoid div by 0
                double r = std::sqrt(distSqr); // r
                double invr3 = 1.0 / (r * r * r); // 1/r^3

                double f = G * mass[j] * invr3; // Gravitational force magnitude

                // Apply force to accel components for body i
                ax += f * dx;
                ay += f * dy;
                az += f * dz;
            }
        }

        // Store computed acceleration
        accel[3*i] = ax;
        accel[3*i + 1] = ay;
        accel[3*i + 2] = az;
    }

    // Update velocities and positions
    for (int i = 0; i < n; ++i) {
        // Update velocity from accel: v = v + a*dt
        vel[3*i] += accel[3*i] * dt;
        vel[3*i + 1] += accel[3*i + 1] * dt;
        vel[3*i + 2] += accel[3*i + 2] * dt;

        // Update position from velocity: x = x + v*dt
        pos[3*i] += vel[3*i] * dt;
        pos[3*i + 1] += vel[3*i + 1] * dt;
        pos[3*i + 2] += vel[3*i + 2] * dt;
    }
}

}