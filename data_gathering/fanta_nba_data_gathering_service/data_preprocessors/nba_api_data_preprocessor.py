import pandas as pd
from icecream import ic

class NbaApiDataPreProcessor:

    def get_statistics(self, games_df: pd.DataFrame):

        teams_ids = NbaApiDataPreProcessor.get_nba_team_ids(games_df)
        teams_stats = NbaApiDataPreProcessor.get_teams_stats(teams_ids, games_df)
        teams_stats = NbaApiDataPreProcessor.add_teams_names(teams_stats, games_df)

        dataset = []
        
        for i, game in games_df.iterrows():

            # get home and away teams
            home_team_id = game["TEAM_ID"]
            game_ids = games_df[games_df["GAME_ID"] == game["GAME_ID"]]
            host_team_id = game_ids[game_ids["TEAM_ID"] != home_team_id]["TEAM_ID"].values[0]
        
            # get home and away teams stats
            home_team_stats = teams_stats[teams_stats["TEAM_ID"] == home_team_id].drop("TEAM_ID", axis=1).rename(columns = {
                'win_percentage_away': 'home_team_win_percentage_away', 
                'win_percentage_at_home': 'home_team_win_percentage_at_home',
                'average_points_scored_away': 'home_team_average_points_scored_away',
                'average_points_scored_at_home': 'home_team_average_points_scored_at_home'}).reset_index()
        
            host_team_stats = teams_stats[teams_stats["TEAM_ID"] == host_team_id].drop("TEAM_ID", axis=1).rename(columns = {
                'win_percentage_away': 'host_team_win_percentage_away', 
                'win_percentage_at_home': 'host_team_win_percentage_at_home',
                'average_points_scored_away': 'host_team_average_points_scored_away',
                'average_points_scored_at_home': 'host_team_average_points_scored_at_home'}).reset_index()
            
            home_team_stats = home_team_stats.drop(["TEAM_NAME", "TEAM_ABBREVIATION"], axis=1)
            host_team_stats = host_team_stats.drop(["TEAM_NAME", "TEAM_ABBREVIATION"], axis=1)

            merged_stats = pd.concat([home_team_stats, host_team_stats], axis=1)
            
            # add other fields
            home_won = NbaApiDataPreProcessor.get_home_winner(game["WL"])
            merged_stats.insert(0, "home_team_won", home_won, True)

            dataset.append(
                merged_stats
            )
        dataset = pd.concat(dataset).drop("index", axis=1).dropna()
        ic(dataset)
        ic(dataset.columns)
        ic(teams_stats)
        ic(teams_stats.columns)


        return dataset.to_dict(orient="records"), teams_stats.to_dict(orient="records")

    @staticmethod
    def add_teams_names(teams_stats, games_df):
        merged_df = pd.merge(games_df, teams_stats, on='TEAM_ID', how='inner')
        merged_df = merged_df.drop_duplicates(subset=["TEAM_ID"])
        teams_stats['TEAM_ABBREVIATION'] = merged_df['TEAM_ABBREVIATION']
        teams_stats['TEAM_NAME'] = merged_df['TEAM_NAME']
        return teams_stats

    @staticmethod
    def get_win_percentage_for_team(games_df, team_id, home_game: bool):
        loc = "vs." if home_game else "@"
        col_name = "win_percentage_at_home" if home_game else "win_percentage_away"
        games = games_df[(games_df['TEAM_ID'] == team_id) & games_df['MATCHUP'].str.contains(loc)  ]
        win_percentage = games.groupby('TEAM_ID')['WL'].apply(lambda x: (x == 'W').sum() / len(x)).reset_index()
        win_percentage.rename(columns={'WL': col_name}, inplace=True)
        return win_percentage

    @staticmethod
    def get_average_points_scored_for_team(games_df, team_id, home_game: bool):
        loc = "vs." if home_game else "@"
        col_name = 'average_points_scored_at_home' if home_game else "average_points_scored_away"
        
        games = games_df[(games_df['TEAM_ID'] == team_id) & games_df['MATCHUP'].str.contains(loc)  ]
        avg_points_scored = games.groupby('TEAM_ID')['PTS'].mean().reset_index()
        avg_points_scored.rename(columns={'PTS': col_name}, inplace=True)
        return avg_points_scored

    @staticmethod
    def get_teams_stats(teams_ids, games_df):
        teams_stats = []
        for team_id in teams_ids:
            teams_stats.append(NbaApiDataPreProcessor.get_stats_for_team(team_id, games_df))
        teams_stats = pd.concat(teams_stats).reset_index().drop("index", axis=1)
        return teams_stats
    
    @staticmethod
    def get_stats_for_team(team_id: int, games_df):
        df_wp_home = NbaApiDataPreProcessor.get_win_percentage_for_team(games_df, team_id, False)
        df_wp_away = NbaApiDataPreProcessor.get_win_percentage_for_team(games_df, team_id, True)
        merged_wp_df = pd.merge(df_wp_home, df_wp_away, on='TEAM_ID')

        df_ap_home = NbaApiDataPreProcessor.get_average_points_scored_for_team(games_df, team_id, False)
        df_ap_away = NbaApiDataPreProcessor.get_average_points_scored_for_team(games_df, team_id, True)
        merged_ap_df = pd.merge(df_ap_home, df_ap_away, on='TEAM_ID')
        
        merged_stats = pd.merge(merged_wp_df, merged_ap_df, on='TEAM_ID')
        return merged_stats

    @staticmethod
    def get_nba_team_ids(games_df):
        teams_ids = set()
        for i, game in games_df.iterrows():
            teams_ids.add(game["TEAM_ID"])    
        return teams_ids

    @staticmethod
    def get_home_winner(winner_str):
        if winner_str == "W":
            return 1
        return 0
    
