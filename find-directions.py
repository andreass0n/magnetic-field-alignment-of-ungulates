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


# VARIABLES (TIMES IN SECONDS FROM START OF VIDEO)                              UNCLEAR HERE REVISE TO ALIGN WITH VIDEO!!!!

frame_rate = 30
start_time = 1
end_time = 2


# LOAD DATASET & MAKE SUBSET

postures = np.load('posture_data_utms/observation015-postures.npy')


start_frame = int(start_time * frame_rate)
end_frame = int(end_time * frame_rate)



# Extract tail and neck points for all animals in the 10th frame
tail_points = postures[:, start_frame:end_frame, 8]
neck_points = postures[:, start_frame:end_frame, 3]



def angle_from_north(tail, neck):

    # Calculate the differences in Easting and Northing
    delta_easting = neck[0] - tail[0]
    delta_northing = neck[1] - tail[1]

    # Calculate the angle of the vector between the tail and neck points
    angle_rad = math.atan2(delta_northing, delta_easting)

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Convert the angle relative to East direction to an angle relative to North direction
    angle_from_north = (90 - angle_deg) % 360
    
    return angle_from_north


# Calculate the angle relative to North for each animal and store in a 2D list
angles_from_north = [[angle_from_north(tail_points[i, j], neck_points[i, j]) for j in range(tail_points.shape[1])] for i in range(tail_points.shape[0])]

# Print the results
for i, animal_angles in enumerate(angles_from_north):
    for j, angle in enumerate(animal_angles):
        print(f"Animal {i+1} in frame {j+10}: Angle relative to North in degrees: {angle:.2f}")
    print()
