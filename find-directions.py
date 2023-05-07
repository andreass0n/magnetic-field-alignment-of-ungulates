import numpy as np
import matplotlib.pyplot as plt
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

# frame 0 of numpy array corresponds to what time in what video:
# 015-01 // frame 0 = 2:47m or 167s
# 083-01 // frame 0 = 0:43 or 43s


# Variables (add array_relation_constant (time in seconds into the video when array frame 0 starts (look up in table above)) // add timewindow in seconds from start of video of specific segment)

frame_rate = 30
array_relation_constant = 167
start_time = 370
end_time = 371

# Convert start/end time of segment to start of array frames

start_frame = int((start_time - array_relation_constant) * frame_rate)
end_frame = int((end_time - array_relation_constant) * frame_rate)


# Load array and extract neck and tail keypoints of frames of interest

postures = np.load('posture_data_utms/observation015-postures.npy')

neck_points = postures[:, start_frame:end_frame, 3]
tail_points = postures[:, start_frame:end_frame, 8]


# Create function to calculate all orientation angles relative to true north of all animals in specific segment 

def angle_from_north(tail, neck):

    # Calculate differences in easting and northing of neck and tail

    delta_easting = neck[0] - tail[0]
    delta_northing = neck[1] - tail[1]


    # Calculate angle of the vector between tail and neck points relative to east

    angle_rad = math.atan2(delta_northing, delta_easting)


    # Convert angle from radians to degrees

    angle_deg = math.degrees(angle_rad)


    # Convert angle relative to east to angle relative to north

    angle_from_north = (90 - angle_deg) % 360
    return angle_from_north


# Run function for every animal; store results in list

angles_from_north = [[angle_from_north(tail_points[i, j], neck_points[i, j]) for j in range(tail_points.shape[1])] for i in range(tail_points.shape[0])]


# Print results

for i, animal_angles in enumerate(angles_from_north):
    for j, angle in enumerate(animal_angles):
        print(f"Animal {i+1} in frame {start_frame + j}: Angle relative to North in degrees: {angle:.1f}")
    print()
