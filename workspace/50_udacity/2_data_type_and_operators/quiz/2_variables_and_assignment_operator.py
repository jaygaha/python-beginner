# The current volume of a water reservoir (in cubic metres)
reservoir_volume = 4.445e8
# The amount of rainfall from a storm (in cubic metres)
rainfall = 5e6

# Decrease the rainfall variable by 10% to account for runoff
rainfall *= 0.9

# Add the rainfall variable to the reservoir_volume variable
reservoir_volume += rainfall

# Increase reservoir_volume by 5% to account for stormwater that flows
# into the reservoir in the days following the storm
reservoir_volume *= 1.05

# Decrease reservoir_volume by 5% to account for evaporation
reservoir_volume *= 0.95

# Subtract 2.5e5 cubic metres from reservoir_volume to account for water
# that's piped to arid regions.
reservoir_volume -= 2.5e5

# Print the new value of the reservoir_volume variable
print(reservoir_volume)
