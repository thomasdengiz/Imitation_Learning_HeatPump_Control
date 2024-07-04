## Content
This repository contains the code for the paper “Imitation learning with artificial neural networks for demand response with a heuristic control approach for heat pumps.” by [ToDo: Add names and link]. In the paper, different machine learning approaches (multi-layer-perceptron, random forest, gradient boosting decision trees) are investigated for learning the optimal control action of a heat pump for demand response. The models learn from training data that has been genereated by exactly solving the corresponding optimization problem. The machine learning models are combined with an effective heuristic control approach that utilizes domain knowledge. The results show that integrating imitation learning approaches into a smart control method leads to significant improvements.

## Setup
The code was tested with Python 3.9. In the [config file](config.py), set up the main data directory (default: "/data") and mainly the input data directory variables and files.

The data can be downloaded [here](https://radar.kit.edu/radar/en/dataset/JieKFMOeZgzCYGmh#) and the three folder `Input_Data` must be placed in the main data directory (default: inside `/data` folder)

You can install the necessary packages listed in the requirements file with

```pip install -r requirements.txt```

Additionally, the [Gurobi solver](https://www.gurobi.com/) is required for the optimal control method (to solve the optimization problem exactly) and to generate the training data. You can also use any other solver for mixed-integer linear programming that is compatible with the optimization framework Pyomo (e.g. the free [GLPK solver](https://www.gnu.org/software/glpk/)). 

## First steps / base simulation runs
The main file for running the different approaches is [Run_Simulations](Run_Simulations.py). Here you can specify the different methods used for the control problem by setting the boolean variables `useCentralizedOptimization`, `useConventionalControl`, `usePriceStorageControl_BT4` and `useSupervisedLearning`. If `useSupervisedLearning` is activated, 4 different runs with a supervised learning models for imitation learning are used that first train a ML model and then use the trained model for generating the control actions. The 4 different ML methods are: 2 different multi-layer-perceptrons (with different configurations, one random forest approach and one gradient boosting decision trees approach). In the file [ML](ML.py) the different ML methods can be altered regarding their hyperparameters, training parameters, input features and output labels. The file [ICSimulation](ICSimulation.py) contains functions for executing the control actions on the simulation environment. It is called from [Run_Simulations](Run_Simulations.py). Nothing should be changed here. The file [Building_Optimization_Problem](Building_Optimization_Problem.py) contains the basic mixed-integer-linear optimization problems for different buildings types with the constraints and objective functions. It is called from [Run_Simulations](Run_Simulations.py). The file [SetUpScenarions](SetUpScenarions.py) specifies the used scenario for the simulations. Here you could alter the technical parameters of the heat pump (and possible other controllable electrical loads like electric vehicles or batteries) and different building types. However, in the paper only BT4 (multi-family building with a heat pump) is used and the training data was only generated for this building type. 

## If you use this code, please cite the corresponding paper:
```Dengiz et al., “Imitation learning with artificial neural networks for demand response with a heuristic control approach for heat pumps.” ```

