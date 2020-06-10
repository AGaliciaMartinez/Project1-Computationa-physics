import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import matplotlib as mpl
import sys
sys.path.append('../scripts/')
from plot_utils import set_size

nice_fonts = {
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 14,
    "font.size": 16,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
}

mpl.rcParams.update(nice_fonts)

data1 = np.load('../script_output/protecting_carbon.npz')
data2 = np.load('../script_output/protecting_carbon_sequences_2.npz')
data4 = np.load('../script_output/protecting_carbon_sequences_4.npz')
data8 = np.load('../script_output/protecting_carbon_sequences_8.npz')
data16 = np.load('../script_output/protecting_carbon_sequences_16.npz')
data16_glued = np.load(
    '../script_output/protecting_carbon_sequences_16_glued.npz')

time1 = data1['time']
exp_mean1 = (data1['exp_mean'] + 1) / 2
exp_std1 = data1['exp_std'] / 2

time2 = data2['time']
exp_mean2 = data2['exp_mean']
exp_std2 = data2['exp_std']

time4 = data4['time']
exp_mean4 = data4['exp_mean']
exp_std4 = data4['exp_std']

time8 = data8['time']
exp_mean8 = data8['exp_mean']
exp_std8 = data8['exp_std']

time16 = np.concatenate((data16['time'], data16_glued['time']))
exp_mean16 = np.concatenate((data16['exp_mean'], data16_glued['exp_mean']))
exp_std16 = np.concatenate((data16['exp_std'], data16_glued['exp_std']))


def fitter(x, T, n, a):
    return (0.5 * np.exp(-np.power(x / T, n))) * a + 0.5


popt1, pcov1 = curve_fit(fitter,
                         time1,
                         exp_mean1,
                         p0=(750, 3, 1),
                         sigma=exp_std1)
popt2, pcov2 = curve_fit(fitter,
                         time2,
                         exp_mean2,
                         p0=(750, 3, 1),
                         sigma=exp_std2)
popt4, pcov4 = curve_fit(fitter,
                         time4,
                         exp_mean4,
                         p0=(750, 3, 1),
                         sigma=exp_std4)
popt8, pcov8 = curve_fit(fitter,
                         time8,
                         exp_mean8,
                         p0=(750, 3, 1),
                         sigma=exp_std8)
popt16, pcov16 = curve_fit(fitter,
                           time16,
                           exp_mean16,
                           p0=(750, 3, 1),
                           sigma=exp_std16)
print(popt2[0])
print(popt4[0])
print(popt8[0])
print(popt16[0])

times = np.logspace(0, 4, 100000)
fig, ax = plt.subplots(1, 1, figsize=set_size(width='report_full'))

# plt.errorbar(time1, exp_mean1, exp_std1, label='N=1', color='black')
# plt.plot(times, fitter(times, *popt1), '--', color='black')
plt.errorbar(time2, exp_mean2, exp_std2, label='N=2', color='orange', fmt='.')
plt.plot(times, fitter(times, *popt2), '-', color='orange')
plt.errorbar(time4, exp_mean4, exp_std4, label='N=4', color='blue', fmt='.')
plt.plot(times, fitter(times, *popt4), 'b-')
plt.errorbar(time8, exp_mean8, exp_std8, label='N=8', color='green', fmt='.')
plt.plot(times, fitter(times, *popt8), '-', color='green')
plt.errorbar(time16, exp_mean16, exp_std16, label='N=16', color='red', fmt='.')
plt.plot(times, fitter(times, *popt16), 'r-')
plt.title('Dynamical Decoupling of Carbon atoms')
plt.ylabel('Projection on x-axis')
plt.xlabel(r'$\tau$')
plt.xscale('log')
plt.xlim(40, 6000)
plt.legend()
plt.show()

N = [2, 4, 8, 16]
Ts = [popt2[0], popt4[0], popt8[0], popt16[0]]
Ts_err = [
    np.sqrt(pcov2[0, 0]),
    np.sqrt(pcov4[0, 0]),
    np.sqrt(pcov8[0, 0]),
    np.sqrt(pcov16[0, 0])
]


def scaling(N, frac, a):
    return a * N**frac


popt_T, pcov_T = curve_fit(scaling, N, Ts, p0=(2 / 3, 100), sigma=Ts_err)
print(popt_T[0])
print(np.sqrt(pcov_T[0]))

Ns = np.linspace(1.01, 20, 10)
fig, ax = plt.subplots(1, 1, figsize=(7, 3))
plt.errorbar(N, Ts, Ts_err)
plt.plot(Ns, scaling(Ns, popt_T[0], popt_T[1]), 'r--')
plt.title('Improved Protection through Decoupling')
plt.ylabel(r'Decoherence Time ($T_{1/e}$)')
plt.xlabel('Number of Decoupling Sequences Applied')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.show()
