import pandas as pd
import numpy as np

data_path = "data/"

# Extracting the attendance data for PortAventura World
df_attendance = pd.read_csv(data_path + 'attendance.csv')
df_attendance_extract = df_attendance[df_attendance["FACILITY_NAME"]
                                      == "PortAventura World"].copy()
df_attendance_extract["USAGE_DATE"] = pd.to_datetime(
    df_attendance_extract["USAGE_DATE"], format="%Y-%m-%d")
df_attendance_extract.rename(
    columns={"attendance": "PARK_ATTENDANCE"}, inplace=True)

# Extracting the list of attractions for PortAventura World
df_link_attraction_park = pd.read_csv(data_path + 'link_attraction_park.csv')
df_link_attraction_park["attraction"] = df_link_attraction_park["ATTRACTION;PARK"].str.split(
    ";").str[0]
df_link_attraction_park["park"] = df_link_attraction_park["ATTRACTION;PARK"].str.split(
    ";").str[1]
df_link_attraction_park = df_link_attraction_park.drop(
    "ATTRACTION;PARK", axis=1)
df_link_attraction_park = df_link_attraction_park.sort_values("park")

# Extracting the schedule data for PortAventura World and merging it with the attendance data
df_entity_schedule = pd.read_csv(data_path + 'entity_schedule.csv')
df_entity_schedule_extract = df_entity_schedule[df_entity_schedule["ENTITY_TYPE"] == "ATTR"].copy(
)
df_entity_schedule_extract["PARK"] = df_entity_schedule_extract["ENTITY_DESCRIPTION_SHORT"].map(
    df_link_attraction_park.set_index("attraction")["park"])
df_entity_schedule_extract = df_entity_schedule_extract[df_entity_schedule_extract["PARK"] == "PortAventura World"].copy(
)
df_entity_schedule_extract = df_entity_schedule_extract[[
    "WORK_DATE", "ENTITY_DESCRIPTION_SHORT", "REF_CLOSING_DESCRIPTION"]].copy()
df_entity_schedule_extract["WORK_DATE"] = pd.to_datetime(
    df_entity_schedule_extract["WORK_DATE"], format="%Y-%m-%d")
df_entity_schedule_extract.sort_values("WORK_DATE", inplace=True)
df_entity_schedule_extract = df_entity_schedule_extract.rename(
    columns={"WORK_DATE": "USAGE_DATE"})
df_closure_and_attendance = pd.merge(
    df_entity_schedule_extract,
    df_attendance_extract[["USAGE_DATE", "PARK_ATTENDANCE"]],
    on="USAGE_DATE",
    how="left"
)

# Extracting the waiting times data for PortAventura World and merging it with the schedule and attendance data
df_waiting_times = pd.read_csv(data_path + 'waiting_times.csv')
df_waiting_times["PARK"] = df_waiting_times["ENTITY_DESCRIPTION_SHORT"].map(
    df_link_attraction_park.set_index("attraction")["park"])
df_waiting_times_extract = df_waiting_times[df_waiting_times["PARK"]
                                            == "PortAventura World"].copy()
df_waiting_times_extract.drop(columns=["PARK"], inplace=True)
df_waiting_times_extract.rename(
    columns={"WORK_DATE": "USAGE_DATE"}, inplace=True)
df_waiting_times_extract["USAGE_DATE"] = pd.to_datetime(
    df_waiting_times_extract["USAGE_DATE"], format="%Y-%m-%d")
df_closure_and_attendance_and_waiting = pd.merge(df_waiting_times_extract, df_closure_and_attendance, on=[
                                                 "USAGE_DATE", "ENTITY_DESCRIPTION_SHORT"], how="left")

df_final = df_closure_and_attendance_and_waiting.sort_values(
    ["ENTITY_DESCRIPTION_SHORT", "DEB_TIME"])
# adding weather
weather = pd.read_csv(data_path + 'weather_data.csv')
weather['dt'] = pd.to_datetime(weather['dt'], unit='s')

df_final['DEB_TIME'] = pd.to_datetime(df_final['DEB_TIME']).dt.floor('s')
df_final_with_weather = pd.merge(
    df_final,
    weather[['temp', 'humidity', 'wind_speed']],  # Only the relevant columns
    left_on=df_final['DEB_TIME'],  # Merge on the 'DEB_TIME' column
    right_on=weather['dt'],  # Merge on 'dt' column from weather
    how='left'
)
df_final = df_final_with_weather.sort_values(
    ["ENTITY_DESCRIPTION_SHORT", "DEB_TIME"])
df_final = df_final.drop(columns=['key_0']
                         )

df_final.to_csv(data_path + 'portaventura_world_data.csv', index=False)
