# -*-coding:utf-8 -*-
# to get the fitness
import random
import math
import GetR8Dex
import csv
import copy


class GA(object):

    def __init__(self, population_size, chromosome_length, pc, pm):

        self.population_size = population_size
        self.choromosome_length = chromosome_length
        # self.population=[[]]
        self.pc = pc
        self.pm = pm
        # self.fitness_value=[]

    def species_origin(self):
        population = [[]]
        for i in range(self.population_size):

            temporary = []

            for j in range(self.choromosome_length):
                temporary.append(random.randint(0, 1))


            population.append(temporary)

        return population[1:]
        # why 1:?

    def translation(self, population):

        temporary = []
        for i in range(len(population)):
            total = 0
            for j in range(self.choromosome_length):
                total += population[i][j] * (math.pow(2, j))
            temporary.append(total)
        return temporary

    def function(self, population):
        function1 = []
        for i in range(self.population_size):
            function1.append(GetR8Dex.getScore(population[i]))

        return function1


    def fitness(self, function1):

        fitness_value = []
        for i in range(self.population_size):
            fitness_value.append(1.0/function1[i])

        return fitness_value

    def sum(self, fitness_value):
        total = 0

        for i in range(len(fitness_value)):
            total += fitness_value[i]
        return total

    def cumsum(self, fitness1):
        for i in range(len(fitness1) - 2, -1, -1):
            # range(start,stop,[step])
            total = 0
            j = 0

            while (j <= i):
                total += fitness1[j]
                j += 1

            fitness1[i] = total
            fitness1[len(fitness1) - 1] = 1

    def selection(self, population, fitness_value):
        new_fitness = []

        total_fitness = self.sum(fitness_value)

        for i in range(len(fitness_value)):
            new_fitness.append(fitness_value[i] / total_fitness)

        self.cumsum(new_fitness)

        ms = []

        pop_len = len(population)

        for i in range(pop_len):
            ms.append(random.random())

        ms.sort()

        fitin = 0
        newin = 0
        new_pop = copy.deepcopy(population)
        # 轮盘赌方式

        while newin < pop_len:
            if (ms[newin] < new_fitness[fitin]):
                new_pop[newin] = population[fitin]
                newin += 1
            else:
                fitin += 1
        index = fitness_value.index(max(fitness_value))
        new_pop[0] = population[index]

        return new_pop


    def crossover(self, population):
        pop_len = len(population)

        for i in range(pop_len - 1):

            if (random.random() < self.pc):
                cpoint = random.randint(0, len(population[0]))

                temporary1 = []
                temporary2 = []

                temporary1.extend(population[i][0:cpoint])
                temporary1.extend(population[i + 1][cpoint:len(population[i])])

                temporary2.extend(population[i + 1][0:cpoint])
                temporary2.extend(population[i][cpoint:len(population[i])])

                population[i] = temporary1
                population[i + 1] = temporary2

    def mutation(self, population):

        px = len(population)

        py = len(population[0])

        for i in range(px):
            if (random.random() < self.pm):
                mpoint = random.randint(0, py - 1)
                #
                if (population[i][mpoint] == 1):
                    population[i][mpoint] = 0
                else:
                    population[i][mpoint] = 1

    def run(self,iteration):

        result_population = [[]]
        result_score = [[]]
        result_fitness = [[]]

        population = self.species_origin()

        for i in range(iteration):

            print(i)
            population1 = copy.deepcopy(population)
            result_population.append(population1)
            function_value = self.function(population)

            result_score.append(function_value)

            fitness_value = self.fitness(function_value)

            result_fitness.append(fitness_value)

            population = self.selection(population, fitness_value)

            self.crossover(population)

            self.mutation(population)


        result_population = result_population[1:]
        result_score = result_score[1:]
        result_fitness = result_fitness[1:]

        ##################write to file#################
        with open("ga_population.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            for i in range(iteration):
                tmp = []
                for j in range(self.population_size):
                    tmp.append(result_population[i][j])
                writer.writerow(tmp)

        with open("ga_fitness.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            for i in range(iteration):
                tmp = []
                for j in range(self.population_size):
                    tmp.append(result_fitness[i][j])
                writer.writerow(tmp)

        with open("ga_score.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            for i in range(iteration):
                tmp = []
                for j in range(self.population_size):
                    tmp.append(result_score[i][j])
                writer.writerow(tmp)