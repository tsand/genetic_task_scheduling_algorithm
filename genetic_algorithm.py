# To run this file use the command "python genetic_algorithm.py" in the base directory
# This is file is where the genetic algorithm code will be
# Note: I've added a little skeleton code here just as a placeholder. No need to use it.

###############
#  Constants
###############

POPULATION_SIZE = 10

REPRODUCE_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.1

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
		return min([len(schedule) for schedule in self.processor_schedules])

	def get_processor_schedule(self, processor_index, from_index, to_index=-1):
		if to_index >= 0:
			return self.processor_schedules[processor_index][from_index:to_index]
		else:
			return self.processor_schedules[processor_index][from_index:]

	def set_processor_schedule(self, value, processor_index, from_index, to_index=-1):
		if to_index >= 0:
			self.processor_schedules[processor_index][from_index:to_index] = value
		else:
			self.processor_schedules[processor_index][from_index:] = value


###############
#    Code
###############

"""
This function, given the tasks, number of processors, and population size, will
produce an initial population.
"""
def initialize(tasks, num_processors, population_size):
	# Generate first schedule based on min completion time
	tasks.sort(None, lambda task: task.get_min_completion_time())
	processor_schedules = [[]] * num_processors

	for i in range(len(tasks)):
		processor_schedules[i%num_processors].append(tasks[i])

	population = [Schedule(processor_schedules)]

	# Generate the rest of the initial population from random mutations of the first schedule

	return population

"""
This function, given two genomes, will produce an offspring genome that takes traits
from both of its parents genomes. There also is a slight chance of mutation
"""
def reproduce(schedule1, schedule2):
	return []

"""
This function decides likelihood of the given genome surviving to reproduce
"""
def fitness_function(schedule):
	return 0

"""
This function determines the individuals that get to reproduce based on their fitness
"""
def select(population):
	fitness_list = [fitness_function(population[j]) for j in range(len(population))]
	return population

"""
Given a list of tasks and constraints, this function will run the genetic algorithm
to find a good schedule.
"""
def schedule_tasks(tasks, num_processors, generations):
	population = initialize(tasks, num_processors, POPULATION_SIZE)

	for i in range(generations):
		population = select(population)

		# Randomly select schedules to reproduce and add children to population

	return population.sort(None, lambda schedule: fitness_function(schedule))[0]

if __name__ == "__main__":
	t1=Task("T1", 2, 8)
	t2=Task("T2", 3, 2, [t1])
	schedule = schedule_tasks([t1,t2], 3, 10)
	print "This is just like the java main method"