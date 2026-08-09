from pybaseball import statcast

data = statcast(
    start_dt="2026-03-26",
    end_dt="2026-08-03"
)

data.to_csv("statcast_2026_to_dl.csv", index=False)