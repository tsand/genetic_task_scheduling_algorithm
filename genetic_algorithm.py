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

POPULATION_SIZE = 10

REPRODUCE_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.1

TOTAL_TIME_WEIGHT = 0.8
PRIORITY_FLOWTIME_WEIGHT = 0.2

###############
#   Classes
###############


class Task:
    def __init__(self, identifier, name, duration, priority, dependencies=None):
        if not dependencies:
            dependencies = []

        self.identifier = identifier
        self.name = name
        self.duration = duration
        self.priority = priority
        self.dependencies = dependencies
        self.min_completion_time = -1

    def is_dependency_of(self, other):
        """
        Returns true if this task is a dependency (direct or indirect) of other
        """
        return (self in other.dependencies) or any(self.is_dependency_of(task) for task in other.dependencies)

    def get_min_completion_time(self):
        """
        Returns the minimum completion time of this task based on the minimum completion times of its dependencies
        """
        if self.min_completion_time < 0:
            self.min_completion_time = self.duration
            if len(self.dependencies) > 0:
                self.min_completion_time += max(
                    [task.get_min_completion_time() for task in self.dependencies])
        return self.min_completion_time

    def __repr__(self):
        return '<Task %s>' % self.identifier


class Schedule:
    def __init__(self, processor_schedules=None):
        if not processor_schedules:
            processor_schedules = []
        self.processor_schedules = processor_schedules
        self.task_completion_map = {}
        self.task_dependency_set_map = {}

    def min_processor_schedule_length(self):
        """
        Returns the number of tasks in the smallest processor
        """
        return min([len(processor) for processor in self.processor_schedules])

    def has_unique_tasks(self):
        """
        Returns true if the schedule does not have more than one of the same task
        """
        task_set = set()
        task_sum = 0
        for processor in self.processor_schedules:
            task_set.update(processor)
            task_sum += len(processor)
        return len(task_set) == task_sum

    def has_direct_dependency_violation(self):
        """
        Returns true if in any processor, a task is executed before one of its dependencies
        """
        for processor in self.processor_schedules:
            for i in range(len(processor)):
                for dependency in processor[i].dependencies:
                    if dependency in processor[i+1:]:
                        return True
        return False

    def get_task_location(self, task):
        """
        Returns the processor and task indices of any given task, None if the task is not in this schedule
        """
        for i in range(len(self.processor_schedules)):
            for j in range(len(self.processor_schedules[i])):
                if self.processor_schedules[i][j].name == task.name:
                    return i, j
        return None

    def get_dependency_set(self, task):
        """
        Returns the set of all tasks the given task must be executed after in this schedule
        """
        if task in self.task_dependency_set_map:
            return self.task_dependency_set_map[task]

        dependency_set = set()

        for dependency in task.dependencies:
            dependency_set.add(dependency)
            dependency_set.update(self.get_dependency_set(dependency))

        location = self.get_task_location(task)
        for previous_task in self.processor_schedules[location[0]][0:location[1]]:
            dependency_set.add(previous_task)
            dependency_set.update(self.get_dependency_set(previous_task))

        self.task_dependency_set_map[task] = dependency_set

        return dependency_set

    def calculate_task_completion(self, processor_index, task_index):
        """
        Recursively determines when a task completes
        """
        task = self.processor_schedules[processor_index][task_index]

        if task in self.task_completion_map:
            return self.task_completion_map[task.identifier]

        previous_task_completion = 0 if task_index <= 0 else self.calculate_task_completion(processor_index,
                                                                                            task_index - 1)
        dependency_completions = []
        for dependency in task.dependencies:
            if dependency in self.task_completion_map:
                dependency_completions.append(self.task_completion_map[dependency])
            else:
                location = self.get_task_location(dependency)
                dependency_completions.append(
                    self.calculate_task_completion(location[0], location[1]))

        self.task_completion_map[task.identifier] = max(previous_task_completion,
                                                        max(dependency_completions + [0])) + task.duration
        return self.task_completion_map[task.identifier]

    def get_task_completion_map(self):
        """
        For each task determine when it completes
        """
        for i in range(len(self.processor_schedules)):
            for j in range(len(self.processor_schedules[i])):
                self.calculate_task_completion(i, j)
        return self.task_completion_map

    def calculate_time_grid(self, total_time):
        """
        Calculates the grid of time slots and which task is executing during each
        """
        time_grid = [[0 for x in range(total_time)] for y in range(len(self.processor_schedules))]
        for i, processor in enumerate(self.processor_schedules):
            for j, task in enumerate(processor):
                end_time = self.calculate_task_completion(i, j)
                time_grid[i][(end_time - task.duration):end_time] = [task] * task.duration

        return time_grid

    def clone(self):
        """
        Duplicates the schedule
        """
        return Schedule([list(processor) for processor in self.processor_schedules])

    def reproduce(self, other):
        """
        Given another schedule, generates at most two offspring
        """
        max_crossover_index = min(self.min_processor_schedule_length(),
                                  other.min_processor_schedule_length())
        crossover_index = random.randrange(0, max_crossover_index + 1)

        child1 = self.clone()
        for i, processor in enumerate(child1.processor_schedules):
            processor[crossover_index:] = other.processor_schedules[i][crossover_index:]

        child2 = other.clone()
        for i, processor in enumerate(child2.processor_schedules):
            processor[crossover_index:] = self.processor_schedules[i][crossover_index:]

        return [child for child in [child1, child2] if not child.has_direct_dependency_violation()]

    def mutate(self):
        """
        Chooses 1 task and moves it to a random valid index in the schedule
        """
        self.task_completion_map.clear()
        self.task_dependency_set_map.clear()
        from_processor = random.choice([processor for processor in self.processor_schedules if len(processor)])
        from_task = random.choice(from_processor)

        processor_range = list(range(len(self.processor_schedules)))
        random.shuffle(processor_range)
        for i in processor_range:
            to_processor = self.processor_schedules[i]

            min_to_index = 0
            for j in range(len(to_processor)):
                for dependency in from_task.dependencies:
                    if to_processor[j] == dependency or to_processor[j] in self.get_dependency_set(dependency):
                        min_to_index = j + 1
                        break

            max_to_index = len(to_processor)
            for j in reversed(range(len(to_processor))):
                if from_task in self.get_dependency_set(to_processor[j]):
                    max_to_index = j

            if min_to_index <= max_to_index:
                insert_index = random.randrange(min_to_index, max_to_index + 1)
                if from_processor == to_processor and from_processor.index(from_task) < insert_index:
                    to_processor.insert(insert_index, from_task)
                    from_processor.remove(from_task)
                else:
                    from_processor.remove(from_task)
                    to_processor.insert(insert_index, from_task)
                return


class GeneticTaskScheduler:
    def __init__(self, tasks):
        self.tasks = tasks
        self.total_time = 0
        self.total_time_bound = 0
        self.priority_flowtime_bound = 0

    def initialize(self, num_processors, population_size, total_time):
        """
        This function, given the tasks, number of processors, and population size, will
        produce an initial population.
        """
        self.total_time = total_time

        # Calculate upper bounds for fitness measures
        prioritized_tasks = list(self.tasks)
        prioritized_tasks.sort(key=lambda task: task.priority)
        for task in prioritized_tasks:
            self.total_time_bound += task.duration
            self.priority_flowtime_bound += self.total_time_bound * task.priority

        self.total_time_bound += 1
        self.priority_flowtime_bound += 1

        # Generate first schedule based on min completion time
        self.tasks.sort(key=lambda task: task.get_min_completion_time())
        processor_schedules = [[] for i in range(num_processors)]

        for i in range(len(self.tasks)):
            processor_schedules[i % num_processors].append(self.tasks[i])

        population = [Schedule(processor_schedules)]

        # Generate the rest of the initial population from random mutations of the first schedule
        for j in range(population_size - 1):
            new_schedule = population[0].clone()
            new_schedule.mutate()
            population.append(new_schedule)

        return population

    def _get_task(self, identifier):
        """
        Retrieves a task by its identifier
        """
        for task in self.tasks:
            if task.identifier == identifier:
                return task
        return None

    def reproduce(self, population):
        """
        This function, given the population, will randomly select individuals for reproduction
        and add the children to the population
        """
        fertile_list = []
        for individual in population:
            if random.random() < REPRODUCE_PROBABILITY:
                fertile_list.append(individual)

        random.shuffle(fertile_list)
        for i in range(0, len(fertile_list) - 1, 2):
            population += fertile_list[i].reproduce(fertile_list[i + 1])

    def mutate(self, population):
        """
        This function, given the population, will randomly select individuals for mutation
        """
        for individual in population:
            if individual.has_unique_tasks() and random.random() < MUTATION_PROBABILITY:
                individual.mutate()

    def fitness(self, population):
        """
        This function calculates a list of fitness values for the population
        """
        fitness_list = []

        for schedule in population:
            if not schedule.has_unique_tasks():
                fitness_list.append(0)
                continue

            task_completions = schedule.get_task_completion_map()
            total_time = max(task_completions.values())
            if total_time > self.total_time:
                fitness_list.append(0)
                continue

            priority_flowtime = 0
            for key in task_completions:
                task = self._get_task(key)
                value = task_completions[key]
                priority_flowtime += task.priority * value

            fitness_value = round(TOTAL_TIME_WEIGHT * (self.total_time_bound - total_time) +
                                  PRIORITY_FLOWTIME_WEIGHT * (self.priority_flowtime_bound - priority_flowtime))
            fitness_list.append(fitness_value)

        return fitness_list

    def select(self, old_population):
        """
        This function randomly selects the individuals that survive to reproduce based on their fitness
        """
        new_population = []
        fitness_list = self.fitness(old_population)
        fitness_sum = sum([val for val in fitness_list if val])

        for i in range(POPULATION_SIZE):
            survival_value = random.randrange(1, fitness_sum + 1)
            for j, fitness in enumerate(fitness_list):
                survival_value -= fitness
                if survival_value <= 0:
                    new_population.append(old_population[j])

        return new_population

    def schedule_tasks(self, num_processors, generations, total_time):
        """
        Given a list of constraints, this function will run the genetic algorithm
        on the tasks to find a good schedule.
        """
        population = self.initialize(num_processors, POPULATION_SIZE, total_time)

        for i in range(generations):
            self.select(population)
            self.reproduce(population)
            self.mutate(population)

        random.shuffle(population)
        fitness_list = self.fitness(population)
        best_schedule = population[fitness_list.index(max(fitness_list))]

        time_grid = []
        for processor in best_schedule.calculate_time_grid(total_time):
            time_grid.append(processor)

        return time_grid
