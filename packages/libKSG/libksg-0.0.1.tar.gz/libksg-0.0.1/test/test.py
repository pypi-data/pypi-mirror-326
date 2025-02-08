from libKSG import KSG
import numpy as np

n = 1_000;

theta = np.linspace(0, 2*np.pi, n)
phi = np.random.randn(n) + 10
x = phi * np.cos(theta)
y = phi * np.sin(theta)
ksg = KSG()
I = ksg.mi(x, y)

print(I)
