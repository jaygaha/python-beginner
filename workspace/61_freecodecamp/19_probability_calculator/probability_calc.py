# Build a Probability Calculator
# Ref: https://www.freecodecamp.org/learn/scientific-computing-with-python/build-a-probability-calculator-project/build-a-probability-calculator-project
#
# Suppose there is a hat containing 5 blue balls, 4 red balls, and 2 green balls. What is the probability that a random draw of 4 balls will contain at least 1 red ball
# and 2 green balls? While it would be possible to calculate the probability using advanced mathematics, an easier way is to write a program to perform a large number of experiments to
# estimate an approximate probability.
#
# For this project, you will write a program to determine the approximate probability of drawing certain balls randomly from a hat.
import random
import copy
from collections import Counter

class Hat:
    def __init__(self, **kwargs):
        """
        Initialize the Hat with balls of different colors.
        Each keyword argument represents the color and the number of balls of that color.
        """
        self.contents = []

        for color, num in kwargs.items():
            self.contents.extend([color] * num)

    def draw(self, num_balls):
        """
        Draw num_balls balls randomly from the hat and return them.
        If num_balls exceeds the number of available balls, return all remaining balls.
        """
        if num_balls >= len(self.contents):
            # If more balls are requested than are available, return all remaining balls
            drawn_balls = self.contents
            self.contents = []  # Empty the hat after drawing all balls
        else:
            drawn_balls = random.sample(self.contents, num_balls)
            for ball in drawn_balls:
                self.contents.remove(ball)

        return drawn_balls

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    """
    Run num_experiments experiments where balls are drawn from the hat and check how many
    times we match the expected_balls.
    """
    success_count = 0

    for _ in range(num_experiments):
        # make a copy of the hat contents to avoid changing the original
        # hat_copy = Hat(**{color: hat.contents.count(color) for color in set(hat.contents)})
        # Create a deep copy of the hat for each experiment
        hat_copy = copy.deepcopy(hat)

        # draw ball from the hat
        drawn_balls = hat_copy.draw(num_balls_drawn)

        # Count how many of each color is in the drawn balls
        drawn_counter = Counter(drawn_balls)
        # ball_counts = {color: drawn_balls.count(color) for color in set(drawn_balls)}

        # Check if the drawn balls meet or exceed the expected number of each color
        # if all(ball_counts.get(color, 0) >= count for color, count in expected_balls.items()):
        if all(drawn_counter[color] >= count for color, count in expected_balls.items()):
            success_count += 1

    # Calculate the probability as the ratio of successful experiments to total experiments
    probability = success_count / num_experiments

    return probability


if __name__ == "__main__":
    hat = Hat(black=6, red=4, green=3)
    probability = experiment(hat=hat,
                             expected_balls={'red': 2, 'green': 1},
                             num_balls_drawn=5,
                             num_experiments=2000)

    print(probability) # 0.3725
