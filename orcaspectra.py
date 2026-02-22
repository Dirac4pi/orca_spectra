'''
This script is used to visualize ORCA UV-Vis absorption spectra and distinguish
the contribution of each root to the total spectrum.
coding:UTF-8
env:vis2c
'''

import sys
import numpy as np
import matplotlib.pyplot as plt

rootscolor = ['#1668a7', '#2b74ad', '#4181b4', '#578dbb', '#6c9ac1', \
              '#82a6c8', '#98b3cf', '#adbfd5', '#c3ccdc']

def orcaspectra(spec_files=None) -> None:
  '''
  plot (multi) UV-Vis absorption spectra based on ORCA calculation.
  --
  :orcaspectra: ORCA absorption spectra files
  '''
  plt.figure(figsize=(10, 6))
  for f in spec_files:
    try:
      try:
        data = np.loadtxt(f)
      except ValueError:
        data = np.loadtxt(f, skiprows=1)
      if data.ndim != 2 or data.shape[1] < 2:
        print(f"Warning: {f} does not contain at least two columns.")
        continue
      energy = data[:, 0]
      spectrum = data[:, 1]
      if (f.endswith('spectrum')):
        label = 'total spectrum'
        color = '#005ba0'
      elif (f.find('spectrum.root') != -1):
        label = 'individual spectrum of state '+str(f.split('.root')[-1])
        color = rootscolor[int(f.split('.root')[-1])-1] \
          if int(f.split('.root')[-1]) <= len(rootscolor) else None
      else:
        # For unrecognized files: use filename as label and default color
        label = f
        color = None
      plt.plot(energy, spectrum, linewidth=2, label=label, color=color)
    except Exception as e:
      print(f"Error when loading {f}: {e}")
      continue
  plt.xlabel('Wavelength / nm')
  plt.ylabel('Absorbance')
  plt.legend()
  plt.tight_layout()
  plt.show()

if __name__ == "__main__":
  args = sys.argv[1:]
  if not args:
    print("Error: No spectra files provided.")
    print("Usage: python orcaspectra.py 1.spectrum 1.spectrum.root1 ...")
    sys.exit(1)
  orcaspectra(args)