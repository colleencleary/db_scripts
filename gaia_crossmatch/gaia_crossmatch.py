import pandas as pd
from astrodbkit import astrodb

def matches_sortCSV(gaia_catalogue, search_radius = 0.000048481, db_path = '../BDNYCdb_practice/bdnycdev_copy.db', save_all = False, save_needsreview = False):
    """Sort Gaia data into separate dataframes row by row, one for 'matches', one for 'new objects', and one for objects with more than one match that need review. Returns dataframes for matches and new objects.

    Required Parameters:
        gaia_catalogue: pandas dataframe of data. Requires RA and DEC for matching against the database

    Optional Parameters:
        search_radius: __float__ Search radius for cross matching RA/DEC against database.
            Default is 0.000048481 radians (10 arcseconds).
        db_path: __string__ Local path to database.
            Default is '../BDNYCdb_practice/bdnycdev_copy.db'.
        save_all: __boolean__ Saves all dataframes as CSV files. Default is False
        save_needsreview: __boolean__ Saves only the needs_review dataframe as a CSV file.
            Default is False.
    """

    db = astrodb.Database('../BDNYCdb_practice/bdnycdev_copy.db')

    # matches will store gaia data for objects in BDNYC database
    matches = pd.DataFrame(columns=np.insert(gaia_catalogue.columns.values, 0, 'source_id', axis=0))

    # new_objects will store gaia data for objects that do not exist in BDNYC database
    new_objects = pd.DataFrame(columns=gaia_catalogue.columns.values)
    # needs_review will store gaia data for objects that have too many matched in the database and need further review
    needs_review = pd.DataFrame(columns=gaia_catalogue.columns.values)

    # ===============================================
    # sort each row of gaia data into matches/new_objects using celestial coordinates: right ascension (ra/RA) and declination (dec/DEC)
    # ===============================================
    for i in range(len(gaia_catalogue)):
        results=db.search((gaia_catalogue['RA'][i], gaia_catalogue['DEC'][i]), 'sources', radius=0.000048481, fetch=True)

        if len(results) == 1:
            matches = matches.append(gaia_catalogue.loc[[i]])
            matches['source_id'].loc[i]=results['id'][0]
        elif len(results)>1:
        # if there is MORE THAN ONE result, just print a note
            needs_review = needs_review.append(gaia_catalogue.loc[[i]])
        else:
            new_objects = new_objects.append(gaia_catalogue.loc[[i]])

    if save_all==True:
        matches.to_csv('matches.csv')
        new_objects.to_csv('new_objects.csv')
        needs_review.to_csv('needs_review.csv')
        print('matches, new_objects, and needs_review saved as CSV files.')

    if save_needsreview==True:
        needs_review.to_csv('needs_review.csv')

    return matches, new_objects


def generateMatchtables(matches, addToDb=False):
    ##################################################
    # matches tables
    ##################################################

    # create new empty list to store data we want to add to database
    matchParallax_data = list()
    matchPropermotions_data = list()
    matchPhotometry_data = list()

    # append the column name (as it's written in the BDNYC database) to match on the appropriate column
    matchParallax_data.append(['source_id','parallax', 'parallax_unc','publication_shortname', 'adopted','comments'])
    matchPropermotions_data.append(['source_id','proper_motion_ra', 'proper_motion_ra_unc','proper_motion_dec', 'proper_motion_dec_unc','publication_shortname', 'comments'])
    matchPhotometry_data.append(['source_id','band', 'magnitude','magnitude_unc', 'publication_shortname', 'comments'])



    for i in range(len(matches)):
        matchParallax_data.append([matches.iloc[[i]]['source_id'].values[0], matches.iloc[[i]]['PARALLAX'].values[0], matches.iloc[[i]]['PARALLAX_ERROR'].values[0], 'GaiaDR2', 1, 'added by SpectreCell'])
        matchPropermotions_data.append([matches.iloc[[i]]['source_id'].values[0], matches.iloc[[i]]['PMRA'].values[0], matches.iloc[[i]]['PMRA_ERROR'].values[0], matches.iloc[[i]]['PMDEC'].values[0], matches.iloc[[i]]['PMDEC_ERROR'].values[0],'GaiaDR2','added by SpectreCell'])
        matchPhotometry_data.append([matches.iloc[[i]]['source_id'].values[0], 'GaiaDR2_G', matches.iloc[[i]]['PHOT_G_MEAN_MAG'].values[0], matches.iloc[[i]]['PHOT_G_MEAN_MAG_ERROR'].values[0],'GaiaDR2','added by SpectreCell'])
        matchPhotometry_data.append([matches.iloc[[i]]['source_id'].values[0], 'GaiaDR2_BP', matches.iloc[[i]]['PHOT_BP_MEAN_MAG'].values[0], matches.iloc[[i]]['PHOT_BP_MEAN_MAG_ERROR'].values[0],'GaiaDR2','added by SpectreCell'])
        matchPhotometry_data.append([matches.iloc[[i]]['source_id'].values[0], 'GaiaDR2_RP', matches.iloc[[i]]['PHOT_RP_MEAN_MAG'].values[0], matches.iloc[[i]]['PHOT_RP_MEAN_MAG_ERROR'].values[0],'GaiaDR2','added by SpectreCell'])

    if addToDb==True:
        db.add_data(matchParallax_data, 'parallaxes')
        db.add_data(matchPropermotions_data, 'proper_motions')
        db.add_data(matchPhotometry_data, 'photometry')

    return matchParallax_data, matchPropermotions_data, matchPhotometry_data

def generateNewObjTables(new_objects, db, addSourceTable=False):
    ##################################################
    # new objects tables
    ##################################################

    # create new empty list to store data we want to add to database
    newobjects_data = list()

    # append the column name (as it's written in the BDNYC database) to match on the appropriate column
    newobjects_data.append(['ra','dec', 'designation','publication_shortname', 'shortname','names', 'comments'])

    for i in range(len(new_objects)):
        newobjects_data.append([new_objects.iloc[[i]]['RA'].values[0], new_objects.iloc[[i]]['DEC'].values[0], new_objects.iloc[[i]]['DISCOVERYNAME'].values[0], 'GaiaDR2', new_objects.iloc[[i]]['SHORTNAME'].str.replace('J', '').str.strip().values[0], new_objects.iloc[[i]]['SOURCE_ID'].values[0],'added by SpectreCell'])

    if addSourceTable==True:
        db.add_data(newobjects_data, 'sources')

    # create new empty list to store data we want to add to database
    newObjParallax_data = list()
    newObjPropermotions_data = list()
    newObjPhotometry_data = list()

    # append the column name (as it's written in the BDNYC database) to match on the appropriate column
    newObjParallax_data.append(['source_id','parallax', 'parallax_unc','publication_shortname', 'adopted','comments'])
    newObjPropermotions_data.append(['source_id','proper_motion_ra', 'proper_motion_ra_unc','proper_motion_dec', 'proper_motion_dec_unc','publication_shortname', 'comments'])
    newObjPhotometry_data.append(['source_id','band', 'magnitude','magnitude_unc', 'publication_shortname', 'comments'])

    for i in range(len(new_objects)):
        db_sourceid=db.search((new_objects['RA'].iloc[[i]], new_objects['DEC'].iloc[[i]]), 'sources', radius=0.00278, fetch=True)['id'][0]

        newObjParallax_data.append([db_sourceid, new_objects.iloc[[i]]['PARALLAX'].values[0], new_objects.iloc[[i]]['PARALLAX_ERROR'].values[0], 'GaiaDR2', 1, 'added by SpectreCell'])

        newObjPropermotions_data.append([db_sourceid, new_objects.iloc[[i]]['PMRA'].values[0], new_objects.iloc[[i]]['PMRA_ERROR'].values[0], new_objects.iloc[[i]]['PMDEC'].values[0], new_objects.iloc[[i]]['PMDEC_ERROR'].values[0],'GaiaDR2','added by SpectreCell'])

        newObjPhotometry_data.append([db_sourceid, 'GaiaDR2_G', new_objects.iloc[[i]]['PHOT_G_MEAN_MAG'].values[0], new_objects.iloc[[i]]['PHOT_G_MEAN_MAG_ERROR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, 'GaiaDR2_BP', new_objects.iloc[[i]]['PHOT_BP_MEAN_MAG'].values[0], new_objects.iloc[[i]]['PHOT_BP_MEAN_MAG_ERROR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, 'GaiaDR2_RP', new_objects.iloc[[i]]['PHOT_RP_MEAN_MAG'].values[0], new_objects.iloc[[i]]['PHOT_RP_MEAN_MAG_ERROR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, '2MASS_J', new_objects.iloc[[i]]['TMASSJ'].values[0], new_objects.iloc[[i]]['TMASSJERR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, '2MASS_H', new_objects.iloc[[i]]['TMASSH'].values[0], new_objects.iloc[[i]]['TMASSHERR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, '2MASS_K', new_objects.iloc[[i]]['TMASSK'].values[0], new_objects.iloc[[i]]['TMASSKERR'].values[0],'GaiaDR2','added by SpectreCell'])

        newObjPhotometry_data.append([db_sourceid, 'WISE_W1', new_objects.iloc[[i]]['WISEW1'].values[0], new_objects.iloc[[i]]['WISEW1ERR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, 'WISE_W2', new_objects.iloc[[i]]['WISEW2'].values[0], new_objects.iloc[[i]]['WISEW2ERR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, 'WISE_W3', new_objects.iloc[[i]]['WISEW3'].values[0], new_objects.iloc[[i]]['WISEW3ERR'].values[0],'GaiaDR2','added by SpectreCell'])

        newObjPhotometry_data.append([db_sourceid, 'GUNN_G', new_objects.iloc[[i]]['GUNNG'].values[0], new_objects.iloc[[i]]['GUNNGERR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, 'GUNN_R', new_objects.iloc[[i]]['GUNNR'].values[0], new_objects.iloc[[i]]['GUNNRERR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, 'GUNN_I', new_objects.iloc[[i]]['GUNNI'].values[0], new_objects.iloc[[i]]['GUNNIERR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, 'GUNN_Z', new_objects.iloc[[i]]['GUNNZ'].values[0], new_objects.iloc[[i]]['GUNNZERR'].values[0],'GaiaDR2','added by SpectreCell'])
        newObjPhotometry_data.append([db_sourceid, 'GUNN_Y', new_objects.iloc[[i]]['GUNNY'].values[0], new_objects.iloc[[i]]['GUNNYERR'].values[0],'GaiaDR2','added by SpectreCell'])

    return newObjParallax_data, newObjPropermotions_data, newObjPhotometry_data
