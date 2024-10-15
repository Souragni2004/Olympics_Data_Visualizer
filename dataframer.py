import pandas as pd

def data(athletes,noc_data):
    athletes = athletes[athletes['Season'] == 'Summer']
    athletes = athletes.merge(noc_data, on='NOC', how='left')
    athletes.drop_duplicates(inplace=True)
    athletes_dummy = pd.concat([athletes, pd.get_dummies(athletes['Medal']).astype(int)], axis=1)
    return athletes_dummy