# -*- coding: utf-8 -*-
from operator import itemgetter
import random
import matplotlib.pyplot as plt
import numpy as np
from iris_dataset import read_data, pre_processing
import time


# 双曲函数
def tanh(x):
    return np.tanh(x)


# 双曲函数导数
def tanh_derivate(x):
    return 1.0 - np.tanh(x) * np.tanh(x)


# Sigmoid函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# Sigmoid函数导数
def sigmoid_derivate(x):
    return sigmoid(x) * (1 - sigmoid(x))


# Each fitness is a small fraction of the total error
def calculate_fit(loss):
    total, fitnesses = sum(loss), []
    for i in range(len(loss)):
        fitnesses.append(loss[i] / total)
    return fitnesses


# takes a population of NetWork objects
def pair_pop(iris_data, pop):
    weights, loss = [], []

    # for each individual
    for individual_obj in pop:
        weights.append([individual_obj.weights_input, individual_obj.weights_output])
        # append 1/sum(MSEs) of individual to list of pop errors
        loss.append(individual_obj.sum_loss(data=iris_data))

    # fitnesses are a fraction of the total error
    fitnesses = calculate_fit(loss)
    for i in range(int(pop_size * 0.15)):
        print(str(i).zfill(2), '1/sum(MSEs)', str(loss[i]).rjust(15), str(
            int(loss[i] * graphical_error_scale) * '-').rjust(20), 'fitness'.rjust(12), str(fitnesses[i]).rjust(
            17), str(int(fitnesses[i] * 1000) * '-').rjust(20))
    del pop

    # Weight becomes item [0] and fitness [1] in this way, fitness is paired with its weight in a tuple
    return zip(weights, loss, fitnesses)


def roulette(fitness_scores):
    """The fitness score is part and their sum is 1. Fitter chromosomes have a bigger score."""
    cumalative_fitness = 0.0
    r = random.random()
    # Fitness score for each chromosome
    for i in range(len(fitness_scores)):
        # Fitness scores are added for each chromosome to accrue fitness
        cumalative_fitness += fitness_scores[i]
        # The colorimetric index is returned if the cumulative fitness is greater than r
        if cumalative_fitness > r:
            return i


def iterate_pop(ranked_pop):
    ranked_weights = [item[0] for item in ranked_pop]
    fitness_scores = [item[-1] for item in ranked_pop]
    new_pop_weight = [eval(repr(x)) for x in ranked_weights[:int(pop_size * 0.15)]]

    # Reproduce two randomly selected, but different chromos, until pop_size is reached
    while len(new_pop_weight) <= pop_size:
        ch1, ch2 = [], []
        index1 = roulette(fitness_scores)
        index2 = roulette(fitness_scores)
        while index1 == index2:
            # Make sure different chromosomes are used for breeding
            index2 = roulette(fitness_scores)
        # index1, index2 = 3,4
        ch1.extend(eval(repr(ranked_weights[index1])))
        ch2.extend(eval(repr(ranked_weights[index2])))
        if random.random() < crossover_rate:
            ch1, ch2 = crossover(ch1, ch2)
        mutate(ch1)
        mutate(ch2)
        new_pop_weight.append(ch1)
        new_pop_weight.append(ch2)
    return new_pop_weight


def crossover(m1, m2):
    # ni*nh+nh*no  = total weights
    r = random.randint(0, (nodes_input * nodes_hidden) + (nodes_hidden * nodes_output))
    output1 = [[[0.0] * nodes_hidden] * nodes_input, [[0.0] * nodes_output] * nodes_hidden]
    output2 = [[[0.0] * nodes_hidden] * nodes_input, [[0.0] * nodes_output] * nodes_hidden]
    for i in range(len(m1)):
        for j in range(len(m1[i])):
            for k in range(len(m1[i][j])):
                if r >= 0:
                    output1[i][j][k] = m1[i][j][k]
                    output2[i][j][k] = m2[i][j][k]
                elif r < 0:
                    output1[i][j][k] = m2[i][j][k]
                    output2[i][j][k] = m1[i][j][k]
                r -= 1
    return output1, output2


def mutate(m):
    # A constant can be included to control how much the weight has been abruptly changed
    for i in range(len(m)):
        for j in range(len(m[i])):
            for k in range(len(m[i][j])):
                if random.random() < mutation_rate:
                    m[i][j][k] = random.uniform(-2.0, 2.0)


def rank_pop(new_pop_weight, pop):
    # The new neural network is assigned to the pop_size list
    loss, copy = [], []
    pop = [NeuralNetwork(nodes_input, nodes_hidden, nodes_output) for _ in range(pop_size)]
    for i in range(pop_size):
        copy.append(new_pop_weight[i])

    for i in range(pop_size):
        # Everyone is assigned the weight generated by the previous iteration
        pop[i].assign_weights(new_pop_weight, i)
        pop[i].test_weights(new_pop_weight, i)

    for i in range(pop_size):
        pop[i].test_weights(new_pop_weight, i)

    # Calculate the fitness of these weights and modify them with weights
    paired_pop = pair_pop(iris_train_data, pop)

    # The weights are sorted in descending order of fitness (most suitable)
    ranked_pop = sorted(paired_pop, key=itemgetter(-1), reverse=True)
    loss = [eval(repr(x[1])) for x in ranked_pop]
    return ranked_pop, eval(repr(ranked_pop[0][1])), float(sum(loss)) / float(len(loss))


def randomize_matrix(matrix, a, b):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = random.uniform(a, b)


class NeuralNetwork(object):
    def __init__(self, nodes_input, nodes_hidden, nodes_output, activation_fun='tanh'):
        # number of input, hidden, and output nodes
        self.nodes_input = nodes_input
        self.nodes_hidden = nodes_hidden
        self.nodes_output = nodes_output

        # activations for nodes
        self.activations_input = [1.0] * self.nodes_input
        self.activations_hidden = [1.0] * self.nodes_hidden
        self.activations_output = [1.0] * self.nodes_output

        # create weights
        self.weights_input = [[0.0] * self.nodes_hidden for _ in range(self.nodes_input)]
        self.weights_output = [[0.0] * self.nodes_output for _ in range(self.nodes_hidden)]
        randomize_matrix(self.weights_input, -0.1, 0.1)
        randomize_matrix(self.weights_output, -2.0, 2.0)

        # define activation function
        if activation_fun is 'tanh':
            self.activation_fun = tanh
            self.activation_fun_deriv = tanh_derivate
        elif activation_fun is 'sigmoid':
            self.activation_fun = sigmoid
            self.activation_fun_deriv = sigmoid_derivate

    def sum_loss(self, data):
        loss = 0.0
        for item in data:
            inputs = item[0]
            targets = item[1]
            self.feed_forward(inputs)
            loss += self.calculate_loss(targets)
        inverr = 1.0 / loss
        return inverr

    def calculate_loss(self, targets):
        loss = 0.0
        for k in range(len(targets)):
            loss += 0.5 * (targets[k] - self.activations_output[k]) ** 2
        return loss

    def feed_forward(self, inputs):
        if len(inputs) != self.nodes_input:
            print('incorrect number of inputs')

        for i in range(self.nodes_input):
            self.activations_input[i] = inputs[i]

        for j in range(self.nodes_hidden):
            self.activations_hidden[j] = self.activation_fun(
                sum([self.activations_input[i] * self.weights_input[i][j] for i in range(self.nodes_input)]))
        for k in range(self.nodes_output):
            self.activations_output[k] = self.activation_fun(
                sum([self.activations_hidden[j] * self.weights_output[j][k] for j in range(self.nodes_hidden)]))
        return self.activations_output

    def assign_weights(self, weights, I):
        io = 0
        for i in range(self.nodes_input):
            for j in range(self.nodes_hidden):
                self.weights_input[i][j] = weights[I][io][i][j]
        io = 1
        for j in range(self.nodes_hidden):
            for k in range(self.nodes_output):
                self.weights_output[j][k] = weights[I][io][j][k]

    def test_weights(self, weights, I):
        same = []
        io = 0
        for i in range(self.nodes_input):
            for j in range(self.nodes_hidden):
                if self.weights_input[i][j] != weights[I][io][i][j]:
                    same.append(('I', i, j, round(self.weights_input[i][j], 2), round(weights[I][io][i][j], 2),
                                 round(self.weights_input[i][j] - weights[I][io][i][j], 2)))

        io = 1
        for j in range(self.nodes_hidden):
            for k in range(self.nodes_output):
                if self.weights_output[j][k] != weights[I][io][j][k]:
                    same.append((('O', j, k), round(self.weights_output[j][k], 2), round(weights[I][io][j][k], 2),
                                 round(self.weights_output[j][k] - weights[I][io][j][k], 2)))
        if same:
            print(same)

    def test(self, data):
        results, targets = [], []
        for d in data:
            inputs = d[0]
            rounded = [round(i) for i in self.feed_forward(inputs)]
            if rounded == d[1]:
                result = '√ Classification Prediction is Correct '
            else:
                result = '× Classification Prediction is Wrong'
            print('{0} {1} {2} {3} {4} {5} {6}'.format(
                'Inputs:', d[0], '-->', str(self.feed_forward(inputs)).rjust(65), 'target classification', d[1],
                result))
            results += self.feed_forward(inputs)
            targets += d[1]
        return results, targets


start = time.clock()

graphical_error_scale = 300
max_iterations = 10
pop_size = 100
mutation_rate = 0.1
crossover_rate = 0.8
nodes_input, nodes_hidden, nodes_output = 4, 6, 1
x_train, x_test, y_train, y_test = read_data()
iris_train_data, iris_test_data = pre_processing(x_train, x_test, y_train, y_test)

# Sort the random population for the first time
pop = [NeuralNetwork(nodes_input, nodes_hidden, nodes_output) for i in range(pop_size)]  # fresh pop

paired_pop = pair_pop(iris_train_data, pop)

ranked_pop = sorted(paired_pop, key=itemgetter(-1), reverse=True)  # THIS IS CORRECT

# Sort the random population for the first time
iters = 0
tops, avgs = [], []

while iters != max_iterations:
    if iters % 1 == 0:
        print('Iteration'.rjust(150), iters)

    new_pop_weight = iterate_pop(ranked_pop)
    ranked_pop, toperr, avgerr = rank_pop(new_pop_weight, pop)

    tops.append(toperr)
    avgs.append(avgerr)
    iters += 1

end = time.clock()
print("generations of genetic total time-consuming: " + str(end - start))

# test a NN with the fittest weights
tester = NeuralNetwork(nodes_input, nodes_hidden, nodes_output)
fittestWeights = [x[0] for x in ranked_pop]
tester.assign_weights(fittestWeights, 0)
results, targets = tester.test(iris_test_data)
x = np.arange(0, 150)
title2 = 'Test after ' + str(iters) + ' iterations'
plt.title(title2)
plt.ylabel('Node output')
plt.xlabel('Instances')
plt.plot(results, 'xr', linewidth=0.5)
plt.plot(targets, 's', color='black', linewidth=3)
# lines = plt.plot(results, 'sg')
plt.annotate(s='Target Values', xy=(110, 0), color='black', family='sans-serif', size='small')
plt.annotate(s='Test Values', xy=(110, 0.5), color='red', family='sans-serif', size='small', weight='bold')
plt.figure(2)
plt.subplot(121)
plt.title('Top individual error evolution')
plt.ylabel('Inverse error')
plt.xlabel('Iterations')
plt.plot(tops, '-g', linewidth=1)
plt.subplot(122)
plt.plot(avgs, '-g', linewidth=1)
plt.title('Population average error evolution')
plt.ylabel('Inverse error')
plt.xlabel('Iterations')
plt.show()

print('max_iterations', max_iterations, 'pop_size', pop_size, 'pop_size*0.15', int(
    pop_size * 0.15), 'mutation_rate', mutation_rate, 'crossover_rate', crossover_rate,
      'nodes_input, nodes_hidden, nodes_output', nodes_input, nodes_hidden, nodes_output)
