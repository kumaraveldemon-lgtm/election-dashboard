print("Simulation file loaded")
import pandas as pd
import random

def simulate_tvk(df, tvk_share=0.05):
    new_data = []

    for const in df["Constituency"].unique():
        subset = df[df["Constituency"] == const].copy()

        # Reduce votes from existing parties
        subset["VoteShare_%"] = subset["VoteShare_%"] * (1 - tvk_share)

        # Create TVK row
        tvk_row = subset.iloc[0].copy()
        tvk_row["Party"] = "TVK"
        tvk_row["VoteShare_%"] = tvk_share * 100

        new_data.append(subset)
        new_data.append(pd.DataFrame([tvk_row]))

    return pd.concat(new_data)