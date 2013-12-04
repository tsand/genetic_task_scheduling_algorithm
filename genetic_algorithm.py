# To run this file use the command "python genetic_algorithm.py" in the base directory
# This is file is where the genetic algorithm code will be
# Note: I've added a little skeleton code here just as a placeholder. No need to use it.

###############
#   imports
###############

import random

###############
#  Constants
###############

POPULATION_SIZE = 20

REPRODUCE_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.1

TOTAL_TIME_WEIGHT = 0.8
PRIORITIZED_THROUGHPUT_WEIGHT = 0.2

###############
#   Classes
###############


class Task:
	def __init__(self, name, duration, priority, dependencies=[]):
		self.name = name
		self.duration = duration
		self.priority = priority
		self.dependencies = dependencies
		self.min_completion_time = -1

	def get_name(self):
		return self.name

	def get_duration(self):
		return self.duration

	def get_priority(self):
		return self.priority

	def get_dependencies(self):
		return self.dependencies

	def get_min_completion_time(self):
		if self.min_completion_time < 0:
			self.min_completion_time = self.duration
			if len(self.dependencies) > 0:
				self.min_completion_time += max([task.get_min_completion_time() for task in self.dependencies])
		return self.min_completion_time


class Schedule:
	def __init__(self, processor_schedules=[]):
		self.processor_schedules = processor_schedules

	def min_processor_schedule_length(self):
		return min([len(processor) for processor in self.processor_schedules])

	def has_unique_tasks(self, num_tasks):
		task_map = {}
		for processor in self.processor_schedules:
			for task in processor:
				if task in task_map:
					return False
				else:
					task_map[task.name] = None

		return len(task_map) == num_tasks

	def get_task_location(self, task):
		for i in range(len(self.processor_schedules)):
			for j in range(len(self.processor_schedules[i])):
				if self.processor_schedules[i][j].name == task.name:
					return i, j
		return None

	def calculate_task_completion(self, results, processor_index, task_index):
		task = self.processor_schedules[processor_index][task_index]

		if task in results:
			return results[task.get_name()]

		previous_task_completion = 0 if task_index == 0 else self.calculate_task_completion(results, processor_index, task_index - 1)

		dependency_completions = []
		for dependency in task.get_dependencies():
			if dependency in results:
				dependency_completions.append(results[dependency])
			else:
				location = self.get_task_location(dependency)
				dependency_completions.append(self.calculate_task_completion(results, location[0], location[1]))

		results[task.get_name()] = max(previous_task_completion, max(dependency_completions + [0])) + task.get_duration()
		return results[task.get_name()]

	def calculate_task_completion_map(self):
		results = {}
		for i in range(len(self.processor_schedules)):
			for j in range(len(self.processor_schedules[i])):
				self.calculate_task_completion(results, i, j)
		return results

	def clone(self):
		return Schedule([list(processor) for processor in self.processor_schedules])

	def reproduce(self, other):
		max_crossover_index = min(self.min_processor_schedule_length(), other.min_processor_schedule_length())
		crossover_index = random.randrange(0, max_crossover_index)

		child1 = self.clone()
		for i in range(len(child1.processor_schedules)):
			child1.processor_schedules[i][crossover_index:] = other.processor_schedules[i][crossover_index:]

		child2 = other.clone()
		for i in range(len(child2.processor_schedules)):
			child2.processor_schedules[i][crossover_index:] = self.processor_schedules[i][crossover_index:]

		return [child1, child2]

	def mutate(self):
		from_processor = random.choice(self.processor_schedules)
		to_processor = random.choice(self.processor_schedules)

		from_task = random.choice(from_processor)
		from_processor.remove(from_task)

		min_to_index = 0
		for i in range(len(to_processor)):
			if to_processor[i] in from_task.get_dependencies():
				min_to_index = i

		to_processor.insert(random.randrange(min_to_index + 1, len(to_processor) + 1), from_task)


class GeneticTaskScheduler:

	def __init__(self, tasks):
		self.tasks = tasks

	"""
	This function, given the tasks, number of processors, and population size, will
	produce an initial population.
	"""
	def initialize(self, num_processors, population_size):
		# Generate first schedule based on min completion time
		self.tasks.sort(None, lambda task: task.get_min_completion_time())
		processor_schedules = [[]] * num_processors

		for i in range(len(self.tasks)):
			processor_schedules[i % num_processors].append(self.tasks[i])

		population = [Schedule(processor_schedules)]

		# Generate the rest of the initial population from random mutations of the first schedule
		for j in range(population_size - 1):
			new_schedule = population[0].clone()
			new_schedule.mutate()
			population.append(new_schedule)

		return population

	"""
	This function, given the population, will randomly select individuals for reproduction
	"""
	def reproduce(self, population):
		fertile_list = []
		for individual in population:
			if random.random() < REPRODUCE_PROBABILITY:
				fertile_list.append(individual)

		random.shuffle(fertile_list)
		for i in range(0, len(fertile_list) - 1, 2):
			population.append(fertile_list[i].reproduce(fertile_list[i+1]))


	"""
	This function, given the population, will randomly select individuals for mutation
	"""
	def mutate(self, population):
		for individual in population:
			if random.random() < MUTATION_PROBABILITY:
				individual.mutate()

	"""
	This function calculates a list of fitness values for the population
	"""
	def fitness(self, population):
		fitness_list = []
		total_time_list = []
		prioritized_throughput_list = []

		for i in range(len(population)):
			if not population[i].has_unique_tasks(len(self.tasks)):
				total_time_list[i] = None
				prioritized_throughput_list[i] = None
			else:
				task_completions = population[i].calculate_task_completion_map()
				total_time_list[i] = max(task_completions.values())
				prioritized_throughput_list[i] = sum(item[0].get_priority() * item[1] for item in task_completions.items())

		min_total_time = min(val for val in total_time_list if val > 0)
		max_total_time = max(total_time_list)

		min_prioritized_throughput = min(val for val in prioritized_throughput_list if val > 0)
		max_prioritized_throughput = max(prioritized_throughput_list)

		for i in range(len(population)):
			if total_time_list[i] <= 0 or prioritized_throughput_list[i] <= 0:
				fitness_list[i] = 0
			else:
				if min_total_time == max_total_time:
					total_time_comp = 1
				else:
					total_time_comp = (max_total_time - total_time_list[i]) / (max_total_time - min_total_time)

				if min_prioritized_throughput == max_prioritized_throughput:
					prioritized_throughput_comp = 1
				else:
					prioritized_throughput_comp = (max_prioritized_throughput - prioritized_throughput_list[i]) / (max_prioritized_throughput - min_prioritized_throughput)

				fitness_list[i] = 1 + (TOTAL_TIME_WEIGHT * total_time_comp) + (PRIORITIZED_THROUGHPUT_WEIGHT * prioritized_throughput_comp)

		return fitness_list

	"""
	This function determines the individuals that survive to reproduce based on their fitness
	"""
	def select(self, old_population):
		new_population = []
		fitness_list = self.fitness(old_population)
		fitness_sum = sum(fitness_list)

		for i in range(POPULATION_SIZE):
			survival_value = random.randrange(1, fitness_sum + 1)
			for j in range(len(fitness_list)):
				survival_value -= fitness_list[j]
				if survival_value <= 0:
					new_population.append(old_population[j])

		return new_population

	"""
	Given a list of tasks and constraints, this function will run the genetic algorithm
	to find a good schedule.
	"""
	def schedule_tasks(self, num_processors, generations):
		population = self.initialize(num_processors, POPULATION_SIZE)

		for i in range(generations):
			self.select(population)
			self.reproduce(population)
			self.mutate(population)

		random.shuffle(population)
		fitness_list = self.fitness(population)
		return population[fitness_list.index(max(fitness_list))]

if __name__ == "__main__":
	t1=Task("T1", 2, 8)
	t2=Task("T2", 3, 2, [t1])

	scheduler = GeneticTaskScheduler([t1,t2])
	scheduler.schedule_tasks(3, 10)
	print "This is just like the java main method"