# genetic algorithm neural network
Classification model prediction, neural network optimization based on genetic algorithm --- iris dataset

**This is the final exam for the last course (Computational Intelligence) when I was a graduate student at Chonnam National University.**

- Neural network architecture is 4,6,1

- the data source is iris data set, a total of 150 cases, which is divided into three categories: iris-setosa, iris-versicolor, iris-virginica

- use the marker in supervised learning. -1 ---> iris-setosa  0 ---> iris-versicolor   1 ---> iris-virginica

- the training set selected a total of 120 cases, evenly distributed three types of tags.

- the test set selected 30 cases.

## Result:
### 1. When the maximum number of iterations is 300 generations:

max_iterations 300, pop_size 100, pop_size*0.15, 15 mutation_rate 0.1, crossover_rate 0.8 , [nodes_input, nodes_hidden, nodes_output 4 6 1]

![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/300%20generations/Figure_0.png)

There are 2 classification prediction errors in 30 cases. The success rate is very high, indicating that genetic algorithms do start to work.

![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/300%20generations/Figure_1.png)
![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/300%20generations/Figure_2.png)

### 2. When the maximum number of iterations is 1000 generations:

max_iterations 1000, pop_size 100, pop_size*0.15, 15 mutation_rate 0.1, crossover_rate 0.8 , [nodes_input, nodes_hidden, nodes_output 4 6 1]

![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/1000%20generations/Figure_0.png)

All 30 categories in the test data set were correctly predicted, indicating that the best basic gene was found.	
![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/1000%20generations/Figure_1.png)
![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/1000%20generations/Figure_2.png)

### 3. When the maximum number of iterations is 3000 generations:

max_iterations 3000, pop_size 100, pop_size*0.15, 15 mutation_rate 0.1, crossover_rate 0.8 , [nodes_input, nodes_hidden, nodes_output 4 6 1]

![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/3000%20generations/Figure_0.png)

Instead, there is 1 classification error, indicating that good genes may mutate each time they go down to multiply iterations. But still does not affect the prediction accuracy. You can use fuzzy theory to circumvent this situation.

![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/3000%20generations/Figure_1.png)

But most classification predictions are getting closer and closer to the target output.

![](https://github.com/WEIHAITONG1/genetic-algorithm-neural-network/blob/master/3000%20generations/Figure_2.png)

> PS: 
> 一、Python script depends on 3 packages :

> 1.	pandas         pip3 install pandas
> 2.	numpy          pip3 install numpy
> 3.	matplotlib      pip3 install matplotlib

> 二、python runtime environment in python3.6.3 version of the operation

> 三、Please run gann_main script.
