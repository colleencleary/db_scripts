# db_scripts

## Gaia Cross Match
__Currently has functions to sort Gaia data into separate dataframes row by row, one for 'matches', one for 'new objects', and one for objects with more than one match that need review. This function returns dataframes for matches and new objects. Other functions generate parallax, proper motions, and photometry tables formatted for database ingestion.__

### Current State
  Copied over from Brown Scholar repository. Worked within original project, but needs to be tested in new directory. Script is in [gaia_crossmatch/gaia_crossmatch.py](gaia_crossmatch/gaia_crossmatch.py)

#### Existing Functions
  - **matches_sortCSV()**: requires a pandas dataframe with RA and DEC
  - **generateMatchtables()**: requires matches dataframe
  - **generateNewObjTables()**: requires new objects dataframe and BDNYC database (currently).

### ToDo
  - Check that the code is still working after being moved
  - Rename functions and variables
  - Needs function to determine if >1 parallax and set adopted to false if not from Gaia
  - Package as importable library
  - Create test scripts and ensure they pass
  - Complete and improve documentation within script
  - More efficient methods?
  - Option to save tables?




<hr>




## Spectral Type String Parser
__Script for splitting one column of strings that contain data for spectral type, gravity, and suffix in one column. Returns a 4-column list with spectral_type (as float), gravity (as text), suffix (as text), and comments (original string as text).__


### Current State
  Accepts arguments and returns as expected. Script is in [STparse/STparse.py](STparse/STparse.py).

#### Existing Functions
 - **stparser()**: requires a series of strings

### ToDo
  - Package as importable library
  - Create tests (including all hardcoded cases) and ensure they pass
  - Complete and improve documentation within script
  - Maybe an option to save the table?
  - Create a new function to extend a previous list (such as source id) with the list generated by stparser.
