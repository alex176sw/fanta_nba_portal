from dg.data_preprocessors.nba_api_data_preprocessor_base import DataPreProcessorBase
import numpy as np
import pandas as pd

class NbaApiDataPreProcessor(DataPreProcessorBase):
    
    def get_dataset(self, games_df: pd.DataFrame):
        home_win_percentage_df = NbaApiDataPreProcessor.home_teams_win_percentage(games_df)
        away_win_percentage_df = NbaApiDataPreProcessor.away_teams_win_percentage(games_df)
        home_avg_points_df     = NbaApiDataPreProcessor.home_teams_average_points_scored(games_df)
        away_avg_points_df     = NbaApiDataPreProcessor.away_teams_average_points_scored(games_df)

        dataset = []
        columns = ["home_won", "minutes", "home_win_percentage", "home_avg_points", "away_win_percentage", "away_avg_points"]

        for index, row in games_df.iterrows():

            team_id = row["TEAM_ID"]
            home_won = NbaApiDataPreProcessor.get_home_winner(row["WL"])
            minutes = row["MIN"]

            home_win_percentage = NbaApiDataPreProcessor.get_value_for_team(home_win_percentage_df, team_id, "home_team_win_percentage")
            home_avg_points = NbaApiDataPreProcessor.get_value_for_team(home_avg_points_df, team_id, "home_team_average_points_scored")
            
            
            game_ids = games_df[games_df["GAME_ID"] == row["GAME_ID"]]
            away_team_id = game_ids[game_ids["TEAM_ID"] != team_id]["TEAM_ID"].values[0]

            away_win_percentage = NbaApiDataPreProcessor.get_value_for_team(away_win_percentage_df, away_team_id, "away_team_win_percentage")
            away_avg_points = NbaApiDataPreProcessor.get_value_for_team(away_avg_points_df, away_team_id, "away_team_average_points_scored")

            dataset.append(
                (home_won, minutes, home_win_percentage, home_avg_points, away_win_percentage, away_avg_points)
            )

        return pd.DataFrame(dataset, columns=columns)

            


    @staticmethod
    def home_teams_win_percentage(df):
        home_games = df[df['MATCHUP'].str.contains('vs.')]

        win_percentage = home_games.groupby('TEAM_ID')['WL'].apply(lambda x: (x == 'W').sum() / len(x)).reset_index()
        win_percentage.rename(columns={'WL': 'home_team_win_percentage'}, inplace=True)

        return win_percentage

    @staticmethod
    def away_teams_win_percentage(df):
        away_games = df[df['MATCHUP'].str.contains('@')]

        win_percentage = away_games.groupby('TEAM_ID')['WL'].apply(lambda x: (x == 'W').sum() / len(x)).reset_index()
        win_percentage.rename(columns={'WL': 'away_team_win_percentage'}, inplace=True)

        return win_percentage

    @staticmethod
    def home_teams_average_points_scored(df):
        home_games = df[df['MATCHUP'].str.contains('vs.')]

        avg_points_scored = home_games.groupby('TEAM_ID')['PTS'].mean().reset_index()
        avg_points_scored.rename(columns={'PTS': 'home_team_average_points_scored'}, inplace=True)

        return avg_points_scored

    @staticmethod
    def away_teams_average_points_scored(df):
        away_games = df[df['MATCHUP'].str.contains('@')]

        avg_points_scored = away_games.groupby('TEAM_ID')['PTS'].mean().reset_index()
        avg_points_scored.rename(columns={'PTS': 'away_team_average_points_scored'}, inplace=True)

        return avg_points_scored

    @staticmethod
    def add_team_names(df, nba_teams):
        team_id_to_name = {team['id']: team['full_name'] for team in nba_teams}
        df['TEAM_NAME'] = df['TEAM_ID'].map(team_id_to_name)   
        return df

    @staticmethod
    def get_home_winner(winner_str):
        if winner_str == "W":
            return 1
        return 0
    
    @staticmethod
    def get_value_for_team(df, team_id, column):
        values = df[ df["TEAM_ID"] == team_id][column].values
        if len(values) > 0:
            return values[0]
        else:
            return np.nan