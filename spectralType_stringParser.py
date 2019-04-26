import pandas as pd


# import gaia csv
gaia_catalogue = pd.read_csv('/Users/colleencleary/BridgeUp-astro/GUCDScat.csv')

st_string = gaia_catalogue['SPTNIRNAME']






stparser(st_string)





i=547
st_string[i]
st_original[i]
suffix
gravity



st.append([i, float(st_string[i]), gravity, suffix, comment])

st_string[i]

try:
    st.append([i, float(st_string[i]), gravity, suffix, comment])
except ValueError:
    invalid_spectralTypes.append([i, st_original[i]])

invalid_spectralTypes

data.append(['source_id'])
for i in new_objects.index:
    data.append([i])
data[0].extend((st[0][1:]))

for i in range(1, len(data)):
    for j in range(1, len(st)):
        if data[i][0] == st[j][0]:
            data[i].extend((st[j][1:]))
    if len(data[i]) == 1:
        del data[i]
        print(i)



data

data.remove
data
