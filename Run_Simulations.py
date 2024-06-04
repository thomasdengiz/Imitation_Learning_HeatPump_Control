# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:26:50 2021

@author: wi9632
"""
import SetUpScenarios
import numpy as np
import os
from datetime import datetime


#Set up

# Specify the used optimization methods
useDecentralizedOptimization = False
useReinforcementLearning = False
generateTrainingData = False

useCentralizedOptimization = True
useConventionalControl = True
usePriceStorageControl_BT4 = True
print_results_of_different_methods = False

useSupervisedLearning = False
used_trained_models_in_simulations_supervised_learning = False

building_type_for_supervised_learning = "kWh25"
#help_string_features_use = 'COP (Space Heating),numberOfStarts_HP,HP_isRunning,PriceFactor,StorageFactor,AverageTemperature'
help_string_features_use = 'COP (Space Heating),numberOfStarts_HP,HP_isRunning,PriceFactor,StorageFactor,AverageTemperature'

# Define parameters for ML
numberOfWeeksForEvaluation = 26
useChronologicalOrderForFirstTestWeek = True
number_of_iterations_ML_method = 4


numberOfTrainingWeeks = 20
numberOfBuildingsForTrainingData_Overall = 1
numberOfTestWeeks_Oveall = 5

#Indexes for further building testing
building_index_increment_training = 1
building_index_increment_simulation = 0





#Objectives and scenarios

optimizationGoal_minimizeSurplusEnergy = False
optimizationGoal_minimizePeakLoad = False
optimizationGoal_minimizeCosts = True

useCorrectionsAtTheEndOfWeek = False


# Choose internal Controller
run_simulateWeeks_NoAddtionalController_ANNSchedule = False
run_simulateWeeks_WithAddtionalController_Schedule =True
useInternalControllerToOverruleActions_simulateWeeks_WithAddtionalController_Schedule = True

useInternalControllerForRL = True



#Maximal starting times for the heating devices
considerMaximumNumberOfStartsHP_Combined = True
considerMaxiumNumberOfStartsHP_Individual = False
considerMaxiumNumberOfStartsHP_MFH_Individual = True
isHPAlwaysSwitchedOn = False
maximumNumberOfStarts_Combined = 4 * 7
maximumNumberOfStarts_Individual = 4  * 7

#Parameters for the internal controller
minimalRunTimeHeatPump = 0
timeslotsForCorrectingActionsBeforeTheAndOfTheWeek = 0
numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat =0

#Adjust parameters to the time resolution
if SetUpScenarios.timeResolution_InMinutes ==1:
    minimalRunTimeHeatPump = 30
    timeslotsForCorrectingActionsBeforeTheAndOfTheWeek = 0
    numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat = 5
if SetUpScenarios.timeResolution_InMinutes ==5:
    minimalRunTimeHeatPump = 6
    timeslotsForCorrectingActionsBeforeTheAndOfTheWeek = 0
    numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat = 4
if SetUpScenarios.timeResolution_InMinutes ==10:
    minimalRunTimeHeatPump = 3
    timeslotsForCorrectingActionsBeforeTheAndOfTheWeek = 0
    numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat = 4
if SetUpScenarios.timeResolution_InMinutes ==15:
    minimalRunTimeHeatPump = 2
    timeslotsForCorrectingActionsBeforeTheAndOfTheWeek = 0
    numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat = 2
if SetUpScenarios.timeResolution_InMinutes ==30:
    minimalRunTimeHeatPump = 1
    timeslotsForCorrectingActionsBeforeTheAndOfTheWeek = 0
    numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat = 1
if SetUpScenarios.timeResolution_InMinutes ==60:
    minimalRunTimeHeatPump = 1
    timeslotsForCorrectingActionsBeforeTheAndOfTheWeek = 0
    numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat = 1
additionalNumberOfAllowedStarts = 7
additionalNumberOfAllowedStarts_BeforeConsideringMinimalRuntime = 3

if useCorrectionsAtTheEndOfWeek ==False:
    timeslotsForCorrectingActionsBeforeTheAndOfTheWeek = -1

minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection = 0.7 # Should be between 0.5 and 1. Only quantifies the minimal degree. If no new peak is created by this action in the simulation , the value will be higher


differntWeigthsForTheOptimization_2Objectives = [(1.0, 0.0), (0.0, 1.0), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75)]
differntWeigthsForTheOptimization_3Objectives = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.33, 0.33, 0.33),
                                                 (0.5, 0.25, 0.25), (0.25, 0.5, 0.25), (0.25, 0.25, 0.5)]


#Values are determined below
optimization_1Objective = False
optimization_2Objective = False
optimization_3Objectives = False

#Determine the boolean values of the variables for the number of objectives considered
if ((optimizationGoal_minimizeSurplusEnergy == True and optimizationGoal_minimizePeakLoad == False and optimizationGoal_minimizeCosts == False) or
    (optimizationGoal_minimizeSurplusEnergy == False and optimizationGoal_minimizePeakLoad == True and optimizationGoal_minimizeCosts == False) or
    (optimizationGoal_minimizeSurplusEnergy == False and optimizationGoal_minimizePeakLoad == False and optimizationGoal_minimizeCosts == True)):
    optimization_1Objective = True
    print("1 Objectives")
if ((optimizationGoal_minimizeSurplusEnergy == True and optimizationGoal_minimizePeakLoad == True and optimizationGoal_minimizeCosts == False) or
    (optimizationGoal_minimizeSurplusEnergy == False and optimizationGoal_minimizePeakLoad == True and optimizationGoal_minimizeCosts == True) or
    (optimizationGoal_minimizeSurplusEnergy == True and optimizationGoal_minimizePeakLoad == False and optimizationGoal_minimizeCosts == True)):
    optimization_2Objective = True
    print("2 Objectives")
if (optimizationGoal_minimizeSurplusEnergy == True and optimizationGoal_minimizePeakLoad == True and optimizationGoal_minimizeCosts == True):
    optimization_3Objectives = True
    print("3 Objectives")




#Constants
ML_METHOD_RANDOM_FOREST = "Random_Forest"
ML_METHOD_MULTI_LAYER_PERCEPTRON_1 = "Multi_Layer_Perceptron_1"
ML_METHOD_MULTI_LAYER_PERCEPTRON_2 = "Multi_Layer_Perceptron_2"
ML_METHOD_GRADIENT_BOOSTING = "Gradient_Boosting"
ML_METHOD_RNN = "RNN"
ML_METHOD_LSTM = "LSTM"

OPT_OBJECTIVE_MIN_PEAK = 'Min_Peak'
OPT_OBJECTIVE_MIN_SURPLUS = 'Min_SurplusEnergy'
OPT_OBJECTIVE_MIN_COSTS = 'Min_Costs'

numberOfBuildingDataOverall = 20




###################################################################################################################################################################################################

def generateTrainingDataForML():
    print("Generate Training Data")
    import pandas as pd

    for buildingIndex in range (1, 21):
        WeeksOfTheYearForSimulation_Training_Period1 = [i for i in range (1, 13)]
        WeeksOfTheYearForSimulation_Training_Period2 = [i for i in range (39, 53)]


        pathForCreatingTheResultData_Centralized = folderPath_WholeSimulation + "/Centralized/Min_Costs_Scaled_PV_"+ str(SetUpScenarios.averagePVPeak) + "_kWp_" +  str(SetUpScenarios.timeResolution_InMinutes) + "_Min/BT4_HH" + str(buildingIndex) + "/"

        indexOfBuildingsOverall_BT1 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT1 + 1)]
        indexOfBuildingsOverall_BT2 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT2 + 1)]
        indexOfBuildingsOverall_BT3 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT3 + 1)]
        indexOfBuildingsOverall_BT4 = [buildingIndex]
        indexOfBuildingsOverall_BT5 =  [i for i in range (1, SetUpScenarios.numberOfBuildings_BT5 + 1)]


        numberOfWeeksWithNegativeScore = 0
        df_results_overall = pd.DataFrame(columns =['Building','Week', 'Surplus Energy [kWh]', 'Peak Load [kW]', 'Costs [Euro]', 'Score', 'Negative Score'])

        for currentWeek in WeeksOfTheYearForSimulation_Training_Period1:
            print("buildingIndex for generating Data: ", buildingIndex)
            print("currentWeek for generating Data: ", currentWeek)
            print()
            print()
            outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT1, outputVectorOptimization_heatGenerationCoefficientDHW_BT1, outputVectorOptimization_chargingPowerEV_BT1, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT2, outputVectorOptimization_heatGenerationCoefficientDHW_BT2, outputVectorOptimization_chargingPowerEV_BT3, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT4,  outputVectorOptimization_chargingPowerBAT_BT5, outputVectorOptimization_disChargingPowerBAT_BT5 =   Building_Optimization_Problem.optimizeOneWeek(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentWeek)

            #Call the internal controller with the schedules
            overruleActions = False
            simulationObjective_surplusEnergy_kWh_combined , simulationObjective_maximumLoad_kW_combined, simulationObjective_costs_Euro_combined, simulationObjective_combinedScore_combined, negativeScore_total_overall = ICSimulation.simulateWeeks_WithAddtionalController_Schedule(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentWeek, overruleActions, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT1, outputVectorOptimization_heatGenerationCoefficientDHW_BT1, outputVectorOptimization_chargingPowerEV_BT1, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT2, outputVectorOptimization_heatGenerationCoefficientDHW_BT2, outputVectorOptimization_chargingPowerEV_BT3, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT4, outputVectorOptimization_chargingPowerBAT_BT5, outputVectorOptimization_disChargingPowerBAT_BT5, pathForCreatingTheResultData_Centralized)
            if negativeScore_total_overall > 0.1:
                numberOfWeeksWithNegativeScore = numberOfWeeksWithNegativeScore + 1

            #Save results of the runs in a csv file
            df_results_overall.loc[len(df_results_overall)] = [buildingIndex, currentWeek, simulationObjective_surplusEnergy_kWh_combined[0], simulationObjective_maximumLoad_kW_combined[0], simulationObjective_costs_Euro_combined[0], simulationObjective_combinedScore_combined[0], negativeScore_total_overall[0]]
            df_results_overall.to_csv( pathForCreatingTheResultData_Centralized  + "/results_overall.csv", sep=";")

        for currentWeek in WeeksOfTheYearForSimulation_Training_Period2:
            print("buildingIndex for generating Data: ", buildingIndex)
            print("currentWeek for generating Data: ", currentWeek)
            print()
            print()
            outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT1, outputVectorOptimization_heatGenerationCoefficientDHW_BT1, outputVectorOptimization_chargingPowerEV_BT1, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT2, outputVectorOptimization_heatGenerationCoefficientDHW_BT2, outputVectorOptimization_chargingPowerEV_BT3, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT4,  outputVectorOptimization_chargingPowerBAT_BT5, outputVectorOptimization_disChargingPowerBAT_BT5 =   Building_Optimization_Problem.optimizeOneWeek(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentWeek)

            #Call the internal controller with the schedules
            overruleActions = True
            simulationObjective_surplusEnergy_kWh_combined , simulationObjective_maximumLoad_kW_combined, simulationObjective_costs_Euro_combined, simulationObjective_combinedScore_combined, negativeScore_total_overall = ICSimulation.simulateWeeks_WithAddtionalController_Schedule(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentWeek, overruleActions, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT1, outputVectorOptimization_heatGenerationCoefficientDHW_BT1, outputVectorOptimization_chargingPowerEV_BT1, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT2, outputVectorOptimization_heatGenerationCoefficientDHW_BT2, outputVectorOptimization_chargingPowerEV_BT3, outputVectorOptimization_heatGenerationCoefficientSpaceHeating_BT4, outputVectorOptimization_chargingPowerBAT_BT5, outputVectorOptimization_disChargingPowerBAT_BT5, pathForCreatingTheResultData_Centralized)
            if negativeScore_total_overall > 0.1:
                numberOfWeeksWithNegativeScore = numberOfWeeksWithNegativeScore + 1
            #Save results of the runs in a csv file
            df_results_overall.loc[len(df_results_overall)] = [buildingIndex, currentWeek, simulationObjective_surplusEnergy_kWh_combined[0], simulationObjective_maximumLoad_kW_combined[0], simulationObjective_costs_Euro_combined[0], simulationObjective_combinedScore_combined[0], negativeScore_total_overall[0]]
            df_results_overall.to_csv( pathForCreatingTheResultData_Centralized  + "/results_overall.csv", sep=";")

        print()
        print()
        print("Finished generateTrainingDataANN")
        print("numberOfWeeksWithNegativeScore: ", numberOfWeeksWithNegativeScore)




####################################################################################################################################################################################



#Method for randomly assigning Weeks to the training and test data
def chooseTrainingAndTestWeeks_Random (numberOfTrainingWeeks_Overall, numberOfBuildingsForTrainingData_Overall, numberOfTestWeeks_Oveall, numberOfBuildingsForTestData_Overall, numberOfBuildingDataOverall, useChronologicalOrderForFirstTestWeek, currentWeekForChronologicalOrder):

    from random import randrange
    import numpy as np

    trainingWeeks_Overall = np.zeros((numberOfBuildingsForTrainingData_Overall, numberOfTrainingWeeks_Overall))
    testWeeks_Overall = np.zeros((numberOfBuildingsForTestData_Overall, numberOfTestWeeks_Oveall))

    usedTestData = np.zeros((numberOfBuildingDataOverall, 52))
    indexTestWeek = 0
    indexBuilding = 0

    first_part_chronologicalWeeksForTesting = [i for i in range(12)]
    second_partchronologicalWeeksForTesting = [i for i in range(38, 52)]
    chronologicalWeeksForTesting_array = first_part_chronologicalWeeksForTesting + second_partchronologicalWeeksForTesting


    while indexBuilding < numberOfBuildingsForTestData_Overall:
        if useChronologicalOrderForFirstTestWeek == True and indexTestWeek ==0 and indexBuilding ==0:
            usedWeek = chronologicalWeeksForTesting_array [currentWeekForChronologicalOrder]
            usedTestData[indexBuilding][usedWeek] = 1
            testWeeks_Overall[indexBuilding][indexTestWeek] = usedWeek
            indexTestWeek = indexTestWeek + 1
            continue
        while indexTestWeek < numberOfTestWeeks_Oveall:
            # Choose the test data
            randomNumber_WeekOfTheYear = randrange(52)

            while randomNumber_WeekOfTheYear > 11 and randomNumber_WeekOfTheYear < 38:
                randomNumber_WeekOfTheYear = randrange(52)
            if usedTestData[indexBuilding][randomNumber_WeekOfTheYear] == 0:
                usedTestData[indexBuilding][randomNumber_WeekOfTheYear] = 1
                testWeeks_Overall [indexBuilding][indexTestWeek] = randomNumber_WeekOfTheYear
            elif usedTestData[indexBuilding][randomNumber_WeekOfTheYear] == 1:
                continue
            indexTestWeek = indexTestWeek + 1

        indexBuilding = indexBuilding + 1
        indexTestWeek = 0

    #testWeeks_Overall= np.sort(testWeeks_Overall, axis=1).flatten()


    usedTrainingData = np.zeros((numberOfBuildingDataOverall, 52))
    indexTrainingWeek = 0
    indexBuilding = 0
    while indexBuilding < numberOfBuildingsForTrainingData_Overall:
        while indexTrainingWeek < numberOfTrainingWeeks_Overall:
            # Choose the Training data
            randomNumber_WeekOfTheYear = randrange(52)

            while randomNumber_WeekOfTheYear > 11 and randomNumber_WeekOfTheYear < 38:
                randomNumber_WeekOfTheYear = randrange(52)
            if usedTrainingData[indexBuilding][randomNumber_WeekOfTheYear] == 0 and usedTestData [indexBuilding][randomNumber_WeekOfTheYear] == 0:
                usedTrainingData[indexBuilding][randomNumber_WeekOfTheYear] = 1
                trainingWeeks_Overall [indexBuilding][indexTrainingWeek] = randomNumber_WeekOfTheYear
            elif usedTrainingData[indexBuilding][randomNumber_WeekOfTheYear] == 1 or usedTestData [indexBuilding][randomNumber_WeekOfTheYear] == 1:
                continue
            indexTrainingWeek = indexTrainingWeek + 1

        indexBuilding = indexBuilding + 1
        indexTrainingWeek = 0


    trainingWeeks_Overall = trainingWeeks_Overall.astype(int)
    testWeeks_Overall= testWeeks_Overall.astype(int)


    return trainingWeeks_Overall, testWeeks_Overall



#################################################################################################################################################################################################################

#Run simulations


if __name__ == "__main__":
    import Building_Optimization_Problem
    import ANN
    import ICSimulation
    import pandas as pd
    import time

    # Measure wall-clock time and CPU time
    start_time = time.time()
    start_cpu = time.process_time()

    file_path_additional_information = ""

    list_test_prediction_practise_mode_avg_mse = []
    df_results = pd.DataFrame(columns=['Week', 'Centralized Optimization (Costs)', 'Centralized Optimization (negative Score)', 'Price Storage Control (Costs)', 'Price Storage Control (negative Score)', 'Conventional Control (Costs)', 'Conventional Control (negative Score)', 'SL MLP1 (Costs)', 'SL MLP1 (negative Score)' , 'SL MLP1 (Correction Limit)', 'SL MLP1 (Physical Limit)', 'SL MLP2 (Costs)', 'SL MLP2 (negative Score)' , 'SL MLP2 (Correction Limit)', 'SL MLP2 (Physical Limit)',  'SL RF1 (Costs)', 'SL RF1 (negative Score)' , 'SL RF1 (Correction Limit)', 'SL RF1 (Physical Limit)', 'SL GB1 (Costs)', 'SL GB1 (negative Score)' , 'SL GB1 (Correction Limit)', 'SL GB1 (Physical Limit)',  'Training weeks'])
    firstIterationSimulation = True
    currentWeek = -1
    for i in range (0, numberOfWeeksForEvaluation):
        # define the directory to be created for the result file
        if firstIterationSimulation == True:
            currentDatetimeString = datetime.today().strftime('%d_%m_%Y_Time_%H_%M_%S')
            firstIterationSimulation = False


        numberOfBuildingsForTestData_Overall = 1
        currentWeekForChronologicalOrder = i
        trainingWeeksForSupervisedLearning, testWeeksForSupvervisedLearning = chooseTrainingAndTestWeeks_Random(numberOfTrainingWeeks, numberOfBuildingsForTrainingData_Overall , numberOfTestWeeks_Oveall ,numberOfBuildingsForTestData_Overall, numberOfBuildingDataOverall, useChronologicalOrderForFirstTestWeek, currentWeekForChronologicalOrder)
        currentWeek = testWeeksForSupvervisedLearning[0][0] + 1

        simulationName = "BT4_N1_Test/Week"
        folderName_WholeSimulation = currentDatetimeString + "_" + simulationName + "_BTCombined_" + str(SetUpScenarios.numberOfBuildings_Total)
        folderPath_WholeSimulation = "C:/Users/wi9632/Desktop/Ergebnisse/DSM/Instance_1/Instance_Base/" + folderName_WholeSimulation
        pathForCreatingTheResultData_Centralized = folderPath_WholeSimulation + "/Centralized"
        pathForCreatingTheResultData_Decentralized = folderPath_WholeSimulation + "/Decentralized"
        pathForCreatingTheResultData_SupervisedML = folderPath_WholeSimulation + "/ML"
        pathForCreatingTheResultData_RL = folderPath_WholeSimulation + "/RL"
        pathForCreatingTheResultData_Conventional = folderPath_WholeSimulation + "/Conventional"
        pathForCreatingTheResultData_PriceStorageControl = folderPath_WholeSimulation + "/PSC"
        pathForCreatingTheResultData_SupervisedML_MLP1 = folderPath_WholeSimulation + "/ML/MLP1"
        pathForCreatingTheResultData_SupervisedML_MLP2 = folderPath_WholeSimulation + "/ML/MLP2"
        pathForCreatingTheResultData_SupervisedML_RF = folderPath_WholeSimulation + "/ML/RF"
        pathForCreatingTheResultData_SupervisedML_GB = folderPath_WholeSimulation + "/ML/GB"

        paths_ML = [pathForCreatingTheResultData_SupervisedML_MLP1,pathForCreatingTheResultData_SupervisedML_MLP2,pathForCreatingTheResultData_SupervisedML_RF, pathForCreatingTheResultData_SupervisedML_GB]

        try:
            os.makedirs(folderPath_WholeSimulation)
            os.makedirs(pathForCreatingTheResultData_Centralized)
            #os.makedirs(pathForCreatingTheResultData_Decentralized)
            os.makedirs(pathForCreatingTheResultData_SupervisedML)
            #os.makedirs(pathForCreatingTheResultData_RL)
            os.makedirs(pathForCreatingTheResultData_Conventional)
            os.makedirs(pathForCreatingTheResultData_PriceStorageControl)
            os.makedirs(pathForCreatingTheResultData_SupervisedML_MLP1)
            os.makedirs(pathForCreatingTheResultData_SupervisedML_MLP2)
            os.makedirs(pathForCreatingTheResultData_SupervisedML_RF)
            os.makedirs(pathForCreatingTheResultData_SupervisedML_GB)

        except OSError:
            print ("Creation of the directory %s failed" % folderPath_WholeSimulation)
        else:
            print ("Successfully created the directory %s" % folderPath_WholeSimulation)



        #Path for additional information text file
        file_path_additional_information = str(folderPath_WholeSimulation) + "/additional_information.txt"




        if generateTrainingData ==True:
            generateTrainingDataForML()

        #Exact methods decentralized (testing)

        #ANN methods (testing)
        if useSupervisedLearning == True:
            print("\n--------------Supervised Control------------\n")

            indexOfBuildingsOverall_BT1 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT1 + 1)]
            indexOfBuildingsOverall_BT2 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT2 + 1)]
            indexOfBuildingsOverall_BT3 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT3 + 1)]
            indexOfBuildingsOverall_BT4 = [i + building_index_increment_simulation for i in range (1, SetUpScenarios.numberOfBuildings_BT4 + 1 )]
            indexOfBuildingsOverall_BT5 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT5 + 1 )]


            #Choose training and test Weeks
            WeekSelectionMethod = 'Random'    # Options: ['Random'] ['Clustering_kMeans'] ['Clustering_Wards']

            numberOfBuildingsForTestData_Overall = 1
            currentWeekForChronologicalOrder = i
            trainingWeeksForSupervisedLearning, testWeeksForSupvervisedLearning = chooseTrainingAndTestWeeks_Random(numberOfTrainingWeeks, numberOfBuildingsForTrainingData_Overall , numberOfTestWeeks_Oveall ,numberOfBuildingsForTestData_Overall, numberOfBuildingDataOverall, useChronologicalOrderForFirstTestWeek, currentWeekForChronologicalOrder)


            #Test prediction of single Weeks

            testWeeksPrediction =  []
            testWeeksPrediction.append(testWeeksForSupvervisedLearning[0][0])
            testWeeksPrediction.append(testWeeksForSupvervisedLearning[0][1])
            testWeeksPrediction.append(testWeeksForSupvervisedLearning[0][2])
            testWeeksPrediction.append(testWeeksForSupvervisedLearning[0][3])
            testWeeksPrediction.append(testWeeksForSupvervisedLearning[0][4])
            #testWeeksPrediction.append(testWeeksForSupvervisedLearning[0][3])

            testWeeksInTrainingData = False
            for a in range (0, len(testWeeksPrediction)):
                if testWeeksPrediction [a] in trainingWeeksForSupervisedLearning [0]:
                    testWeeksInTrainingData = True

            print(f"trainingWeeksForSupervisedLearning: {trainingWeeksForSupervisedLearning[0]}")

            print(f"Week 1 Test Predictions: {testWeeksPrediction[0]}")
            print(f"Week 2 Test Predictions: {testWeeksPrediction[1]}")
            print(f"Week 3 Test Predictions: {testWeeksPrediction[2]}")
            print(f"Week 4 Test Predictions: {testWeeksPrediction[3]}")
            print(f"Week 5 Test Predictions: {testWeeksPrediction[4]}")
            #print(f"Week 4 Test Predictions: {testWeeksPrediction[3]}")
            print(f"testWeeksInTrainingData: {testWeeksInTrainingData}")

            #Clustering
            useKneeMethod = True
            maxNumberOfClusters = 20
            printPlotsForClusterScores = False
            usePredefinedNumberOfClusters = True
            predefinedNumberOfClusters = 3
            useClustering = False


            if useClustering == True:
                trainedClusteringModel, resultingNumberOfClusters, dataScalerClustering = ANN.clusterTrainingData(trainingWeeksForSupervisedLearning, useKneeMethod, maxNumberOfClusters, printPlotsForClusterScores, usePredefinedNumberOfClusters, predefinedNumberOfClusters)

                #Assign cluster to the Weeks of the training and test data
                clusterAssignmentToTheWeeksOfTheTrainingData = np.zeros(len(trainingWeeksForSupervisedLearning[0]))
                clustersWithAssignedWeeks_ForTraining = np.zeros((resultingNumberOfClusters,len(trainingWeeksForSupervisedLearning[0])) )
                clustersWithAssignedWeeks_ForTraining = clustersWithAssignedWeeks_ForTraining -1


                for i in range (0, len(trainingWeeksForSupervisedLearning[0])):
                    WeekForTesting = [trainingWeeksForSupervisedLearning [0][i]]
                    clusterAssignmentToTheWeeksOfTheTrainingData [i] = ANN.assignClusterNumberToAWeek(trainedClusteringModel, dataScalerClustering, WeekForTesting)


                clusterAssignmentToTheWeeksOfTheTestData = np.zeros(len(testWeeksForSupvervisedLearning[0]))
                clustersWithAssignedWeeks_ForTest = np.zeros((resultingNumberOfClusters,len(testWeeksForSupvervisedLearning[0])) )
                clustersWithAssignedWeeks_ForTest = clustersWithAssignedWeeks_ForTest -1
                for i in range (0, len(testWeeksForSupvervisedLearning[0])):
                    WeekForTesting = [testWeeksForSupvervisedLearning [0][i]]
                    clusterAssignmentToTheWeeksOfTheTestData [i] = ANN.assignClusterNumberToAWeek(trainedClusteringModel, dataScalerClustering, WeekForTesting)


                helpIndexForAssigningWeeksToCluster = [0] * resultingNumberOfClusters
                for i in range(0, len(clusterAssignmentToTheWeeksOfTheTrainingData)):
                    assignedClusterForTheCurrentWeek = int(clusterAssignmentToTheWeeksOfTheTrainingData [i])
                    clustersWithAssignedWeeks_ForTraining [assignedClusterForTheCurrentWeek] [helpIndexForAssigningWeeksToCluster [assignedClusterForTheCurrentWeek]] = trainingWeeksForSupervisedLearning [0] [i]
                    helpIndexForAssigningWeeksToCluster [assignedClusterForTheCurrentWeek] = helpIndexForAssigningWeeksToCluster [assignedClusterForTheCurrentWeek] + 1

                helpIndexForAssigningWeeksToCluster = [0] * resultingNumberOfClusters
                for i in range(0, len(clusterAssignmentToTheWeeksOfTheTestData)):
                    assignedClusterForTheCurrentWeek = int(clusterAssignmentToTheWeeksOfTheTestData [i])
                    clustersWithAssignedWeeks_ForTest [assignedClusterForTheCurrentWeek] [helpIndexForAssigningWeeksToCluster [assignedClusterForTheCurrentWeek]] = testWeeksForSupvervisedLearning [0] [i]
                    helpIndexForAssigningWeeksToCluster [assignedClusterForTheCurrentWeek] = helpIndexForAssigningWeeksToCluster [assignedClusterForTheCurrentWeek] + 1

            else:
                resultingNumberOfClusters = 1



            #Create arrays for the different ML methods
            usedMLMethod_array = [""] * number_of_iterations_ML_method
            usedMLMethod_array [0] = ML_METHOD_MULTI_LAYER_PERCEPTRON_1
            usedMLMethod_array [1] = ML_METHOD_MULTI_LAYER_PERCEPTRON_2
            usedMLMethod_array [2] = ML_METHOD_RANDOM_FOREST
            usedMLMethod_array [3] = ML_METHOD_GRADIENT_BOOSTING




            resultSupervisedLearning_array = np.zeros(number_of_iterations_ML_method)
            negativScoreTotal_SupervisedLearning_array = np.zeros(number_of_iterations_ML_method)
            negativScoreTotal_SupervisedLearning_CorrectionLimit_array= np.zeros(number_of_iterations_ML_method)
            negativScoreTotal_SupervisedLearning_PhysicalLimit_array= np.zeros(number_of_iterations_ML_method)

            #Do the iteration of the different ML methdos
            for iteration_ML_method in range (0, number_of_iterations_ML_method):

                pathForTheTrainedModels = paths_ML[iteration_ML_method] + "/ML Training Configurations/Week" + str(currentWeek) + "/"
                print(f"Week iteration i: {i}")
                print(f"iteration_ML_method: {iteration_ML_method}")

                try:
                    os.makedirs(pathForTheTrainedModels)
                except:
                    print("Creation of the directory %s failed" % pathForTheTrainedModels)

                #Train the supvervised learning model
                usedMLMethod = usedMLMethod_array [iteration_ML_method]  # Options: [ML_METHOD_MULTI_LAYER_PERCEPTRON], [ML_METHOD_RANDOM_FOREST], [ML_METHOD_GRADIENT_BOOSTING], [ML_METHOD_LSTM], [ML_METHOD_RNN]
                if optimizationGoal_minimizePeakLoad==True:
                    objective = OPT_OBJECTIVE_MIN_PEAK
                if optimizationGoal_minimizeSurplusEnergy ==True:
                    objective = OPT_OBJECTIVE_MIN_SURPLUS
                if optimizationGoal_minimizeCosts ==True:
                    objective = OPT_OBJECTIVE_MIN_COSTS

                useNormalizedData = False
                useStandardizedData = True
                practiseModeWithTestPredictions = True
                perfectForecastForSequencePredictions = False


                #Call method for training the supervised ML
                dataScalers_InputFeatures = []
                dataScalers_OutputLabels  = []
                trainedModels = []

                for b in range (0, resultingNumberOfClusters):
                    if useClustering == False:
                        inputFormatForClustering = np.zeros((1, len(trainingWeeksForSupervisedLearning[0])))
                        inputFormatForClustering[0] = trainingWeeksForSupervisedLearning[0]
                    else:
                        inputFormatForClustering = np.zeros((1, len(clustersWithAssignedWeeks_ForTraining[b])))
                        inputFormatForClustering [0]  =clustersWithAssignedWeeks_ForTraining[b]


                    dataScaler_InputFeatures, dataScaler_OutputLabels, trainedModel, test_prediction_avg_mse = ANN.trainSupervisedML_SingleTimeslot_SingleBuildingOptScenario (inputFormatForClustering, objective ,useNormalizedData, useStandardizedData, usedMLMethod,pathForTheTrainedModels, practiseModeWithTestPredictions, testWeeksPrediction, help_string_features_use,building_index_increment_training, building_index_increment_simulation )
                    list_test_prediction_practise_mode_avg_mse.append(test_prediction_avg_mse)
                    if usedMLMethod == ML_METHOD_LSTM or usedMLMethod == ML_METHOD_RNN:
                        dataScaler_InputFeatures, dataScaler_OutputLabels, trainedModel = ANN.trainRNN_MultipleTimeslot_SingleBuildingOptScenario(inputFormatForClustering, objective, useNormalizedData, useStandardizedData, usedMLMethod, practiseModeWithTestPredictions, perfectForecastForSequencePredictions)

                    dataScalers_InputFeatures.append(dataScaler_InputFeatures)
                    dataScalers_OutputLabels.append(dataScaler_OutputLabels)
                    trainedModels.append(trainedModel)

                #Classify the current Week using the established clusters

                if useClustering == True:
                    assignedClusterForTheCurrentSingleWeek =  ANN.assignClusterNumberToAWeek(trainedClusteringModel, dataScalerClustering, [currentWeek])[0]
                else:
                    assignedClusterForTheCurrentSingleWeek = 0


                if used_trained_models_in_simulations_supervised_learning == True:


                    if SetUpScenarios.numberOfBuildings_BT4 == 1:

                        week_for_testing_supervised_learning_in_simulation = testWeeksForSupvervisedLearning[0][0] + 1
                        currentWeek = week_for_testing_supervised_learning_in_simulation
                        print("")
                        print(f"week_for_testing_supervised_learning_in_simulation: {week_for_testing_supervised_learning_in_simulation}")


                        #Call method for the simulation of one Week by generating and taking actions for single time slots
                        outputVectorANN_heatGenerationCoefficientSpaceHeating_BT4, outputVectorANN_temperatureBufferStorage_BT4 = ANN.generateActionsForSingleTimeslotWithANN_SingleBuildingOptScenario(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, week_for_testing_supervised_learning_in_simulation, pathForTheTrainedModels,objective, WeekSelectionMethod, dataScaler_InputFeatures, dataScaler_OutputLabels, trainedModel, building_index_increment_simulation)

                        if usedMLMethod == ML_METHOD_LSTM or usedMLMethod == ML_METHOD_RNN:
                            # Call method for the simulation of one Week by generating and taking actions for multiple time slots
                            outputVectorANN_heatGenerationCoefficientSpaceHeating_BT4 = ANN.generateActionsForMutipleTimeslotWithANN_SingleBuildingOptScenario(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, week_for_testing_supervised_learning_in_simulation, pathForCreatingTheResultData_SupervisedML,objective, WeekSelectionMethod, dataScaler_InputFeatures, dataScaler_OutputLabels, trainedModel)


                        outputVectorANN_heatGenerationCoefficientSpaceHeating_BT1 = np.zeros(0)
                        outputVectorANN_heatGenerationCoefficientDHW_BT1 = np.zeros(0)
                        outputVectorANN_chargingPowerEV_BT1 = np.zeros(0)
                        outputVectorANN_heatGenerationCoefficientSpaceHeating_BT2 = np.zeros(0)
                        outputVectorANN_heatGenerationCoefficientDHW_BT2 =np.zeros(0)
                        outputVectorANN_chargingPowerEV_BT3 = np.zeros(0)
                        outputVectorANN_chargingPowerBAT_BT5 = np.zeros(0)
                        outputVectorANN_disChargingPowerEV_BT5 = np.zeros(0)


                        #Reshape outputdata of the ANN (:=input data for the internal controller)
                        outputVectorANN_heatGenerationCoefficientSpaceHeating_BT4 = outputVectorANN_heatGenerationCoefficientSpaceHeating_BT4.reshape((1, SetUpScenarios.numberOfTimeSlotsPerWeek), order='F')

                        #Call the internal controller with the schedules
                        overruleActions = False
                        simulationObjective_surplusEnergy_kWh_combined , simulationObjective_maximumLoad_kW_combined, simulationObjective_costs_Euro_combined, simulationObjective_combinedScore_combined, negativeScore_total_overall, negativeScore_CorrectionLimit, negativeScore_PhysicalLimit = ICSimulation.simulateWeeks_WithAddtionalController_Schedule(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, week_for_testing_supervised_learning_in_simulation, overruleActions, outputVectorANN_heatGenerationCoefficientSpaceHeating_BT1, outputVectorANN_heatGenerationCoefficientDHW_BT1, outputVectorANN_chargingPowerEV_BT1, outputVectorANN_heatGenerationCoefficientSpaceHeating_BT2, outputVectorANN_heatGenerationCoefficientDHW_BT2, outputVectorANN_chargingPowerEV_BT3, outputVectorANN_heatGenerationCoefficientSpaceHeating_BT4, outputVectorANN_chargingPowerBAT_BT5, outputVectorANN_disChargingPowerEV_BT5, paths_ML [iteration_ML_method])
                        resultSupervisedLearning_array[iteration_ML_method] = simulationObjective_costs_Euro_combined
                        negativScoreTotal_SupervisedLearning_array [iteration_ML_method] = negativeScore_total_overall
                        negativScoreTotal_SupervisedLearning_CorrectionLimit_array[iteration_ML_method] = negativeScore_CorrectionLimit
                        negativScoreTotal_SupervisedLearning_PhysicalLimit_array[iteration_ML_method] = negativeScore_PhysicalLimit





        #Exact methods centralized (testing)
        if useCentralizedOptimization == True:
            print("\n-----------Centralized Optimization---------\n")


            indexOfBuildingsOverall_BT1 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT1 + 1)]
            indexOfBuildingsOverall_BT2 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT2 + 1)]
            indexOfBuildingsOverall_BT3 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT3 + 1)]
            indexOfBuildingsOverall_BT4 = [i + building_index_increment_simulation for i in range (1, SetUpScenarios.numberOfBuildings_BT4 + 1 )]
            indexOfBuildingsOverall_BT5 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT5 + 1 )]
            outputVector_heatGenerationCoefficientSpaceHeating_BT1, outputVector_heatGenerationCoefficientDHW_BT1, outputVector_chargingPowerEV_BT1, outputVector_heatGenerationCoefficientSpaceHeating_BT2, outputVector_heatGenerationCoefficientDHW_BT2, outputVector_chargingPowerEV_BT3, outputVector_heatGenerationCoefficientSpaceHeating_BT4, outputVector_chargingPowerBAT_BT5, outputVector_disChargingPowerBAT_BT5 =   Building_Optimization_Problem.optimizeOneWeek(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentWeek)

            #Call the internal controller with the schedules
            overruleActions = False
            simulationObjective_surplusEnergy_kWh_combined , simulationObjective_maximumLoad_kW_combined, simulationObjective_costs_Euro_combined, simulationObjective_combinedScore_combined, negativeScore_total_overall, negativeScore_total_CorrectionLimit, negativeScore_total_PhysicalLimit = ICSimulation.simulateWeeks_WithAddtionalController_Schedule(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentWeek, overruleActions, outputVector_heatGenerationCoefficientSpaceHeating_BT1, outputVector_heatGenerationCoefficientDHW_BT1, outputVector_chargingPowerEV_BT1, outputVector_heatGenerationCoefficientSpaceHeating_BT2, outputVector_heatGenerationCoefficientDHW_BT2, outputVector_chargingPowerEV_BT3, outputVector_heatGenerationCoefficientSpaceHeating_BT4, outputVector_chargingPowerBAT_BT5, outputVector_disChargingPowerBAT_BT5, pathForCreatingTheResultData_Centralized)
            resultCentralizedOptimization = simulationObjective_costs_Euro_combined
            negativScoreTotal_CentralizedOptimization = negativeScore_total_overall


        # RL methods
        if useReinforcementLearning == True:
            print("RL Control")


        # Price Storage control
        if usePriceStorageControl_BT4 ==True:

            print("\n--------------Price Storage Control------------\n")

            indexOfBuildingsOverall_BT1 = [i + 1 for i in range (0, SetUpScenarios.numberOfBuildings_BT1)]
            indexOfBuildingsOverall_BT2 = [i + 1 for i in range (0, SetUpScenarios.numberOfBuildings_BT2)]
            indexOfBuildingsOverall_BT3 = [i + 1 for i in range (0, SetUpScenarios.numberOfBuildings_BT3)]
            indexOfBuildingsOverall_BT4 = [i + building_index_increment_simulation for i in range (1, SetUpScenarios.numberOfBuildings_BT4 + 1 )]
            indexOfBuildingsOverall_BT5 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT5 + 1 )]

            pathForCreatingTheResultData_PriceStorageControl_Week = pathForCreatingTheResultData_PriceStorageControl+ "/Week" + str(currentWeek) + "/"
            try:
                os.makedirs(pathForCreatingTheResultData_PriceStorageControl_Week)
            except OSError:
                print("Creation of the directory %s failed" % pathForCreatingTheResultData_PriceStorageControl_Week)

            simulationObjective_surplusEnergy_kWh_combined , simulationObjective_maximumLoad_kW_combined, simulationObjective_costs_Euro_combined, simulationObjective_combinedScore_combined, negativeScore_total_overall = ICSimulation.simulateWeeks_ConventionalControl(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4,indexOfBuildingsOverall_BT5, currentWeek, pathForCreatingTheResultData_PriceStorageControl_Week, usePriceStorageControl_BT4)
            resultPriceStorageControl = simulationObjective_costs_Euro_combined
            negativScoreTotal_PriceStorageControl = negativeScore_total_overall
            #negativScoreTotal_PriceStorageControl_CorrectionLimit = negativeScore_CorrectionLimit
            #negativScoreTotal_PriceStorageControl_PhysicalLimit = negativeScore_PhysicalLimit

        # Conventional Control
        if useConventionalControl == True:
            print("\n--------------Conventional Control------------\n")

            usePriceStorageControl_BT4 = False

            indexOfBuildingsOverall_BT1 = [i + 1 for i in range (0, SetUpScenarios.numberOfBuildings_BT1)]
            indexOfBuildingsOverall_BT2 = [i + 1 for i in range (0, SetUpScenarios.numberOfBuildings_BT2)]
            indexOfBuildingsOverall_BT3 = [i + 1 for i in range (0, SetUpScenarios.numberOfBuildings_BT3)]
            indexOfBuildingsOverall_BT4 = [i + building_index_increment_simulation for i in range (1, SetUpScenarios.numberOfBuildings_BT4 + 1 )]
            indexOfBuildingsOverall_BT5 = [i for i in range (1, SetUpScenarios.numberOfBuildings_BT5 + 1 )]

            pathForCreatingTheResultData_Conventional_Week = pathForCreatingTheResultData_Conventional + "/Week" + str(currentWeek) + "/"
            try:
                os.makedirs(pathForCreatingTheResultData_Conventional_Week)
            except OSError:
                print("Creation of the directory %s failed" % pathForCreatingTheResultData_Conventional_Week)


            simulationObjective_surplusEnergy_kWh_combined , simulationObjective_maximumLoad_kW_combined, simulationObjective_costs_Euro_combined, simulationObjective_combinedScore_combined, negativeScore_total_overall = ICSimulation.simulateWeeks_ConventionalControl(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4,indexOfBuildingsOverall_BT5, currentWeek, pathForCreatingTheResultData_Conventional_Week, usePriceStorageControl_BT4)
            resultConventionalControl = simulationObjective_costs_Euro_combined
            negativScoreTotal_ConventionalControl = negativeScore_total_overall
            usePriceStorageControl_BT4 = True

        if print_results_of_different_methods == True:
            trainingWeeksForSupervisedLearning[0] += 1
            trainingWeeksForSupervisedLearning_string = ', '.join(map(str, trainingWeeksForSupervisedLearning[0]))
            new_row = {'Week': currentWeek, 'Centralized Optimization (Costs)': round(float(resultCentralizedOptimization), 1),'Centralized Optimization (negative Score)': round(float(negativScoreTotal_CentralizedOptimization), 1) , 'Price Storage Control (Costs)': round(float(resultPriceStorageControl), 1),'Price Storage Control (negative Score)': round(float(negativScoreTotal_PriceStorageControl), 1), 'Conventional Control (Costs)': round(float(resultConventionalControl),1), 'Conventional Control (negative Score)': round(float(negativScoreTotal_ConventionalControl),1), 'SL MLP1 (Costs)': round(float(resultSupervisedLearning_array[0]),1), 'SL MLP1 (negative Score)': round(float(negativScoreTotal_SupervisedLearning_array[0]),1), 'SL MLP1 (Correction Limit)': round(float(negativScoreTotal_SupervisedLearning_CorrectionLimit_array[0]),1), 'SL MLP1 (Physical Limit)': round(float(negativScoreTotal_SupervisedLearning_PhysicalLimit_array[0]),1), 'SL MLP2 (Costs)': round(float(resultSupervisedLearning_array[1]),1), 'SL MLP2 (negative Score)': round(float(negativScoreTotal_SupervisedLearning_array[1]),1), 'SL MLP2 (Correction Limit)': round(float(negativScoreTotal_SupervisedLearning_CorrectionLimit_array[1]),1), 'SL MLP2 (Physical Limit)': round(float(negativScoreTotal_SupervisedLearning_PhysicalLimit_array[1]),1),  'SL RF1 (Costs)': round(float(resultSupervisedLearning_array[2]),1), 'SL RF1 (negative Score)': round(float(negativScoreTotal_SupervisedLearning_array[2]),1), 'SL RF1 (Correction Limit)': round(float(negativScoreTotal_SupervisedLearning_CorrectionLimit_array[2]),1), 'SL RF1 (Physical Limit)': round(float(negativScoreTotal_SupervisedLearning_PhysicalLimit_array[2]),1),  'SL GB1 (Costs)': round(float(resultSupervisedLearning_array[3]),1), 'SL GB1 (negative Score)': round(float(negativScoreTotal_SupervisedLearning_array[3]),1), 'SL GB1 (Correction Limit)': round(float(negativScoreTotal_SupervisedLearning_CorrectionLimit_array[3]),1), 'SL GB1 (Physical Limit)': round(float(negativScoreTotal_SupervisedLearning_PhysicalLimit_array[3]),1),  'Training Weeks': trainingWeeksForSupervisedLearning_string}
            df_results = pd.concat([df_results, pd.DataFrame([new_row])], ignore_index=True)
            df_results = df_results.applymap(lambda x: x[0] if isinstance(x, list) else x)

    #Caluclate statistics of the training run
    if useSupervisedLearning == True:
        average_mse_practise_mode = sum(list_test_prediction_practise_mode_avg_mse) / len(list_test_prediction_practise_mode_avg_mse)
        max_value_mse = max(list_test_prediction_practise_mode_avg_mse)
        min_value_mse = min(list_test_prediction_practise_mode_avg_mse)
        spread_mse = max_value_mse - min_value_mse
        print("")
        print(f"Results Method: {usedMLMethod}")
        print(f"average_mse_practise_mode: {round(average_mse_practise_mode, 2)}")
        print(f"max_value_mse: {round(max_value_mse, 2)}")
        print(f"min_value_mse: {round(min_value_mse, 2)}")
        print(f"spread_mse: {round(spread_mse, 2)}")

        #Create df for ML training results without simulation
        mlp1_data = list_test_prediction_practise_mode_avg_mse[::4]
        mlp2_data = list_test_prediction_practise_mode_avg_mse[1::4]
        rf1_data = list_test_prediction_practise_mode_avg_mse[2::4]
        gb1_data = list_test_prediction_practise_mode_avg_mse[3::4]

        df_ML_results = pd.DataFrame({"MLP1": mlp1_data,"MLP2": mlp2_data,"RF1": rf1_data,"GB1": gb1_data})
        average_row = df_ML_results.mean()
        df_ML_results = df_ML_results.append(average_row, ignore_index=True)
        df_ML_results.to_csv(folderPath_WholeSimulation + '/results_ML_no_simulation.csv', index=False, sep=";")

    if print_results_of_different_methods == True:
        average_results = df_results.drop(columns=['Week']).mean(numeric_only=True)
        average_results_df = pd.DataFrame(average_results).T
        average_results_df.index = ['Average']
        df_results = pd.concat([df_results, average_results_df])
        df_results.to_csv(folderPath_WholeSimulation + '/results_simulation.csv', index=False, sep=";")

    end_time = time.time()
    execution_time = end_time - start_time
    end_cpu = time.process_time()
    execution_cpu = end_cpu - start_cpu
    print("")
    hours, remainder = divmod(execution_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time_normal = "{:02d} hours, {:02d} minutes, {:02d} seconds".format(int(hours), int(minutes), int(seconds))
    print("Normal Execution Time:", formatted_time_normal)

    hours, remainder = divmod(execution_cpu, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time_cpu = "{:02d} hours, {:02d} minutes, {:02d} seconds".format(int(hours), int(minutes), int(seconds))
    print("CPU  Time:", formatted_time_cpu)

    # Print additional information text file
    with open(file_path_additional_information, "w") as file:
        # Write the desired text to the file
        file.write(f"Time resolution: {SetUpScenarios.timeResolution_InMinutes}\n")
        file.write(f"Building Type: {building_type_for_supervised_learning}\n")
        file.write(f"Used features: {help_string_features_use}\n")
        file.write(f"Number of weeks for the evaluation: {numberOfWeeksForEvaluation}\n")
        file.write(f"Input Data: Number of training weeks: {numberOfTrainingWeeks}\n")
        file.write(f"Input Data: Number of buildings: {numberOfBuildingsForTrainingData_Overall}\n")
        file.write(f"Number of test weeks (no simulation evaluation): {numberOfTestWeeks_Oveall}\n")
        file.write(f"Normal Execution Time: {formatted_time_normal}\n")
        file.write(f"Household for simulation: HH{building_index_increment_simulation + 1}\n")
        file.write(f"Household for training: HH{building_index_increment_training + 1}\n")






