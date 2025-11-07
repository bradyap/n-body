#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <thread>
#ifdef _OPENMP
#include <omp.h>
#endif

struct Body {
    double x, y, vx, vy, m;
};

void compute_forces_serial(std::vector<Body>& b, double dt) {
    const double G = 6.674e-11;
    int N = b.size();
    for (int i = 0; i < N; ++i) {
        double fx = 0.0, fy = 0.0;
        for (int j = 0; j < N; ++j) {
            if (i == j) continue;
            double dx = b[j].x - b[i].x;
            double dy = b[j].y - b[i].y;
            double r2 = dx*dx + dy*dy + 1e-9;
            double f = G * b[i].m * b[j].m / r2;
            double invr = 1.0 / std::sqrt(r2);
            fx += f * dx * invr;
            fy += f * dy * invr;
        }
        b[i].vx += fx / b[i].m * dt;
        b[i].vy += fy / b[i].m * dt;
    }
    for (auto& bi : b) {
        bi.x += bi.vx * dt;
        bi.y += bi.vy * dt;
    }
}

// TODO: Parallelize outer loop with std::thread

// TODO: Parallelize outer loop with OpenMP

int main() {
    const int N = 1000;
    std::vector<Body> bodies(N);
    for (auto& b : bodies)
        b = {drand48(), drand48(), 0, 0, 1e10};

    auto start = std::chrono::high_resolution_clock::now();
    compute_forces_serial(bodies, 1e-3);
    auto end = std::chrono::high_resolution_clock::now();

    std::cout << "Serial N-body step time: "
              << std::chrono::duration<double>(end - start).count() << " s\n";
}
