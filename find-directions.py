import pandas as pd
import os
import numpy as np
import math

# Order of points is:
# 0 = central location (black)
# 1 = nose (red)
# 2 = head (orange)
# 3 = base of neck (yellow)
# 4 = left shoulder (green)
# 5 = right shoulder (blue)
# 6 = left hip (cyan)
# 7 = right hip (purple)
# 8 = base of tail (magenta)
# 9 = tip of tail (turqoise)

# Defining parameters
observation = '083'  
bout_id = observation + '.01'   # 01 = foraging, 02 = resting, 03 = reacting
behavior = 'foraging'
species = 'Grevys_zebra'
video_start_time = 286          # Start time of segment in video (in seconds)
video_end_time = 400            # End time of segment in video (in seconds)
start_frame_num = 2576          # Start frame number of video (where numpy frame 0 corresponds to)
video_frame_rate = 60
numpy_frame_rate = 30
stepsize = 30                   # Only include every stepsize'th frame

# Calculate corresponding start and end frames in numpy array of segment
start_frame = int((video_start_time * video_frame_rate - start_frame_num) / (video_frame_rate / numpy_frame_rate))
end_frame = int((video_end_time * video_frame_rate - start_frame_num) / (video_frame_rate / numpy_frame_rate))

# Load posture data
postures = np.load(f'posture_data_utms/observation{observation}-postures.npy')

# Define function to calculate angles from EAST
def angle_from_east(tail, neck):
    delta_easting = neck[0] - tail[0]
    delta_northing = neck[1] - tail[1]
    angle_rad = math.atan2(delta_northing, delta_easting)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360

# Extract key points and calculate angles
neck_points = postures[:, start_frame:end_frame:stepsize, 3]
tail_points = postures[:, start_frame:end_frame:stepsize, 8]
angles_from_east = [[round(angle_from_east(tail_points[i, j], neck_points[i, j]), 1) for j in range(tail_points.shape[1])] for i in range(tail_points.shape[0])]

# Prepare data for dataframe
data = []
for i, animal_angles in enumerate(angles_from_east):
    for j, angle in enumerate(animal_angles):
        if not math.isnan(angle):
            numpy_frame_num = start_frame + j * stepsize
            frame_num = observation + '-' + str(numpy_frame_num)
            individual_id = observation + '-' + str(i)
            data.append([observation, bout_id, behavior, species, individual_id, frame_num, angle])

# Create dataframe
df = pd.DataFrame(data, columns=['observation', 'bout_id', 'behavior', 'species', 'individual_id', 'frame_num', 'orientation'])

# Save DataFrame to excel file
output_filename = 'behavior_data.xlsx'
if os.path.exists(output_filename):
    df_existing = pd.read_excel(output_filename, dtype=np.object_)
    df_combined = pd.concat([df_existing, df])
    duplicates = df_combined[df_combined.duplicated(keep='last')]
    if not duplicates.empty:
        print("Duplicates found:")
        for idx, row in duplicates.iterrows():
            print(f"Row {idx+2}: {row.tolist()}")
        print("Cannot add duplicate entries.")
    else:
        df_combined.to_excel(output_filename, index=False)
else:
    df.to_excel(output_filename, index=False)
