# 🌀 Mass-Spring-Damper Simulator (Torch)

This project simulates a **mass-spring-damper** system using **PyTorch** for numerical integration and **Matplotlib** for visualization. It generates time-domain responses under various excitation types and saves the output as `.csv` and `.png`.

---

## 🧠 Background

A mass-spring-damper system is a classic second-order mechanical system governed by the ODE:

```
m.ẍ(t) + d.ẋ(t) + c.x(t) = F(t)
```

Where:
- `m` = mass  
- `d` = damping coefficient  
- `c` = spring stiffness  
- `F(t)` = external force (sin, step, square wave, impulse)  
- `x(t)` = displacement  
- `ẋ(t)` = velocity  
- `ẍ(t)` = acceleration

---

## 🛠️ Technologies Used

- 🐍 Python 3
- 🔥 PyTorch — for modeling and numerical integration
- 📊 Matplotlib — for plotting simulation results
- 📄 Pandas — for saving `.csv` files

---

## 📁 Project Structure

```
├── msd_simulator.py        # Main simulation script
├── README.md               # Project description
├── .gitignore              # Ensures sim_dataset/ is not tracked by Git
└── sim_dataset/            # Auto-generated output folder (plots + CSVs)
```

---

<details>
<summary><strong>⚙️ Simulation Settings</strong></summary>

### System Parameters

```python
params = {
  'm': 1.0,    # mass (kg)
  'd': 0.5,    # damping (Ns/m)
  'c': 4.0     # spring constant (N/m)
}
```

### Input Signal Types
- `sine`: smooth periodic signal
- `step`: jumps from 0 to 1 at t=1
- `square_wave`: toggles between -1 and 1
- `impulse`: sharp pulse at t=1

### Initial Conditions Used
- `[0.0, 1.0]`  
- `[1.0, 0.0]`  
- `[0.5, -0.5]`  
- `[0.0, 0.0]`  

</details>

---

<details>
<summary><strong>📤 Output Details</strong></summary>

- A total of **16 simulations** are performed: 4 inputs × 4 initial conditions
- Each result is saved in:
  - `.csv` with `time`, `x`, `xdot`
  - `.png` plot of displacement and velocity

### Output Folder
```
sim_dataset/
├── sine_x0_0.0_v0_1.0.csv
├── sine_x0_0.0_v0_1.0.png
├── ...
```

</details>

---

## ▶️ How to Run

```bash
# Step 1: Install dependencies
pip install torch matplotlib pandas

# Step 2: Run the simulation
python msd_simulator.py
```

> This creates a `sim_dataset/` folder in the **same directory as the script**.

---

## 🧪 Example Output Plot

Each plot includes:
- Displacement `x(t)`
- Velocity `ẋ(t)`

Example:
![Example](output.png)

---

## 📝 Notes

- Euler integration is used (explicit method).
- Easy to modify or extend for:
  - Nonlinear dynamics
  - Stochastic excitation
  - Custom simulation ranges

---

## 📚 References

- [Damped Harmonic Oscillator – Wikipedia](https://en.wikipedia.org/wiki/Damped_harmonic_oscillator)
- [PyTorch Docs](https://pytorch.org/docs/stable/index.html)
- [Matplotlib Docs](https://matplotlib.org/stable/contents.html)

---

## 📜 License

This repository is intended for educational and experimental use. Contributions are welcome!