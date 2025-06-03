import torch
import matplotlib.pyplot as plt


m, d, c = 1.0, 0.5, 4.0
t = torch.linspace(0, 10, 1000)
dt = t[1] - t[0]


def F(t): return torch.sin(2 * torch.pi * 0.5 * t)


def state_derivative(x, t_i):
    x1, x2 = x[0], x[1]
    force = F(t_i)
    dx1 = x2
    dx2 = (force - d * x2 - c * x1) / m
    return torch.tensor([dx1, dx2])


x = torch.zeros((len(t), 2))
x[0, 0] = 0.0
x[0, 1] = 1.0


for i in range(1, len(t)):
    dx = state_derivative(x[i-1], t[i-1])
    x[i] = x[i-1] + dx * dt


plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t, x[:, 0])
plt.ylabel("Displacement x(t)")
plt.grid(True)


plt.subplot(2, 1, 2)
plt.plot(t, x[:, 1])
plt.ylabel("Velocity ẋ(t)")
plt.xlabel("Time t")
plt.grid(True)
plt.tight_layout()
plt.show()