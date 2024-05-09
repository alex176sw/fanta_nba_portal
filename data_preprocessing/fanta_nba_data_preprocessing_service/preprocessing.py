import pandas as pd
from sklearn.preprocessing import StandardScaler

def standardize(dataset, scaler=None):
    dataset = pd.DataFrame(dataset)
    columns = list(dataset.columns)

    if scaler is None:
        scaler = StandardScaler()
        dataset = scaler.fit_transform(dataset).tolist()
    else:
        dataset = scaler.transform(dataset).tolist()
        
    return dataset, columns, scaler
        


def get_teams_statistics(home_team, host_team, teams_stats):
    home_team_stats = None
    host_team_stats = None
    for json_dict in teams_stats:
        if json_dict["TEAM_NAME"] == home_team:
            home_team_stats = json_dict
        if json_dict["TEAM_NAME"] == host_team:
            host_team_stats = json_dict

    for key in ["TEAM_NAME", "TEAM_ABBREVIATION", "TEAM_ID"]:
        del home_team_stats[key]
        del host_team_stats[key]

    return home_team_stats, host_team_stats