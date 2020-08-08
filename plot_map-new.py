import matplotlib.pyplot as plt
from obspy.imaging.beachball import beach
from obspy.geodetics.base import gps2dist_azimuth
import numpy as np
from mpl_toolkits.basemap import Basemap
from plotting_topo import plot_topo, plot_topo_netcdf
import pandas as pd
import glob



etopo_file = "/Users/utpalkumar50/Documents/bin/ETOPO1_Bed_g_gmt4.grd"

lonmin, lonmax = 60, 95
latmin, latmax = 0, 25
# lonmin, lonmax = 162, 170
# latmin, latmax = -14, -8

fig = plt.figure(figsize=(10,6))
axx = fig.add_subplot(111)
# m = Basemap(projection='merc', resolution="f", llcrnrlon=150, llcrnrlat=-12, urcrnrlon=170, urcrnrlat=-8)
m = Basemap(projection='merc', resolution="f", llcrnrlon=lonmin, llcrnrlat=latmin, urcrnrlon=lonmax, urcrnrlat=latmax)
# cs = plot_topo_netcdf(m,etopo_file,cmap='terrain',lonextent=(lonmin, lonmax),latextent=(latmin, latmax),zorder=0)
cs = plot_topo(m,cmap=plt.cm.jet,zorder=2,lonextent=(lonmin, lonmax),latextent=(latmin, latmax))

fig.colorbar(cs, ax=axx, shrink=0.6)

m.drawcoastlines(color='k',linewidth=0.5,zorder=3)
m.drawcountries(color='k',linewidth=0.1,zorder=3)

parallelmin = int(latmin)
parallelmax = int(latmax)+5
m.drawparallels(np.arange(parallelmin, parallelmax,5,dtype='int16').tolist(),labels=[1,0,0,0],linewidth=0,fontsize=10, zorder=3)

meridianmin = int(lonmin)
meridianmax = int(lonmax)+1
m.drawmeridians(np.arange(meridianmin, meridianmax,5,dtype='int16').tolist(),labels=[0,0,0,1],linewidth=0,fontsize=10, zorder=3)

# datafiles = ["01_TRACKS/AS_2011-9_DISTANCE_(DD).txt", "01_TRACKS/AS_2017-9_DISTANCE_(OCKHI).txt"
# ,"01_TRACKS/AS_2018-1_DISTANCE_(D).txt","01_TRACKS/AS_2018-13_DISTANCE_(GAJA).txt","01_TRACKS/BoB_2010-7_DISTANCE_(JAL).txt",""]

colors = ['C0','C1','C3','C2','C4','C5','C6','C7']
datafiles = glob.glob("01_TRACKS/*.txt")
for jj in range(8):
    dff = pd.read_csv(datafiles[jj],sep='\s+', dtype={'time': object})
    year = datafiles[jj].split("/")[1].split("_")[1].split("-")[0]
    track_name = datafiles[jj].split("/")[1].split("(")[1].split(")")[0]
    if track_name=="D":
        track_name = "Depression"
    elif track_name=="DD":
        track_name = "Deep Depression"
    track_name = track_name.capitalize()
    print(f"year: {year} {track_name}")

    lons = dff['lon'].values
    lats = dff['lat'].values
    x, y = m(lons, lats)
    m.plot(x, y,'o-',color=colors[jj],ms=4, zorder=4,label=f"TRACK {jj} ({year})")

    typh_time=[]
    for i in range(dff.shape[0]):
        date=dff.loc[i,'date']
        try:
            dd = date.split(".")[0]
            month = date.split(".")[1]
        except:
            dd = date.split("/")[0]
            month = date.split("/")[1]

        time=dff.loc[i,'time']

        track_times="{}{} ({})".format(month, dd, time[:2])
        typh_time.append(track_times)
    typh_time=np.array(typh_time)

    for i in np.arange(0,len(typh_time),5):
        plt.text(x[i]+20000,y[i]-10000,typh_time[i],fontsize=6,zorder=4)
    plt.arrow(x[-1], y[-1]+1, x[-1]-x[-2], y[-1]-y[-2],head_width=50000, head_length=60000, fc='w', ec='k',color='k',alpha=1,zorder=4)

# obs_site_lat = [14.4742, 8.5335]
# obs_site_lon = [78.7098, 76.9047]
# x_os, y_os = m(obs_site_lon, obs_site_lat)
# m.plot(x_os, y_os,'s',ms=6, zorder=5, color='r')
plt.legend(loc=1)


# plt.savefig('map.eps')
plt.savefig('map.png',bbox_inches='tight',dpi=300)