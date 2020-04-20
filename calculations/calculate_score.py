def calculate_score_for_single_cup(teams, cup):
    return  3 * teams["Wins"+cup] + 1*teams["Draws"+cup] /(teams["MatchesPlayed"+cup] * 3)

def calculate_weight(df):
    df_ranks = []
    for year in my_uefa["Year"].unique():
        df = my_uefa[my_uefa["Year"]==year]
        df['Weight'] = [(x_i-min(df["Points"]))/(max(df["Points"])-min(df["Points"])) for x_i in df["Points"]]
        df_ranks.append(df)
    return pd.concat(df_ranks)