from mesa.batchrunner import BatchRunner
from traffic_simulation.model import MoneyModel, compute_gini
import matplotlib.pyplot as plt

fixed_params = {
    "width": 10,
    "height": 10
}

variable_params = {"N": range(10, 100, 10)}
# The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
batch_run = BatchRunner(
    MoneyModel,
    variable_params,
    fixed_params,
    iterations=1,
    max_steps=30,
    model_reporters={"Gini": compute_gini}
)

batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
# run_data.head()
plt.scatter(run_data.N, run_data.Gini)
plt.show()
