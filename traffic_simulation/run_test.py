from model import CarModel
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.stats as stats

# Config
n = 1000  # Amount of model steps
acceleration = 1
randomization = 0.005

traffic_occupations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 50]  # Car counts
speed_limits = [5, 8, 10, 13]

results_speed = []
results_delay = []
for num, cars in enumerate(traffic_occupations, start=0):

    print("Running: " + str(cars) + " cars..")
    results_speed.append([])
    results_delay.append([])
    settings = []
    for x in speed_limits:
        settings.append([cars, 100, acceleration, 50, randomization, x])

    for num_setting, setting in enumerate(settings, start=0):
        results_speed[num].append([])
        results_delay[num].append([])
        all_delay = []
        all_speeds = []
        model = CarModel(*setting)
        for i in range(n):
            model.step()

            # Store the results
            total = 0
            for agent in model.schedule.agents:
                total += agent.speed
            ave_speed = total / model.num_agents
            all_delay.append(abs(setting[5] - ave_speed))
            all_speeds.append(ave_speed)
        results_speed[num][num_setting] = np.mean(all_speeds)
        results_delay[num][num_setting] = np.mean(all_delay)


def plot_line(x_data, y_data, y_label):
    y_data_t = np.transpose(y_data)

    for data in y_data_t:
        plt.errorbar(x_data, data, yerr=data*1.65/math.sqrt(len(data)), fmt="-o")

    plt.xticks(x_data)
    plt.title("Effect van wegbezetting en snelheidslimiet op verkeersflow")
    plt.xlabel("Weg bezetting (%)")
    plt.ylabel(y_label)
    # plt.xlim(0, len(traffic_occupations))
    labels = []
    for x in settings:
        labels.append("Snelheidslimiet: " + str(x[5]))
    plt.legend(labels)
    plt.grid()
    plt.show()


plot_line(traffic_occupations, results_delay, "Gemiddelde vertraging")
plot_line(traffic_occupations, results_speed, "Gemiddelde snelheid")