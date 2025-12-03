Basic n-body sim developed for a university project. Usage is self-explanatory - if you have questions, see the quick start guide below. Feel free to reach out or open an issue with any questions!

## Quick start
Clone the repo:
```bash
git clone https://github.com/bradyap/n-body
```
Cd into the project directory:
```bash
cd n-body
```
Create a python venv for dependencies:
```bash
python3 -m venv .venv
```
Activate the venv:
```bash
source .venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Build the project:
```bash
make
```
Run the simulation:
```bash
python3 sim.py
```

Note: sim.py will only work on systems with a graphical interface. The benchmark functions (times.py, times_serial.py) and their associated plotting functions will work just fine without.

P.S. Euler integration sucks - this isn't intended to be an accurate physics simulation, just a proof of concept and demonstration of how CPU based parallelization works.
