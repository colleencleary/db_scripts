import pandas as pd

def stparser(st_string):
    """splits string that consists of spectral type, gravity and suffix in one column and returns a 4-column table with spectral_type (as float), gravity (as text), suffix (as text), and comments (includes original string as text)."""

    # all existing possibilities for gravity and suffix entries in BDNYC database. Used for comparison.
    gravitylist = ['gamma', 'FLD-G', 'INT-G', 'Int-G', 'd/sd', 'VL-G', 'Vl-G', 'beta', 'b/g', 'bg', '()', 'g', 'b', 'd', 'δ']
    suffixlist = ['p(blue)', 'p(red)', 'IV-Ve', 'd/sd', 'blue', ':pec', 'IVe', 'pec', 'nir', '::p', '::.', 'sd:', 'sd?', 'red', 'Ve', 'sd', '::', ':b', ':p', ':', 'e', 'p', 'd', '?', '>', '?']

    combined = list(suffixlist+gravitylist)
    combined.sort(key=len, reverse=True)

    # initialize empty list with appropriate column names
    st = list()
    st.append(['','spectral_type', 'gravity', 'suffix', 'comments'])

    st_original = st_string.str.strip()

    # replace original string values M, L, Y, and T with empty character, 1, 2, and 3. Also removes spaces and null values
    st_string = st_string.str.replace('M ', 'M4').str.replace('M', '').str.replace('L ', 'L4').str.replace('L', '1').str.replace('T ', 'T4').str.replace('T', '2').str.replace('Y ', 'Y4').str.replace('Y', '3').str.strip().str.replace(' ','').dropna()

    invalid_spectralTypes = list()

    for i in st_string.index:
        comment=st_original[i]

        if st_string[i].strip()!='...' and '-99999' not in st_string[i]:
            gravity=''
            suffix=''

            st_string[i]=st_string[i].replace(' ', '').lower()

            if 'blu' in st_string[i] and 'e' not in st_string[i]:
                st_string[i]=st_string[i]+'e'

            if '(' in st_string[i] and ')' not in st_string[i]:
                st_string[i]=st_string[i]+')'

            if '+' in st_string[i]:
                st_string[i]=st_string[i].split('+', 1)[0]

            for c in combined:
                if c.lower() in st_string[i]:
                    if c in suffixlist:
                        suffix+=str(c)
                    if c in gravitylist:
                        gravity+=str(c)
                    st_string[i]=st_string[i].replace(c.lower(), '')
            try:
                st.append([i, float(st_string[i]), gravity, suffix, comment])
            except ValueError:
                invalid_spectralTypes.append([i, st_original[i]])
        else:
            invalid_spectralTypes.append([i, st_original[i]])

    if i == len(st_string)-1 and len(invalid_spectralTypes) > 0:
        print('There are %d invalid strings out of %d strings.\nSee the original indices and strings below:' %(len(invalid_spectralTypes), len(st_original)))
        print(*invalid_spectralTypes, sep = "\n")
    return st
