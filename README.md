Basic n-body sim developed for a university project. Usage is self-explanatory - if you have questions, see the quick start guide below. Feel free to reach out or open an issue with any questions!

### Quick start:
1. Clone the repo: git clone [https://github.com/bradyap/n-body](https://github.com/bradyap/n-body)
2. Cd into the project directory: cd n-body
3. Create a python venv for dependencies: python3 -m venv .venv
4. Activate the venv: source .venv/bin/activate
5. Install dependencies: pip install -r requirements.txt
6. Build the project: make
7. Run the simulation: python3 sim.py

Note: sim.py will only work on systems with a graphical interface. The benchmark functions (times.py, times_serial.py) and their associated plotting functions will work just fine without.

P.S. Euler integration sucks - this isn't intended to be an accurate physics simulation, just a proof of concept and demonstration of how CPU based parallelization works.
