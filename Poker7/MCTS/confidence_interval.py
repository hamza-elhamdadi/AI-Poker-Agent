import random
import math

def monte_carlo_simulation(num_simulations):
    wins = 0
    for _ in range(num_simulations):
        if random.random() < 0.5:  # Probability of winning
            wins += 1
    return wins / num_simulations

def calculate_confidence_interval(estimated_probability, num_simulations, confidence_level):
    z_score = {
        0.90: 1.645,
        0.95: 1.960,
        0.99: 2.576
    }

    z = z_score.get(confidence_level)
    if not z:
        raise ValueError("Unsupported confidence level. Supported levels are 0.90, 0.95, and 0.99.")

    standard_error = math.sqrt((estimated_probability * (1 - estimated_probability)) / num_simulations)
    margin_of_error = z * standard_error
    lower_bound = estimated_probability - margin_of_error
    upper_bound = estimated_probability + margin_of_error
    return (lower_bound, upper_bound)

num_simulations = 1000
estimated_probability = monte_carlo_simulation(num_simulations)
confidence_level = 0.95  # You can change this to 0.90 or 0.99 for different confidence levels
confidence_interval = calculate_confidence_interval(estimated_probability, num_simulations, confidence_level)

print("Estimated probability of winning:", estimated_probability)
print(f"{int(confidence_level * 100)}% Confidence Interval:", confidence_interval)