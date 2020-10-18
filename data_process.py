#!/usr/bin/python3
import netCDF4 as nc
import numpy as np
from datetime import date
from marineHeatWaves import detect
fn = 'Port_Hacking_Site.nc'
ds = nc.Dataset(fn)
time=ds['time']
#1981-1-1
start_day=date(1981,1,1).toordinal()
dtime = [start_day + ((tt-55200)/86400) for tt in time]


#list of availablke times
#this is the processed raw data where missing time is not filled.
dates = [date.fromordinal(tt.astype(int)) for tt in dtime]


#for refference only, we arbitarrily take 1 point:
la = ds['lat']
lat = []
for i in la:
    lat.append(i.data.item(0))
lo = ds['lon']
lon = []
for i in lo:
    lon.append(i.data.item(0))


#this is the tempreture array
temp = []
#creating time array t
#this is the comnplete timne series with all missing value filled
t = []
i=dtime[0]
j = 0
while i <= dtime[-1]:
    t.append(date.fromordinal((i).astype(int)).toordinal())
    #if the data on a specific day is misisng, fill it wilth 0
    if i == dtime[j]:
        j+=1
        index = dtime.index(i)
        t_temp = 0
        t_ntemp = 0
        for latitude in range(0,5):

            for longitude in range (130,135):
                tt = ds['sea_surface_temperature'][index,latitude,longitude].data.item(0) 
                if tt != 0.0:
                    t_temp += tt
                    t_ntemp += 1
        avg_temp = 0
        if t_ntemp != 0:

            avg_temp = t_temp / t_ntemp
        temp.append(avg_temp )
    else:
        temp.append(0)    
    i+=1

t = np.array(t)
temp = np.array(temp)
mhws = detect(t,temp)
print(mhws[0])
