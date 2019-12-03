remote = False
local = False
demo = True
pristine = False
other = False

if remote:
    DB_HOST = 'magenta.mysitehosted.com'
    DB_USER = 'team07'
    DB_PASSWORD = 'gatech'
    DB_PORT = '3306'
    DB_DB = 'cs6400_phase3_team07'
elif local:
    # specify your local credentials and set local = True and everything else = False
    DB_HOST = 'lamp'
    DB_USER = 'team07'
    DB_PASSWORD = 'gatech'
    DB_PORT = '3306'
    DB_DB = 'cs6400_demo_team07'
elif demo:
    # specify your other credentials and set demo = True and everything else = False
    DB_HOST = 'magenta.mysitehosted.com'
    DB_USER = 'team07'
    DB_PASSWORD = 'gatech'
    DB_PORT = '3306'
    DB_DB = 'cs6400_demo_team07'
elif pristine:
    # specify your other credentials and set pristine = True and everything else = False
    DB_HOST = 'magenta.mysitehosted.com'
    DB_USER = 'team07'
    DB_PASSWORD = 'gatech'
    DB_PORT = '3306'
    DB_DB = 'cs6400_demo_bu_team07'
elif other:
    # specify your other credentials and set other = True and everything else = False
    DB_HOST = 'magenta.mysitehosted.com'
    DB_USER = 'team07'
    DB_PASSWORD = 'gatech'
    DB_PORT = '3306'
    DB_DB = 'cs6400_test_data_team07'
