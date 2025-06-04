import torch
import matplotlib.pyplot as plt
import pandas as pd
import os

# ------------------ System Parameters ------------------
# These define how the oscillator behaves
params = {
    'm': 1.0,   # mass (kg)
    'd': 0.5,   # damping coefficient (Ns/m)
    'c': 4.0    # spring stiffness (N/m)
}

# ------------------ Input Signal Functions ------------------
# Different kinds of force inputs applied to the system

def sin_input(t):
    """Smooth sinusoidal input"""
    return torch.sin(2 * torch.pi * 0.5 * t)

def step_input(t):
    """Step input turns on at t=1"""
    return torch.tensor(1.0) if t > 1 else torch.tensor(0.0)

def square_wave_input(t):
    """Alternating on/off square wave"""
    return torch.sign(torch.sin(2 * torch.pi * 0.2 * t))

def impulse_input(t):
    """Sharp impulse at t=1"""
    return torch.tensor(10.0) if abs(t - 1) < 0.01 else torch.tensor(0.0)

# ------------------ Oscillator Class ------------------
class Oscillator:
    def __init__(self, p, input_function):
        self.p = p  # System parameters (m, d, c)
        self.input_function = input_function  # External force function

    def f(self, x, t):
        """Compute derivatives of displacement and velocity"""
        m, d, c = self.p['m'], self.p['d'], self.p['c']
        x1, x2 = x[0], x[1]
        force = self.input_function(t)
        dx1 = x2
        dx2 = (force - d * x2 - c * x1) / m
        return torch.tensor([dx1, dx2])

    def step(self, x, t, dt):
        """Euler integration step"""
        dx = self.f(x, t)
        return x + dx * dt

    def predict(self, x0, t_span):
        """Simulate full trajectory over time"""
        dt = t_span[1] - t_span[0]
        x = torch.zeros((len(t_span), 2))  # [displacement, velocity]
        x[0] = x0
        for i in range(1, len(t_span)):
            x[i] = self.step(x[i - 1], t_span[i - 1], dt)
        return x

    def visualize(self, t_span, x, title=None, save_path=None):
        """Plot and optionally save the displacement and velocity"""
        plt.figure(figsize=(10, 5))

        # Displacement
        plt.subplot(2, 1, 1)
        plt.plot(t_span, x[:, 0], label='x(t)')
        plt.ylabel("Displacement x(t)")
        plt.grid(True)

        # Velocity
        plt.subplot(2, 1, 2)
        plt.plot(t_span, x[:, 1], label='ẋ(t)', color='orange')
        plt.ylabel("Velocity ẋ(t)")
        plt.xlabel("Time t")
        plt.grid(True)

        if title:
            plt.suptitle(title)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

# ------------------ Dataset Generation ------------------

# Create output folder in the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "sim_dataset")
os.makedirs(output_dir, exist_ok=True)

# Time vector: simulate for 20 seconds at high resolution
t = torch.linspace(0, 20, 2000)

# Initial conditions: different starting positions/velocities
initial_conditions = [
    torch.tensor([0.0, 1.0]),
    torch.tensor([1.0, 0.0]),
    torch.tensor([0.5, -0.5]),
    torch.tensor([0.0, 0.0])
]

# Dictionary of input functions and their labels
input_functions = {
    "sine": sin_input,
    "step": step_input,
    "square_wave": square_wave_input,
    "impulse": impulse_input
}

# Run simulations for all combinations of input and initial condition
for input_name, input_fn in input_functions.items():
    for x0 in initial_conditions:
        osc = Oscillator(params, input_fn)
        x_sim = osc.predict(x0, t)

        # Save CSV data
        filename_csv = os.path.join(
            output_dir,
            f"{input_name}_x0_{x0[0].item()}_v0_{x0[1].item()}.csv"
        )
        df = pd.DataFrame({
            'time': t.numpy(),
            'x': x_sim[:, 0].numpy(),
            'xdot': x_sim[:, 1].numpy()
        })
        df.to_csv(filename_csv, index=False)

        # Save graph image
        plot_title = f"{input_name} input | x0 = {x0[0].item()}, v0 = {x0[1].item()}"
        filename_png = os.path.join(
            output_dir,
            f"{input_name}_x0_{x0[0].item()}_v0_{x0[1].item()}.png"
        )
        osc.visualize(t, x_sim, title=plot_title, save_path=filename_png)

print("✅ All 16 simulations complete. CSVs and plots saved to:", output_dir)