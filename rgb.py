import numpy as np
import matplotlib.pyplot as plt

# max discrepancy in nm
max_d = 2000
# box size for plotting
nx = max_d
ny = int(nx / 1.1)

# add the discrepancy in the oil layer
d = max_d * 1.5 ** (-np.linspace(0, 5, max_d))
d = d[::-1]

# wavelength array for calculation
ll = range(380, 780, 10)  # in nm
nl = len(ll)

# GEN. the phase of EMW
xspace = np.linspace(0, 4 * np.pi, 1000)

# RGB 색상 변환 함수 정의
def rgb(wavelength):
    gamma = 2.2
    intensity_max = 255
    factor = 0.0
    R, G, B = 0, 0, 0

    if 380 <= wavelength <= 435:
        R = -(wavelength - 440) / (440 - 380)
        G = 0.0
        B = 0.8
    elif 435 <= wavelength <= 485:
        R = 0.0
        G = (wavelength - 435) / (485 - 435)
        B = 0.8
    elif 485 <= wavelength <= 500:
        R = 0.0
        G = 0.8
        B = -(wavelength - 500) / (500 - 485)
    elif 500 <= wavelength <= 570:
        R = (wavelength - 500) / (570 - 500)
        G = 0.8
        B = 0.0
    elif 570 <= wavelength <= 645:
        R = 0.8
        G = -(wavelength - 645) / (645 - 570)
        B = 0.0
    elif 645 <= wavelength <= 780:
        R = 0.8
        G = 0.0
        B = 0.0

    # Intensity adjustment
    if 380 <= wavelength <= 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 <= wavelength <= 645:
        factor = 1.0
    elif 645 <= wavelength <= 780:
        factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 645)

    R = int(intensity_max * (R * factor) ** gamma)
    G = int(intensity_max * (G * factor) ** gamma)
    B = int(intensity_max * (B * factor) ** gamma)

    return (R / 255, G / 255, B / 255)

# Apply interference into RGB-power for all wavelengths
line = np.zeros([nx, 3])
for i in range(nx):
    for j in range(nl):
        wave = np.sin(xspace) + np.sin(xspace - 2 * np.pi * d[i] / ll[j])
        line[i, 0] += np.sum(wave ** 2) * rgb(ll[j])[0]
        line[i, 1] += np.sum(wave ** 2) * rgb(ll[j])[1]
        line[i, 2] += np.sum(wave ** 2) * rgb(ll[j])[2]
##########
# Normalize the intensities
for j in range(3):
    line[:, j] = line[:, j] / np.max(line[:, j])

# Plot the relative intensity for each RGB color
plt.close('all')
fig1, (ax1, ax2) = plt.subplots(num=1, nrows=2, figsize=(8, 10))

ax1.plot(d, line[:, 0], '#fa8072', label='R')
ax1.plot(d, line[:, 1], 'limegreen', label='G')
ax1.plot(d, line[:, 2], 'deepskyblue', label='B')
ax1.set_xlabel("path length difference [nm]")
ax1.set_ylabel('intensity')
ax1.legend()
ax1.grid()

# Plot the color image with RGB colors
img = np.zeros([nx, ny, 3])
for k in range(ny):
    for j in range(3):
        img[:, k, j] = line[:, j]  # Corrected assignment

ax2.imshow(img)
ax2.set_ylabel("path length difference [nm]")
plt.show()