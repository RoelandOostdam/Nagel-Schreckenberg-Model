from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import random


# def compute_traffic_flow(model):
#     agent_speeds = [agent.speed for agent in model.schedule.agents]
#     x = sorted(agent_speeds)
#     n = model.num_agents
#     return sum(x)/n

class CarAgent(Agent):
	""" An agent with fixed initial wealth."""

	def __init__(self, unique_id, model, acceleration, vision_range, randomization, speed_limit):
		super().__init__(unique_id, model)
		self.acceleration = acceleration
		self.vision_range = vision_range
		self.speed = speed_limit
		self.randomization = randomization
		self.speed_limit = speed_limit
		self.iteration = 0
		self.distance_to_precursor = 0
		self.state = "Cruising"

	def perceive(self):
		distance_to_precursor = 0
		for t in range(self.pos[0]+1, self.vision_range):
			tile = (t, 0)
			if self.model.grid.is_cell_empty(tile):
				distance_to_precursor += 1
			else:
				break
		if distance_to_precursor == 0:
			distance_to_precursor = self.vision_range
		self.distance_to_precursor = distance_to_precursor

		ran = random.randrange(0, 100)
		if self.speed > 0 and ran / 100 < self.randomization:
			self.state = "RandomBraking"
		elif distance_to_precursor < self.speed and self.speed > 0:
			self.state = "Braking"
		elif distance_to_precursor == self.speed and self.speed > 0 or self.speed == self.speed_limit:
			self.state = "Cruising"
		else:
			self.state = "Accelerating"

	def act(self):
		if self.state == "Braking":
			self.speed = self.distance_to_precursor-self.acceleration
		if self.state == "RandomBraking":
			self.speed -= self.acceleration
		if self.state == "Accelerating":
			self.speed += self.acceleration

		if self.speed < 0:
			self.speed = 0
		if self.speed > self.speed_limit:
			self.speed = self.speed_limit

	def update(self):
		pass

	def move(self):
		pos = list(self.pos)
		pos[0] += self.speed
		self.model.grid.move_agent(self, pos)

	def step(self):
		self.perceive()

	def advance(self):
		self.act()
		self.move()
		self.iteration += 1
		if self.unique_id == 5:
			print("Step:", self.iteration, "::", "Speed:", str(self.speed) + "/" + str(self.speed_limit),"-->", "Distance:", self.distance_to_precursor ,self.state)


class CarModel(Model):
	"""A model with some number of agents."""

	def __init__(self, car_count, width, height, acceleration, vision_range, randomization, speed_limit):
		self.num_agents = car_count
		self.grid = MultiGrid(width, height, True)

		self.schedule = SimultaneousActivation(self)
		self.running = True

		# Create agents
		for i in range(car_count):
			a = CarAgent(i, self, acceleration, vision_range, randomization, speed_limit)
			self.schedule.add(a)
			# Add the agent to a random grid cell
			self.grid.place_agent(a, (i, 0))

		# self.datacollector = DataCollector(
		#     model_reporters={"Traffic Flow": compute_traffic_flow(self)},
		#     agent_reporters={"Speed": "speed"}
		# )

	def step(self):
		# self.datacollector.collect(self)
		self.schedule.step()
