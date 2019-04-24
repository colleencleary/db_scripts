import pandas as pd
from astrodbkit import astrodb


# import gaia csv
gaia_catalogue = pd.read_csv('/Users/colleencleary/BridgeUp-astro/GUCDScat.csv')
# import bdnyc database
db = astrodb.Database('/Users/colleencleary/BridgeUp-astro/BDNYCdb_practice/bdnycdev_copy.db')

new_objects = pd.read_csv('new_objects.csv', index_col=0)
st_string = new_objects['SPTNIRNAME']

st_string.unique()

def stparser(st_string, db):
    """splits string that consists of spectral type, gravity and suffix in one column and returns a 4-column table with spectral_type (as float), gravity (as text), suffix (as text), and comments (includes original string as text)."""

    # all existing possibilities for gravity and suffix entries in BDNYC database. Used for comparison.
    gravitylist = ['FLD-G', 'INT-G', 'd/sd', 'VL-G', 'b/g', 'bg', '()', 'g', 'b', 'd', 'δ']
    suffixlist = ['p(blue)', 'p(red)', 'IV-Ve', 'd/sd', 'blue', ':pec', 'IVe', 'pec', 'nir', '::.', 'sd:', 'red', 'sd?', 'Ve', 'sd', '::', ':b', ':p', ':', 'e', 'p', 'd', '?', '>', '?']

    # replace original string values M, L, Y, and T with empty character, 1, 2, and 3. Also removes spaces and null values
    st_string = st_string.str.replace('M ', 'M4').str.replace('M', '').str.replace('L ', 'L4').str.replace('L', '1').str.replace('T ', 'T4').str.replace('T', '2').str.replace('Y ', 'Y4').str.replace('Y', '3').str.strip().str.replace(' ','').dropna()

    # fix formatting for specific values. Change as necessary for strings with known issues. Below example did not include a closing parenthesis.
    st_string[641]=st_string[641]+')'

    # initialize empty list with appropriate column names
    st = list()
    st.append(['','spectral_type', 'gravity', 'suffix', 'comments'])


    for i in st_string[pd.notna(st_string)].index:
        if st_string[i].strip()!='...' and '-999' not in st_string[i]:
            gravity=''
            suffix=''
            comment='added by SpectreCell: '+new_objects['SPTNIRNAME'][i].strip()

            st_string[i]=st_string[i].replace(' ', '')

            for s in suffixlist:
                if str(s) in st_string[i]:
                    suffix+=str(s)
                    if str(s) in gravitylist:
                        gravity+=str(s)
                    st_string[i]=st_string[i].replace(str(s), '')

            for g in gravitylist:
                if str(g) in st_string[i]:
                    gravity+=str(g)
                    st_string[i]=st_string[i].replace(str(g), '').replace('amma', '')
            if '+' in st_string[i]:
                st_string[i]=st_string[i].split('+', 1)[0]
            else:
                st.append([i, float(st_string[i]), gravity, suffix, comment])


st



data = list()

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
