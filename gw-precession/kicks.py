# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import scipy
import matplotlib.pyplot as plt

MEDIUM_SIZE = 18
BIGGER_SIZE = 22

plt.rcdefaults()

# plt.rc('font',**{'family':'serif','serif':['Times']})
# plt.rc('text', usetex=True)

plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


# %matplotlib inline

# %%
import precession as prec

# fig,ax = plt.subplots(ncols=1, nrows=1, figsize=(6,4))

# ax.plot([],[])

# ax.grid(True,linestyle=':',linewidth='1.')
# ax.xaxis.set_ticks_position('both')
# ax.yaxis.set_ticks_position('both')
# ax.tick_params('both',length=3,width=0.5,which='both',direction = 'in',pad=10)


# ax.set_xlabel('time (s)')
# ax.set_ylabel('amplitude')

# ax.legend();

# %%
rng = np.random.default_rng()

num = 200

# theta1 = np.arccos(-1 + 2*rng.uniform(size=num))
# theta2 = np.arccos(-1 + 2*rng.uniform(size=num))
# dphi = 2*np.pi*rng.uniform(size=num)

theta1 = np.linspace(0,np.pi,num)
theta2 = np.linspace(0,np.pi,num)

dphi = np.full_like(theta2, np.pi)
q = np.full_like(theta2, 1.)
chi1 = np.full_like(theta2, 0.7)
chi2 = np.full_like(theta2, 0.7)

vk = []

for thth in theta1:
    arr = np.full_like(theta2, thth)
    kick = prec.remnantkick(
        arr, theta2, dphi, q, chi1, chi2, 
        kms=True, maxphase=True,
        superkick=True,
        hangupkick=True,
        crosskick=True
    )
    vk.append(kick)

vk = np.array(vk)

vmax = vk.max()

# %%
from matplotlib.colors import LogNorm, Normalize

fig,ax = plt.subplots(ncols=1, nrows=1, figsize=(8,5))

cax = ax.pcolor(
    *np.meshgrid(theta1,theta2), vk,
    shading='auto', norm=Normalize(),
)

nlevel = np.floor(vmax/1000)

CS = ax.contour(
    *np.meshgrid(theta1,theta2), vk, 1000*np.arange(1,nlevel+1),
    colors='white'
)

ax.clabel(CS, CS.levels, fontsize=15)

ax.grid(True,linestyle=':',linewidth='1.')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
ax.tick_params('both',length=3,width=0.5,which='both',direction = 'in',pad=10)

ax.set_xticks(np.linspace(0,np.pi,5))
ax.set_yticks(np.linspace(0,np.pi,5))



ax.set_xlabel('$\\theta_1$')
ax.set_ylabel('$\\theta_2$')

ax.set_aspect('equal')

ax.set_title('$v_{{\\rm max}}={:d}$ km/s'.format(int(vmax)))

fig.colorbar(cax, ax=ax)

#ax.legend(loc='upper right');

# %%
