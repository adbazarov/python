import pandas as pd
import pathlib
from pathlib import Path
from pyproj import Proj
from pyproj import Transformer
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#from datetime import datetime
import datetime
import scipy.signal
from scipy.interpolate import CubicSpline
def read_line_file(name=''):
    headers=['x','depth','Vel']
    dtypes={'x':float,'depth':float,'Vel':float}
    print(name)
    data = pd.read_csv(name,sep='\t', names=headers,  dtype =dtypes)
    return data
def annot_max(x,y, ax=None):
    maxIxVal = np.argmax(y);
    zeroBasedIx = np.argwhere(y.index==maxIxVal).flatten()[0];
    xmax = x[zeroBasedIx];
    ymax = y.max()
    text= "k={:d}, measure={:.3f}".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="round,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="-",connectionstyle="arc3,rad=0.1")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.90), **kw)
def main():
    print('main')
    work_path = pathlib.Path.cwd()
    print(work_path)
    Fname='Bub_SP26_25.txt'
    data=read_line_file(Fname)
    print(data.head())
    #data['Vel'].plot.hist(bins=30)
    #ax = data.plot()
    fig = plt.figure()

    ax1 = fig.add_subplot(111,label='1')
    ax2 = ax1.twinx()#fig.add_subplot(111,label='3')#,frame_on=False)
    rangex=[float(i) for i in np.arange(0, 7, 0.05)]
    pl=data['Vel'].plot.density(color='green',bw_method=0.1,ind=rangex,ax=ax1)#hist(bins=30)
    density = np.histogram(data['Vel'], density=True)

    print(density)
    ax2.xaxis.tick_bottom()
    ax2.yaxis.tick_left()
    ax1.set_xlim([0, 7])
    ax1.set_xlabel('Скорость км/с', color="C0")
    ax1.set_title(Fname )
    ax1.set_ylabel('Плотность', color="C0")
    #annot_max(df[data['Vel'], data['Vel']], pl);


    data['Vel'].plot.hist(bins=30,ax=ax2)
    ax2.set_ylabel('Частота', color="C0")
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(0.2))

    ax2.set_xlim([0, 7])
    #   data.groupby('Vel').count().plot()
    #plt.text(1, 35, 'Hello World !')
    plt.show()

   # fig2 = plt.figure()
    #X=data['x']
    #Y=data['depth']
    #Z=data['Vel']
    #print(X)
    #contours = plt.contour(X, Y, Z, 3, colors='black')
    #plt.clabel(contours, inline=True, fontsize=8)
    #plt.imshow(Z, extent=[0, 5, 0, 5], origin='lower', cmap='RdGy', alpha=0.5)
    #plt.colorbar();
    #plt.show()




    

if __name__=='__main__':
    main()
