## If you use this code, please cite the corresponding paper:
```Dengiz et al., “Pareto Local Search for a Multi-Objective Demand Response Problem in Residential Areas with Heat Pumps and Electric Vehicles.” ```

## Setup
The code was tested with Python 3.11 and 3.12. In the [config file](config.py), set up the main data directory (default: "/data") and mainly the input data directory variables and files.

The data can be downloaded [here](https://www.radar-service.eu/radar/en/dataset/ZxeqNfKvVlQcjQAt?token=IZoONgGpjZoiAyiHvtlT#) and the three folders (`Input_Data`, `Reinforcement_Learning`, `Results`) must be placed in the main data directory (default: inside `/data` folder)

You can install the necessary packages listed in the requirements file with

```pip install -r requirements.txt```

Additionally, the Gurobi solver is required for the dichotomous method and for the box method. You can also use any other solver that is compatible with the optimization framework Pyomo. No external solver is necessary for the PALSS and RELAPALSS algorithms.
## First steps / base simulation runs
See also the [notebook file](quick_start.ipynb) for examples of the main functions.



### Set up variables for PALSS
 - In the [Run_Simulations_Combined file](Run_Simulations_Combined.py) set up the following boolean variables (directly in the file or after import):
   - ```useCentralizedOptimization``` 
   - ```useConventionalControl```
     - ```useLocalSearch = True``` (default)
 - Execute the function ```run_simulations(...)``` in the [Run_Simulations_Combined file](Run_Simulations_Combined.py) with `withRL = False`
 - Further options:
   - Set up the days. If `calculate_pareto_front_comparisons = True`, the days have to be in the list of those for which a Pareto Front was calculated. You can pass a list of days to the function.
   - Other parameters have to be adjusted directly in the file, e.g.
     - ```max_population_size``` (default 20)
     - ```number_of_pareto_optimal_solutions_in_population``` 
     - ```number_of_new_solutions_per_solution_in_iteration``` (default 3)
     - ```number_of_iterations_local_search``` (default 12)
     - ```time_limit_in_seconds_for_local_search``` (default 10 minutes)
  
### Set up variables for RELAPALSS 
- Train the peak shift and the price shift operator
    - Options, have to be changed in this [file](RL_Training_One_Shift_OperatorTmp.py) (all have valid default values):
      - Set up training days (specific or random) with ```number_of_days_for_training```,```choose_days_randomly```,```days_for_training```
      - Set up the number of iterations per day with ```number_of_iterations_per_day = 2```
      - Set up number of new solutions per iteration and per solution with ```number_of_new_solutions_per_iteration```,```number_of_new_solutions_per_solution```
      - Number and amount of shifting can also be modified: ```timeslots_for_state_load_percentages_obj```,```number_of_discrete_shifting_actions```,```minimum_shifting_percentage```,```maximum_shifting_percentage```
      - Model will be saved to: ```<models_dir>/trained_PPO_model``` (default: inside ```data/Reinforcement_Learning/RL_Trained_Models```)
    - Start training with ```ml_train_one_shift_operator(isPriceOperator = False)``` for the peak shift operator and ```ml_train_one_shift_operator(isPriceOperator = True)``` for the price shift operator.
  
- Set base variables
  - Set up the correct model names directly in or after the import of the [Run_Simulations_Combined file](Run_Simulations_Combined.py) (```dir_price_shift_model```,```dir_peak_shift_model```) 

  - Execute the function ```run_simulations(withRL = True)``` in the [Run_Simulations_Combined file](Run_Simulations_Combined.py) with `withRL = True`
    - Options:
      - Set up the days. The days should be different from those used for training. If `calculate_pareto_front_comparisons = True`, the days have to be in the list of those for which a Pareto Front was calculated. You can pass a list of days to the function.
      - ...


### Other optimization methods
- In the [Run_Simulations_Combined file](Run_Simulations_Combined.py), you can also use the dichotomous method, the box method (also called epsilon-constraint method) and the conventional control. Therefore, set up the following booleans. 
   - ```useCentralizedOptimization``` 
   - ```useConventionalControl```
   - ```useDichotomicMethodCentralized_Cost_Peak```
   - ```useBoxMethodCentralized_Cost_Peak```
   - ```useLocalSearch```

- Note that the dichotomous method and the box method will require an external solver.

### Additional settings
Change parameters in [this file](SetUpScenarios.py) for the scenarios for the residential area:
- heat pump
- building
- EV
- stationary battery (not used in the paper)
- gas boiler (not used in the paper)
- fan heater (not used in the paper)
- solver options


### NSGA-II and SPEA-II
For comparison, NSGA-II and SPEA-II have also been implemented in [this file](PymooMOEA.py). This part is independent of the proposed PALSS and RELAPALSS algorithms.
