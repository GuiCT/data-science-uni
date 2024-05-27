import pandas as pd
import numpy as np
import os


# If directory ".data" already exists, assume data has already been downloaded
if os.path.exists('.data'):
    print('CSV data already available!')
else:
    # Get environment variable HOME
    home = os.environ['HOME']
    # Check if kaggle.json is present
    if not os.path.exists('kaggle.json'):
        print('Please copy kaggle.json file to project root!')
        exit(1)
    os.makedirs(os.path.join(home, '.kaggle'), exist_ok=True)
    # Copy kaggle.json to ~/.kaggle
    os.system('cp kaggle.json ~/.kaggle/')
    # Set permissions
    os.system('chmod 600 ~/.kaggle/kaggle.json')
    # Download data
    os.system(
        'kaggle datasets download -d rohanrao/formula-1-world-championship-1950-2020')
    # Unzip data
    os.system('unzip formula-1-world-championship-1950-2020.zip -d .data')
    # Remove zip file
    os.system('rm formula-1-world-championship-1950-2020.zip')
    print('Data downloaded and unzipped!')

# Generating parquets
if os.path.exists('.data_parquet'):
    print('Parquet data already available!')
    exit(0)
else:
    print('Generating parquet data...')
    os.makedirs('.data_parquet', exist_ok=True)
    # CIRCUITS
    circuits_df_raw = pd.read_csv(
        ".data/circuits.csv",
        index_col="circuitId"
    )
    circuits_df_raw["alt"] = pd.to_numeric(
        circuits_df_raw["alt"], errors="coerce")
    circuits_df_raw.to_parquet(".data_parquet/circuits.parquet")
    del circuits_df_raw

    # CONSTRUCTORS RESULTS
    constructor_results_df_raw = pd.read_csv(
        ".data/constructor_results.csv",
        index_col="constructorResultsId"
    )
    constructor_results_df_raw.to_parquet(
        ".data_parquet/constructor_results.parquet")
    del constructor_results_df_raw

    # CONSTRUCTORS STANDINGS
    constructor_standings_df_raw = pd.read_csv(
        ".data/constructor_standings.csv",
        index_col=["raceId", "constructorId"]
    )
    constructor_standings_df_raw = constructor_standings_df_raw.drop(
        columns=["constructorStandingsId"])
    constructor_standings_df_raw.to_parquet(
        ".data_parquet/constructor_standings.parquet")
    del constructor_standings_df_raw

    # CONSTRUCTORS
    constructors_df_raw = pd.read_csv(
        ".data/constructors.csv",
        index_col="constructorId"
    )
    constructors_df_raw.to_parquet(".data_parquet/constructors.parquet")
    del constructors_df_raw

    # DRIVERS STANDINGS
    driver_standings_df_raw = pd.read_csv(
        ".data/driver_standings.csv",
        index_col="driverStandingsId"
    )
    driver_standings_df_raw.to_parquet(
        ".data_parquet/driver_standings.parquet")
    
    # DRIVERS
    drivers_df_raw = pd.read_csv(
        ".data/drivers.csv",
        index_col="driverId"
    )
    drivers_df_raw["number"] = pd.to_numeric(
        drivers_df_raw["number"], errors="coerce")
    drivers_df_raw["dob"] = pd.to_datetime(
        drivers_df_raw["dob"], errors="coerce")
    drivers_df_raw.to_parquet(".data_parquet/drivers.parquet")
    del drivers_df_raw

    # LAP TIMES
    lap_times_df_raw = pd.read_csv(
        ".data/lap_times.csv",
        index_col=["raceId", "driverId", "lap"]
    )
    # Redundant data
    lap_times_df_raw = lap_times_df_raw.drop(columns=["time"])
    lap_times_df_raw.to_parquet(".data_parquet/lap_times.parquet")
    del lap_times_df_raw

    # RACES
    races_df_raw = pd.read_csv(
        ".data/races.csv",
        index_col="raceId"
    )
    races_df_raw["datetime"] = pd.to_datetime(
        races_df_raw["date"] + " " + races_df_raw["time"], errors="coerce")
    races_df_raw.to_parquet(".data_parquet/races.parquet")
    del races_df_raw

    # PIT STOPS
    pit_stops_df_raw = pd.read_csv(
        ".data/pit_stops.csv",
        index_col=["raceId", "driverId", "stop"]
    )
    pit_stops_df_raw = pit_stops_df_raw.drop(columns=["duration"])
    pit_stops_df_raw.to_parquet(".data_parquet/pit_stops.parquet")

    # QUALIFYING
    qualifying_df_raw = pd.read_csv(
        ".data/qualifying.csv",
        index_col=["raceId", "driverId"]
    )
    qualifying_df_raw = qualifying_df_raw.drop(columns=["qualifyId"])

    def lap_time_to_millis(lap_time: str):
        try:
            minutes, rest = lap_time.split(":")
            seconds, millis = rest.split(".")
            millis_total = int(minutes) * 60_000 + \
                int(seconds) * 1_000 + int(millis)
            return np.float64(millis_total)
        except Exception:
            return np.nan
    qualifying_df_raw["q1"] = qualifying_df_raw["q1"].apply(
        lap_time_to_millis)  # type: ignore
    qualifying_df_raw["q2"] = qualifying_df_raw["q2"].apply(
        lap_time_to_millis)  # type: ignore
    qualifying_df_raw["q3"] = qualifying_df_raw["q3"].apply(
        lap_time_to_millis)  # type: ignore
    qualifying_df_raw.to_parquet(".data_parquet/qualifying.parquet")
    del qualifying_df_raw

    # RESULTS
    results_df_raw = pd.read_csv(
        ".data/results.csv",
        index_col=["raceId", "driverId"]
    )
    results_df_raw = results_df_raw.drop(columns=[
        "resultId",
        "number",
        "positionText",
        "positionOrder",
        "time"])
    results_df_raw["position"] = pd.to_numeric(
        results_df_raw["position"], errors="coerce")
    results_df_raw["milliseconds"] = pd.to_numeric(
        results_df_raw["milliseconds"], errors="coerce")
    results_df_raw["fastestLap"] = pd.to_numeric(
        results_df_raw["fastestLap"], errors="coerce")
    results_df_raw["rank"] = pd.to_numeric(
        results_df_raw["rank"], errors="coerce")
    results_df_raw["fastestLapMillis"] = results_df_raw["fastestLapTime"].apply(
        lap_time_to_millis)  # type: ignore
    results_df_raw.to_parquet(".data_parquet/results.parquet")
    del results_df_raw

    # STATUS
    status_df_raw = pd.read_csv(
        ".data/status.csv",
        index_col="statusId"
    )
    status_df_raw.to_parquet(".data_parquet/status.parquet")
    del status_df_raw
