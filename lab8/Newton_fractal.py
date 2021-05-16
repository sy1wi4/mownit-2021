import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


eps = 1.e-8

def newton(z0, f, der, MAX_IT=1000):
    # MAX_IT - max number of iterations

    z = z0
    for _ in range(MAX_IT):
        dz = f(z)/der(z)
        if abs(dz) < eps:
            return z
        z -= dz
    return False

def plot_newton_fractal(f, der, n=200, domain=(-1, 1, -1, 1)):

    roots = []
    m = np.zeros((n, n))

    def get_root_index(roots, r):
        try:
            return np.where(np.isclose(roots, r, atol=eps))[0][0]
        except IndexError:
            roots.append(r)
            return len(roots) - 1


    xmin, xmax, ymin, ymax = domain
    for ix, x in enumerate(np.linspace(xmin, xmax, n)):
        for iy, y in enumerate(np.linspace(ymin, ymax, n)):
            z0 = x + y*1j
            r = newton(z0, f, der)
            if r is not False:
                ir = get_root_index(roots, r)
                m[iy, ix] = ir
    
    plt.imshow(m, cmap='afmhot', origin='lower')
    plt.axis('off')
    plt.show()


f = lambda z: z**12 - 1
der = lambda z: 12*z**11

# n**2 - number of points
plot_newton_fractal(f, der, n=500, domain = (-1.5,1.5,-1.5,1.5))


# f = lambda z: (z-2)*(z-1/2)*(z+3/2)*(z+2)
# der = lambda z: -4 - (19*z)/2 + 3*z**2 + 4*z**3

# # n**2 - number of points
# plot_newton_fractal(f, der, n=500, domain = (1.23,1.45,-0.1,0.1))