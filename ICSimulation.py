# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:26:50 2021

@author: wi9632
"""
import SetUpScenarios
import numpy as np
import pandas as pd
import Run_Simulations
import ANN
import os



# Method for simulating variable number of weeks with an additional controller if dersired.
# Input: boolean overruleActions, 3-dim-arrays inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] etc.

def simulateWeeks_WithAddtionalController_Schedule(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentweek, overruleActions, inputVector_BT1_heatGenerationCoefficientSpaceHeating, inputVector_BT1_heatGenerationCoefficientDHW, inputVector_BT1_chargingPowerEV, inputVector_BT2_heatGenerationCoefficientSpaceHeating, inputVector_BT2_heatGenerationCoefficientDHW, inputVector_BT3_chargingPowerEV, inputVector_BT4_heatGenerationCoefficientSpaceHeating, inputVector_BT5_chargingPowerBAT, inputVector_BT5_disChargingPowerBAT, pathForCreatingTheResultData):

    #Variables of the simulation for all buildings combined

    simulationResult_electricalLoad_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusEnergy_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))

    simulationObjective_surplusEnergy_kWh_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    simulationObjective_costs_Euro_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    simulationObjective_maximumLoad_kW_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    simulationObjective_combinedScore_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))

    total_ConstraintViolation_BufferStorageTemperatureRange_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_DHWTankRange_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_DHWTankLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_OnlyOneStorage_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_MinimalModulationDegree_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_SOCRangeOfTheEV_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_SOCOfTheEVLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_ChargingPowerOfTheEV_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_numberOfStarts_Individual_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_numberOfStarts_Combined_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))

    total_ConstraintViolation_SOCRangeOfTheBAT_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_SOCOfTheBATLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_ChargingPowerOfTheBAT_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))

    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankRange_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_OnlyOneStorage_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_MinimalModulationDegree_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_ChargingPowerOfTheEV_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_numberOfStarts_Individual_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    hypotheticalSOCDropWithNoCharging_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))


    #Variables of the simulation for BT1

    simulationResult_electricalLoad_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_BufferStorageTemperature_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_UsableVolumeDHW_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SOCofEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_energyLevelOfEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    hypotheticalSOCDropWithNoCharging_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))

    simulationResult_numberOfStartsBufferStorage_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationResult_numberOfStartsDHWTank_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationResult_numberOfStartsCombined_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationResult_numberOfStartsHP_PerTimeslot_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfStandbySlotsHP_PerTimeslot_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_isHPRunning_PerTimeslot_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))


    simulationObjective_surplusEnergyKWH_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationObjective_costs_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationObjective_maximumLoad_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))

    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_DHWTankRange_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_OnlyOneStorage_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_MinimalModulationDegree_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_SOCRangeOfTheEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_DHWTankRange_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_DHWTankLastValue_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_OnlyOneStorage_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_MinimalModulationDegree_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_SOCRangeOfTheEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_SOCOfTheEVLastValue_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_ChargingPowerOfTheEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_numberOfStarts_Individual_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_numberOfStarts_Combined_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))


    #Variables of the simulation for BT2

    simulationResult_electricalLoad_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_BufferStorageTemperature_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_UsableVolumeDHW_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfStartsBufferStorage_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationResult_numberOfStartsDHWTank_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationResult_numberOfStartsCombined_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationResult_numberOfStartsHP_PerTimeslot_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfStandbySlotsHP_PerTimeslot_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_isHPRunning_PerTimeslot_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))


    simulationObjective_surplusEnergyKWH_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationObjective_costs_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationObjective_maximumLoad_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))

    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_DHWTankRange_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_OnlyOneStorage_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_MinimalModulationDegree_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_DHWTankRange_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_DHWTankLastValue_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_OnlyOneStorage_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_MinimalModulationDegree_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_numberOfStarts_Individual_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_numberOfStarts_Combined_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))



    #Variables of the simulation for BT3

    simulationResult_electricalLoad_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SOCofEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_energyLevelOfEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    hypotheticalSOCDropWithNoCharging_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))

    simulationObjective_surplusEnergyKWH_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
    simulationObjective_costs_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
    simulationObjective_maximumLoad_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))

    simulation_ConstraintViolation_SOCRangeOfTheEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_SOCRangeOfTheEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
    total_ConstraintViolation_SOCOfTheEVLastValue_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
    total_ConstraintViolation_ChargingPowerOfTheEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))


    #Variables of the simulation for BT4

    simulationResult_electricalLoad_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_BufferStorageTemperature_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfStartsBufferStorage_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    simulationResult_numberOfStartsHP_PerTimeslot_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfStandbySlotsHP_PerTimeslot_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_isHPRunning_PerTimeslot_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))


    simulationObjective_surplusEnergyKWH_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    simulationObjective_costs_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    simulationObjective_maximumLoad_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))

    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_MinimalModulationDegree_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_MinimalModulationDegree_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_numberOfStarts_Individual_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))


    #Variables of the simulation for BT5

    simulationResult_electricalLoad_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SOCofBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_energyLevelOfBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))

    simulationObjective_surplusEnergyKWH_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    simulationObjective_costs_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    simulationObjective_maximumLoad_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))

    simulation_ConstraintViolation_SOCRangeOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_ChargingPowerOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_disChargingPowerOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_SOCRangeOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    total_ConstraintViolation_SOCOfTheBATLastValue_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    total_ConstraintViolation_ChargingPowerOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    total_ConstraintViolation_disChargingPowerOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))


    # Additional constraint violation variables for the internal controller

    total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))

    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_overall = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))


    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_DHWTankRange_CorrectionLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_DHWTankRange_PhysicalLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_DHWTankRange_CorrectionLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_DHWTankRange_PhysicalLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))


    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_DHWTankRange_CorrectionLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_DHWTankRange_PhysicalLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_DHWTankRange_CorrectionLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_DHWTankRange_PhysicalLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))


    total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))


    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))


    # Define the correcting vectors

    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    outputVector_BT1_heatGenerationCoefficientDHW_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    outputVector_BT1_chargingPowerEV_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))

    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    outputVector_BT2_heatGenerationCoefficientDHW_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))

    outputVector_BT3_chargingPowerEV_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))

    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))

    outputVector_BT5_chargingPowerBAT_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    outputVector_BT5_disChargingPowerBAT_corrected = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))


    for index_week in range (0, 1):
        # Define the correcting vectors
        if inputVector_BT1_heatGenerationCoefficientSpaceHeating.size != 0:
            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected = inputVector_BT1_heatGenerationCoefficientSpaceHeating.copy()
            outputVector_BT1_heatGenerationCoefficientDHW_corrected =  inputVector_BT1_heatGenerationCoefficientDHW.copy()
            outputVector_BT1_chargingPowerEV_corrected =  inputVector_BT1_chargingPowerEV.copy()
        else:
            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected =-1
            outputVector_BT1_heatGenerationCoefficientDHW_corrected =-1
            outputVector_BT1_chargingPowerEV_corrected =-1

        if inputVector_BT2_heatGenerationCoefficientSpaceHeating.size != 0:
            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected =  inputVector_BT2_heatGenerationCoefficientSpaceHeating.copy()
            outputVector_BT2_heatGenerationCoefficientDHW_corrected =  inputVector_BT2_heatGenerationCoefficientDHW.copy()
        else:
            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected = -1

        if inputVector_BT3_chargingPowerEV.size != 0:
            outputVector_BT3_chargingPowerEV_corrected =  inputVector_BT3_chargingPowerEV.copy()
        else:
            outputVector_BT3_chargingPowerEV_corrected = -1

        if inputVector_BT4_heatGenerationCoefficientSpaceHeating.size != 0:
            outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected =  inputVector_BT4_heatGenerationCoefficientSpaceHeating.copy()
        else:
            outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected =  -1

        if inputVector_BT5_chargingPowerBAT.size != 0:
            outputVector_BT5_chargingPowerBAT_corrected =  inputVector_BT5_chargingPowerBAT.copy()
            outputVector_BT5_disChargingPowerBAT_corrected =  inputVector_BT5_disChargingPowerBAT.copy()
        else:
            outputVector_BT5_chargingPowerBAT_corrected = -1
            outputVector_BT5_disChargingPowerBAT_corrected  =-1


        #Define the statistic variables for the correcting actions

        correctingStats_BT1_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
        correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
        correctingStats_BT1_heatGenerationCoefficientDHW_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
        correctingStats_BT1_heatGenerationCoefficientDHW_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
        correctingStats_BT1_chargingPowerEV_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
        correctingStats_BT1_chargingPowerEV_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
        correctingStats_BT1_heatGenerationCoefficientSpaceHeating_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
        correctingStats_BT1_heatGenerationCoefficientDHW_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
        correctingStats_BT1_chargingPowerEV_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))

        correctingStats_BT2_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
        correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
        correctingStats_BT2_heatGenerationCoefficientDHW_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
        correctingStats_BT2_heatGenerationCoefficientDHW_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
        correctingStats_BT2_heatGenerationCoefficientSpaceHeating_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
        correctingStats_BT2_heatGenerationCoefficientDHW_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))

        correctingStats_BT3_chargingPowerEV_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
        correctingStats_BT3_chargingPowerEV_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
        correctingStats_BT3_chargingPowerEV_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))

        correctingStats_BT4_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
        correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
        correctingStats_BT4_heatGenerationCoefficientSpaceHeating_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))

        correctingStats_BT5_chargingPowerBAT_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
        correctingStats_BT5_chargingPowerBAT_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
        correctingStats_BT5_chargingPowerBAT_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
        correctingStats_BT5_disChargingPowerBAT_numberOfTimeSlots = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
        correctingStats_BT5_disChargingPowerBAT_sumOfCorrections = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
        correctingStats_BT5_disChargingPowerBAT_profile = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))



        simulationInput_BT1_SpaceHeating = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT1_DHW = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT1_availabilityPattern = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT1_energyConsumptionOfTheEV = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT1_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))

        simulationInput_BT2_SpaceHeating = np.zeros((len(indexOfBuildingsOverall_BT2), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT2_DHW = np.zeros((len(indexOfBuildingsOverall_BT2), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT2_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT2), SetUpScenarios.numberOfTimeSlotsPerWeek))

        simulationInput_BT3_availabilityPattern = np.zeros((len(indexOfBuildingsOverall_BT3), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT3_energyConsumptionOfTheEV = np.zeros((len(indexOfBuildingsOverall_BT3), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT3_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT3), SetUpScenarios.numberOfTimeSlotsPerWeek))

        simulationInput_BT4_SpaceHeating = np.zeros((len(indexOfBuildingsOverall_BT4), SetUpScenarios.numberOfTimeSlotsPerWeek))
        simulationInput_BT4_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT4), SetUpScenarios.numberOfTimeSlotsPerWeek))

        simulationInput_BT5_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT5), SetUpScenarios.numberOfTimeSlotsPerWeek))


        #Building Type 1
        for index_BT1 in range (0, len(indexOfBuildingsOverall_BT1) ):

            #Reading of the data

            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT1_mHP_EV_SFH_1Minute_weeks/HH" + str(indexOfBuildingsOverall_BT1[index_BT1]) + "/HH" + str(indexOfBuildingsOverall_BT1[index_BT1]) + "_week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_weeks/Outside_Temperature_1Minute_week' +  str(currentweek) + '.csv', sep =";")


            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"
            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            for i in range (0, len(df_buildingData['Availability of the EV'])):
                if df_buildingData['Availability of the EV'] [i] > 0.1:
                    df_buildingData['Availability of the EV'] [i] = 1.0
                if df_buildingData['Availability of the EV'] [i] < 0.1 and df_buildingData['Availability of the EV'] [i] >0.01:
                    df_buildingData['Availability of the EV'] [i] = 0.0

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

            #Create availability array for the EV
            availabilityOfTheEV = np.zeros(( SetUpScenarios.numberOfTimeSlotsPerWeek))
            for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerWeek):
                availabilityOfTheEV [index_timeslot_for_Availability] = df_buildingData['Availability of the EV'] [index_timeslot_for_Availability +1]
            indexOfTheEV = index_BT1
            energyConsumptionOfEVs_Joule = SetUpScenarios.generateEVEnergyConsumptionPatterns(availabilityOfTheEV, indexOfTheEV)


            df_availabilityPatternEV = pd.DataFrame({'Timeslot': df_buildingData.index, 'Availability of the EV':df_buildingData['Availability of the EV'] })
            del df_availabilityPatternEV['Timeslot']

            df_energyConsumptionEV_Joule = pd.DataFrame({'Timeslot': df_buildingData.index, 'Energy':energyConsumptionOfEVs_Joule  })
            del df_energyConsumptionEV_Joule['Timeslot']
            df_energyConsumptionEV_Joule.index +=1


            #Wind generation

            indexBuildingForWindPowerAssignment = index_BT1
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1


            # Set up inital values for the simulation
            simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, 0] = SetUpScenarios.initialBufferStorageTemperature
            simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, 0] = SetUpScenarios.initialUsableVolumeDHWTank
            simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, 0]= (SetUpScenarios.initialSOC_EV/100) * SetUpScenarios.capacityMaximal_EV
            simulationResult_SOCofEV_BT1 [index_week, index_BT1, 0]= SetUpScenarios.initialSOC_EV


            simulationResult_PVGeneration_BT1 [index_week, index_BT1, 0] = df_buildingData ['PV [nominal]'][1]  * SetUpScenarios.determinePVPeakOfBuildings (index_BT1)
            simulationResult_RESGeneration_BT1 [index_week, index_BT1, 0] = df_buildingData ['PV [nominal]'] [1]  * SetUpScenarios.determinePVPeakOfBuildings (index_BT1) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [1] * SetUpScenarios.maximalPowerOfWindTurbine
            simulationResult_electricalLoad_BT1 [index_week, index_BT1, 0] = (inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, 0] +  inputVector_BT1_heatGenerationCoefficientDHW[ index_BT1, 0]) * SetUpScenarios.electricalPower_HP + inputVector_BT1_chargingPowerEV[index_BT1, 0] + df_buildingData['Electricity [W]'] [1]
            simulationResult_SurplusPower_BT1 [index_week, index_BT1, 0] = simulationResult_RESGeneration_BT1 [index_week, index_BT1, 0] - simulationResult_electricalLoad_BT1 [index_week, index_BT1, 0]
            simulationResult_costs_BT1 [index_week, index_BT1, 0] = (simulationResult_electricalLoad_BT1 [index_week, index_BT1, 0] - simulationResult_PVGeneration_BT1 [index_week, index_BT1, 0]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [1]/3600000)


            helpCountNumberOfStartsIndividual_SpaceHeating =0
            helpCountNumberOfStartsIndividual_DHW =0
            helpCountNumberOfStartsIndividual_Combined =0
            helpCounterNumberOfRunningSlots_SpaceHeating =0
            helpCounterNumberOfRunningSlots_DHW =0
            helpCounterNumberOfRunningSlots_Combined =0
            helpCounterNumberOfStandBySlots_SpaceHeating =0
            helpCounterNumberOfStandBySlots_DHW =0
            helpCounterNumberOfStandBySlots_Combined =0

            startedHeatingHeatPump = False
            stoppedHeatingHeatPump = False

            helpCurrentPeakLoadOfTheweek =0

            numberOfHeatPumpStartsReachedSoftLimit = False
            numberOfHeatPumpStartsReachedHardLimit = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = False

            heatingStartedPhysicalLimit_BufferStorage = False
            heatingStartedPhysicalLimit_DHWTank = False

            startedHeatingDHWCorrection_end = False
            startedHeatingSpaceHeatingCorrection_end = False

            correction_bothStorageHeatedUp_lastTimeBufferStorageOverruled = True
            correction_bothStorageHeatedUp_lastTimeDHWOverruled = False



            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):

                #Check how often the heat pump has been started so far
                if index_timeslot >= 2:

                    if outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 2] == 0 and outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1] >0.001:
                        helpCountNumberOfStartsIndividual_SpaceHeating +=1

                    if outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 2] == 0 and outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1] >0.001:
                        helpCountNumberOfStartsIndividual_DHW +=1

                    if (outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 2] == 0 and outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 2] == 0) and ( outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1] >0.001 or outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1] >0.001):
                        helpCountNumberOfStartsIndividual_Combined +=1
                        startedHeatingHeatPump = True
                        stoppedHeatingHeatPump = False
                    if (outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 2] > 0.01 or outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 2] > 0.01) and ( outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1] ==0  and outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1] ==0):
                        stoppedHeatingHeatPump = True
                        startedHeatingHeatPump = False
                        if lastHeatingAfterHeatPumpStartsReachedHardLimitStarted ==True:
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = True

                #Update the currentNumberOfRunningSlots for the heat pump
                    if  outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1] > 0.001:
                        helpCounterNumberOfRunningSlots_SpaceHeating +=1
                        helpCounterNumberOfStandBySlots_SpaceHeating =0
                    if outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1] > 0.001:
                        helpCounterNumberOfRunningSlots_DHW +=1
                        helpCounterNumberOfStandBySlots_DHW =0
                    if  outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1] > 0.001 or outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1] > 0.001:
                        helpCounterNumberOfRunningSlots_Combined +=1
                        helpCounterNumberOfStandBySlots_Combined =0
                    if  outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1] == 0:
                        helpCounterNumberOfStandBySlots_SpaceHeating  +=1
                        helpCounterNumberOfRunningSlots_SpaceHeating =0
                    if outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1] == 0:
                        helpCounterNumberOfStandBySlots_DHW  +=1
                        helpCounterNumberOfRunningSlots_DHW =0
                    if  outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1]  == 0 and outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1]  == 0:
                        helpCounterNumberOfStandBySlots_Combined  +=1
                        helpCounterNumberOfRunningSlots_Combined =0

                if startedHeatingHeatPump == True and helpCounterNumberOfRunningSlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
                    startedHeatingHeatPump = False
                if stoppedHeatingHeatPump == True and helpCounterNumberOfStandBySlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
                    stoppedHeatingHeatPump = False

                if numberOfHeatPumpStartsReachedHardLimit == True:
                    numberOfHeatPumpStartsReachedSoftLimit = False



                # Pre-Corrections of input values: too high or low input values
                if inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot]  > 1:
                    inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot]  =1
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot]  =1
                    print("Pre-Corrections too high value Space Heating. Time: " +  str(index_timeslot) + "\n")
                if inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]  > 1:
                    inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] =1
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot]  =1
                    print("Pre-Corrections too high value DHW. Time:"+  str(index_timeslot)  + "\n")
                if inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] > SetUpScenarios.chargingPowerMaximal_EV:
                    inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] = SetUpScenarios.chargingPowerMaximal_EV
                    outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] = SetUpScenarios.chargingPowerMaximal_EV

                if inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot]  < 0:
                    inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot]  =0
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot]  =0

                if inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]  < 0:
                    inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] =0
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot]  =0

                if inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] < 0:
                    inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] = 0
                    outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] = 0


                # Pre-Corrections: Set small heating values to 0
                if inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] > 0 and inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] < 0.1:
                    inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] = 0

                if inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] > 0 and inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] < 0.1:
                    inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] = 0

                # Pre-Corrections of input values: minimal modulation
                if inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] > 0.001 and inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP / 100:
                    print("Pre_Correction: Min Modulation. Time: " + str( index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + "\n")
                    inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP / 100

                if inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] > 0.001 and inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP / 100:
                    print("Pre_Correction: Min Modulation. Time: " + str(index_timeslot) + "; ANN value DHW: " + str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "\n")
                    inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP / 100




                # Pre-Corrections of input values: heating up only one storage at one time
                if inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] > 0.001 and inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]  > 0.001:
                    print("Pre_Correction Only one storage. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot])  + "\n")
                    if correction_bothStorageHeatedUp_lastTimeBufferStorageOverruled==True:
                        inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] = 0
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot]  =0
                        correction_bothStorageHeatedUp_lastTimeBufferStorageOverruled = False
                        correction_bothStorageHeatedUp_lastTimeDHWOverruled = True
                    elif correction_bothStorageHeatedUp_lastTimeDHWOverruled ==True:
                        inputVector_BT1_heatGenerationCoefficientSpaceHeating  [index_BT1, index_timeslot] = 0
                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                        correction_bothStorageHeatedUp_lastTimeBufferStorageOverruled = True
                        correction_bothStorageHeatedUp_lastTimeDHWOverruled = False


                # Pre_Corrections for the availability of the EV (charging is only possible if the EV is available at the charging station of the building)
                if inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] > 0.001 and  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] ==0:
                    inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] =0
                    outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] =0
                    print("Pre_Correction EV is not available for charging: " +  str(index_timeslot))

                if  simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts_BeforeConsideringMinimalRuntime:
                    numberOfHeatPumpStartsReachedSoftLimit = True

                if simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts - 2:
                    numberOfHeatPumpStartsReachedHardLimit = True
                    numberOfHeatPumpStartsReachedSoftLimit = False

                #Calculate the hypothetical simulation values if the non-corrected actions were applied
                cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot]  =simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot - 1] + ( inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]  = (simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] = SetUpScenarios.initialUsableVolumeDHWTank + ((inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot]  = SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + ( inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]  = (simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100


                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT1_SpaceHeating [index_BT1, index_timeslot] = df_buildingData['Space Heating [W]'] [index_timeslot + 1]
                simulationInput_BT1_DHW [index_BT1, index_timeslot] = df_buildingData ['DHW [W]'] [index_timeslot + 1]
                simulationInput_BT1_availabilityPattern [index_BT1, index_timeslot] = df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1]
                simulationInput_BT1_energyConsumptionOfTheEV [index_BT1, index_timeslot] = df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]
                simulationInput_BT1_electricityDemand [index_BT1, index_timeslot] = df_buildingData ['Electricity [W]'] [index_timeslot + 1]


               # Calculate the maximum power of the heat pump and the EV for not creating a new peak load
                if index_timeslot >=1:
                    if (simulationResult_electricalLoad_BT1  [index_week, index_BT1, index_timeslot - 1] - simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_electricalLoad_BT1  [index_week, index_BT1, index_timeslot - 1] - simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot - 1]
                    if (simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot - 1] - simulationResult_electricalLoad_BT1  [index_week, index_BT1, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot - 1] - simulationResult_electricalLoad_BT1  [index_week, index_BT1, index_timeslot - 1]

                maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP
                maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP
                maximumPowerEVChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_EV

                if (inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot] + inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) * SetUpScenarios.electricalPower_HP + inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] + df_buildingData ['Electricity [W]'] [index_timeslot + 1] > simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = helpCurrentPeakLoadOfTheweek - inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = helpCurrentPeakLoadOfTheweek - inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]
                    maximumPowerEVChargingForNotCreatingANewPeak = helpCurrentPeakLoadOfTheweek  - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot] - (inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot] + inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) * SetUpScenarios.electricalPower_HP

                if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek > SetUpScenarios.electricalPower_HP:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP
                if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek > SetUpScenarios.electricalPower_HP:
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP

                if  maximumPowerEVChargingForNotCreatingANewPeak >  SetUpScenarios.chargingPowerMaximal_EV:
                    maximumPowerEVChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_EV

                if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP
                if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP:
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek =Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP
                if  maximumPowerEVChargingForNotCreatingANewPeak < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection *  SetUpScenarios.chargingPowerMaximal_EV:
                    maximumPowerEVChargingForNotCreatingANewPeak = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.chargingPowerMaximal_EV





                #Corrections due to violations of the temperature and volume constraints
                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] <= SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                    print("Correction volume too low DHW (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] >= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                    helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if helpCounterNumberOfStandBySlots_Combined >0:
                        helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] > 0.001 and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod < SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit  and (numberOfHeatPumpStartsReachedSoftLimit == False or stoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
                       outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                       print("Correction DHW too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                    else:
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                        print("Correction DHW volume too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")

                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:

                    helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    if helpCounterNumberOfStandBySlots_Combined >0:
                        helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    if inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] > 0.001 and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod < SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and (numberOfHeatPumpStartsReachedSoftLimit == False or stoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
                       outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                       print("Correction BufferStorage too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                    else:
                       outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                       print("Correction BufferStorage too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")

                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary and simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                    print("Correction BufferStorage too low (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")


                # Corrections due to minimal modulation degree of the heat pump
                if inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] > 0.001 and inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP /100:
                    inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP /100
                    print("Correction Minimal Mod. SpaceHeating. Time: " +  str(index_timeslot) + "; ANN value: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                if inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] > 0.001 and inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP /100:
                    inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP /100
                    print("Correction Minimal Mod. DHW. Time: " +  str(index_timeslot) + "; ANN value: " + str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")

                # Corrections for the SOC of the EV
                if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] > 100:
                    outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] = 0




                #Calculate the hypothetical simulation values if the  corrected actions were applied
                cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] = SetUpScenarios.initialUsableVolumeDHWTank + ((outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))



                if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] >= SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection  * 2:
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 2:
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                    startedHeatingSpaceHeatingCorrection_end = False
                    startedHeatingDHWCorrection_end = True
                if startedHeatingDHWCorrection_end == True and simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot] >= SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 2:
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                if startedHeatingDHWCorrection_end == True and simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 2:
                    startedHeatingDHWCorrection_end = False
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0




                #Corrections due to high number of starts of the heat pump

                #Soft Limit Reached --> Consider minimum runtimes and standbytimes of the heat pump
                if numberOfHeatPumpStartsReachedSoftLimit ==True and startedHeatingDHWCorrection_end==False and startedHeatingSpaceHeatingCorrection_end ==False:
                    print("numberOfHeatPumpStartsReachedSoftLimit; Timeslot: ",index_timeslot)
                    if startedHeatingHeatPump == True:
                        print("numberOfHeatPumpStartsReachedSoftLimit; started HP")
                        if outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] > 0.01 and simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot]
                        elif outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] > 0.01 and simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                            helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                            if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                                outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                            elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                                elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                    if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                    elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                                    elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0

                        if outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] > 0.01 and simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot] <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] =  outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot]
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                        elif outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] > 0.01 and simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                            helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                            if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] =   0
                            elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] =  SetUpScenarios.minimalModulationdDegree_HP/100
                                elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                                    if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] =  0
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] =  SetUpScenarios.minimalModulationdDegree_HP/100
                                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0

                        if outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] == 0 and outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] ==0:
                            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                            helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                            currentSOCBufferStorage_CorrectionLimits =  (simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1] - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
                            currentSOCDHWTank_CorrectionLimits = ( simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary) / ( SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary )
                            if currentSOCBufferStorage_CorrectionLimits < currentSOCDHWTank_CorrectionLimits:
                                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                                elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod  <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] =  SetUpScenarios.minimalModulationdDegree_HP/100
                            else:
                                if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod  <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] =  SetUpScenarios.minimalModulationdDegree_HP/100
                                elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0


                    elif stoppedHeatingHeatPump ==True:
                        print("numberOfHeatPumpStartsReachedSoftLimit; stopped HP")
                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0




                # Last heating of the week if the numberOfHeatPumpStartsReachedHardLimit
                if numberOfHeatPumpStartsReachedHardLimit ==True and startedHeatingDHWCorrection_end==False and startedHeatingSpaceHeatingCorrection_end ==False:
                    print("numberOfHeatPumpStartsReachedHardLimit")
                    # Last heating of the week
                    if lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == False:
                        fractionOfweekLeft =1 - (index_timeslot / SetUpScenarios.numberOfTimeSlotsPerWeek)
                        currentSOCBufferStorage_CorrectionLimits =  (simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1] - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
                        currentSOCDHWTank_CorrectionLimits = ( simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary) / ( SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary )
                        differenceTargetValueEndAndUpperLimit_SpaceHeating = SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - (SetUpScenarios.initialBufferStorageTemperature)
                        possibleTargetTemperatureForLastHeating_SpaceHeating = SetUpScenarios.initialBufferStorageTemperature  + differenceTargetValueEndAndUpperLimit_SpaceHeating  * fractionOfweekLeft
                        differenceTargetValueEndAndUpperLimit_DHW = SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - (SetUpScenarios.initialUsableVolumeDHWTank)
                        possibleTargetVolumeForLastHeating_DHW = SetUpScenarios.initialUsableVolumeDHWTank  + differenceTargetValueEndAndUpperLimit_DHW  * fractionOfweekLeft
                        if currentSOCBufferStorage_CorrectionLimits <= currentSOCDHWTank_CorrectionLimits:
                            if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1] < possibleTargetTemperatureForLastHeating_SpaceHeating:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                                        lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                            elif simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot - 1] < possibleTargetVolumeForLastHeating_DHW:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] =  maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                                        lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                        elif currentSOCBufferStorage_CorrectionLimits > currentSOCDHWTank_CorrectionLimits:
                            if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot - 1] < possibleTargetVolumeForLastHeating_DHW:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] =  maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                                        lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                            elif simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1] < possibleTargetTemperatureForLastHeating_SpaceHeating:
                                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                                        lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                        if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot - 1] >= possibleTargetVolumeForLastHeating_DHW and simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1] >= possibleTargetTemperatureForLastHeating_SpaceHeating:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                    elif lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == True:
                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0



                #Corrections for the last value of the optimization horizon
                if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek:


                    helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot
                    helpHypotheticalBufferStorageTemperatureWhenHeating = simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot - 1]
                    helpHypotheticalBufferStorageTemperatureWhenNotHeating = simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot - 1]
                    helpHypotheticalDHWVolumeWhenHeating = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]
                    helpHypotheticalDHWVolumeWhenNotHeating = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]


                    averageSpaceHeatingDemandLastTimeslots = 0
                    averageDHWDemandLastTimeSlots = 0
                    averageCOPSpaceHeatingLastTimeSlots = 0
                    averageCOPDHWLastTimeSlots = 0
                    helpSumSpaceHeatingDemandLastTimeslots = 0
                    helpSumDHWDemandLastTimeSlots = 0
                    helpSumCOPSpaceHeatingLastTimeSlots = 0
                    helpSumCOPDHWLastTimeSlots = 0

                    for i in range (0, Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek):
                        helpSumSpaceHeatingDemandLastTimeslots = helpSumSpaceHeatingDemandLastTimeslots + df_buildingData['Space Heating [W]'] [index_timeslot - i]
                        helpSumDHWDemandLastTimeSlots = helpSumDHWDemandLastTimeSlots + df_buildingData['DHW [W]'] [index_timeslot - i]
                        helpSumCOPSpaceHeatingLastTimeSlots = helpSumCOPSpaceHeatingLastTimeSlots + cop_heatPump_SpaceHeating[index_timeslot  - i]
                        helpSumCOPDHWLastTimeSlots = helpSumCOPDHWLastTimeSlots + cop_heatPump_DHW[index_timeslot  - i]

                    averageSpaceHeatingDemandLastTimeslots = helpSumSpaceHeatingDemandLastTimeslots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
                    averageDHWDemandLastTimeSlots = helpSumDHWDemandLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
                    averageCOPSpaceHeatingLastTimeSlots = helpSumCOPSpaceHeatingLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
                    averageCOPDHWLastTimeSlots =  helpSumCOPDHWLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek


                    for helpCurrentHypotheticalTimeSlot in range (0, helpTimeSlotsToEndOfweek):
                        helpHypotheticalBufferStorageTemperatureWhenHeating = helpHypotheticalBufferStorageTemperatureWhenHeating + (((maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP )* averageCOPSpaceHeatingLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - averageSpaceHeatingDemandLastTimeslots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                        helpHypotheticalBufferStorageTemperatureWhenNotHeating = helpHypotheticalBufferStorageTemperatureWhenNotHeating + ((0* averageCOPSpaceHeatingLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - averageSpaceHeatingDemandLastTimeslots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                        helpHypotheticalDHWVolumeWhenHeating = helpHypotheticalDHWVolumeWhenHeating + (((maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP ) * averageCOPDHWLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - averageDHWDemandLastTimeSlots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                        helpHypotheticalDHWVolumeWhenNotHeating = helpHypotheticalDHWVolumeWhenNotHeating + ((0 * averageCOPDHWLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - averageDHWDemandLastTimeSlots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


                    if helpHypotheticalBufferStorageTemperatureWhenNotHeating > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 1.0:
                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                        startedHeatingDHWCorrection_end = False
                        startedHeatingSpaceHeatingCorrection_end = False
                        print("Correction BufferStorage too high (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                        print("helpHypotheticalBufferStorageTemperatureWhenNotHeating: ", helpHypotheticalBufferStorageTemperatureWhenNotHeating)
                        print("")
                    if  helpHypotheticalBufferStorageTemperatureWhenHeating < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 1.0:
                        helpValueAdjustedHeating =  maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                        if helpValueAdjustedHeating < outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot]:
                            helpValueAdjustedHeating = outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot]
                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = helpValueAdjustedHeating
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                        startedHeatingDHWCorrection_end = False
                        startedHeatingSpaceHeatingCorrection_end = True
                        print("Correction BufferStorage too low (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                        print("helpHypotheticalBufferStorageTemperatureWhenHeating: ", helpHypotheticalBufferStorageTemperatureWhenHeating)
                        print("")
                    if helpHypotheticalDHWVolumeWhenNotHeating > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 1.0:
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                        startedHeatingDHWCorrection_end = False
                        startedHeatingSpaceHeatingCorrection_end = False
                        print("Correction DHW too high (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                        print ("helpHypotheticalDHWVolumeWhenNotHeating: ", helpHypotheticalDHWVolumeWhenNotHeating)
                        print("")
                    if helpHypotheticalDHWVolumeWhenHeating < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 1.0:
                        helpValueAdjustedHeating =  maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                        if helpValueAdjustedHeating < outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot]:
                            helpValueAdjustedHeating = outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot]
                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = helpValueAdjustedHeating
                        startedHeatingDHWCorrection_end = True
                        startedHeatingSpaceHeatingCorrection_end = False
                        print("Correction DHW too low (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                        print ("helpHypotheticalDHWVolumeWhenHeating: ", helpHypotheticalDHWVolumeWhenHeating)
                        print("")


                #Corrections for the violations of the physical limits of the storage systems
                helpValue_BufferStorageTemperature_CorrectedModulationDegree = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                helpValue_UsableVolumeDHW_CorrectedModulationDegree = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

                if heatingStartedPhysicalLimit_BufferStorage == True and numberOfHeatPumpStartsReachedHardLimit == True:
                    helpValue_BufferStorageTemperature_MediumModulationDegree = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((0.6 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    helpValue_UsableVolumeDHW_MediumModulationDegree = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((0.6 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if helpValue_UsableVolumeDHW_CorrectedModulationDegree >= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                        if helpValue_BufferStorageTemperature_MediumModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit and helpValue_BufferStorageTemperature_MediumModulationDegree <= SetUpScenarios.initialBufferStorageTemperature:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0.6
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                        elif helpValue_BufferStorageTemperature_MediumModulationDegree < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 1
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                        elif helpValue_BufferStorageTemperature_MediumModulationDegree > SetUpScenarios.initialBufferStorageTemperature:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                            heatingStartedPhysicalLimit_BufferStorage =False

                if heatingStartedPhysicalLimit_DHWTank == True and numberOfHeatPumpStartsReachedHardLimit == True:
                    helpValue_BufferStorageTemperature_MediumModulationDegree = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((0.6 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    helpValue_UsableVolumeDHW_MediumModulationDegree = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((0.6 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                       if helpValue_UsableVolumeDHW_MediumModulationDegree >= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit and helpValue_UsableVolumeDHW_MediumModulationDegree <= SetUpScenarios.initialUsableVolumeDHWTank:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0.6
                       elif helpValue_UsableVolumeDHW_MediumModulationDegree < SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 1
                       elif helpValue_UsableVolumeDHW_MediumModulationDegree > SetUpScenarios.initialUsableVolumeDHWTank:
                            outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                            outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                            heatingStartedPhysicalLimit_DHWTank =False


                if index_timeslot ==0:
                    helpValue_BufferStorageTemperature_CorrectedModulationDegree =  SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    helpValue_UsableVolumeDHW_CorrectedModulationDegree =  SetUpScenarios.initialUsableVolumeDHWTank + ((outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

                if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                    print("Corrections Physical limit too high value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")

                if helpValue_BufferStorageTemperature_CorrectedModulationDegree <= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 1
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                    print("Corrections Physical limit too low value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                    heatingStartedPhysicalLimit_BufferStorage = True

                if helpValue_UsableVolumeDHW_CorrectedModulationDegree  >= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 0
                    print("Corrections Physical limit too high value DHW. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")

                if helpValue_UsableVolumeDHW_CorrectedModulationDegree  <= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                    outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = 0
                    outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = 1
                    print("Corrections Physical limit too low value DHW. Time: " +  str(index_timeslot)+ "; ANN value SpaceHeating: " + str(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]) + "\n")
                    heatingStartedPhysicalLimit_DHWTank = True





                #Corrections for the SOC of the EV
                if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] >  100:
                   outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] = 0
                   print("Correction of the EV. SOC too high. Time: " +  str(index_timeslot))
                if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] <  0:
                   outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] = maximumPowerEVChargingForNotCreatingANewPeak

                #Corrections for the last value of the optimization horizon for the SOC
                if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek * 2:
                    helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot
                    helpHypotheticalEnergyEVWhenCharging = simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot - 1]
                    helpHypotheticalSOCWhenCharging = (helpHypotheticalEnergyEVWhenCharging / maximumPowerEVChargingForNotCreatingANewPeak)*100
                    for helpCurrentHypotheticalTimeSlot in range (0, helpTimeSlotsToEndOfweek):
                        helpHypotheticalEnergyEVWhenCharging  = helpHypotheticalEnergyEVWhenCharging + (maximumPowerEVChargingForNotCreatingANewPeak *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 )
                        helpHypotheticalSOCWhenCharging  = (helpHypotheticalEnergyEVWhenCharging / SetUpScenarios.capacityMaximal_EV)*100

                    if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] >= SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection:
                        outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] = 0
                        print("Correction of the EV (End of the week). SOC too high. Time: " +  str(index_timeslot))
                    if helpHypotheticalSOCWhenCharging <= SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection * 0.5:
                        outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] =  maximumPowerEVChargingForNotCreatingANewPeak
                        if inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] > maximumPowerEVChargingForNotCreatingANewPeak:
                            outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] =  inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot]
                        print("Correction of the EV (End of the week). SOC too low. Time: " +  str(index_timeslot))



                #Calculate the simulation values with the corrected input vectors
                if index_timeslot >=1:
                    if overruleActions == False:
                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]
                        outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] = inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot]
                    simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot]  =simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot - 1] + (outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]  = (simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalSOCDropWithNoCharging_BT1 [index_week, index_BT1] = hypotheticalSOCDropWithNoCharging_BT1 [index_week, index_BT1] + (df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]/ SetUpScenarios.capacityMaximal_EV)*100

                if index_timeslot ==0:
                    if overruleActions == False:
                        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] = inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]
                        outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] = inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]
                        outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] = inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot]
                    simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] = SetUpScenarios.initialUsableVolumeDHWTank + ((outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot]  = SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + (outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]  = (simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalSOCDropWithNoCharging_BT1 [index_week, index_BT1] =  (df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]/ SetUpScenarios.capacityMaximal_EV)*100


                simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings (index_BT1)
                simulationResult_RESGeneration_BT1 [index_week, index_BT1, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings (index_BT1) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine
                simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] = (outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] + outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] ) * SetUpScenarios.electricalPower_HP + outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] + df_buildingData ['Electricity [W]'] [index_timeslot + 1]
                simulationResult_SurplusPower_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_RESGeneration_BT1 [index_week, index_BT1, index_timeslot] - simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot]

                if simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] > simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]:
                    simulationResult_costs_BT1 [index_week, index_BT1, index_timeslot] = (simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] - simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] <= simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]:
                    simulationResult_costs_BT1 [index_week, index_BT1, index_timeslot] = (simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot] - simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)



                # Calculate number and degree of corrections (for statistical purposes)
                if inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] != outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot]:
                   correctingStats_BT1_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots [index_week, index_BT1] +=1
                   correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week, index_BT1] = correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week, index_BT1] + abs(inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot] - outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] )
                   correctingStats_BT1_heatGenerationCoefficientSpaceHeating_profile [index_week, index_BT1, index_timeslot] = outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot]  - inputVector_BT1_heatGenerationCoefficientSpaceHeating [index_BT1, index_timeslot]
                if inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] != outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot]:
                   correctingStats_BT1_heatGenerationCoefficientDHW_numberOfTimeSlots [index_week, index_BT1] +=1
                   correctingStats_BT1_heatGenerationCoefficientDHW_sumOfCorrections [index_week, index_BT1] = correctingStats_BT1_heatGenerationCoefficientDHW_sumOfCorrections [index_week, index_BT1] + abs(inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] - outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] )
                   correctingStats_BT1_heatGenerationCoefficientDHW_profile [index_week, index_BT1, index_timeslot] = outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] - inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]
                if inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] != outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot]:
                   correctingStats_BT1_chargingPowerEV_numberOfTimeSlots [index_week, index_BT1] +=1
                   correctingStats_BT1_chargingPowerEV_sumOfCorrections [index_week, index_BT1] = correctingStats_BT1_chargingPowerEV_sumOfCorrections [index_week, index_BT1] + abs(inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] - outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot] )
                   correctingStats_BT1_chargingPowerEV_profile [index_week, index_BT1, index_timeslot] = outputVector_BT1_chargingPowerEV_corrected [index_BT1, index_timeslot]  - inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot]




               #Calculate the constraint violation
                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] >SetUpScenarios.maximalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] -SetUpScenarios.maximalBufferStorageTemperature
                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] <SetUpScenarios.minimalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - SetUpScenarios.minimalBufferStorageTemperature

                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.maximumCapacityDHWTankOptimization:
                    simulation_ConstraintViolation_DHWTankRange_BT1  [index_week, index_BT1, index_timeslot] = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - SetUpScenarios.maximumCapacityDHWTankOptimization
                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.minimumCapacityDHWTankOptimization:
                    simulation_ConstraintViolation_DHWTankRange_BT1  [index_week, index_BT1, index_timeslot] = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - SetUpScenarios.minimumCapacityDHWTankOptimization

                if inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot] > 0 and inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] >0:
                    simulation_ConstraintViolation_OnlyOneStorage_BT1 [index_week, index_BT1, index_timeslot] =1

                if (inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP/100) and (inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot]>0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] = (SetUpScenarios.minimalModulationdDegree_HP/100) - inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot]

                if inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot] > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] + inputVector_BT1_heatGenerationCoefficientSpaceHeating[index_BT1, index_timeslot] -1
                if (inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] < (SetUpScenarios.minimalModulationdDegree_HP/100)) and (inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]>0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] +  (SetUpScenarios.minimalModulationdDegree_HP/100) - inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot]
                if inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] + inputVector_BT1_heatGenerationCoefficientDHW [index_BT1, index_timeslot] - 1

                if  simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] < 0:
                    simulation_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]
                if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] >100:
                    simulation_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1, index_timeslot] =simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] - 100

                if inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] < 0:
                    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1, index_timeslot] = inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot]
                if inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] > SetUpScenarios.chargingPowerMaximal_EV:
                    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1, index_timeslot] = inputVector_BT1_chargingPowerEV [index_BT1, index_timeslot] - SetUpScenarios.chargingPowerMaximal_EV



                # Calculate the additional constraint violations of the internal controller
                if  simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] >SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary
                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary
                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] >SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit
                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit

                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                    simulation_ConstraintViolation_DHWTankRange_CorrectionLimit_BT1 [index_week, index_BT1, index_timeslot]  = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary
                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
                    simulation_ConstraintViolation_DHWTankRange_CorrectionLimit_BT1 [index_week, index_BT1, index_timeslot]  = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary
                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                    simulation_ConstraintViolation_DHWTankRange_PhysicalLimit_BT1 [index_week, index_BT1, index_timeslot]  = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary
                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                    simulation_ConstraintViolation_DHWTankRange_PhysicalLimit_BT1 [index_week, index_BT1, index_timeslot]  = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary

                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT1 [index_week, index_BT1] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection)
                    if  simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT1 [index_week, index_BT1] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection) - simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]
                    if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection:
                        total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_BT1 [index_week, index_BT1] = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - ( SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection)
                    if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection:
                        total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_BT1 [index_week, index_BT1] = (SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection) - simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]
                    if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] > (SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection):
                        total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_BT1  [index_week, index_BT1] =  simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] - ((SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection))
                    if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] < (SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection):
                        total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_BT1  [index_week, index_BT1] = ((SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection)) - simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]

            #Count number of starts of the heat pump
                simulationResult_numberOfStartsHP_PerTimeslot_BT1[index_week, index_BT1, index_timeslot] = simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1]
                simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT1 [index_week, index_BT1, index_timeslot]= helpCounterNumberOfRunningSlots_Combined
                simulationResult_numberOfStandbySlotsHP_PerTimeslot_BT1[index_week, index_BT1, index_timeslot] = helpCounterNumberOfStandBySlots_Combined

                if simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT1 [index_week, index_BT1, index_timeslot] >0:
                    simulationResult_isHPRunning_PerTimeslot_BT1 [index_week, index_BT1, index_timeslot] =1

                if index_timeslot >= 1:
                    if  outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1] == 0 and outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] >0.0001 :
                        simulationResult_numberOfStartsBufferStorage_BT1 [index_week, index_BT1] += 1
                    if outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1] == 0 and outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] >0.0001 :
                        simulationResult_numberOfStartsDHWTank_BT1 [index_week, index_BT1] += 1
                    if  (outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot - 1] == 0 and outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot - 1] == 0) and (outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] >0.001 or outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] >0.001):
                        simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] += 1



                #Calculate the total additional constraint violations
                total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT1 [index_week, index_BT1] =  total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT1 [index_week, index_BT1] +  abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_DHWTankRange_CorrectionLimit_BT1 [index_week, index_BT1] = total_ConstraintViolation_DHWTankRange_CorrectionLimit_BT1 [index_week, index_BT1] +  abs(simulation_ConstraintViolation_DHWTankRange_CorrectionLimit_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT1 [index_week, index_BT1] =  total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT1 [index_week, index_BT1] +  abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_DHWTankRange_PhysicalLimit_BT1 [index_week, index_BT1] = total_ConstraintViolation_DHWTankRange_PhysicalLimit_BT1 [index_week, index_BT1] +  abs(simulation_ConstraintViolation_DHWTankRange_PhysicalLimit_BT1 [index_week, index_BT1, index_timeslot])

                if Run_Simulations.considerMaximumNumberOfStartsHP_Combined == True:
                    if simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] > (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts:
                        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_BT1 [index_week, index_BT1] = simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] - (Run_Simulations.maximumNumberOfStarts_Combined + 1)  - Run_Simulations.additionalNumberOfAllowedStarts
                if Run_Simulations.considerMaxiumNumberOfStartsHP_Individual  == True:
                    if simulationResult_numberOfStartsBufferStorage_BT1 [index_week, index_BT1] > Run_Simulations.maximumNumberOfStarts_Individual + Run_Simulations.additionalNumberOfAllowedStarts:
                        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT1 [index_week, index_BT1]  = simulationResult_numberOfStartsBufferStorage_BT1 [index_week, index_BT1] - Run_Simulations.maximumNumberOfStarts_Individual + Run_Simulations.additionalNumberOfAllowedStarts
                    if simulationResult_numberOfStartsDHWTank_BT1 [index_week, index_BT1] > Run_Simulations.maximumNumberOfStarts_Individual + Run_Simulations.additionalNumberOfAllowedStarts:
                        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT1 [index_week, index_BT1]  = total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]+  simulationResult_numberOfStartsDHWTank_BT1 [index_week, index_BT1] - Run_Simulations.maximumNumberOfStarts_Individual - Run_Simulations.additionalNumberOfAllowedStarts





        #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                total_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1] = total_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1] + abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_DHWTankRange_BT1 [index_week, index_BT1] = total_ConstraintViolation_DHWTankRange_BT1 [index_week, index_BT1] + abs(simulation_ConstraintViolation_DHWTankRange_BT1 [index_week, index_BT1, index_timeslot])
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:

                    if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT1 [index_week, index_BT1] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue)
                    if  simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT1 [index_week, index_BT1] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue) - simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]
                    if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        total_ConstraintViolation_DHWTankLastValue_BT1 [index_week, index_BT1] = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - ( SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue)
                    if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        total_ConstraintViolation_DHWTankLastValue_BT1 [index_week, index_BT1] = (SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue) - simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]
                    if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] > (SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue):
                        total_ConstraintViolation_SOCOfTheEVLastValue_BT1  [index_week, index_BT1] =  simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] - ((SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue))
                    if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] < (SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue):
                        total_ConstraintViolation_SOCOfTheEVLastValue_BT1  [index_week, index_BT1] = ((SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue)) - simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]




                if outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected [index_BT1, index_timeslot] > 0.0001 and outputVector_BT1_heatGenerationCoefficientDHW_corrected [index_BT1, index_timeslot] > 0.0001:
                    total_ConstraintViolation_OnlyOneStorage_BT1 [index_week, index_BT1] = total_ConstraintViolation_OnlyOneStorage_BT1 [index_week, index_BT1] + 1
                total_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1] = total_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1] + abs(simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1] =  total_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1] + abs(simulation_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1] = total_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1] + abs (simulation_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1, index_timeslot])
                if Run_Simulations.considerMaximumNumberOfStartsHP_Combined == True:
                    if simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] > (Run_Simulations.maximumNumberOfStarts_Combined + 1):
                        total_ConstraintViolation_numberOfStarts_Combined_BT1 [index_week, index_BT1] = simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] - (Run_Simulations.maximumNumberOfStarts_Combined + 1)
                if Run_Simulations.considerMaxiumNumberOfStartsHP_Individual  == True:
                    if simulationResult_numberOfStartsBufferStorage_BT1 [index_week, index_BT1] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]  = simulationResult_numberOfStartsBufferStorage_BT1 [index_week, index_BT1] - Run_Simulations.maximumNumberOfStarts_Individual
                    if simulationResult_numberOfStartsDHWTank_BT1 [index_week, index_BT1] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]  = total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]+  simulationResult_numberOfStartsDHWTank_BT1 [index_week, index_BT1] - Run_Simulations.maximumNumberOfStarts_Individual


        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT1  [index_week, index_BT1, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT1  [index_week, index_BT1] = simulationObjective_surplusEnergyKWH_BT1  [index_week, index_BT1] + ((simulationResult_SurplusPower_BT1  [index_week, index_BT1, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] - simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]) > simulationObjective_maximumLoad_BT1 [index_week, index_BT1]:
                    simulationObjective_maximumLoad_BT1 [index_week, index_BT1] = simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] -  simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]
                if (simulationResult_PVGeneration_BT1  [index_week, index_BT1, index_timeslot] -  simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot]) > simulationObjective_maximumLoad_BT1 [index_week, index_BT1]:
                    simulationObjective_maximumLoad_BT1 [index_week, index_BT1] = simulationResult_PVGeneration_BT1  [index_week, index_BT1, index_timeslot] -   simulationResult_electricalLoad_BT1[index_week, index_BT1, index_timeslot]
                simulationObjective_costs_BT1  [index_week, index_BT1]  = simulationObjective_costs_BT1  [index_week, index_BT1] +  simulationResult_costs_BT1 [index_week, index_BT1, index_timeslot]




        #Building Type 2
        for index_BT2 in range (0, len(indexOfBuildingsOverall_BT2)):


            #Reading of the data
            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT2_mHP_SFH_1Minute_weeks/HH" + str(indexOfBuildingsOverall_BT2[index_BT2]) + "/HH" + str(indexOfBuildingsOverall_BT2[index_BT2]) + "_week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_weeks/Outside_Temperature_1Minute_week' +  str(currentweek) + '.csv', sep =";")

            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"
            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()



            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

            #Wind generation

            indexBuildingForWindPowerAssignment = SetUpScenarios.numberOfBuildings_BT1 + index_BT2
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1

            # Set up inital values for the simulation
            simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, 0] = SetUpScenarios.initialBufferStorageTemperature
            simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, 0] = SetUpScenarios.initialUsableVolumeDHWTank
            simulationResult_PVGeneration_BT2 [index_week, index_BT2, 0] = df_buildingData ['PV [nominal]'] [1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + index_BT2)
            simulationResult_RESGeneration_BT2 [index_week, index_BT2, 0] = df_buildingData ['PV [nominal]'] [1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + index_BT2)  + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [1]  * SetUpScenarios.maximalPowerOfWindTurbine
            simulationResult_electricalLoad_BT2 [index_week, index_BT2, 0] = (inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, 0] +  inputVector_BT2_heatGenerationCoefficientDHW[index_BT2, 0]) * SetUpScenarios.electricalPower_HP   + df_buildingData['Electricity [W]'] [1]
            simulationResult_SurplusPower_BT2 [index_week, index_BT2, 0] = simulationResult_RESGeneration_BT2 [index_week, index_BT2, 0] - simulationResult_electricalLoad_BT2 [index_week, index_BT2, 0]
            simulationResult_costs_BT2 [index_week, index_BT2, 0] = (simulationResult_electricalLoad_BT2 [index_week, index_BT2, 0] - simulationResult_PVGeneration_BT2 [index_week, index_BT2, 0]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [1]/3600000)


            helpCountNumberOfStartsIndividual_SpaceHeating =0
            helpCountNumberOfStartsIndividual_DHW =0
            helpCountNumberOfStartsIndividual_Combined =0
            helpCounterNumberOfRunningSlots_SpaceHeating =0
            helpCounterNumberOfRunningSlots_DHW =0
            helpCounterNumberOfRunningSlots_Combined =0
            helpCounterNumberOfStandBySlots_SpaceHeating =0
            helpCounterNumberOfStandBySlots_DHW =0
            helpCounterNumberOfStandBySlots_Combined =0

            startedHeatingHeatPump = False
            stoppedHeatingHeatPump = False

            helpCurrentPeakLoadOfTheweek =0

            numberOfHeatPumpStartsReachedSoftLimit = False
            numberOfHeatPumpStartsReachedHardLimit = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = False

            heatingStartedPhysicalLimit_BufferStorage = False
            heatingStartedPhysicalLimit_DHWTank = False

            startedHeatingDHWCorrection_end = False
            startedHeatingSpaceHeatingCorrection_end = False

            correction_bothStorageHeatedUp_lastTimeBufferStorageOverruled = True
            correction_bothStorageHeatedUp_lastTimeDHWOverruled = False



            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):

                #Check how often the heat pump has been started so far
                if index_timeslot >= 2:

                    if outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 2] == 0 and outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1] >0.001:
                        helpCountNumberOfStartsIndividual_SpaceHeating +=1

                    if outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 2] == 0 and outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1] >0.001:
                        helpCountNumberOfStartsIndividual_DHW +=1

                    if (outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 2] == 0 and outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 2] == 0) and ( outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1] >0.001 or outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1] >0.001):
                        helpCountNumberOfStartsIndividual_Combined +=1
                        startedHeatingHeatPump = True
                        stoppedHeatingHeatPump = False

                    if (outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 2] > 0.01 or outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 2] > 0.01) and ( outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1] ==0  and outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1] ==0):
                        stoppedHeatingHeatPump = True
                        startedHeatingHeatPump = False
                        if lastHeatingAfterHeatPumpStartsReachedHardLimitStarted ==True:
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = True

                #Update the currentNumberOfRunningSlots for the heat pump
                    if  outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1] > 0.001:
                        helpCounterNumberOfRunningSlots_SpaceHeating +=1
                        helpCounterNumberOfStandBySlots_SpaceHeating =0
                    if outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1] > 0.001:
                        helpCounterNumberOfRunningSlots_DHW +=1
                        helpCounterNumberOfStandBySlots_DHW =0
                    if  outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1] > 0.001 or outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1] > 0.001:
                        helpCounterNumberOfRunningSlots_Combined +=1
                        helpCounterNumberOfStandBySlots_Combined =0
                    if  outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1] == 0:
                        helpCounterNumberOfStandBySlots_SpaceHeating  +=1
                        helpCounterNumberOfRunningSlots_SpaceHeating =0
                    if outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1] == 0:
                        helpCounterNumberOfStandBySlots_DHW  +=1
                        helpCounterNumberOfRunningSlots_DHW =0
                    if  outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1]  == 0 and outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1]  == 0:
                        helpCounterNumberOfStandBySlots_Combined  +=1
                        helpCounterNumberOfRunningSlots_Combined =0

                if startedHeatingHeatPump == True and helpCounterNumberOfRunningSlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
                    startedHeatingHeatPump = False
                if stoppedHeatingHeatPump == True and helpCounterNumberOfStandBySlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
                    stoppedHeatingHeatPump = False

                if numberOfHeatPumpStartsReachedHardLimit == True:
                    numberOfHeatPumpStartsReachedSoftLimit = False

                # Pre-Corrections of input values: too high input values or low
                if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]  > 1:
                    inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]  =1
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot]  =1
                    print("Pre-Corrections too high value Space Heating. Time: " +  str(index_timeslot) + "\n")
                if inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]  > 1:
                    inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] =1
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot]  =1
                    print("Pre-Corrections too high value DHW. Time:"+  str(index_timeslot)  + "\n")

                if inputVector_BT2_heatGenerationCoefficientSpaceHeating[index_BT2, index_timeslot]  < 0:
                    inputVector_BT2_heatGenerationCoefficientSpaceHeating[index_BT2, index_timeslot]  =0
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot]  =0

                if inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]  < 0:
                    inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] =0
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot]  =0


                # Pre-Corrections: Set small heating values to 0
                if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] > 0 and inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] < 0.1:
                    inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] = 0

                if inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] > 0 and inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] < 0.1:
                    inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] = 0

                # Pre-Corrections of input values: minimal modulation
                if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] > 0.001 and inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP / 100:
                    print("Pre_Correction: Min Modulation. Time: " + str( index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + "\n")
                    inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP / 100

                if inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] > 0.001 and inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP / 100:
                    print("Pre_Correction: Min Modulation. Time: " + str(index_timeslot) + "; ANN value DHW: " + str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "\n")
                    inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP / 100





                # Pre-Corrections of input values: heating up only one storage at one time
                if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] > 0.001 and inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]  > 0.001:
                    print("Pre_Correction Only one storage. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot])  + "\n")
                    if correction_bothStorageHeatedUp_lastTimeBufferStorageOverruled==True:
                        inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] = 0
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot]  =0
                        correction_bothStorageHeatedUp_lastTimeBufferStorageOverruled = False
                        correction_bothStorageHeatedUp_lastTimeDHWOverruled = True
                    elif correction_bothStorageHeatedUp_lastTimeDHWOverruled ==True:
                        inputVector_BT2_heatGenerationCoefficientSpaceHeating  [index_BT2, index_timeslot] = 0
                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                        correction_bothStorageHeatedUp_lastTimeBufferStorageOverruled = True
                        correction_bothStorageHeatedUp_lastTimeDHWOverruled = False


                if  simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts_BeforeConsideringMinimalRuntime:
                    numberOfHeatPumpStartsReachedSoftLimit = True

                if simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts - 2:
                    numberOfHeatPumpStartsReachedHardLimit = True
                    numberOfHeatPumpStartsReachedSoftLimit = False

                #Calculate the hypothetical simulation values if the non-corrected actions were applied
                cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] = SetUpScenarios.initialUsableVolumeDHWTank + ((inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


               # Calculate the maximum power of the heat pump and the EV for not creating a new peak load
                if index_timeslot >=1:
                    if (simulationResult_electricalLoad_BT2  [index_week, index_BT2, index_timeslot - 1] - simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_electricalLoad_BT2  [index_week, index_BT2, index_timeslot - 1] - simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot - 1]
                    if (simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot - 1] - simulationResult_electricalLoad_BT2  [index_week, index_BT2, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot - 1] - simulationResult_electricalLoad_BT2  [index_week, index_BT2, index_timeslot - 1]

                maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP
                maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP

                if (inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] + inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) * SetUpScenarios.electricalPower_HP + df_buildingData ['Electricity [W]'] [index_timeslot + 1] > simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = helpCurrentPeakLoadOfTheweek - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = helpCurrentPeakLoadOfTheweek  - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]

                if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek > SetUpScenarios.electricalPower_HP:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP
                if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek > SetUpScenarios.electricalPower_HP:
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP


                if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP
                if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP:
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek =Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP




                #Corrections due to violations of the temperature and volume constraints
                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] <= SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                    print("Correction volume too low DHW (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] >= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                    helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if helpCounterNumberOfStandBySlots_Combined >0:
                        helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] > 0.001 and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod < SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and (numberOfHeatPumpStartsReachedSoftLimit == False or stoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
                       outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                       print("Correction DHW too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                    else:
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                        print("Correction DHW volume too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")

                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:

                    helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    if helpCounterNumberOfStandBySlots_Combined >0:
                        helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] > 0.001 and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod < SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and (numberOfHeatPumpStartsReachedSoftLimit == False or stoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
                       outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                       print("Correction BufferStorage too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                    else:
                       outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                       print("Correction BufferStorage too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")

                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary and simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                    print("Correction BufferStorage too low (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")


                # Corrections due to minimal modulation degree of the heat pump
                if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] > 0.001 and inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP /100:
                    inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP /100
                    print("Correction Minimal Mod. SpaceHeating. Time: " +  str(index_timeslot) + "; ANN value: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                if inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] > 0.001 and inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP /100:
                    inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP /100
                    print("Correction Minimal Mod. DHW. Time: " +  str(index_timeslot) + "; ANN value: " + str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")



                #Calculate the hypothetical simulation values if the  corrected actions were applied
                cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] = SetUpScenarios.initialUsableVolumeDHWTank + ((outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT2_SpaceHeating [index_BT2, index_timeslot] = df_buildingData['Space Heating [W]'] [index_timeslot + 1]
                simulationInput_BT2_DHW [index_BT2, index_timeslot] = df_buildingData ['DHW [W]'] [index_timeslot + 1]
                simulationInput_BT2_electricityDemand [index_BT2, index_timeslot] = df_buildingData ['Electricity [W]'] [index_timeslot + 1]


                if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] >= SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection:
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection:
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                    startedHeatingSpaceHeatingCorrection_end = False
                    startedHeatingDHWCorrection_end = True
                if startedHeatingDHWCorrection_end == True and simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot] >= SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 2:
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                if startedHeatingDHWCorrection_end == True and simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 2:
                    startedHeatingDHWCorrection_end = False
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0




                #Corrections due to high number of starts of the heat pump

                #Soft Limit Reached --> Consider minimum runtimes and standbytimes of the heat pump
                if numberOfHeatPumpStartsReachedSoftLimit ==True and startedHeatingDHWCorrection_end==False and startedHeatingSpaceHeatingCorrection_end ==False:
                    print("numberOfHeatPumpStartsReachedSoftLimit; Timeslot: ",index_timeslot)
                    if startedHeatingHeatPump == True:
                        print("numberOfHeatPumpStartsReachedSoftLimit; started HP")
                        if outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] > 0.01 and simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot]
                        elif outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] > 0.01 and simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                            helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                            if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                                outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                            elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                                elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                    if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                    elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                                    elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0

                        if outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] > 0.01 and simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot] <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] =  outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot]
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                        elif outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] > 0.01 and simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                            helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                            if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] =   0
                            elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] =  SetUpScenarios.minimalModulationdDegree_HP/100
                                elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                                    if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] =  0
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] =  SetUpScenarios.minimalModulationdDegree_HP/100
                                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0

                        if outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] == 0 and outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] ==0:
                            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                            helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                            currentSOCBufferStorage_CorrectionLimits =  (simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1] - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
                            currentSOCDHWTank_CorrectionLimits = ( simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary) / ( SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary )
                            if currentSOCBufferStorage_CorrectionLimits < currentSOCDHWTank_CorrectionLimits:
                                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                                elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod  <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] =  SetUpScenarios.minimalModulationdDegree_HP/100
                            else:
                                if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod  <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] =  SetUpScenarios.minimalModulationdDegree_HP/100
                                elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0


                    elif stoppedHeatingHeatPump ==True:
                        print("numberOfHeatPumpStartsReachedSoftLimit; stopped HP")
                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0


                # Last heating of the week if the numberOfHeatPumpStartsReachedHardLimit
                if numberOfHeatPumpStartsReachedHardLimit ==True and startedHeatingDHWCorrection_end==False and startedHeatingSpaceHeatingCorrection_end ==False:
                    print("numberOfHeatPumpStartsReachedHardLimit")
                    # Last heating of the week
                    if lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == False:
                        fractionOfweekLeft =1 - (index_timeslot / SetUpScenarios.numberOfTimeSlotsPerWeek)
                        currentSOCBufferStorage_CorrectionLimits =  (simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1] - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
                        currentSOCDHWTank_CorrectionLimits = ( simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary) / ( SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary )
                        differenceTargetValueEndAndUpperLimit_SpaceHeating = SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - (SetUpScenarios.initialBufferStorageTemperature)
                        possibleTargetTemperatureForLastHeating_SpaceHeating = SetUpScenarios.initialBufferStorageTemperature  + differenceTargetValueEndAndUpperLimit_SpaceHeating  * fractionOfweekLeft
                        differenceTargetValueEndAndUpperLimit_DHW = SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - (SetUpScenarios.initialUsableVolumeDHWTank)
                        possibleTargetVolumeForLastHeating_DHW = SetUpScenarios.initialUsableVolumeDHWTank  + differenceTargetValueEndAndUpperLimit_DHW  * fractionOfweekLeft
                        if currentSOCBufferStorage_CorrectionLimits <= currentSOCDHWTank_CorrectionLimits:
                            if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1] < possibleTargetTemperatureForLastHeating_SpaceHeating:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                                        lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                            elif simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot - 1] < possibleTargetVolumeForLastHeating_DHW:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] =  maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                                        lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                        elif currentSOCBufferStorage_CorrectionLimits > currentSOCDHWTank_CorrectionLimits:
                            if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot - 1] < possibleTargetVolumeForLastHeating_DHW:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] =  maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                                        lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                            elif simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1] < possibleTargetTemperatureForLastHeating_SpaceHeating:
                                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                                        lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                        if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot - 1] >= possibleTargetVolumeForLastHeating_DHW and simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1] >= possibleTargetTemperatureForLastHeating_SpaceHeating:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                    elif lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == True:
                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0




                #Corrections for the last value of the optimization horizon
                if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek:


                    helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot
                    helpHypotheticalBufferStorageTemperatureWhenHeating = simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot - 1]
                    helpHypotheticalBufferStorageTemperatureWhenNotHeating = simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot - 1]
                    helpHypotheticalDHWVolumeWhenHeating = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]
                    helpHypotheticalDHWVolumeWhenNotHeating = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]

                    averageSpaceHeatingDemandLastTimeslots = 0
                    averageDHWDemandLastTimeSlots = 0
                    averageCOPSpaceHeatingLastTimeSlots = 0
                    averageCOPDHWLastTimeSlots = 0
                    helpSumSpaceHeatingDemandLastTimeslots = 0
                    helpSumDHWDemandLastTimeSlots = 0
                    helpSumCOPSpaceHeatingLastTimeSlots =0
                    helpSumCOPDHWLastTimeSlots = 0


                    for i in range (0, Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek):
                        helpSumSpaceHeatingDemandLastTimeslots = helpSumSpaceHeatingDemandLastTimeslots + df_buildingData['Space Heating [W]'] [index_timeslot - i]
                        helpSumDHWDemandLastTimeSlots = helpSumDHWDemandLastTimeSlots + df_buildingData['DHW [W]'] [index_timeslot - i]
                        helpSumCOPSpaceHeatingLastTimeSlots = helpSumCOPSpaceHeatingLastTimeSlots + cop_heatPump_SpaceHeating[index_timeslot  - i]
                        helpSumCOPDHWLastTimeSlots = helpSumCOPDHWLastTimeSlots + cop_heatPump_DHW[index_timeslot  - i]

                    averageSpaceHeatingDemandLastTimeslots = helpSumSpaceHeatingDemandLastTimeslots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
                    averageDHWDemandLastTimeSlots = helpSumDHWDemandLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
                    averageCOPSpaceHeatingLastTimeSlots = helpSumCOPSpaceHeatingLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
                    averageCOPDHWLastTimeSlots =  helpSumCOPDHWLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek


                    for helpCurrentHypotheticalTimeSlot in range (0, helpTimeSlotsToEndOfweek):
                        helpHypotheticalBufferStorageTemperatureWhenHeating = helpHypotheticalBufferStorageTemperatureWhenHeating + (((maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP )* averageCOPSpaceHeatingLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - averageSpaceHeatingDemandLastTimeslots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                        helpHypotheticalBufferStorageTemperatureWhenNotHeating = helpHypotheticalBufferStorageTemperatureWhenNotHeating + ((0* averageCOPSpaceHeatingLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - averageSpaceHeatingDemandLastTimeslots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                        helpHypotheticalDHWVolumeWhenHeating = helpHypotheticalDHWVolumeWhenHeating + (((maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP ) * averageCOPDHWLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - averageDHWDemandLastTimeSlots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                        helpHypotheticalDHWVolumeWhenNotHeating = helpHypotheticalDHWVolumeWhenNotHeating + ((0 * averageCOPDHWLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - averageDHWDemandLastTimeSlots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


                    if helpHypotheticalBufferStorageTemperatureWhenNotHeating > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 1.0:
                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                        startedHeatingDHWCorrection_end = False
                        startedHeatingSpaceHeatingCorrection_end = False
                        print("Correction BufferStorage too high (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                        print("helpHypotheticalBufferStorageTemperatureWhenNotHeating: ", helpHypotheticalBufferStorageTemperatureWhenNotHeating)
                        print("")
                    if  helpHypotheticalBufferStorageTemperatureWhenHeating < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 1.0:
                        helpValueAdjustedHeating =  maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                        if helpValueAdjustedHeating < outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot]:
                            helpValueAdjustedHeating = outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot]

                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = helpValueAdjustedHeating
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0

                        startedHeatingDHWCorrection_end = False
                        startedHeatingSpaceHeatingCorrection_end = True
                        print("Correction BufferStorage too low (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                        print("helpHypotheticalBufferStorageTemperatureWhenHeating: ", helpHypotheticalBufferStorageTemperatureWhenHeating)
                        print("averageCOPSpaceHeatingLastTimeSlots: ", averageCOPSpaceHeatingLastTimeSlots)
                        print("averageSpaceHeatingDemandLastTimeslots: ", averageSpaceHeatingDemandLastTimeslots)

                        print("")
                    if helpHypotheticalDHWVolumeWhenNotHeating > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 1.0:
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                        startedHeatingDHWCorrection_end = False
                        startedHeatingSpaceHeatingCorrection_end = False
                        print("Correction DHW too high (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                        print ("helpHypotheticalDHWVolumeWhenNotHeating: ", helpHypotheticalDHWVolumeWhenNotHeating)
                        print("")
                    if helpHypotheticalDHWVolumeWhenHeating < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 1.0:
                        helpValueAdjustedHeating =  maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
                        if helpValueAdjustedHeating < outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot]:
                            helpValueAdjustedHeating = outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot]

                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = helpValueAdjustedHeating
                        startedHeatingDHWCorrection_end = True
                        startedHeatingSpaceHeatingCorrection_end = False
                        print("Correction DHW too low (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                        print ("helpHypotheticalDHWVolumeWhenHeating: ", helpHypotheticalDHWVolumeWhenHeating)
                        print("")


                #Corrections for the violations of the physical limits of the storage systems
                helpValue_BufferStorageTemperature_CorrectedModulationDegree = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                helpValue_UsableVolumeDHW_CorrectedModulationDegree = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

                if heatingStartedPhysicalLimit_BufferStorage == True and numberOfHeatPumpStartsReachedHardLimit == True:
                    helpValue_BufferStorageTemperature_MediumModulationDegree = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((0.6 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    helpValue_UsableVolumeDHW_MediumModulationDegree = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((0.6 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if helpValue_UsableVolumeDHW_CorrectedModulationDegree >= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                        if helpValue_BufferStorageTemperature_MediumModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit and helpValue_BufferStorageTemperature_MediumModulationDegree <= SetUpScenarios.initialBufferStorageTemperature:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0.6
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                        elif helpValue_BufferStorageTemperature_MediumModulationDegree < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 1
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                        elif helpValue_BufferStorageTemperature_MediumModulationDegree > SetUpScenarios.initialBufferStorageTemperature:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                            heatingStartedPhysicalLimit_BufferStorage =False

                if heatingStartedPhysicalLimit_DHWTank == True and numberOfHeatPumpStartsReachedHardLimit == True:
                    helpValue_BufferStorageTemperature_MediumModulationDegree = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((0.6 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    helpValue_UsableVolumeDHW_MediumModulationDegree = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((0.6 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                       if helpValue_UsableVolumeDHW_MediumModulationDegree >= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit and helpValue_UsableVolumeDHW_MediumModulationDegree <= SetUpScenarios.initialUsableVolumeDHWTank:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0.6
                       elif helpValue_UsableVolumeDHW_MediumModulationDegree < SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 1
                       elif helpValue_UsableVolumeDHW_MediumModulationDegree > SetUpScenarios.initialUsableVolumeDHWTank:
                            outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                            outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                            heatingStartedPhysicalLimit_DHWTank =False


                if index_timeslot ==0:
                    helpValue_BufferStorageTemperature_CorrectedModulationDegree =  SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    helpValue_UsableVolumeDHW_CorrectedModulationDegree =  SetUpScenarios.initialUsableVolumeDHWTank + ((outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

                if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                    print("Corrections Physical limit too high value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")

                if helpValue_BufferStorageTemperature_CorrectedModulationDegree <= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 1
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                    print("Corrections Physical limit too low value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                    heatingStartedPhysicalLimit_BufferStorage = True

                if helpValue_UsableVolumeDHW_CorrectedModulationDegree  >= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 0
                    print("Corrections Physical limit too high value DHW. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")

                if helpValue_UsableVolumeDHW_CorrectedModulationDegree  <= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                    outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = 0
                    outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = 1
                    print("Corrections Physical limit too low value DHW. Time: " +  str(index_timeslot)+ "; ANN value SpaceHeating: " + str(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]) + ", ANN value DHW: "+ str(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]) + "\n")
                    heatingStartedPhysicalLimit_DHWTank = True




                #Calculate the simulation values with the corrected input vectors
                if index_timeslot >=1:
                    if overruleActions == False:
                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]
                    simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                if index_timeslot ==0:
                    if overruleActions == False:
                        outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] = inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]
                        outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] = inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]
                    simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] = SetUpScenarios.initialUsableVolumeDHWTank + ((outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

                simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + index_BT2)
                simulationResult_RESGeneration_BT2 [index_week, index_BT2, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + index_BT2)  + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine
                simulationResult_SurplusPower_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_RESGeneration_BT2 [index_week, index_BT2, index_timeslot] - simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot]
                simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] = (outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] + outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] ) * SetUpScenarios.electricalPower_HP + df_buildingData ['Electricity [W]'] [index_timeslot + 1]



                if simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] > simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]:
                    simulationResult_costs_BT2 [index_week, index_BT2, index_timeslot] = (simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] - simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] <= simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]:
                    simulationResult_costs_BT2 [index_week, index_BT2, index_timeslot] = (simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot] - simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)



                # Calculate number and degree of corrections (for statistical purposes)
                if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] != outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot]:
                   correctingStats_BT2_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots [index_week, index_BT2] +=1
                   correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week, index_BT2] = correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week, index_BT2] + abs(inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] - outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] )
                   correctingStats_BT2_heatGenerationCoefficientSpaceHeating_profile [index_week, index_BT2, index_timeslot] = outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot]  - inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]
                if inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] != outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot]:
                   correctingStats_BT2_heatGenerationCoefficientDHW_numberOfTimeSlots [index_week, index_BT2] +=1
                   correctingStats_BT2_heatGenerationCoefficientDHW_sumOfCorrections [index_week, index_BT2] = correctingStats_BT2_heatGenerationCoefficientDHW_sumOfCorrections [index_week, index_BT2] + abs(inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] - outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] )
                   correctingStats_BT2_heatGenerationCoefficientDHW_profile [index_week, index_BT2, index_timeslot] = outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] - inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]


               #Calculate the constraint violation
                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] >SetUpScenarios.maximalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] -SetUpScenarios.maximalBufferStorageTemperature
                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] <SetUpScenarios.minimalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - SetUpScenarios.minimalBufferStorageTemperature

                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.maximumCapacityDHWTankOptimization:
                    simulation_ConstraintViolation_DHWTankRange_BT2  [index_week, index_BT2, index_timeslot] = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - SetUpScenarios.maximumCapacityDHWTankOptimization
                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.minimumCapacityDHWTankOptimization:
                    simulation_ConstraintViolation_DHWTankRange_BT2  [index_week, index_BT2, index_timeslot] =  simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - SetUpScenarios.minimumCapacityDHWTankOptimization


                if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] > 0 and inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] >0:
                    simulation_ConstraintViolation_OnlyOneStorage_BT2 [index_week, index_BT2, index_timeslot] =1

                if (inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP/100) and (inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]>0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] = (SetUpScenarios.minimalModulationdDegree_HP/100) - inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot]

                if inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] + inputVector_BT2_heatGenerationCoefficientSpaceHeating [index_BT2, index_timeslot] -1
                if (inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] < (SetUpScenarios.minimalModulationdDegree_HP/100)) and (inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]>0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] +  (SetUpScenarios.minimalModulationdDegree_HP/100) - inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot]
                if inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] + inputVector_BT2_heatGenerationCoefficientDHW [index_BT2, index_timeslot] - 1




                # Calculate the additional constraint violations of the internal controller
                if  simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] >SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary
                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary
                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] >SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit
                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit

                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                    simulation_ConstraintViolation_DHWTankRange_CorrectionLimit_BT2 [index_week, index_BT2, index_timeslot]  = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary
                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
                    simulation_ConstraintViolation_DHWTankRange_CorrectionLimit_BT2 [index_week, index_BT2, index_timeslot]  = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary
                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                    simulation_ConstraintViolation_DHWTankRange_PhysicalLimit_BT2 [index_week, index_BT2, index_timeslot]  = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary
                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                    simulation_ConstraintViolation_DHWTankRange_PhysicalLimit_BT2 [index_week, index_BT2, index_timeslot]  = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary

                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT2 [index_week, index_BT2] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection)
                    if  simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT2 [index_week, index_BT2] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection) - simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]
                    if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection:
                        total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_BT2 [index_week, index_BT2] = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - ( SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection)
                    if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection:
                        total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_BT2 [index_week, index_BT2] = (SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection) - simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]

                #Count number of starts of the Heat Pump
                simulationResult_numberOfStartsHP_PerTimeslot_BT2[index_week, index_BT2, index_timeslot] = simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2]
                simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT2 [index_week, index_BT2, index_timeslot]= helpCounterNumberOfRunningSlots_Combined
                simulationResult_numberOfStandbySlotsHP_PerTimeslot_BT2[index_week, index_BT2, index_timeslot] = helpCounterNumberOfStandBySlots_Combined


                if simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT2 [index_week, index_BT2, index_timeslot] >0:
                    simulationResult_isHPRunning_PerTimeslot_BT2 [index_week, index_BT2, index_timeslot] =1

                if index_timeslot >= 1:
                    if  outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1] == 0 and outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] >0.0001 :
                        simulationResult_numberOfStartsBufferStorage_BT2 [index_week, index_BT2] += 1
                    if outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1] == 0 and outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] >0.0001 :
                        simulationResult_numberOfStartsDHWTank_BT2 [index_week, index_BT2] += 1
                    if  (outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot - 1] == 0 and outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot - 1] == 0) and (outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] >0.001 or outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] >0.001):
                        startedHeatingHeatPump = True
                        stoppedHeatingHeatPump = False
                        simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] += 1



                #Calculate the total additional constraint violations
                total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT2 [index_week, index_BT2] =  total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT2 [index_week, index_BT2] +  abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT2 [index_week, index_BT2, index_timeslot])
                total_ConstraintViolation_DHWTankRange_CorrectionLimit_BT2 [index_week, index_BT2] = total_ConstraintViolation_DHWTankRange_CorrectionLimit_BT2 [index_week, index_BT2] +  abs(simulation_ConstraintViolation_DHWTankRange_CorrectionLimit_BT2 [index_week, index_BT2, index_timeslot])
                total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT2 [index_week, index_BT2] =  total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT2 [index_week, index_BT2] +  abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT2 [index_week, index_BT2, index_timeslot])
                total_ConstraintViolation_DHWTankRange_PhysicalLimit_BT2 [index_week, index_BT2] = total_ConstraintViolation_DHWTankRange_PhysicalLimit_BT2 [index_week, index_BT2] +  abs(simulation_ConstraintViolation_DHWTankRange_PhysicalLimit_BT2 [index_week, index_BT2, index_timeslot])

                if Run_Simulations.considerMaximumNumberOfStartsHP_Combined == True:
                    if simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] > (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts:
                        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_BT2 [index_week, index_BT2] = simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] - (Run_Simulations.maximumNumberOfStarts_Combined + 1)  - Run_Simulations.additionalNumberOfAllowedStarts
                if Run_Simulations.considerMaxiumNumberOfStartsHP_Individual  == True:
                    if simulationResult_numberOfStartsBufferStorage_BT2 [index_week, index_BT2] > Run_Simulations.maximumNumberOfStarts_Individual + Run_Simulations.additionalNumberOfAllowedStarts:
                        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT2 [index_week, index_BT2]  = simulationResult_numberOfStartsBufferStorage_BT2 [index_week, index_BT2] - Run_Simulations.maximumNumberOfStarts_Individual + Run_Simulations.additionalNumberOfAllowedStarts
                    if simulationResult_numberOfStartsDHWTank_BT2 [index_week, index_BT2] > Run_Simulations.maximumNumberOfStarts_Individual + Run_Simulations.additionalNumberOfAllowedStarts:
                        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT2 [index_week, index_BT2]  = total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]+  simulationResult_numberOfStartsDHWTank_BT2 [index_week, index_BT2] - Run_Simulations.maximumNumberOfStarts_Individual - Run_Simulations.additionalNumberOfAllowedStarts




            #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                total_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2] = total_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2] + abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2, index_timeslot])
                total_ConstraintViolation_DHWTankRange_BT2 [index_week, index_BT2] = total_ConstraintViolation_DHWTankRange_BT2 [index_week, index_BT2] + abs(simulation_ConstraintViolation_DHWTankRange_BT2 [index_week, index_BT2, index_timeslot])
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT2 [index_week, index_BT2] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue)
                    if  simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT2 [index_week, index_BT2] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue) - simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]
                    if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        total_ConstraintViolation_DHWTankLastValue_BT2 [index_week, index_BT2] = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - ( SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue)
                    if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        total_ConstraintViolation_DHWTankLastValue_BT2 [index_week, index_BT2] = (SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue) - simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]

                if outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected [index_BT2, index_timeslot] > 0.0001 and outputVector_BT2_heatGenerationCoefficientDHW_corrected [index_BT2, index_timeslot] > 0.0001:
                    total_ConstraintViolation_OnlyOneStorage_BT2 [index_week, index_BT2] = total_ConstraintViolation_OnlyOneStorage_BT2 [index_week, index_BT2] + 1
                total_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2] = total_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2] + abs(simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot])
                if Run_Simulations.considerMaximumNumberOfStartsHP_Combined == True:
                    if simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] > (Run_Simulations.maximumNumberOfStarts_Combined + 1):
                        total_ConstraintViolation_numberOfStarts_Combined_BT2 [index_week, index_BT2] = simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] - (Run_Simulations.maximumNumberOfStarts_Combined + 1)
                if Run_Simulations.considerMaxiumNumberOfStartsHP_Individual  == True:
                    if simulationResult_numberOfStartsBufferStorage_BT2 [index_week, index_BT2] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]  = simulationResult_numberOfStartsBufferStorage_BT2 [index_week, index_BT2] - Run_Simulations.maximumNumberOfStarts_Individual
                    if simulationResult_numberOfStartsDHWTank_BT2 [index_week, index_BT2] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]  = total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]+  simulationResult_numberOfStartsDHWTank_BT2 [index_week, index_BT2] - Run_Simulations.maximumNumberOfStarts_Individual


        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT2  [index_week, index_BT2, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT2  [index_week, index_BT2] = simulationObjective_surplusEnergyKWH_BT2  [index_week, index_BT2] + ((simulationResult_SurplusPower_BT2  [index_week, index_BT2, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] - simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]) > simulationObjective_maximumLoad_BT2 [index_week, index_BT2]:
                    simulationObjective_maximumLoad_BT2 [index_week, index_BT2] = simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] -  simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]
                if (simulationResult_PVGeneration_BT2  [index_week, index_BT2, index_timeslot] -  simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot]) > simulationObjective_maximumLoad_BT2 [index_week, index_BT2]:
                    simulationObjective_maximumLoad_BT2 [index_week, index_BT2] = simulationResult_PVGeneration_BT2  [index_week, index_BT2, index_timeslot] -   simulationResult_electricalLoad_BT2[index_week, index_BT2, index_timeslot]
                simulationObjective_costs_BT2  [index_week, index_BT2]  = simulationObjective_costs_BT2  [index_week, index_BT2] +  simulationResult_costs_BT2 [index_week, index_BT2, index_timeslot]



        #Building Type 3
        for index_BT3 in range (0, len(indexOfBuildingsOverall_BT3)):

            #Reading of the data

            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT3_EV_SFH_1Minute_weeks/HH" + str(indexOfBuildingsOverall_BT3[index_BT3]) + "/HH" + str(indexOfBuildingsOverall_BT3[index_BT3]) + "_week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_weeks/Outside_Temperature_1Minute_week' +  str(currentweek) + '.csv', sep =";")

            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"

            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            for i in range (0, len(df_buildingData['Availability of the EV'])):
                if df_buildingData['Availability of the EV'] [i] > 0.1:
                    df_buildingData['Availability of the EV'] [i] = 1.0
                if df_buildingData['Availability of the EV'] [i] < 0.1 and df_buildingData['Availability of the EV'] [i] >0.01:
                    df_buildingData['Availability of the EV'] [i] = 0.0

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

            #Create availability array for the EV

            availabilityOfTheEV = np.zeros(( SetUpScenarios.numberOfTimeSlotsPerWeek))
            for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerWeek):
                availabilityOfTheEV [index_timeslot_for_Availability] = df_buildingData['Availability of the EV'] [index_timeslot_for_Availability +1]
            indexOfTheEV = SetUpScenarios.numberOfBuildings_BT1 +  index_BT3
            energyConsumptionOfEVs_Joule = SetUpScenarios.generateEVEnergyConsumptionPatterns(availabilityOfTheEV, indexOfTheEV)


            df_availabilityPatternEV = pd.DataFrame({'Timeslot': df_buildingData.index, 'Availability of the EV':df_buildingData['Availability of the EV'] })
            del df_availabilityPatternEV['Timeslot']

            df_energyConsumptionEV_Joule = pd.DataFrame({'Timeslot': df_buildingData.index, 'Energy':energyConsumptionOfEVs_Joule  })
            del df_energyConsumptionEV_Joule['Timeslot']
            df_energyConsumptionEV_Joule.index +=1


            #Wind generation

            indexBuildingForWindPowerAssignment = SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1

            #Round column and rename it
            df_buildingData['Electricity [W]'] = df_buildingData['Electricity [W]'].apply(lambda x: round(x, 2))


            # Set up inital values for the simulation
            simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, 0]= (SetUpScenarios.initialSOC_EV/100) * SetUpScenarios.capacityMaximal_EV
            simulationResult_SOCofEV_BT3 [index_week, index_BT3, 0]= SetUpScenarios.initialSOC_EV
            simulationResult_PVGeneration_BT3 [index_week, index_BT3, 0] = df_buildingData ['PV [nominal]'] [1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3)
            simulationResult_RESGeneration_BT3 [index_week, index_BT3, 0] = df_buildingData ['PV [nominal]'] [1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3)  + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [1] * SetUpScenarios.maximalPowerOfWindTurbine
            simulationResult_electricalLoad_BT3 [index_week, index_BT3, 0] =  inputVector_BT3_chargingPowerEV[index_BT3, 0] + df_buildingData['Electricity [W]'] [1]
            simulationResult_SurplusPower_BT3 [index_week, index_BT3, 0] = simulationResult_RESGeneration_BT3 [index_week, index_BT3, 0] - simulationResult_electricalLoad_BT3 [index_week, index_BT3, 0]
            simulationResult_costs_BT3 [index_week, index_BT3, 0] = (simulationResult_electricalLoad_BT3 [index_week, index_BT3, 0] - simulationResult_PVGeneration_BT3 [index_week, index_BT3, 0]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [1]/3600000)



            helpCurrentPeakLoadOfTheweek =0


            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):


                # Pre-Corrections for the availability of the EV (charging is only possible if the EV is available at the charging station of the building)
                if inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] > 0.001 and  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] ==0:
                    inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] =0
                    outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] =0
                    print("Pre_Correction EV is not available for charging: " +  str(index_timeslot))

                # Pre-Corrections too high values or too low
                if inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] > SetUpScenarios.chargingPowerMaximal_EV:
                    inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] = SetUpScenarios.chargingPowerMaximal_EV
                    outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] = SetUpScenarios.chargingPowerMaximal_EV


                if inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] < 0:
                    inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] = 0
                    outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] = 0




                #Calculate the hypothetical simulation values if the non-corrected actions were applied
                if index_timeslot >=1:
                    simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot]  =simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot - 1] + ( inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]  = (simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                if index_timeslot ==0:
                    simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot]  = SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + ( inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]  = (simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100


               # Calculate the maximum power of the heat pump and the EV for not creating a new peak load
                if index_timeslot >=1:
                    if (simulationResult_electricalLoad_BT3  [index_week, index_BT3, index_timeslot - 1] - simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_electricalLoad_BT3  [index_week, index_BT3, index_timeslot - 1] - simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot - 1]
                    if (simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot - 1] - simulationResult_electricalLoad_BT3  [index_week, index_BT3, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot - 1] - simulationResult_electricalLoad_BT3  [index_week, index_BT3, index_timeslot - 1]

                maximumPowerEVChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_EV

                if inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] + df_buildingData ['Electricity [W]'] [index_timeslot + 1] > simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]:
                    maximumPowerEVChargingForNotCreatingANewPeak = helpCurrentPeakLoadOfTheweek  - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]



                if  maximumPowerEVChargingForNotCreatingANewPeak >  SetUpScenarios.chargingPowerMaximal_EV:
                    maximumPowerEVChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_EV

                if  maximumPowerEVChargingForNotCreatingANewPeak < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection *  SetUpScenarios.chargingPowerMaximal_EV:
                    maximumPowerEVChargingForNotCreatingANewPeak = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.chargingPowerMaximal_EV



                # Corrections for the SOC of the EV
                if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] > 100:
                    outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] = 0



                #Corrections for the SOC of the EV
                if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] >  100:
                   outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] = 0
                   print("Correction of the EV. SOC too high. Time: " +  str(index_timeslot))
                if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] <  0:
                   outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] = maximumPowerEVChargingForNotCreatingANewPeak

                #Corrections for the last value of the optimization horizon for the SOC
                if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek * 2:
                    helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot
                    helpHypotheticalEnergyEVWhenCharging = simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot - 1]
                    helpHypotheticalSOCWhenCharging = (helpHypotheticalEnergyEVWhenCharging / maximumPowerEVChargingForNotCreatingANewPeak)*100
                    for helpCurrentHypotheticalTimeSlot in range (0, helpTimeSlotsToEndOfweek):
                        helpHypotheticalEnergyEVWhenCharging  = helpHypotheticalEnergyEVWhenCharging + (maximumPowerEVChargingForNotCreatingANewPeak *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 )
                        helpHypotheticalSOCWhenCharging  = (helpHypotheticalEnergyEVWhenCharging / SetUpScenarios.capacityMaximal_EV)*100

                    if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] >= SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection:
                        outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] = 0
                        print("Correction of the EV (End of the week). SOC too high. Time: " +  str(index_timeslot))
                    if helpHypotheticalSOCWhenCharging <= SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection * 0.5:
                        outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] =  maximumPowerEVChargingForNotCreatingANewPeak
                        if inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] > maximumPowerEVChargingForNotCreatingANewPeak:
                            outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] =  inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot]
                        print("Correction of the EV (End of the week). SOC too low. Time: " +  str(index_timeslot))


                #Calculate the simulation values with the corrected input vectors
                if index_timeslot >=1:
                    if overruleActions == False:
                        outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] = inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot]
                    simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot]  =simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot - 1] + (outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]  = (simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalSOCDropWithNoCharging_BT3 [index_week, index_BT3] = hypotheticalSOCDropWithNoCharging_BT3 [index_week, index_BT3] + (df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]/ SetUpScenarios.capacityMaximal_EV)*100

                if index_timeslot ==0:
                    if overruleActions == False:
                        outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] = inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot]
                    simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot]  = SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + (outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]  = (simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalSOCDropWithNoCharging_BT3 [index_week, index_BT3] = (df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]/ SetUpScenarios.capacityMaximal_EV)*100


                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT3_availabilityPattern [index_BT3, index_timeslot] = df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1]
                simulationInput_BT3_energyConsumptionOfTheEV [index_BT3, index_timeslot] = df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]
                simulationInput_BT3_electricityDemand [index_BT3, index_timeslot] =  df_buildingData ['Electricity [W]'] [index_timeslot + 1]


                simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3)
                simulationResult_RESGeneration_BT3 [index_week, index_BT3, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine
                simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] =  outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] + df_buildingData ['Electricity [W]'] [index_timeslot + 1]
                simulationResult_SurplusPower_BT3 [index_week, index_BT3, index_timeslot] = simulationResult_RESGeneration_BT3 [index_week, index_BT3, index_timeslot] - simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot]

                if simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] > simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]:
                    simulationResult_costs_BT3 [index_week, index_BT3, index_timeslot] = (simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] - simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] <= simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]:
                    simulationResult_costs_BT3 [index_week, index_BT3, index_timeslot] = (simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot] - simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)



                # Calculate number and degree of corrections (for statistical purposes)
                if inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] != outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot]:
                   correctingStats_BT3_chargingPowerEV_numberOfTimeSlots [index_week, index_BT3] +=1
                   correctingStats_BT3_chargingPowerEV_sumOfCorrections [index_week, index_BT3] = correctingStats_BT3_chargingPowerEV_sumOfCorrections [index_week, index_BT3] + abs(inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] - outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot] )
                   correctingStats_BT3_chargingPowerEV_profile [index_week, index_BT3, index_timeslot] = outputVector_BT3_chargingPowerEV_corrected [index_BT3, index_timeslot]  - inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot]




               #Calculate the constraint violation

                if  simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] < 0:
                    simulation_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3, index_timeslot] = simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]
                if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] >100:
                    simulation_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3, index_timeslot] =simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] - 100

                if inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] < 0:
                    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3, index_timeslot] = inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot]
                if inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] > SetUpScenarios.chargingPowerMaximal_EV:
                    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3, index_timeslot] = inputVector_BT3_chargingPowerEV [index_BT3, index_timeslot] - SetUpScenarios.chargingPowerMaximal_EV

                # Calculate the additional constraint violations of the internal controller

                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                   if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] > (SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection):
                        total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_BT3  [index_week, index_BT3] =  simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] - ((SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection))
                   if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] < (SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection):
                        total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_BT3  [index_week, index_BT3] = ((SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection)) - simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]

        #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] > (SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue):
                        total_ConstraintViolation_SOCOfTheEVLastValue_BT3  [index_week, index_BT3] =  simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] - ((SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue))
                    if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] < (SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue):
                        total_ConstraintViolation_SOCOfTheEVLastValue_BT3  [index_week, index_BT3] = ((SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue)) - simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]

                total_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3] =  total_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3] + abs(simulation_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3, index_timeslot])
                total_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3] = total_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3] + abs (simulation_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3, index_timeslot])

        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT3  [index_week, index_BT3, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT3  [index_week, index_BT3] = simulationObjective_surplusEnergyKWH_BT3  [index_week, index_BT3] + ((simulationResult_SurplusPower_BT3  [index_week, index_BT3, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] - simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]) > simulationObjective_maximumLoad_BT3 [index_week, index_BT3]:
                    simulationObjective_maximumLoad_BT3 [index_week, index_BT3] = simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] -  simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]
                if (simulationResult_PVGeneration_BT3  [index_week, index_BT3, index_timeslot] -  simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot]) > simulationObjective_maximumLoad_BT3 [index_week, index_BT3]:
                    simulationObjective_maximumLoad_BT3 [index_week, index_BT3] = simulationResult_PVGeneration_BT3  [index_week, index_BT3, index_timeslot] -   simulationResult_electricalLoad_BT3[index_week, index_BT3, index_timeslot]
                simulationObjective_costs_BT3  [index_week, index_BT3]  = simulationObjective_costs_BT3  [index_week, index_BT3] +  simulationResult_costs_BT3 [index_week, index_BT3, index_timeslot]





        #Building Type 4
        for index_BT4 in range (0, len(indexOfBuildingsOverall_BT4)):

            #Reading of the data

            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT4_mHP_MFH_1Minute_Weeks/HH" + str(indexOfBuildingsOverall_BT4[index_BT4]) + "/HH" + str(indexOfBuildingsOverall_BT4[index_BT4]) + "_Week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_Weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_Week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_Weeks/Outside_Temperature_1Minute_Week' +  str(currentweek) + '.csv', sep =";")


            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"

            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')


            #Round column
            df_buildingData['Electricity [W]'] = df_buildingData['Electricity [W]'].apply(lambda x: round(x, 2))

            #Wind generation
            indexBuildingForWindPowerAssignment =  SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1

            # Set up inital values for the simulation
            simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, 0] = SetUpScenarios.initialBufferStorageTemperature
            simulationResult_PVGeneration_BT4 [index_week, index_BT4, 0] = df_buildingData ['PV [nominal]'] [1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4)
            simulationResult_RESGeneration_BT4 [index_week, index_BT4, 0] = df_buildingData ['PV [nominal]'] [1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [1]  * SetUpScenarios.maximalPowerOfWindTurbine
            simulationResult_electricalLoad_BT4 [index_week, index_BT4, 0] = (inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, 0] ) * SetUpScenarios.electricalPower_HP + df_buildingData['Electricity [W]'] [1]
            simulationResult_SurplusPower_BT4 [index_week, index_BT4, 0] = simulationResult_RESGeneration_BT4 [index_week, index_BT4, 0] - simulationResult_electricalLoad_BT4 [index_week, index_BT4, 0]
            simulationResult_costs_BT4 [index_week, index_BT4, 0] = (simulationResult_electricalLoad_BT4 [index_week, index_BT4, 0] - simulationResult_PVGeneration_BT4 [index_week, index_BT4, 0]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [1]/3600000)


            helpCountNumberOfStartsIndividual_SpaceHeating =0
            helpCounterNumberOfRunningSlots_SpaceHeating =0
            helpCounterNumberOfStandBySlots_SpaceHeating =0

            startedHeatingHeatPump = False
            stoppedHeatingHeatPump = False

            helpCurrentPeakLoadOfTheweek =0

            numberOfHeatPumpStartsReachedSoftLimit = False
            numberOfHeatPumpStartsReachedHardLimit = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = False
            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = False

            heatingStartedPhysicalLimit_BufferStorage = False

            startedHeatingSpaceHeatingCorrection_end = False



            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):


                #Check how often the heat pump has been started so far
                if index_timeslot >= 2:

                    if outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot - 2] == 0 and outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot - 1] >0.001:
                        helpCountNumberOfStartsIndividual_SpaceHeating +=1
                        startedHeatingHeatPump = True
                        stoppedHeatingHeatPump = False


                    if (outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot - 2] > 0.01) and ( outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot - 1] ==0 ):
                        stoppedHeatingHeatPump = True
                        startedHeatingHeatPump = False
                        if lastHeatingAfterHeatPumpStartsReachedHardLimitStarted ==True:
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStopped = True

                #Update the currentNumberOfRunningSlots for the heat pump
                    if  outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot - 1] > 0.001:
                        helpCounterNumberOfRunningSlots_SpaceHeating +=1
                        helpCounterNumberOfStandBySlots_SpaceHeating =0
                    if  outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot - 1] == 0:
                        helpCounterNumberOfStandBySlots_SpaceHeating  +=1
                        helpCounterNumberOfRunningSlots_SpaceHeating =0


                if startedHeatingHeatPump == True and helpCounterNumberOfRunningSlots_SpaceHeating >=Run_Simulations.minimalRunTimeHeatPump:
                    startedHeatingHeatPump = False
                if stoppedHeatingHeatPump == True and helpCounterNumberOfStandBySlots_SpaceHeating >=Run_Simulations.minimalRunTimeHeatPump:
                    stoppedHeatingHeatPump = False

                if numberOfHeatPumpStartsReachedHardLimit == True:
                    numberOfHeatPumpStartsReachedSoftLimit = False

                # Pre-Corrections of input values: too high input values or too low
                if inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]  > 1:
                    inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]  =1
                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot]  =1
                    print("Pre-Corrections too high value Space Heating. Time: " +  str(index_timeslot) + "\n")

                if inputVector_BT4_heatGenerationCoefficientSpaceHeating[index_BT4, index_timeslot]  < 0:
                    inputVector_BT4_heatGenerationCoefficientSpaceHeating[index_BT4, index_timeslot]  =0
                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot]  =0


                # Pre-Corrections: Set small heating values to 0
                if inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] > 0 and inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] < 0.1:
                    inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] = 0


                # Pre-Corrections of input values: minimal modulation
                if inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] > 0.001 and inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP / 100:
                    print("Pre_Correction: Min Modulation. Time: " + str( index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]) + "\n")
                    inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP / 100




                if  simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts_BeforeConsideringMinimalRuntime:
                    numberOfHeatPumpStartsReachedSoftLimit = True

                if simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts - 2:
                    numberOfHeatPumpStartsReachedHardLimit = True
                    numberOfHeatPumpStartsReachedSoftLimit = False

                #Calculate the hypothetical simulation values if the non-corrected actions were applied
                cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


               # Calculate the maximum power of the heat pump and the EV for not creating a new peak load
                if index_timeslot >=1:
                    if (simulationResult_electricalLoad_BT4  [index_week, index_BT4, index_timeslot - 1] - simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_electricalLoad_BT4  [index_week, index_BT4, index_timeslot - 1] - simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot - 1]
                    if (simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot - 1] - simulationResult_electricalLoad_BT4  [index_week, index_BT4, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot - 1] - simulationResult_electricalLoad_BT4  [index_week, index_BT4, index_timeslot - 1]

                maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP_BT4_MFH
                maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP_BT4_MFH

                if (inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] ) * SetUpScenarios.electricalPower_HP_BT4_MFH  + df_buildingData ['Electricity [W]'] [index_timeslot + 1] > simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = helpCurrentPeakLoadOfTheweek - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = helpCurrentPeakLoadOfTheweek - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]

                if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek > SetUpScenarios.electricalPower_HP_BT4_MFH:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP_BT4_MFH
                if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek > SetUpScenarios.electricalPower_HP_BT4_MFH:
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP_BT4_MFH



                if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP_BT4_MFH:
                    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP_BT4_MFH
                if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP_BT4_MFH:
                    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek =Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP_BT4_MFH




                #Corrections due to violations of the temperature and volume constraints

                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    if inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] > 0.001 and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod < SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and (numberOfHeatPumpStartsReachedSoftLimit == False or stoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
                       outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                       print("Correction BufferStorage too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]) + "\n")
                    else:
                       outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 0
                       print("Correction BufferStorage too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]) + "\n")
                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected[index_BT4, index_timeslot] = 0
                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary :
                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP_BT4_MFH
                    print("Correction BufferStorage too low (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]) + "\n")


                # Corrections due to minimal modulation degree of the heat pump
                if inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] > 0.001 and inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP /100:
                    inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP /100
                    print("Correction Minimal Mod. SpaceHeating. Time: " +  str(index_timeslot) + "; ANN value: " + str(inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]) + "\n")




                #Calculate the hypothetical simulation values if the  corrected actions were applied
                cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))

                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))



                if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_BufferStorageTemperature_BT4 [index_week, index_BT4, index_timeslot] >= SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection  * 2:
                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 0
                if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_BufferStorageTemperature_BT4 [index_week, index_BT4, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection  * 2:
                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP_BT4_MFH



                #Corrections due to high number of starts of the heat pump

                #Soft Limit Reached --> Consider minimum runtimes and standbytimes of the heat pump
                if numberOfHeatPumpStartsReachedSoftLimit ==True  and startedHeatingSpaceHeatingCorrection_end ==False:
                    print("numberOfHeatPumpStartsReachedSoftLimit; Timeslot: ",index_timeslot)
                    if startedHeatingHeatPump == True:
                        print("numberOfHeatPumpStartsReachedSoftLimit; started HP")

                        if outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] > 0.01 and simulationResult_BufferStorageTemperature_BT4 [index_week, index_BT4, index_timeslot] <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                            outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] =  outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot]
                        elif outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] > 0.01 and simulationResult_BufferStorageTemperature_BT4 [index_week, index_BT4, index_timeslot] > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                            if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                            elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100
                                elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit :
                                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] =  0


                        if outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] ==0:
                            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                            if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                                outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = SetUpScenarios.minimalModulationdDegree_HP/100

                    elif stoppedHeatingHeatPump ==True:
                        print("numberOfHeatPumpStartsReachedSoftLimit; stopped HP")
                        outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 0


                # Last heating of the week if the numberOfHeatPumpStartsReachedHardLimit
                if numberOfHeatPumpStartsReachedHardLimit ==True and startedHeatingSpaceHeatingCorrection_end ==False:
                    print("numberOfHeatPumpStartsReachedHardLimit")
                    # Last heating of the week
                    if lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == False:
                        fractionOfweekLeft =1 - (index_timeslot / SetUpScenarios.numberOfTimeSlotsPerWeek)
                        currentSOCBufferStorage_CorrectionLimits =  (simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1] - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
                        differenceTargetValueEndAndUpperLimit_SpaceHeating = SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - (SetUpScenarios.initialBufferStorageTemperature)
                        possibleTargetTemperatureForLastHeating_SpaceHeating = SetUpScenarios.initialBufferStorageTemperature  + differenceTargetValueEndAndUpperLimit_SpaceHeating  * fractionOfweekLeft
                        if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1] < possibleTargetTemperatureForLastHeating_SpaceHeating:
                            outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP_BT4_MFH
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                        else:
                            outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 0


                    elif lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == True:
                        outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 0


                #Corrections for the violations of the physical limits of the storage systems
                if index_timeslot >0:
                    helpValue_BufferStorageTemperature_CorrectedModulationDegree = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                else:
                    helpValue_BufferStorageTemperature_CorrectedModulationDegree =  SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


                if heatingStartedPhysicalLimit_BufferStorage == True and numberOfHeatPumpStartsReachedHardLimit == True:
                    helpValue_BufferStorageTemperature_MediumModulationDegree = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((0.6 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    if helpValue_BufferStorageTemperature_MediumModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit and helpValue_BufferStorageTemperature_MediumModulationDegree <= SetUpScenarios.initialBufferStorageTemperature:
                            outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 0.6
                    elif helpValue_BufferStorageTemperature_MediumModulationDegree < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                        outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 1
                    elif helpValue_BufferStorageTemperature_MediumModulationDegree > SetUpScenarios.initialBufferStorageTemperature:
                        outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 0
                        heatingStartedPhysicalLimit_BufferStorage =False


                if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 0
                    print("Corrections Physical limit too high value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]) + "\n")

                if helpValue_BufferStorageTemperature_CorrectedModulationDegree <= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                    outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = 1
                    print("Corrections Physical limit too low value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]) + "\n")
                    heatingStartedPhysicalLimit_BufferStorage = True


                #Calculate the simulation values with the corrected input vectors
                if index_timeslot >=1:
                    if overruleActions == False:
                        outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]

                    simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                if index_timeslot ==0:
                    if overruleActions == False:
                        outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] = inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]
                    simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT4_SpaceHeating [index_BT4, index_timeslot] = df_buildingData['Space Heating [W]'] [index_timeslot + 1]
                simulationInput_BT4_electricityDemand [index_BT4, index_timeslot] = df_buildingData ['Electricity [W]'] [index_timeslot + 1]


                simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4)
                simulationResult_RESGeneration_BT4 [index_week, index_BT4, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine
                simulationResult_SurplusPower_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_RESGeneration_BT4 [index_week, index_BT4, index_timeslot] - simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot]
                simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] = (outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] ) * SetUpScenarios.electricalPower_HP_BT4_MFH + df_buildingData ['Electricity [W]'] [index_timeslot + 1]



                if simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] > simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]:
                    simulationResult_costs_BT4 [index_week, index_BT4, index_timeslot] = (simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] - simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] <= simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]:
                    simulationResult_costs_BT4 [index_week, index_BT4, index_timeslot] = (simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot] - simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)



                # Calculate number and degree of corrections (for statistical purposes)
                if inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] != outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot]:
                   correctingStats_BT4_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots [index_week, index_BT4] +=1
                   correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week, index_BT4] = correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week, index_BT4] + abs(inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] - outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] )
                   correctingStats_BT4_heatGenerationCoefficientSpaceHeating_profile [index_week, index_BT4, index_timeslot] = outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot]  - inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]

               #Calculate the constraint violation
                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] >SetUpScenarios.maximalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] -SetUpScenarios.maximalBufferStorageTemperature
                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] <SetUpScenarios.minimalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - SetUpScenarios.minimalBufferStorageTemperature

                if (inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] < SetUpScenarios.minimalModulationdDegree_HP/100) and (inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]>0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4, index_timeslot] = (SetUpScenarios.minimalModulationdDegree_HP/100) - inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot]

                if inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4, index_timeslot] + inputVector_BT4_heatGenerationCoefficientSpaceHeating [index_BT4, index_timeslot] -1


                # Calculate the additional constraint violations of the internal controller
                if  simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] >SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary
                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary
                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] >SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit
                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit


                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT4 [index_week, index_BT4] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection)
                    if  simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT4 [index_week, index_BT4] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection) - simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]



                #Count number of starts of the heat pump
                simulationResult_numberOfStartsHP_PerTimeslot_BT4[index_week, index_BT4, index_timeslot] = simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4]
                simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT4 [index_week, index_BT4, index_timeslot]= helpCounterNumberOfRunningSlots_SpaceHeating
                simulationResult_numberOfStandbySlotsHP_PerTimeslot_BT4[index_week, index_BT4, index_timeslot] = helpCounterNumberOfStandBySlots_SpaceHeating


                if simulationResult_numberOfRunningSlotsHP_PerTimeslot_BT4 [index_week, index_BT4, index_timeslot] >0:
                    simulationResult_isHPRunning_PerTimeslot_BT4 [index_week, index_BT4, index_timeslot] =1

                if index_timeslot >= 1:
                    if  outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot - 1] == 0 and outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected [index_BT4, index_timeslot] >0.0001 :
                        startedHeatingHeatPump = True
                        stoppedHeatingHeatPump = False
                        simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] += 1




                #Calculate the total additional constraint violations
                total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT4 [index_week, index_BT4] =  total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT4 [index_week, index_BT4] +  abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT4 [index_week, index_BT4, index_timeslot])
                total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT4 [index_week, index_BT4] =  total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT4 [index_week, index_BT4] +  abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT4 [index_week, index_BT4, index_timeslot])

                if Run_Simulations.considerMaxiumNumberOfStartsHP_MFH_Individual  == True:
                    if simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] > (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts:
                        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT4 [index_week, index_BT4]  = simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] - (Run_Simulations.maximumNumberOfStarts_Combined + 1) - Run_Simulations.additionalNumberOfAllowedStarts


            #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                total_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4] = total_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4] + abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4, index_timeslot])
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 [index_week, index_BT4] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue)
                    if  simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 [index_week, index_BT4] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue) - simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]

                total_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4] = total_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4] + abs(simulation_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4, index_timeslot])
                if Run_Simulations.considerMaxiumNumberOfStartsHP_MFH_Individual  == True:
                    if simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] > (Run_Simulations.maximumNumberOfStarts_Combined + 1):
                        total_ConstraintViolation_numberOfStarts_Individual_BT4 [index_week, index_BT4]  = simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] - (Run_Simulations.maximumNumberOfStarts_Combined + 1)


        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT4  [index_week, index_BT4, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT4  [index_week, index_BT4] = simulationObjective_surplusEnergyKWH_BT4  [index_week, index_BT4] + ((simulationResult_SurplusPower_BT4  [index_week, index_BT4, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] - simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]) > simulationObjective_maximumLoad_BT4 [index_week, index_BT4]:
                    simulationObjective_maximumLoad_BT4 [index_week, index_BT4] = simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] -  simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]
                if (simulationResult_PVGeneration_BT4  [index_week, index_BT4, index_timeslot] -  simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot]) > simulationObjective_maximumLoad_BT4 [index_week, index_BT4]:
                    simulationObjective_maximumLoad_BT4 [index_week, index_BT4] = simulationResult_PVGeneration_BT4  [index_week, index_BT4, index_timeslot] -   simulationResult_electricalLoad_BT4[index_week, index_BT4, index_timeslot]
                simulationObjective_costs_BT4  [index_week, index_BT4]  = simulationObjective_costs_BT4  [index_week, index_BT4] +  simulationResult_costs_BT4 [index_week, index_BT4, index_timeslot]





        #Building Type 5
        for index_BT5 in range (0, len(indexOfBuildingsOverall_BT5)):

            #Reading of the data

            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT5_BAT_SFH_1Minute_weeks/HH" + str(indexOfBuildingsOverall_BT5[index_BT5]) + "/HH" + str(indexOfBuildingsOverall_BT5[index_BT5]) + "_week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_weeks/Outside_Temperature_1Minute_week' +  str(currentweek) + '.csv', sep =";")

            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"

            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()



            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')



            #Wind generation

            indexBuildingForWindPowerAssignment = SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT5
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1

            #Round column and rename it
            df_buildingData['Electricity [W]'] = df_buildingData['Electricity [W]'].apply(lambda x: round(x, 2))


            # Set up inital values for the simulation
            simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, 0]= (SetUpScenarios.initialSOC_BAT/100) * SetUpScenarios.capacityMaximal_BAT
            simulationResult_SOCofBAT_BT5 [index_week, index_BT5, 0]= SetUpScenarios.initialSOC_BAT
            simulationResult_PVGeneration_BT5 [index_week, index_BT5, 0] = df_buildingData ['PV [nominal]'] [1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT5)
            simulationResult_RESGeneration_BT5 [index_week, index_BT5, 0] = df_buildingData ['PV [nominal]'] [1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT5)  + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [1] * SetUpScenarios.maximalPowerOfWindTurbine
            simulationResult_electricalLoad_BT5 [index_week, index_BT5, 0] =  inputVector_BT5_chargingPowerBAT[index_BT5, 0] - inputVector_BT5_disChargingPowerBAT[index_BT5, 0] + df_buildingData['Electricity [W]'] [1]
            simulationResult_SurplusPower_BT5 [index_week, index_BT5, 0] = simulationResult_RESGeneration_BT5 [index_week, index_BT5, 0] - simulationResult_electricalLoad_BT5 [index_week, index_BT5, 0]
            simulationResult_costs_BT5 [index_week, index_BT5, 0] = (simulationResult_electricalLoad_BT5 [index_week, index_BT5, 0] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, 0]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [1]/3600000)



            helpCurrentPeakLoadOfTheweek =0


            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):



                # Pre-Corrections too high values or too low
                if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] > SetUpScenarios.chargingPowerMaximal_BAT:
                    inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] = SetUpScenarios.chargingPowerMaximal_BAT
                    outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] = SetUpScenarios.chargingPowerMaximal_BAT

                if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] < 0:
                    inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] = 0
                    outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] = 0


                if inputVector_BT5_disChargingPowerBAT[index_BT5, index_timeslot] >  df_buildingData['Electricity [W]'] [index_timeslot + 1]:
                    inputVector_BT5_disChargingPowerBAT[index_BT5, index_timeslot] = df_buildingData['Electricity [W]'] [index_timeslot+ 1]
                    outputVector_BT5_disChargingPowerBAT_corrected[index_BT5, index_timeslot] = df_buildingData['Electricity [W]'] [index_timeslot + 1]

                if inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] > SetUpScenarios.chargingPowerMaximal_BAT:
                    testValue = inputVector_BT5_disChargingPowerBAT[index_BT5, index_timeslot]
                    inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] = SetUpScenarios.chargingPowerMaximal_BAT
                    outputVector_BT5_disChargingPowerBAT_corrected [index_BT5, index_timeslot] = SetUpScenarios.chargingPowerMaximal_BAT


                if inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] < -0.1:
                    inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] = 0
                    outputVector_BT5_disChargingPowerBAT_corrected [index_BT5, index_timeslot] = 0

                # Pre-Corrections: No charging and discharging of the BAT at the same timeslot
                if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] > 0.01 and inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] >0.01:
                    if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] >inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot]:
                            inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] = 0

                    if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] <=inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot]:
                        inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] = 0


                #Calculate the hypothetical simulation values if the non-corrected actions were applied
                if index_timeslot >=1:
                    if overruleActions == False:
                        outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] = inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot]
                    simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot]  =simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot - 1] + ((inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] * (SetUpScenarios.chargingEfficiency_BAT) - inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )
                    simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]  = (simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot] / SetUpScenarios.capacityMaximal_BAT)*100
                if index_timeslot ==0:
                    if overruleActions == False:
                        outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] = inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot]
                    simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot]  =(SetUpScenarios.initialSOC_BAT/100) * SetUpScenarios.capacityMaximal_BAT + ((inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] * (SetUpScenarios.chargingEfficiency_BAT) - inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )
                    simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]  = (simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot] / SetUpScenarios.capacityMaximal_BAT)*100


               # Calculate the maximum power of the BAT for not creating a new peak load
                if index_timeslot >=1:
                    if (simulationResult_electricalLoad_BT5  [index_week, index_BT5, index_timeslot - 1] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_electricalLoad_BT5  [index_week, index_BT5, index_timeslot - 1] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot - 1]
                    if (simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot - 1] - simulationResult_electricalLoad_BT5  [index_week, index_BT5, index_timeslot - 1]) > helpCurrentPeakLoadOfTheweek:
                        helpCurrentPeakLoadOfTheweek = simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot - 1] - simulationResult_electricalLoad_BT5  [index_week, index_BT5, index_timeslot - 1]

                maximumPowerBATChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_BAT

                if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] + df_buildingData ['Electricity [W]'] [index_timeslot + 1] > simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]:
                    maximumPowerBATChargingForNotCreatingANewPeak = helpCurrentPeakLoadOfTheweek  - df_buildingData ['Electricity [W]'] [index_timeslot + 1]  + simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]



                if  maximumPowerBATChargingForNotCreatingANewPeak >  SetUpScenarios.chargingPowerMaximal_BAT:
                    maximumPowerBATChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_BAT

                if  maximumPowerBATChargingForNotCreatingANewPeak < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection *  SetUpScenarios.chargingPowerMaximal_BAT:
                    maximumPowerBATChargingForNotCreatingANewPeak = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.chargingPowerMaximal_BAT


                #Corrections for the SOC of the BAT
                if simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] >  100.01:
                   outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] = 0
                   print("Correction of the BAT. SOC too high. Time: " +  str(index_timeslot))
                if simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] <  -0.01:
                   outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] = maximumPowerBATChargingForNotCreatingANewPeak
                   print("Correction of the BAT. SOC too low. Time: " +  str(index_timeslot))



                #Calculate the simulation values with the corrected input vectors
                if index_timeslot >=1:
                    if overruleActions == False:
                        outputVector_BT5_chargingPowerBAT_corrected[index_BT5, index_timeslot] = inputVector_BT5_chargingPowerBAT[index_BT5, index_timeslot]
                        outputVector_BT5_disChargingPowerBAT_corrected[index_BT5, index_timeslot] = inputVector_BT5_disChargingPowerBAT[index_BT5, index_timeslot]
                    simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot]  =simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot - 1] + ((outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot]  * (SetUpScenarios.chargingEfficiency_BAT) - outputVector_BT5_disChargingPowerBAT_corrected [index_BT5, index_timeslot] *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )
                    simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]  = (simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot] / SetUpScenarios.capacityMaximal_BAT)*100

                if index_timeslot ==0:
                    if overruleActions == False:
                        outputVector_BT5_chargingPowerBAT_corrected[index_BT5, index_timeslot] = inputVector_BT5_chargingPowerBAT[index_BT5, index_timeslot]
                        outputVector_BT5_disChargingPowerBAT_corrected[index_BT5, index_timeslot] = inputVector_BT5_disChargingPowerBAT[index_BT5, index_timeslot]
                    simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot]  =(SetUpScenarios.initialSOC_BAT/100) * SetUpScenarios.capacityMaximal_BAT + ((outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] * (SetUpScenarios.chargingEfficiency_BAT) - outputVector_BT5_disChargingPowerBAT_corrected [index_BT5, index_timeslot] *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )
                    simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]  = (simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot] / SetUpScenarios.capacityMaximal_BAT)*100

                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT5_electricityDemand [index_BT5, index_timeslot] =  df_buildingData ['Electricity [W]'] [index_timeslot + 1]


                simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT5)
                simulationResult_RESGeneration_BT5 [index_week, index_BT5, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT5) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine
                simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] =  outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] - outputVector_BT5_disChargingPowerBAT_corrected [index_BT5, index_timeslot] + df_buildingData ['Electricity [W]'] [index_timeslot + 1]
                simulationResult_SurplusPower_BT5 [index_week, index_BT5, index_timeslot] = simulationResult_RESGeneration_BT5 [index_week, index_BT5, index_timeslot] - simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot]

                if simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] > simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]:
                    simulationResult_costs_BT5 [index_week, index_BT5, index_timeslot] = (simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] <= simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]:
                    simulationResult_costs_BT5 [index_week, index_BT5, index_timeslot] = (simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot] - simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)



                # Calculate number and degree of corrections (for statistical purposes)
                if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] != outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot]:
                   correctingStats_BT5_chargingPowerBAT_numberOfTimeSlots [index_week, index_BT5] +=1
                   correctingStats_BT5_chargingPowerBAT_sumOfCorrections [index_week, index_BT5] = correctingStats_BT5_chargingPowerBAT_sumOfCorrections [index_week, index_BT5] + abs(inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] - outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot] )
                   correctingStats_BT5_chargingPowerBAT_profile [index_week, index_BT5, index_timeslot] = outputVector_BT5_chargingPowerBAT_corrected [index_BT5, index_timeslot]  - inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot]

                if inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] != outputVector_BT5_disChargingPowerBAT_corrected [index_BT5, index_timeslot]:
                   correctingStats_BT5_disChargingPowerBAT_numberOfTimeSlots [index_week, index_BT5] +=1
                   correctingStats_BT5_disChargingPowerBAT_sumOfCorrections [index_week, index_BT5] = correctingStats_BT5_disChargingPowerBAT_sumOfCorrections [index_week, index_BT5] + abs(inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] - outputVector_BT5_disChargingPowerBAT_corrected [index_BT5, index_timeslot] )
                   correctingStats_BT5_disChargingPowerBAT_profile [index_week, index_BT5, index_timeslot] = outputVector_BT5_disChargingPowerBAT_corrected [index_BT5, index_timeslot]  - inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot]


                #Calculate the constraint violation

                if  simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] < 0:
                    simulation_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]
                if simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] >100:
                    simulation_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] =simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] - 100

                if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] < 0:
                    simulation_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot]
                if inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] > SetUpScenarios.chargingPowerMaximal_BAT:
                    simulation_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = inputVector_BT5_chargingPowerBAT [index_BT5, index_timeslot] - SetUpScenarios.chargingPowerMaximal_BAT

                if inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] < 0:
                    simulation_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot]
                if inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] >df_buildingData ['Electricity [W]'] [index_timeslot + 1]:
                    simulation_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = inputVector_BT5_disChargingPowerBAT [index_BT5, index_timeslot] - df_buildingData ['Electricity [W]'] [index_timeslot + 1]


        #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] > (SetUpScenarios.initialSOC_BAT + SetUpScenarios.endSOC_BATAllowedDeviationFromInitalValueUpperLimit):
                        total_ConstraintViolation_SOCOfTheBATLastValue_BT5  [index_week, index_BT5] =  simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] - ((SetUpScenarios.initialSOC_BAT + SetUpScenarios.endSOC_BATAllowedDeviationFromInitalValueUpperLimit))
                    if simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] < (SetUpScenarios.initialSOC_BAT - SetUpScenarios.endSOC_BATAllowedDeviationFromInitalValueLowerLimit):
                        total_ConstraintViolation_SOCOfTheBATLastValue_BT5  [index_week, index_BT5] = ((SetUpScenarios.initialSOC_BAT - SetUpScenarios.endSOC_BATAllowedDeviationFromInitalValueLowerLimit)) - simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]

                total_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5] =  total_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5] + round(abs(simulation_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5, index_timeslot]),3)
                total_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5] = total_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5] + round(abs (simulation_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot]),3)
                total_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5] = total_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5] + round(abs (simulation_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot]),3)


        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT5  [index_week, index_BT5, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT5  [index_week, index_BT5] = simulationObjective_surplusEnergyKWH_BT5  [index_week, index_BT5] + ((simulationResult_SurplusPower_BT5  [index_week, index_BT5, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]) > simulationObjective_maximumLoad_BT5 [index_week, index_BT5]:
                    simulationObjective_maximumLoad_BT5 [index_week, index_BT5] = simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] -  simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]
                if (simulationResult_PVGeneration_BT5  [index_week, index_BT5, index_timeslot] -  simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot]) > simulationObjective_maximumLoad_BT5 [index_week, index_BT5]:
                    simulationObjective_maximumLoad_BT5 [index_week, index_BT5] = simulationResult_PVGeneration_BT5  [index_week, index_BT5, index_timeslot] -   simulationResult_electricalLoad_BT5[index_week, index_BT5, index_timeslot]
                simulationObjective_costs_BT5  [index_week, index_BT5]  = simulationObjective_costs_BT5  [index_week, index_BT5] +  simulationResult_costs_BT5 [index_week, index_BT5, index_timeslot]




        # Calculate values for all buildings combined
        for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
            for index_BT1 in range (0, len(indexOfBuildingsOverall_BT1)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT1 [index_week, index_BT1, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]
            for index_BT2 in range (0, len(indexOfBuildingsOverall_BT2)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT2 [index_week, index_BT2, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]
            for index_BT3 in range (0, len(indexOfBuildingsOverall_BT3)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT3 [index_week, index_BT3, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]
            for index_BT4 in range (0, len(indexOfBuildingsOverall_BT4)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT4 [index_week, index_BT4, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]
            for index_BT5 in range (0, len(indexOfBuildingsOverall_BT5)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT5 [index_week, index_BT5, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]



            if simulationResult_electricalLoad_combined [index_week,index_timeslot] > simulationResult_PVGeneration_combined [index_week, index_timeslot]:
               simulationResult_costs_combined [index_week, index_timeslot] = (simulationResult_electricalLoad_combined [index_week, index_timeslot] - simulationResult_PVGeneration_combined [index_week, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
            if simulationResult_electricalLoad_combined [index_week, index_timeslot] <= simulationResult_PVGeneration_combined [index_week, index_timeslot]:
               simulationResult_costs_combined [index_week, index_timeslot] = (simulationResult_PVGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)


            #Calculate the objectives for all buidlings combined
            if simulationResult_RESGeneration_combined [index_week, index_timeslot] > simulationResult_electricalLoad_combined [index_week,index_timeslot]:
                simulationObjective_surplusEnergy_kWh_combined [index_week] =  simulationObjective_surplusEnergy_kWh_combined [index_week] +  (simulationResult_RESGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week,index_timeslot]) * ((SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                simulationResult_SurplusEnergy_combined [index_week, index_timeslot] = (simulationResult_RESGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week,index_timeslot]) * ((SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
            simulationObjective_costs_Euro_combined [index_week] =simulationObjective_costs_Euro_combined [index_week] + simulationResult_costs_combined [index_week, index_timeslot]
            if (simulationResult_electricalLoad_combined [index_week, index_timeslot]  > simulationResult_PVGeneration_combined [index_week, index_timeslot]) and (simulationResult_electricalLoad_combined [index_week, index_timeslot]  - simulationResult_PVGeneration_combined [index_week, index_timeslot])> simulationObjective_maximumLoad_kW_combined [index_week]:
                simulationObjective_maximumLoad_kW_combined [index_week] = simulationResult_electricalLoad_combined [index_week, index_timeslot]  - simulationResult_PVGeneration_combined [index_week, index_timeslot]
            if (simulationResult_electricalLoad_combined [index_week, index_timeslot]  <= simulationResult_PVGeneration_combined [index_week, index_timeslot]) and ( simulationResult_PVGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week, index_timeslot])> simulationObjective_maximumLoad_kW_combined [index_week]:
                simulationObjective_maximumLoad_kW_combined [index_week] = simulationResult_PVGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week, index_timeslot]



           #Calculate the combined score
            if Run_Simulations.optimization_1Objective == True:

               if Run_Simulations.optimizationGoal_minimizeSurplusEnergy == True:
                   simulationObjective_combinedScore_combined [index_week] = simulationObjective_surplusEnergy_kWh_combined [index_week]
               if Run_Simulations.optimizationGoal_minimizePeakLoad == True:
                   simulationObjective_combinedScore_combined [index_week] = simulationObjective_maximumLoad_kW_combined [index_week]
               if Run_Simulations.optimizationGoal_minimizeCosts == True:
                  simulationObjective_combinedScore_combined [index_week] = simulationObjective_costs_Euro_combined [index_week]

            if Run_Simulations.optimization_2Objective == True:

               if (Run_Simulations.optimizationGoal_minimizeSurplusEnergy == True and Run_Simulations.optimizationGoal_minimizePeakLoad == True):
                   simulationObjective_combinedScore_combined [index_week] = Run_Simulations.objective_minimizePeakLoad_weight*(simulationObjective_maximumLoad_kW_combined [index_week]/Run_Simulations.objective_minimizePeakLoad_normalizationValue) + Run_Simulations.objective_minimizeSurplusEnergy_weight * (simulationObjective_surplusEnergy_kWh_combined/Run_Simulations.objective_minimizeSurplusEnergy_normalizationValue)
               if (Run_Simulations.optimizationGoal_minimizeSurplusEnergy == True and Run_Simulations.optimizationGoal_minimizeCosts == True):
                   simulationObjective_combinedScore_combined [index_week] = Run_Simulations.objective_minimizeCosts_weight *(simulationObjective_costs_Euro_combined [index_week]/Run_Simulations.objective_minimizeCosts_normalizationValue) + Run_Simulations.objective_minimizeSurplusEnergy_weight * (simulationObjective_surplusEnergy_kWh_combined/Run_Simulations.objective_minimizeSurplusEnergy_normalizationValue)
               if (Run_Simulations.optimizationGoal_minimizePeakLoad == True and Run_Simulations.optimizationGoal_minimizeCosts == True):
                   simulationObjective_combinedScore_combined [index_week] = Run_Simulations.objective_minimizeCosts_weight *(simulationObjective_costs_Euro_combined [index_week]/Run_Simulations.objective_minimizeCosts_normalizationValue) +  Run_Simulations.objective_minimizeCosts_weight *(simulationObjective_costs_Euro_combined [index_week]/Run_Simulations.objective_minimizeCosts_normalizationValue)

            if Run_Simulations.optimization_3Objectives == True:
                simulationObjective_combinedScore_combined [index_week] = Run_Simulations.objective_minimizePeakLoad_weight*(simulationObjective_maximumLoad_kW_combined [index_week]/Run_Simulations.objective_minimizePeakLoad_normalizationValue) + Run_Simulations.objective_minimizeSurplusEnergy_weight * (simulationObjective_surplusEnergy_kWh_combined/Run_Simulations.objective_minimizeSurplusEnergy_normalizationValue) + Run_Simulations.objective_minimizeCosts_weight *(simulationObjective_costs_Euro_combined [index_week]/Run_Simulations.objective_minimizeCosts_normalizationValue)

    #Convert and round values of the objectives
    simulationObjective_maximumLoad_kW_combined [index_week] = simulationObjective_maximumLoad_kW_combined [index_week]  /1000
    simulationObjective_maximumLoad_kW_combined [index_week]  = round(simulationObjective_maximumLoad_kW_combined [index_week],2)
    simulationObjective_costs_Euro_combined [index_week] =  simulationObjective_costs_Euro_combined [index_week] /100
    simulationObjective_costs_Euro_combined [index_week] =  round(simulationObjective_costs_Euro_combined [index_week],2)
    simulationObjective_surplusEnergy_kWh_combined [index_week] =  round(simulationObjective_surplusEnergy_kWh_combined [index_week],2)

    #Calculate constraint violation for all buildings combined
    for index_BT1 in range (0, len(indexOfBuildingsOverall_BT1)):
        total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1]
        total_ConstraintViolation_DHWTankRange_combined [index_week] = total_ConstraintViolation_DHWTankRange_combined [index_week] + total_ConstraintViolation_DHWTankRange_BT1 [index_week, index_BT1]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] +  total_ConstraintViolation_BufferStorageTemperatureLastValue_BT1 [index_week, index_BT1]
        total_ConstraintViolation_DHWTankLastValue_combined [index_week] = total_ConstraintViolation_DHWTankLastValue_combined [index_week] + total_ConstraintViolation_DHWTankLastValue_BT1 [index_week, index_BT1]
        total_ConstraintViolation_OnlyOneStorage_combined [index_week] = total_ConstraintViolation_OnlyOneStorage_combined [index_week] + total_ConstraintViolation_OnlyOneStorage_BT1 [index_week, index_BT1]
        total_ConstraintViolation_MinimalModulationDegree_combined [index_week] = total_ConstraintViolation_MinimalModulationDegree_combined [index_week] + total_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1]
        total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week]  = total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] + total_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1]
        total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week]  = total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] + total_ConstraintViolation_SOCOfTheEVLastValue_BT1 [index_week, index_BT1]
        total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] = total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] +total_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1]
        total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] = total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] + total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]
        total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] = total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] + total_ConstraintViolation_numberOfStarts_Combined_BT1 [index_week, index_BT1]
        hypotheticalSOCDropWithNoCharging_combined [index_week] = hypotheticalSOCDropWithNoCharging_combined [index_week] +  hypotheticalSOCDropWithNoCharging_BT1 [index_week, index_BT1]
        # Additional Constraint Violations of the internal controller
        total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT1 [index_week, index_BT1]
        total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_DHWTankRange_CorrectionLimit_BT1 [index_week, index_BT1]
        total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week]  + total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT1 [index_week, index_BT1]
        total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week] =  total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week] + total_ConstraintViolation_DHWTankRange_PhysicalLimit_BT1 [index_week, index_BT1]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT1 [index_week, index_BT1]
        total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_BT1 [index_week, index_BT1]
        total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week] =  total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week]  + total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_BT1 [index_week, index_BT1]
        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined [index_week] = total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined [index_week]  + total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT1 [index_week, index_BT1]
        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week] = total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week]  + total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_BT1 [index_week, index_BT1]

    for index_BT2 in range (0, len(indexOfBuildingsOverall_BT2)):
        total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2]
        total_ConstraintViolation_DHWTankRange_combined [index_week] = total_ConstraintViolation_DHWTankRange_combined [index_week] + total_ConstraintViolation_DHWTankRange_BT2 [index_week, index_BT2]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] +  total_ConstraintViolation_BufferStorageTemperatureLastValue_BT2 [index_week, index_BT2]
        total_ConstraintViolation_DHWTankLastValue_combined [index_week] = total_ConstraintViolation_DHWTankLastValue_combined [index_week] + total_ConstraintViolation_DHWTankLastValue_BT2 [index_week, index_BT2]
        total_ConstraintViolation_OnlyOneStorage_combined [index_week] = total_ConstraintViolation_OnlyOneStorage_combined [index_week] + total_ConstraintViolation_OnlyOneStorage_BT2 [index_week, index_BT2]
        total_ConstraintViolation_MinimalModulationDegree_combined [index_week] = total_ConstraintViolation_MinimalModulationDegree_combined [index_week] + total_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2]
        total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] = total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] + total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]
        total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] = total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] + total_ConstraintViolation_numberOfStarts_Combined_BT2 [index_week, index_BT2]
        # Additional Constraint Violations of the internal controller
        total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT2 [index_week, index_BT2]
        total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_DHWTankRange_CorrectionLimit_BT2 [index_week, index_BT2]
        total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week]  + total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT2 [index_week, index_BT2]
        total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week] =  total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week] + total_ConstraintViolation_DHWTankRange_PhysicalLimit_BT2 [index_week, index_BT2]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_BT2 [index_week, index_BT2]
        total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_BT2 [index_week, index_BT2]
        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined [index_week] = total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined [index_week]  + total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT2 [index_week, index_BT2]
        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week] = total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week]  + total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_BT2 [index_week, index_BT2]
    for index_BT3 in range (0, len(indexOfBuildingsOverall_BT3)):
        total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week]  = total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] + total_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3]
        total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week]  = total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] + total_ConstraintViolation_SOCOfTheEVLastValue_BT3 [index_week, index_BT3]
        total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] = total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] +total_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3]
        hypotheticalSOCDropWithNoCharging_combined [index_week] = hypotheticalSOCDropWithNoCharging_combined [index_week] +  hypotheticalSOCDropWithNoCharging_BT3 [index_week, index_BT3]
         # Additional Constraint Violations of the internal controller
        total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week] =  total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week]  + total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_BT3 [index_week, index_BT3]
    for index_BT4 in range (0, len(indexOfBuildingsOverall_BT4)):
        total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] +  total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 [index_week, index_BT4]
        total_ConstraintViolation_MinimalModulationDegree_combined [index_week] = total_ConstraintViolation_MinimalModulationDegree_combined [index_week] + total_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4]
        total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] = total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] + total_ConstraintViolation_numberOfStarts_Individual_BT4 [index_week, index_BT4]
        # Additional Constraint Violations of the internal controller
        total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_BT4 [index_week, index_BT4]
        total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week]  + total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_BT4 [index_week, index_BT4]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 [index_week, index_BT4]
        total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined [index_week] = total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined [index_week]  + total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_BT4 [index_week, index_BT4]
    for index_BT5 in range (0, len(indexOfBuildingsOverall_BT5)):
        total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week]  = total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week] + total_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5]
        total_ConstraintViolation_SOCOfTheBATLastValue_combined [index_week]  = total_ConstraintViolation_SOCOfTheBATLastValue_combined [index_week] + total_ConstraintViolation_SOCOfTheBATLastValue_BT5 [index_week, index_BT5]
        total_ConstraintViolation_ChargingPowerOfTheBAT_combined [index_week] = total_ConstraintViolation_ChargingPowerOfTheBAT_combined [index_week] + total_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5] + total_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5]




   #Print results (constraint violations and objectives)
    print("")
    print("Results for week " + str(currentweek) )
    print("")
    print("Constraint violations:"+"\n")
    if total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] > 0.01:
       print ("total_ConstraintViolation_BufferStorageTemperatureRange_combined: " + str(round(total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_DHWTankRange_combined [index_week] >0.1:
       print("total_ConstraintViolation_DHWTankRange_combined: " + str(round(total_ConstraintViolation_DHWTankRange_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] >0.01:
       print("total_ConstraintViolation_BufferStorageTemperatureLastValue_combined: ", str(round(total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_DHWTankLastValue_combined [index_week] >0.1:
       print("total_ConstraintViolation_DHWTankLastValue_combined: ", str(round(total_ConstraintViolation_DHWTankLastValue_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_OnlyOneStorage_combined [index_week] >0.1:
       print("total_ConstraintViolation_OnlyOneStorage_combined: " + str(round(total_ConstraintViolation_OnlyOneStorage_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_MinimalModulationDegree_combined [index_week] >0.2:
       print("total_ConstraintViolation_MinimalModulationDegree_combined: " + str(round(total_ConstraintViolation_MinimalModulationDegree_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] >0.1:
       print("total_ConstraintViolation_SOCOfTheEV_combined: " + str(round(total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] >0.1:
       print("total_ConstraintViolation_SOCOfTheEVLastValue_combined: " + str(round(total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] >1:
       print("total_ConstraintViolation_ChargingPowerOfTheEV_combined: " + str(round(total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] >0.01:
       print("total_ConstraintViolation_numberOfStarts_Individual_combined: " + str(round(total_ConstraintViolation_numberOfStarts_Individual_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] >0.01:
       print("total_ConstraintViolation_numberOfStarts_Combined_combined: " + str(round(total_ConstraintViolation_numberOfStarts_Combined_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week] >1:
       print("total_ConstraintViolation_SOCRangeOfTheBAT_combined: " + str(round(total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCOfTheBATLastValue_combined [index_week] >0.01:
       print("total_ConstraintViolation_SOCOfTheBATLastValue_combined: " + str(round(total_ConstraintViolation_SOCOfTheBATLastValue_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_ChargingPowerOfTheBAT_combined [index_week] >0.01:
       print("total_ConstraintViolation_ChargingPowerOfTheBAT_combined: " + str(round(total_ConstraintViolation_ChargingPowerOfTheBAT_combined [index_week], 2)) + "\n")



    print("Additional constraint violations:" +"\n")
    if total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] > 0.01:
        print("total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined: " + str(round(total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week] > 0.1:
        print("total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined: " + str(round(total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week] > 0.01:
        print("total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined: " + str(round(total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week] > 0.05:
        print("total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined: " + str(round(total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week] > 0.01:
        print("total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined: " + str(round(total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week] > 0.1:
        print("total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined: " + str(round(total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week] > 0.1:
        print("total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined: " + str(round(total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined [index_week] > 0.01:
        print("total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined: " + str(round(total_ConstraintViolation_numberOfStarts_CorrectionLimit_Individual_Combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week] > 0.01:
        print("total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined: " + str(round(total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week], 2)) + "\n")

    print("")
    print("Objectives" + "\n" + "\n")
    print("Consider objective Surplus Energy: " + str(Run_Simulations.optimizationGoal_minimizeSurplusEnergy))
    print("Consider objective Peak Load: " + str(Run_Simulations.optimizationGoal_minimizePeakLoad))
    print("Consider objective Costs: " + str(Run_Simulations.optimizationGoal_minimizeCosts) + "\n")
    print("Objective Surplus Energy [kWh]: " + str(round(simulationObjective_surplusEnergy_kWh_combined [index_week], 2)) )
    print("Objective Peak Load [kW]: " + str(round(simulationObjective_maximumLoad_kW_combined [index_week], 2)))
    print("Objective Costs [Euro]: " + str(round(simulationObjective_costs_Euro_combined [index_week], 2)) )
    print("Objective Score: " + str(round(simulationObjective_combinedScore_combined [index_week]/100, 2)))
    print("")



    #Calculate the negative score due to constraint violations


    #total_ConstraintViolation_BufferStorageTemperatureRange_combined
    averageDeviationPerTimeSlot_BufferStorageTemperatureRange_combined = total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] / SetUpScenarios.numberOfTimeSlotsPerWeek
    allowedTemperatureRange = SetUpScenarios.maximalBufferStorageTemperature - SetUpScenarios.minimalBufferStorageTemperature
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] = ((100/allowedTemperatureRange) * averageDeviationPerTimeSlot_BufferStorageTemperatureRange_combined)/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_DHWTankRange_combined
    averageDeviationPerTimeSlot_DHWTankRange_combined = total_ConstraintViolation_DHWTankRange_combined [index_week]  / SetUpScenarios.numberOfTimeSlotsPerWeek
    allowedVolumeRange = SetUpScenarios.maximumCapacityDHWTankOptimization -  SetUpScenarios.minimumCapacityDHWTankOptimization
    negativeScore_total_ConstraintViolation_DHWTankRange_combined [index_week] = ((100/allowedVolumeRange) * averageDeviationPerTimeSlot_DHWTankRange_combined)/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_BufferStorageTemperatureLastValue_combined
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] = ((100/allowedTemperatureRange) * total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week])/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_DHWTankLastValue_combined
    negativeScore_total_ConstraintViolation_DHWTankLastValue_combined [index_week] = ((100/allowedVolumeRange) * total_ConstraintViolation_DHWTankLastValue_combined [index_week])/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_SOCOfTheEV_combined
    negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] = (total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week])/SetUpScenarios.numberOfBuildings_Total
    if np.isnan(negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week]) == True:
        negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] =0


    #total_ConstraintViolation_SOCOfTheEVLastValue_combined
    if hypotheticalSOCDropWithNoCharging_combined [index_week] == 0:
        negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] =0
    else:
        negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] = (100/hypotheticalSOCDropWithNoCharging_combined [index_week])* (total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week])
        if np.isnan(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week]) == True:
            negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] =0

    #total_ConstraintViolation_SOCOfTheBAT_combined
    negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week] = (total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week])/SetUpScenarios.numberOfBuildings_Total
    if np.isnan(negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week]) == True:
        negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week] =0

    #total_ConstraintViolation_numberOfStarts_Combined_combined
    negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] = (total_ConstraintViolation_numberOfStarts_Combined_combined [index_week])/SetUpScenarios.numberOfBuildings_Total


    #total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined
    averageDeviationPerTimeSlot_BufferStorageTemperatureRange_CorrectionLimit_Combined = total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] / SetUpScenarios.numberOfTimeSlotsPerWeek
    allowedTemperatureRange_CorrectionLimit = SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week] = ((100/allowedTemperatureRange_CorrectionLimit) * averageDeviationPerTimeSlot_BufferStorageTemperatureRange_CorrectionLimit_Combined)/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined
    averageDeviationPerTimeSlot_DHWTankRange_CorrectionLimit_Combined  = total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined / SetUpScenarios.numberOfTimeSlotsPerWeek
    allowedVolumeRange_CorrectionLimit = SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary
    negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week] = ((100/allowedVolumeRange_CorrectionLimit) * averageDeviationPerTimeSlot_DHWTankRange_CorrectionLimit_Combined)/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined
    averageDeviationPerTimeSlot_BufferStorageTemperatureRange_PhysicalLimit_Combined = total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week] / SetUpScenarios.numberOfTimeSlotsPerWeek
    allowedTemperatureRange_PhysicalLimit = SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit - SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week] = ((100/allowedTemperatureRange_PhysicalLimit) * averageDeviationPerTimeSlot_BufferStorageTemperatureRange_PhysicalLimit_Combined)/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined
    averageDeviationPerTimeSlot_DHWTankRange_PhysicalLimit_Combined = total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week] / SetUpScenarios.numberOfTimeSlotsPerWeek
    allowedVolumeRange_PhysicalLimit = SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit - SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit
    negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week] = ((100/allowedVolumeRange_PhysicalLimit) * averageDeviationPerTimeSlot_DHWTankRange_PhysicalLimit_Combined)/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week] = ((100/allowedTemperatureRange_CorrectionLimit) * total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week])/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined
    negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined  [index_week] = ((100/allowedVolumeRange_CorrectionLimit) * total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week] )/SetUpScenarios.numberOfBuildings_Total


    #total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined
    if hypotheticalSOCDropWithNoCharging_combined [index_week] == 0:
        negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week] =0
    else:
        negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week] = (100/hypotheticalSOCDropWithNoCharging_combined [index_week])* (total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week])
        if np.isnan(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week]) == True:
            negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week] =0


    #total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined
    negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined  [index_week] = (total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week])/SetUpScenarios.numberOfBuildings_Total

    #total negative score
    negativeScore_total_overall [index_week] = Run_Simulations.weight_total_ConstraintViolation_BufferStorageTemperatureRange_combined * negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined * negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_DHWTankRange_combined * negativeScore_total_ConstraintViolation_DHWTankRange_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_DHWTankLastValue_combined * negativeScore_total_ConstraintViolation_DHWTankLastValue_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_SOCRangeOfTheEV_combined * negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_SOCOfTheEVLastValue_combined * negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_numberOfStarts_Combined_combined * negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined * negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week]  + Run_Simulations.weight_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined * negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week]  + Run_Simulations.weight_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined * negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week]  + Run_Simulations.weight_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined * negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week]  + Run_Simulations.weight_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined * negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week]  + Run_Simulations.weight_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined * negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week] + negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined * negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_SOCRangeOfTheBAT_combined * negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week]

    print("")
    print("Negative Scores")
    print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined: ", round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_DHWTankRange_combined: ", round(negativeScore_total_ConstraintViolation_DHWTankRange_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_DHWTankLastValue_combined: ",round(negativeScore_total_ConstraintViolation_DHWTankLastValue_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined: ",round(negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week], 2))
    print("negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined: ",round(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined: ",round(negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined: ",round(negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week], 2))
    print("")
    print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined: ",round(negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined: ",round(negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week], 3))
    print("")
    print("negativeScore_total_overall: ",round(negativeScore_total_overall [index_week], 3))



    #Write result data into files

    #Create folder for the week
    pathForCreatingTheResultDataWithweek = pathForCreatingTheResultData + "/Week" + str(currentweek)

    try:
        os.makedirs(pathForCreatingTheResultDataWithweek)
    except OSError:
        print ("Creation of the directory %s failed" % pathForCreatingTheResultDataWithweek)


    #BT1
    for i in range (0, SetUpScenarios.numberOfBuildings_BT1):
        df_resultingProfiles_BT1 = pd.DataFrame({'heatGenerationCoefficientSpaceHeating': outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected[i, :],'heatGenerationCoefficientDHW': outputVector_BT1_heatGenerationCoefficientDHW_corrected[i, :],'chargingPowerEV': outputVector_BT1_chargingPowerEV_corrected[i, :], 'temperatureBufferStorage': simulationResult_BufferStorageTemperature_BT1[0,i, :], 'usableVolumeDHWTank': simulationResult_UsableVolumeDHW_BT1[0,i, :], 'simulationResult_SOCofEV': simulationResult_SOCofEV_BT1[0,i, :], 'simulationResult_energyLevelOfEV': simulationResult_energyLevelOfEV_BT1[0,i, :], 'simulationResult_PVGeneration': simulationResult_PVGeneration_BT1[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT1[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT1[0,i, :], 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT1[0,i, :], 'simulationResult_costs': simulationResult_costs_BT1[0,i, :], 'Space Heating [W]': simulationInput_BT1_SpaceHeating [i, :], 'DHW [W]': simulationInput_BT1_DHW [i, :], 'Electricity [W]': simulationInput_BT1_electricityDemand [i, :], 'Availability of the EV': simulationInput_BT1_availabilityPattern [i, :],'Energy Consumption of the EV':simulationInput_BT1_energyConsumptionOfTheEV [i, :], 'Outside Temperature [C]': df_outsideTemperatureData['Temperature [C]'], 'Price [Cent/kWh]': df_priceData['Price [Cent/kWh]'], 'COP (Space Heating)': cop_heatPump_SpaceHeating [:], 'COP (DHW)': cop_heatPump_DHW [:], 'numberOfStarts_HP': simulationResult_numberOfStartsHP_PerTimeslot_BT1[0,i, :],  'HP_isRunning': simulationResult_isHPRunning_PerTimeslot_BT1 [0,i, :]})

        #Round values
        df_resultingProfiles_BT1 ['heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_BT1 ['heatGenerationCoefficientSpaceHeating'].round(2)
        df_resultingProfiles_BT1 ['heatGenerationCoefficientDHW'] = df_resultingProfiles_BT1 ['heatGenerationCoefficientDHW'].round(2)
        df_resultingProfiles_BT1 ['chargingPowerEV'] = df_resultingProfiles_BT1 ['chargingPowerEV'].round(2)
        df_resultingProfiles_BT1 ['temperatureBufferStorage'] = df_resultingProfiles_BT1 ['temperatureBufferStorage'].round(2)
        df_resultingProfiles_BT1 ['usableVolumeDHWTank'] = df_resultingProfiles_BT1 ['usableVolumeDHWTank'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_SOCofEV'] = df_resultingProfiles_BT1 ['simulationResult_SOCofEV'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_energyLevelOfEV'] = (df_resultingProfiles_BT1 ['simulationResult_energyLevelOfEV']/3600000).round(2)
        df_resultingProfiles_BT1 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT1 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT1 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_costs'] = df_resultingProfiles_BT1 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT1 ['simulationResult_RESGeneration'].round(2)

        df_resultingProfiles_BT1 ['simulationResult_SurplusPower'] = df_resultingProfiles_BT1 ['simulationResult_SurplusPower'].round(2)
        df_resultingProfiles_BT1 ['Space Heating [W]'] = df_resultingProfiles_BT1 ['Space Heating [W]'].round(1)
        df_resultingProfiles_BT1 ['DHW [W]'] = df_resultingProfiles_BT1 ['DHW [W]'].round(1)
        df_resultingProfiles_BT1 ['Electricity [W]'] = df_resultingProfiles_BT1 ['Electricity [W]'].round(1)
        df_resultingProfiles_BT1 ['Outside Temperature [C]'] = df_resultingProfiles_BT1 ['Outside Temperature [C]'].round(2)
        df_resultingProfiles_BT1 ['Price [Cent/kWh]'] = df_resultingProfiles_BT1 ['Price [Cent/kWh]'].round(2)
        df_resultingProfiles_BT1 ['COP (Space Heating)'] = df_resultingProfiles_BT1 ['COP (Space Heating)'].round(2)
        df_resultingProfiles_BT1 ['COP (DHW)'] = df_resultingProfiles_BT1 ['COP (DHW)'].round(2)

        df_resultingProfiles_BT1.index.name = 'timeslot'
        df_resultingProfiles_BT1.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT1), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT1.to_csv(pathForCreatingTheResultDataWithweek + "/BT1_HH" + str(i + 1) + ".csv", index=True,  sep =";")



    #BT2
    for i in range (0, SetUpScenarios.numberOfBuildings_BT2):
        df_resultingProfiles_BT2 = pd.DataFrame({'heatGenerationCoefficientSpaceHeating': outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected[i, :],'heatGenerationCoefficientDHW': outputVector_BT2_heatGenerationCoefficientDHW_corrected[i, :], 'temperatureBufferStorage': simulationResult_BufferStorageTemperature_BT2[0,i, :], 'usableVolumeDHWTank': simulationResult_UsableVolumeDHW_BT2[0,i, :],  'simulationResult_PVGeneration': simulationResult_PVGeneration_BT2[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT2[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT2[0,i, :], 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT2[0,i, :], 'simulationResult_costs': simulationResult_costs_BT2[0,i, :], 'Space Heating [W]': simulationInput_BT2_SpaceHeating [i, :], 'DHW [W]': simulationInput_BT2_DHW [i, :], 'Electricity [W]': simulationInput_BT2_electricityDemand [i, :], 'Outside Temperature [C]': df_outsideTemperatureData['Temperature [C]'], 'Price [Cent/kWh]': df_priceData['Price [Cent/kWh]'], 'COP (Space Heating)': cop_heatPump_SpaceHeating [:], 'COP (DHW)': cop_heatPump_DHW [:], 'numberOfStarts_HP': simulationResult_numberOfStartsHP_PerTimeslot_BT2[0,i, :],  'HP_isRunning': simulationResult_isHPRunning_PerTimeslot_BT2 [0,i, :]})

        #Round values
        df_resultingProfiles_BT2 ['heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_BT2 ['heatGenerationCoefficientSpaceHeating'].round(2)
        df_resultingProfiles_BT2 ['heatGenerationCoefficientDHW'] = df_resultingProfiles_BT2 ['heatGenerationCoefficientDHW'].round(2)
        df_resultingProfiles_BT2 ['temperatureBufferStorage'] = df_resultingProfiles_BT2 ['temperatureBufferStorage'].round(2)
        df_resultingProfiles_BT2 ['usableVolumeDHWTank'] = df_resultingProfiles_BT2 ['usableVolumeDHWTank'].round(2)
        df_resultingProfiles_BT2 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT2 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT2 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT2 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT2 ['simulationResult_costs'] = df_resultingProfiles_BT2 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT2 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT2 ['simulationResult_RESGeneration'].round(2)

        df_resultingProfiles_BT2 ['simulationResult_SurplusPower'] = df_resultingProfiles_BT2 ['simulationResult_SurplusPower'].round(2)
        df_resultingProfiles_BT2 ['Space Heating [W]'] = df_resultingProfiles_BT2 ['Space Heating [W]'].round(1)
        df_resultingProfiles_BT2 ['DHW [W]'] = df_resultingProfiles_BT2 ['DHW [W]'].round(1)
        df_resultingProfiles_BT2 ['Electricity [W]'] = df_resultingProfiles_BT2 ['Electricity [W]'].round(1)
        df_resultingProfiles_BT2 ['Outside Temperature [C]'] = df_resultingProfiles_BT2 ['Outside Temperature [C]'].round(2)
        df_resultingProfiles_BT2 ['Price [Cent/kWh]'] = df_resultingProfiles_BT2 ['Price [Cent/kWh]'].round(2)
        df_resultingProfiles_BT2 ['COP (Space Heating)'] = df_resultingProfiles_BT2 ['COP (Space Heating)'].round(2)
        df_resultingProfiles_BT2 ['COP (DHW)'] = df_resultingProfiles_BT2 ['COP (DHW)'].round(2)

        df_resultingProfiles_BT2.index.name = 'timeslot'
        df_resultingProfiles_BT2.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT2), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT2.to_csv(pathForCreatingTheResultDataWithweek + "/BT2_HH" + str(i + 1) + ".csv", index=True,  sep =";")

    #BT3
    for i in range (0, SetUpScenarios.numberOfBuildings_BT3):
        df_resultingProfiles_BT3 = pd.DataFrame({'chargingPowerEV': outputVector_BT3_chargingPowerEV_corrected[i, :],  'simulationResult_SOCofEV': simulationResult_SOCofEV_BT3[0,i, :], 'simulationResult_energyLevelOfEV': simulationResult_energyLevelOfEV_BT3[0,i, :], 'simulationResult_PVGeneration': simulationResult_PVGeneration_BT3[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT3[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT3[0,i, :], 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT3[0,i, :], 'simulationResult_costs': simulationResult_costs_BT3[0,i, :], 'Electricity [W]': simulationInput_BT3_electricityDemand [i, :], 'Availability of the EV': simulationInput_BT3_availabilityPattern [i, :],'Energy Consumption of the EV':simulationInput_BT3_energyConsumptionOfTheEV [i, :], 'Outside Temperature [C]': df_outsideTemperatureData['Temperature [C]'], 'Price [Cent/kWh]': df_priceData['Price [Cent/kWh]']})
        #Round values
        df_resultingProfiles_BT3 ['chargingPowerEV'] = df_resultingProfiles_BT3 ['chargingPowerEV'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_SOCofEV'] = df_resultingProfiles_BT3 ['simulationResult_SOCofEV'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_energyLevelOfEV'] = (df_resultingProfiles_BT3 ['simulationResult_energyLevelOfEV']/3600000).round(2)
        df_resultingProfiles_BT3 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT3 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT3 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_costs'] = df_resultingProfiles_BT3 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT3 ['simulationResult_RESGeneration'].round(2)

        df_resultingProfiles_BT3 ['simulationResult_SurplusPower'] = df_resultingProfiles_BT3 ['simulationResult_SurplusPower'].round(2)
        df_resultingProfiles_BT3 ['Electricity [W]'] = df_resultingProfiles_BT3 ['Electricity [W]'].round(1)
        df_resultingProfiles_BT3 ['Outside Temperature [C]'] = df_resultingProfiles_BT3 ['Outside Temperature [C]'].round(2)
        df_resultingProfiles_BT3 ['Price [Cent/kWh]'] = df_resultingProfiles_BT3 ['Price [Cent/kWh]'].round(2)


        df_resultingProfiles_BT3.index.name = 'timeslot'
        df_resultingProfiles_BT3.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT3), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT3.to_csv(pathForCreatingTheResultDataWithweek + "/BT3_HH" + str(i + 1) + ".csv", index=True,  sep =";")


    #BT4
    for i in range (0, SetUpScenarios.numberOfBuildings_BT4):
        df_resultingProfiles_BT4 = pd.DataFrame({'heatGenerationCoefficientSpaceHeating': outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected[i, :], 'temperatureBufferStorage': simulationResult_BufferStorageTemperature_BT4[0,i, :], 'simulationResult_PVGeneration': simulationResult_PVGeneration_BT4[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT4[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT4[0,i, :], 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT4[0,i, :], 'simulationResult_costs': simulationResult_costs_BT4[0,i, :], 'Space Heating [W]': simulationInput_BT4_SpaceHeating [i, :],  'Electricity [W]': simulationInput_BT4_electricityDemand [i, :],  'Outside Temperature [C]': df_outsideTemperatureData['Temperature [C]'], 'Price [Cent/kWh]': df_priceData['Price [Cent/kWh]'], 'COP (Space Heating)': cop_heatPump_SpaceHeating [:], 'numberOfStarts_HP': simulationResult_numberOfStartsHP_PerTimeslot_BT4[0,i, :],  'HP_isRunning': simulationResult_isHPRunning_PerTimeslot_BT4 [0,i, :]})
        #Round values

        df_resultingProfiles_BT4 ['heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_BT4 ['heatGenerationCoefficientSpaceHeating'].round(2)
        df_resultingProfiles_BT4 ['temperatureBufferStorage'] = df_resultingProfiles_BT4 ['temperatureBufferStorage'].round(2)
        df_resultingProfiles_BT4 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT4 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT4 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT4 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT4 ['simulationResult_costs'] = df_resultingProfiles_BT4 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT4 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT4 ['simulationResult_RESGeneration'].round(2)

        df_resultingProfiles_BT4 ['simulationResult_SurplusPower'] = df_resultingProfiles_BT4 ['simulationResult_SurplusPower'].round(2)
        df_resultingProfiles_BT4 ['Space Heating [W]'] = df_resultingProfiles_BT4 ['Space Heating [W]'].round(1)
        df_resultingProfiles_BT4 ['Electricity [W]'] = df_resultingProfiles_BT4 ['Electricity [W]'].round(1)
        df_resultingProfiles_BT4 ['Outside Temperature [C]'] = df_resultingProfiles_BT4 ['Outside Temperature [C]'].round(2)
        df_resultingProfiles_BT4 ['Price [Cent/kWh]'] = df_resultingProfiles_BT4 ['Price [Cent/kWh]'].round(2)
        df_resultingProfiles_BT4 ['COP (Space Heating)'] = df_resultingProfiles_BT4 ['COP (Space Heating)'].round(2)


        df_resultingProfiles_BT4.index.name = 'timeslot'
        df_resultingProfiles_BT4.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT4), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT4.to_csv(pathForCreatingTheResultDataWithweek + "/BT4_HH" + str(i + 1) + ".csv", index=True,  sep =";")


    #BT5
    for i in range (0, SetUpScenarios.numberOfBuildings_BT5):
        df_resultingProfiles_BT5 = pd.DataFrame({'chargingPowerBAT': outputVector_BT5_chargingPowerBAT_corrected[i, :], 'disChargingPowerBAT': outputVector_BT5_disChargingPowerBAT_corrected[i, :],  'simulationResult_SOCofBAT': simulationResult_SOCofBAT_BT5[0,i, :], 'simulationResult_energyLevelOfBAT': simulationResult_energyLevelOfBAT_BT5[0,i, :], 'simulationResult_PVGeneration': simulationResult_PVGeneration_BT5[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT5[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT5[0,i, :], 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT5[0,i, :], 'simulationResult_costs': simulationResult_costs_BT5[0,i, :], 'Electricity [W]': simulationInput_BT5_electricityDemand [i, :], 'Outside Temperature [C]': df_outsideTemperatureData['Temperature [C]'], 'Price [Cent/kWh]': df_priceData['Price [Cent/kWh]']})
        #Round values
        df_resultingProfiles_BT5 ['chargingPowerBAT'] = df_resultingProfiles_BT5 ['chargingPowerBAT'].round(2)
        df_resultingProfiles_BT5 ['disChargingPowerBAT'] = df_resultingProfiles_BT5 ['disChargingPowerBAT'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_SOCofBAT'] = df_resultingProfiles_BT5 ['simulationResult_SOCofBAT'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_energyLevelOfBAT'] = (df_resultingProfiles_BT5 ['simulationResult_energyLevelOfBAT']/3600000).round(2)
        df_resultingProfiles_BT5 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT5 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT5 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_costs'] = df_resultingProfiles_BT5 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT5 ['simulationResult_RESGeneration'].round(2)

        df_resultingProfiles_BT5 ['simulationResult_SurplusPower'] = df_resultingProfiles_BT5 ['simulationResult_SurplusPower'].round(2)
        df_resultingProfiles_BT5 ['Electricity [W]'] = df_resultingProfiles_BT5 ['Electricity [W]'].round(1)
        df_resultingProfiles_BT5 ['Outside Temperature [C]'] = df_resultingProfiles_BT5 ['Outside Temperature [C]'].round(2)
        df_resultingProfiles_BT5 ['Price [Cent/kWh]'] = df_resultingProfiles_BT5 ['Price [Cent/kWh]'].round(2)


        df_resultingProfiles_BT5.index.name = 'timeslot'
        df_resultingProfiles_BT5.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT5), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT5.to_csv(pathForCreatingTheResultDataWithweek + "/BT5_HH" + str(i + 1) + ".csv", index=True,  sep =";")



    #Combined results for the whole residential area
    df_resultingProfiles_combined = pd.DataFrame({'simulationResult_electricalLoad_combined': simulationResult_electricalLoad_combined[0, :],'simulationResult_RESGeneration_combined': simulationResult_RESGeneration_combined[0, :],'simulationResult_PVGeneration_combined': simulationResult_PVGeneration_combined[0, :], 'simulationResult_SurplusEnergy_combined': simulationResult_SurplusEnergy_combined[0, :], 'simulationResult_costs_combined': simulationResult_costs_combined[0, :]})
    df_resultingProfiles_combined ['simulationResult_electricalLoad_combined'] =df_resultingProfiles_combined ['simulationResult_electricalLoad_combined'].round(2)
    df_resultingProfiles_combined ['simulationResult_RESGeneration_combined'] =df_resultingProfiles_combined ['simulationResult_RESGeneration_combined'].round(2)
    df_resultingProfiles_combined ['simulationResult_PVGeneration_combined'] =df_resultingProfiles_combined ['simulationResult_PVGeneration_combined'].round(2)
    df_resultingProfiles_combined ['simulationResult_SurplusEnergy_combined'] =df_resultingProfiles_combined ['simulationResult_SurplusEnergy_combined'].round(2)
    df_resultingProfiles_combined ['simulationResult_costs_combined'] =df_resultingProfiles_combined ['simulationResult_costs_combined'].round(2)



    df_resultingProfiles_combined.index.name = 'timeslot'
    df_resultingProfiles_combined.index +=1
    df_resultingProfiles_combined.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_combined), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
    df_resultingProfiles_combined.to_csv (pathForCreatingTheResultDataWithweek + "/wholeResidentialArea.csv", index=True,  sep =";")


    #Print results into file
    filename = pathForCreatingTheResultDataWithweek + "/Results.txt"
    with open(filename, 'w') as f:
        print("Objectives" + "\n" + "\n")
        print("Consider objective Surplus Energy: " + str(Run_Simulations.optimizationGoal_minimizeSurplusEnergy), file = f)
        print("Consider objective Peak Load: " + str(Run_Simulations.optimizationGoal_minimizePeakLoad), file = f)
        print("Consider objective Costs: " + str(Run_Simulations.optimizationGoal_minimizeCosts) + "\n", file = f)
        print("Objective Surplus Energy [kWh]: " + str(round(simulationObjective_surplusEnergy_kWh_combined [index_week], 2)) , file = f)
        print("Objective Peak Load [kW]: " + str(round(simulationObjective_maximumLoad_kW_combined [index_week], 2)), file = f)
        print("Objective Costs [Euro]: " + str(round(simulationObjective_costs_Euro_combined [index_week], 2)), file = f)
        print("Objective Score: " + str(round(simulationObjective_combinedScore_combined [index_week], 2)), file = f)
        print("", file = f)
        print("", file = f)
        print("", file = f)
        print("Negative Scores", file = f)
        print("", file = f)
        print("", file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined: ", round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankRange_combined: ", round(negativeScore_total_ConstraintViolation_DHWTankRange_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankLastValue_combined: ",round(negativeScore_total_ConstraintViolation_DHWTankLastValue_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined: ",round(negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined: ",round(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined: ",round(negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined: ",round(negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined [index_week], 3), file = f)
        print("", file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined: ", round(negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined: ",round(negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week], 3), file = f)
        print("negativeScore_total_overall: ",round(negativeScore_total_overall [index_week],3), file = f)
        print("", file = f)
        print("", file = f)
        print("", file = f)
        print("Correction stats", file = f)
        print("", file = f)
        print("", file = f)
        print("correctingStats_BT1_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots", correctingStats_BT1_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfCorrections", correctingStats_BT1_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week],file = f)
        print("correctingStats_BT1_heatGenerationCoefficientDHW_numberOfTimeSlots", correctingStats_BT1_heatGenerationCoefficientDHW_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT1_heatGenerationCoefficientDHW_sumOfCorrections", correctingStats_BT1_heatGenerationCoefficientDHW_sumOfCorrections [index_week],file = f)
        print("correctingStats_BT1_chargingPowerEV_numberOfTimeSlots", correctingStats_BT1_chargingPowerEV_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT1_chargingPowerEV_sumOfCorrections", correctingStats_BT1_chargingPowerEV_sumOfCorrections [index_week],file = f)
        print("", file = f)
        print("correctingStats_BT2_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots", correctingStats_BT2_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfCorrections", correctingStats_BT2_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week],file = f)
        print("correctingStats_BT2_heatGenerationCoefficientDHW_numberOfTimeSlots", correctingStats_BT2_heatGenerationCoefficientDHW_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT2_heatGenerationCoefficientDHW_sumOfCorrections", correctingStats_BT2_heatGenerationCoefficientDHW_sumOfCorrections [index_week],file = f)
        print("", file = f)
        print("correctingStats_BT3_chargingPowerEV_numberOfTimeSlots", correctingStats_BT3_chargingPowerEV_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT3_chargingPowerEV_sumOfCorrections", correctingStats_BT3_chargingPowerEV_sumOfCorrections [index_week],file = f)
        print("", file = f)
        print("correctingStats_BT4_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots", correctingStats_BT4_heatGenerationCoefficientSpaceHeating_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfCorrections", correctingStats_BT4_heatGenerationCoefficientSpaceHeating_sumOfCorrections [index_week],file = f)
        print("", file = f)
        print("correctingStats_BT5_chargingPowerBAT_numberOfTimeSlots", correctingStats_BT5_chargingPowerBAT_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT5_chargingPowerBAT_sumOfCorrections", correctingStats_BT5_chargingPowerBAT_sumOfCorrections [index_week],file = f)
        print("", file = f)
        print("correctingStats_BT5_chargingPowerBAT_numberOfTimeSlots", correctingStats_BT5_chargingPowerBAT_numberOfTimeSlots [index_week],file = f)
        print("correctingStats_BT5_chargingPowerBAT_sumOfCorrections", correctingStats_BT5_chargingPowerBAT_sumOfCorrections [index_week],file = f)
        print("", file = f)




    negativeScore_CorrectionLimits = round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week], 3)
    negativeScore_PhysicalLimits = round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined[index_week], 3)

    return simulationObjective_surplusEnergy_kWh_combined , simulationObjective_maximumLoad_kW_combined, simulationObjective_costs_Euro_combined, simulationObjective_combinedScore_combined, negativeScore_total_overall, negativeScore_CorrectionLimits, negativeScore_PhysicalLimits
    #End method




#Simulation method for the conventional control strategy



def simulateWeeks_ConventionalControl(indexOfBuildingsOverall_BT1, indexOfBuildingsOverall_BT2, indexOfBuildingsOverall_BT3, indexOfBuildingsOverall_BT4, indexOfBuildingsOverall_BT5, currentweek, pathForCreatingTheResultData, usePriceStorageControl):


    #Variables of the simulation for all buildings combined

    simulationResult_electricalLoad_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusEnergy_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing), SetUpScenarios.numberOfTimeSlotsPerWeek))

    simulationObjective_surplusEnergy_kWh_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    simulationObjective_costs_Euro_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    simulationObjective_maximumLoad_kW_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    simulationObjective_combinedScore_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))

    total_ConstraintViolation_BufferStorageTemperatureRange_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_DHWTankRange_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_DHWTankLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_OnlyOneStorage_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_MinimalModulationDegree_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_SOCRangeOfTheEV_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_SOCOfTheEVLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_ChargingPowerOfTheEV_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_numberOfStarts_Individual_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_numberOfStarts_Combined_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_SOCRangeOfTheBAT_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_SOCOfTheBATLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    total_ConstraintViolation_ChargingPowerOfTheBAT_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))

    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankRange_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_OnlyOneStorage_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_MinimalModulationDegree_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_ChargingPowerOfTheEV_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_numberOfStarts_Individual_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCOfTheBATLastValue_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_ChargingPowerOfTheBAT_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    hypotheticalSOCDropWithNoCharging_combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))


    #Variables of the simulation for BT1

    simulationResult_electricalLoad_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_BufferStorageTemperature_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_UsableVolumeDHW_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SOCofEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_energyLevelOfEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    hypotheticalSOCDropWithNoCharging_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))

    simulationResult_numberOfStartsBufferStorage_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationResult_numberOfStartsDHWTank_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationResult_numberOfStartsCombined_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))

    simulationObjective_surplusEnergyKWH_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationObjective_costs_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    simulationObjective_maximumLoad_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))

    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_DHWTankRange_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_OnlyOneStorage_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_MinimalModulationDegree_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_SOCRangeOfTheEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_DHWTankRange_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_DHWTankLastValue_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_OnlyOneStorage_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_MinimalModulationDegree_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_SOCRangeOfTheEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_SOCOfTheEVLastValue_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_ChargingPowerOfTheEV_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_numberOfStarts_Individual_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))
    total_ConstraintViolation_numberOfStarts_Combined_BT1 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT1))


    #Variables of the simulation for BT2

    simulationResult_electricalLoad_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_BufferStorageTemperature_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_UsableVolumeDHW_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfStartsBufferStorage_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationResult_numberOfStartsDHWTank_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationResult_numberOfStartsCombined_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))

    simulationObjective_surplusEnergyKWH_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationObjective_costs_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    simulationObjective_maximumLoad_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))

    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_DHWTankRange_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_OnlyOneStorage_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_MinimalModulationDegree_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_DHWTankRange_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_DHWTankLastValue_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_OnlyOneStorage_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_MinimalModulationDegree_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_numberOfStarts_Individual_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))
    total_ConstraintViolation_numberOfStarts_Combined_BT2 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT2))



    #Variables of the simulation for BT3

    simulationResult_electricalLoad_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SOCofEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_energyLevelOfEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    hypotheticalSOCDropWithNoCharging_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))

    simulationObjective_surplusEnergyKWH_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
    simulationObjective_costs_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
    simulationObjective_maximumLoad_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))

    simulation_ConstraintViolation_SOCRangeOfTheEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_SOCRangeOfTheEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
    total_ConstraintViolation_SOCOfTheEVLastValue_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))
    total_ConstraintViolation_ChargingPowerOfTheEV_BT3 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT3))


    #Variables of the simulation for BT4

    simulationResult_electricalLoad_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_BufferStorageTemperature_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_numberOfStartsBufferStorage_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))

    simulationObjective_surplusEnergyKWH_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    simulationObjective_costs_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    simulationObjective_maximumLoad_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))

    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_MinimalModulationDegree_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_BufferStorageTemperatureRange_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_MinimalModulationDegree_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))
    total_ConstraintViolation_numberOfStarts_Individual_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4))

    simulationResult_priceFactor_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_storageFactor_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_averageTemperature_BT4 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))

    # Variables of the simulation for BT5

    simulationResult_electricalLoad_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_costs_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SurplusPower_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_PVGeneration_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_RESGeneration_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_SOCofBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationResult_energyLevelOfBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))

    simulationObjective_surplusEnergyKWH_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    simulationObjective_costs_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    simulationObjective_maximumLoad_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))

    simulation_ConstraintViolation_SOCRangeOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_ChargingPowerOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulation_ConstraintViolation_disChargingPowerOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))

    total_ConstraintViolation_SOCRangeOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    total_ConstraintViolation_SOCOfTheBATLastValue_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    total_ConstraintViolation_ChargingPowerOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))
    total_ConstraintViolation_disChargingPowerOfTheBAT_BT5 = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing),SetUpScenarios.numberOfBuildings_BT5))


    # Additional constraint violation variables for the internal controller

    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))
    negativeScore_total_overall = np.zeros((len(Run_Simulations.weeksOfTheYearForSimulation_Testing)))

    #Define the variables for the simulation input (are only used for the output csv file)
    simulationInput_BT1_SpaceHeating = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT1_DHW = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT1_availabilityPattern = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT1_energyConsumptionOfTheEV = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT1_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT1), SetUpScenarios.numberOfTimeSlotsPerWeek))

    simulationInput_BT2_SpaceHeating = np.zeros((len(indexOfBuildingsOverall_BT2), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT2_DHW = np.zeros((len(indexOfBuildingsOverall_BT2), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT2_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT2), SetUpScenarios.numberOfTimeSlotsPerWeek))

    simulationInput_BT3_availabilityPattern = np.zeros((len(indexOfBuildingsOverall_BT3), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT3_energyConsumptionOfTheEV = np.zeros((len(indexOfBuildingsOverall_BT3), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT3_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT3), SetUpScenarios.numberOfTimeSlotsPerWeek))

    simulationInput_BT4_SpaceHeating = np.zeros((len(indexOfBuildingsOverall_BT4), SetUpScenarios.numberOfTimeSlotsPerWeek))
    simulationInput_BT4_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT4), SetUpScenarios.numberOfTimeSlotsPerWeek))

    simulationInput_BT5_electricityDemand = np.zeros((len(indexOfBuildingsOverall_BT5), SetUpScenarios.numberOfTimeSlotsPerWeek))


    for index_week in range (0, len(Run_Simulations.weeksOfTheYearForSimulation_Testing)):

        # Define the output vectors
        outputVector_BT1_heatGenerationCoefficientSpaceHeating_Conventional = np.zeros(( SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
        outputVector_BT1_heatGenerationCoefficientDHW_Conventional = np.zeros((SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))
        outputVector_BT1_chargingPowerEV_Conventional = np.zeros((SetUpScenarios.numberOfBuildings_BT1, SetUpScenarios.numberOfTimeSlotsPerWeek))

        outputVector_BT2_heatGenerationCoefficientSpaceHeating_Conventional = np.zeros((SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))
        outputVector_BT2_heatGenerationCoefficientDHW_Conventional = np.zeros((SetUpScenarios.numberOfBuildings_BT2, SetUpScenarios.numberOfTimeSlotsPerWeek))

        outputVector_BT3_chargingPowerEV_Conventional = np.zeros((SetUpScenarios.numberOfBuildings_BT3, SetUpScenarios.numberOfTimeSlotsPerWeek))

        outputVector_BT4_heatGenerationCoefficientSpaceHeating_Conventional = np.zeros((SetUpScenarios.numberOfBuildings_BT4, SetUpScenarios.numberOfTimeSlotsPerWeek))

        outputVector_BT5_chargingPowerBAT_Conventional = np.zeros((SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))
        outputVector_BT5_disChargingPowerBAT_Conventional = np.zeros((SetUpScenarios.numberOfBuildings_BT5, SetUpScenarios.numberOfTimeSlotsPerWeek))


        #Building Type 1
        for index_BT1 in range (0, len(indexOfBuildingsOverall_BT1)):
            #Reading of the data

            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT1_mHP_EV_SFH_1Minute_weeks/HH" + str(indexOfBuildingsOverall_BT1[index_BT1]) + "/HH" + str(indexOfBuildingsOverall_BT1[index_BT1]) + "_week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_weeks/Outside_Temperature_1Minute_week' +  str(currentweek) + '.csv', sep =";")


            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"

            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            for i in range (0, len(df_buildingData['Availability of the EV'])):
                if df_buildingData['Availability of the EV'] [i] > 0.1:
                    df_buildingData['Availability of the EV'] [i] = 1.0
                if df_buildingData['Availability of the EV'] [i] < 0.1 and df_buildingData['Availability of the EV'] [i] >0.01:
                    df_buildingData['Availability of the EV'] [i] = 0.0

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

            #Create availability array for the EV
            availabilityOfTheEV = np.zeros(( SetUpScenarios.numberOfTimeSlotsPerWeek))
            for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerWeek):
                availabilityOfTheEV [index_timeslot_for_Availability] = df_buildingData['Availability of the EV'] [index_timeslot_for_Availability +1]
            indexOfTheEV = index_BT1
            energyConsumptionOfEVs_Joule = SetUpScenarios.generateEVEnergyConsumptionPatterns(availabilityOfTheEV, indexOfTheEV)


            df_availabilityPatternEV = pd.DataFrame({'Timeslot': df_buildingData.index, 'Availability of the EV':df_buildingData['Availability of the EV'] })
            del df_availabilityPatternEV['Timeslot']

            df_energyConsumptionEV_Joule = pd.DataFrame({'Timeslot': df_buildingData.index, 'Energy':energyConsumptionOfEVs_Joule  })
            del df_energyConsumptionEV_Joule['Timeslot']
            df_energyConsumptionEV_Joule.index +=1


            #Wind generation

            indexBuildingForWindPowerAssignment = index_BT1
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1

            # Set up inital values for the simulation
            simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, 0] = SetUpScenarios.initialBufferStorageTemperature
            simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, 0] = SetUpScenarios.initialUsableVolumeDHWTank
            simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, 0]= (SetUpScenarios.initialSOC_EV/100) * SetUpScenarios.capacityMaximal_EV
            simulationResult_SOCofEV_BT1 [index_week, index_BT1, 0]= SetUpScenarios.initialSOC_EV
            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])


            bufferStorageIsHeatedUp = False
            dhwTankIsHeatedUp = False



            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):
                if index_timeslot >=1:


                    # Calculate required heating power for keeping the temperature
                    targetTemperartueValue = SetUpScenarios.initialBufferStorageTemperature
                    targetVolumeDHW = SetUpScenarios.maximumUsableVolumeDHWTank_ConventionalControl
                    if simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot - 1] > SetUpScenarios.initialBufferStorageTemperature:
                        targetTemperartueValue = simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot - 1]
                    if targetTemperartueValue >= SetUpScenarios.initialBufferStorageTemperature + 0.2:
                        targetTemperartueValue = SetUpScenarios.initialBufferStorageTemperature

                    requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel = ((targetTemperartueValue - simulationResult_BufferStorageTemperature_BT1 [index_week, index_BT1, index_timeslot - 1]) *(SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData['Space Heating [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesBufferStorage
                    requiredHeatingPowerForKeepingTheVolumeOfTheDHWStorageAtInitialLevel = ((targetVolumeDHW - simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1]) * (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData ['DHW [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesDHWTank

                    if outputVector_BT1_heatGenerationCoefficientSpaceHeating_Conventional [index_BT1, index_timeslot - 1]  > 0:
                        bufferStorageIsHeatedUp = True
                    if outputVector_BT1_heatGenerationCoefficientDHW_Conventional [index_BT1, index_timeslot - 1]  > 0:
                        dhwTankIsHeatedUp = True
                    if outputVector_BT1_heatGenerationCoefficientSpaceHeating_Conventional [index_BT1, index_timeslot - 1]  ==0:
                        bufferStorageIsHeatedUp = False
                    if outputVector_BT1_heatGenerationCoefficientDHW_Conventional [index_BT1, index_timeslot - 1]  == 0:
                        dhwTankIsHeatedUp = False


                if index_timeslot ==0:
                     bufferStorageIsHeatedUp = False
                     dhwTankIsHeatedUp = True
                     requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel = ((SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.initialBufferStorageTemperature) *(SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData['Space Heating [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesBufferStorage
                     requiredHeatingPowerForKeepingTheVolumeOfTheDHWStorageAtInitialLevel = ((SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.initialUsableVolumeDHWTank) * (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData ['DHW [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesDHWTank

                if index_timeslot >0:

                    if bufferStorageIsHeatedUp ==False and dhwTankIsHeatedUp == False:
                        if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1] <= SetUpScenarios.minimumBufferStorageTemperature_ConventionalControl:
                            bufferStorageIsHeatedUp = True
                            dhwTankIsHeatedUp = False
                        if simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] <= SetUpScenarios.minimumUsableVolumeDHWTank_ConventionalControl:
                            bufferStorageIsHeatedUp = False
                            dhwTankIsHeatedUp = True


                if bufferStorageIsHeatedUp == True:
                    requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel = (requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel / (cop_heatPump_SpaceHeating[index_timeslot] * SetUpScenarios.electricalPower_HP))*100
                    intendedModulationDegreeForSpaceHeating = requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel
                    intendedModulationDegreeDHW = 0
                    if requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel < SetUpScenarios.minimalModulationdDegree_HP:
                        intendedModulationDegreeForSpaceHeating = SetUpScenarios.minimalModulationdDegree_HP
                    if requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel > 100:
                        intendedModulationDegreeForSpaceHeating = 100

                if dhwTankIsHeatedUp == True:
                    requiredModulatingDegreeofTheHeatPumpForKeepingTheVolumeAtInitialLevel = (requiredHeatingPowerForKeepingTheVolumeOfTheDHWStorageAtInitialLevel / (cop_heatPump_DHW [index_timeslot] * SetUpScenarios.electricalPower_HP))*100
                    intendedModulationDegreeDHW = requiredModulatingDegreeofTheHeatPumpForKeepingTheVolumeAtInitialLevel
                    intendedModulationDegreeForSpaceHeating =0
                    if requiredModulatingDegreeofTheHeatPumpForKeepingTheVolumeAtInitialLevel < SetUpScenarios.minimalModulationdDegree_HP:
                        intendedModulationDegreeDHW = SetUpScenarios.minimalModulationdDegree_HP
                    if requiredModulatingDegreeofTheHeatPumpForKeepingTheVolumeAtInitialLevel > 100:
                        intendedModulationDegreeDHW = 100

                intendedPowerEVCharging = SetUpScenarios.chargingPowerMaximal_EV * (SetUpScenarios.modulationDegreeCharging_ConventionalControl/100) *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1]




                #Calculate hypothetical temperatures, volumes and the SOC of the EV
                if index_timeslot >=1:
                    hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + (((intendedModulationDegreeForSpaceHeating/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + (((intendedModulationDegreeDHW /100) * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    hypotheticalTemperatureBufferStorageWhenHeatingWithMinimalModulation = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + (((SetUpScenarios.minimalModulationdDegree_HP/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    hypotheticalVolumeDHWTankWhenHeatingWithMinimalModulation = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + (((SetUpScenarios.minimalModulationdDegree_HP /100) * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    hypotheticalEnergyLevelOfTheEV  =simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot - 1] + (  intendedPowerEVCharging *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    hypothetical_SOCofEV_BT1  = (hypotheticalEnergyLevelOfTheEV / SetUpScenarios.capacityMaximal_EV)*100


                if index_timeslot ==0:
                    hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation = SetUpScenarios.initialBufferStorageTemperature  + (((intendedModulationDegreeForSpaceHeating/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation = SetUpScenarios.initialUsableVolumeDHWTank + (((intendedModulationDegreeDHW /100) * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    hypotheticalEnergyLevelOfTheEV  = SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + ( intendedPowerEVCharging *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    hypothetical_SOCofEV_BT1  = (simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalTemperatureBufferStorageWhenHeatingWithMinimalModulation = SetUpScenarios.initialBufferStorageTemperature  + (((SetUpScenarios.minimalModulationdDegree_HP/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    hypotheticalVolumeDHWTankWhenHeatingWithMinimalModulation = SetUpScenarios.initialUsableVolumeDHWTank + (((SetUpScenarios.minimalModulationdDegree_HP /100) * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))



                #Adjust the intendedModulationDegrees when having reached the upper and lower limtis
                if hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation < SetUpScenarios.minimumBufferStorageTemperature_ConventionalControl:
                    intendedModulationDegreeForSpaceHeating = 100
                    intendedModulationDegreeDHW = 0
                if hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation > SetUpScenarios.maximumBufferStorageTemperature_ConventionalControl:
                    intendedModulationDegreeForSpaceHeating = 0
                    if hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation > SetUpScenarios.minimumUsableVolumeDHWTank_ConventionalControl and hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation < SetUpScenarios.maximumUsableVolumeDHWTank_ConventionalControl:
                        intendedModulationDegreeDHW = SetUpScenarios.minimalModulationdDegree_HP
                if hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation < SetUpScenarios.minimumUsableVolumeDHWTank_ConventionalControl:
                    intendedModulationDegreeForSpaceHeating = 0
                    intendedModulationDegreeDHW = 100
                if hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation > SetUpScenarios.maximumUsableVolumeDHWTank_ConventionalControl:
                    intendedModulationDegreeDHW = 0

                if hypotheticalTemperatureBufferStorageWhenHeatingWithMinimalModulation >= SetUpScenarios.maximumBufferStorageTemperature_ConventionalControl and hypotheticalVolumeDHWTankWhenHeatingWithMinimalModulation >= SetUpScenarios.maximumUsableVolumeDHWTank_ConventionalControl :
                    intendedModulationDegreeForSpaceHeating = 0
                    intendedModulationDegreeDHW = 0

                if intendedModulationDegreeForSpaceHeating > 0 and intendedModulationDegreeDHW > 0:
                    intendedModulationDegreeForSpaceHeating = 0




                # Adjust the charging Power of the EV if SOC is too high
                if hypothetical_SOCofEV_BT1 >= SetUpScenarios.initialSOC_EV:
                    intendedPowerEVCharging = 0



                # Adjust the heating at the end of the week if the storage values are too high
                if index_timeslot >= (SetUpScenarios.numberOfTimeSlotsPerWeek - 2 * Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek):
                    simulationResult_BufferStorageTemperature_BT1_Pre = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1_Pre  = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((intendedModulationDegreeDHW/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if bufferStorageIsHeatedUp and simulationResult_BufferStorageTemperature_BT1_Pre >SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue * 2:
                        intendedModulationDegreeForSpaceHeating =0
                    if dhwTankIsHeatedUp and simulationResult_UsableVolumeDHW_BT1_Pre > SetUpScenarios.initialUsableVolumeDHWTank + 2* SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        intendedModulationDegreeDHW =0

                #Calculate simulation values
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot - 1]  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_UsableVolumeDHW_BT1[index_week, index_BT1, index_timeslot-1] + ((intendedModulationDegreeDHW/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot]  =simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot - 1] + ( intendedPowerEVCharging *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]  = (simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalSOCDropWithNoCharging_BT1 [index_week, index_BT1] = hypotheticalSOCDropWithNoCharging_BT1 [index_week, index_BT1] + (df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]/ SetUpScenarios.capacityMaximal_EV)*100


                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] = SetUpScenarios.initialUsableVolumeDHWTank + ((intendedModulationDegreeDHW/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot]  = SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + ( intendedPowerEVCharging *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]  = (simulationResult_energyLevelOfEV_BT1 [index_week, index_BT1, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalSOCDropWithNoCharging_BT1 [index_week, index_BT1] =  (df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]/ SetUpScenarios.capacityMaximal_EV)*100


                outputVector_BT1_heatGenerationCoefficientSpaceHeating_Conventional [index_BT1, index_timeslot] = intendedModulationDegreeForSpaceHeating/100
                outputVector_BT1_heatGenerationCoefficientDHW_Conventional [index_BT1, index_timeslot] = intendedModulationDegreeDHW/100
                outputVector_BT1_chargingPowerEV_Conventional [index_BT1, index_timeslot] = intendedPowerEVCharging




                simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings (index_BT1)
                simulationResult_RESGeneration_BT1 [index_week, index_BT1, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings (index_BT1) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine

                simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] = ( intendedModulationDegreeForSpaceHeating/100 + intendedModulationDegreeDHW/100 ) * SetUpScenarios.electricalPower_HP + intendedPowerEVCharging + df_buildingData ['Electricity [W]'] [index_timeslot + 1]
                simulationResult_SurplusPower_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_RESGeneration_BT1 [index_week, index_BT1, index_timeslot] - simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot]
                if simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] > simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]:
                    simulationResult_costs_BT1 [index_week, index_BT1, index_timeslot] = (simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] - simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] <= simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]:
                    simulationResult_costs_BT1 [index_week, index_BT1, index_timeslot] = (simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot] - simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)


                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT1_SpaceHeating [index_BT1, index_timeslot] = df_buildingData['Space Heating [W]'] [index_timeslot + 1]
                simulationInput_BT1_DHW [index_BT1, index_timeslot] = df_buildingData ['DHW [W]'] [index_timeslot + 1]
                simulationInput_BT1_availabilityPattern [index_BT1, index_timeslot] = df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1]
                simulationInput_BT1_energyConsumptionOfTheEV [index_BT1, index_timeslot] = df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]
                simulationInput_BT1_electricityDemand [index_BT1, index_timeslot] = df_buildingData ['Electricity [W]'] [index_timeslot + 1]



                #Calculate the constraint violation
                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] >SetUpScenarios.maximalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] -SetUpScenarios.maximalBufferStorageTemperature
                if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] <SetUpScenarios.minimalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - SetUpScenarios.minimalBufferStorageTemperature

                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.maximumCapacityDHWTankOptimization:
                    simulation_ConstraintViolation_DHWTankRange_BT1  [index_week, index_BT1, index_timeslot] = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - SetUpScenarios.maximumCapacityDHWTankOptimization
                if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.minimumCapacityDHWTankOptimization:
                    simulation_ConstraintViolation_DHWTankRange_BT1  [index_week, index_BT1, index_timeslot] =  simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - SetUpScenarios.minimumCapacityDHWTankOptimization


                if intendedModulationDegreeForSpaceHeating > 0 and intendedModulationDegreeDHW >0:
                    simulation_ConstraintViolation_OnlyOneStorage_BT1 [index_week, index_BT1, index_timeslot] =1

                if (intendedModulationDegreeForSpaceHeating/100 < SetUpScenarios.minimalModulationdDegree_HP/100) and (intendedModulationDegreeForSpaceHeating/100>0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] = (SetUpScenarios.minimalModulationdDegree_HP/100) - intendedModulationDegreeForSpaceHeating

                if intendedModulationDegreeForSpaceHeating/100 > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] + intendedModulationDegreeForSpaceHeating/100 -1
                if (intendedModulationDegreeDHW/100 < (SetUpScenarios.minimalModulationdDegree_HP/100)) and (intendedModulationDegreeDHW/100 > 0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] +  (SetUpScenarios.minimalModulationdDegree_HP/100) - intendedModulationDegreeDHW/100
                if intendedModulationDegreeDHW/100 > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot] + intendedModulationDegreeDHW/100 - 1

                if  simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] < 0:
                    simulation_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1, index_timeslot] = simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]
                if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] >100:
                    simulation_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1, index_timeslot] =simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] - 100

                if intendedPowerEVCharging < 0:
                    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1, index_timeslot] = intendedPowerEVCharging
                if intendedPowerEVCharging > SetUpScenarios.chargingPowerMaximal_EV:
                    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1, index_timeslot] = intendedPowerEVCharging - SetUpScenarios.chargingPowerMaximal_EV


                if index_timeslot >= 1:
                    if  outputVector_BT1_heatGenerationCoefficientSpaceHeating_Conventional [index_BT1, index_timeslot - 1] == 0 and intendedModulationDegreeForSpaceHeating/100 >0.001 :
                        simulationResult_numberOfStartsBufferStorage_BT1 [index_week, index_BT1] += 1
                    if outputVector_BT1_heatGenerationCoefficientDHW_Conventional [index_BT1, index_timeslot - 1] == 0 and intendedModulationDegreeDHW/100 >0.001 :
                        simulationResult_numberOfStartsDHWTank_BT1 [index_week, index_BT1] += 1



        #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                total_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1] = total_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1] + abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_DHWTankRange_BT1 [index_week, index_BT1] = total_ConstraintViolation_DHWTankRange_BT1 [index_week, index_BT1] + abs(simulation_ConstraintViolation_DHWTankRange_BT1 [index_week, index_BT1, index_timeslot])
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT1 [index_week, index_BT1] = simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue)
                    if  simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT1 [index_week, index_BT1] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue) - simulationResult_BufferStorageTemperature_BT1[index_week, index_BT1, index_timeslot]
                    if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        total_ConstraintViolation_DHWTankLastValue_BT1 [index_week, index_BT1] = simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] - ( SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue)
                    if simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot] < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        total_ConstraintViolation_DHWTankLastValue_BT1 [index_week, index_BT1] = (SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue) - simulationResult_UsableVolumeDHW_BT1 [index_week, index_BT1, index_timeslot]

                    if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] > (SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue):
                        total_ConstraintViolation_SOCOfTheEVLastValue_BT1  [index_week, index_BT1] =  simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] - ((SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue))
                    if simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot] < (SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue):
                        total_ConstraintViolation_SOCOfTheEVLastValue_BT1  [index_week, index_BT1] = ((SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue)) - simulationResult_SOCofEV_BT1 [index_week, index_BT1, index_timeslot]

                if intendedModulationDegreeForSpaceHeating > 0.0001 and intendedModulationDegreeDHW > 0.0001:
                    total_ConstraintViolation_OnlyOneStorage_BT1 [index_week, index_BT1] = total_ConstraintViolation_OnlyOneStorage_BT1 [index_week, index_BT1] + 1
                total_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1] = total_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1] + abs(simulation_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1] =  total_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1] + abs(simulation_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1, index_timeslot])
                total_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1] = total_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1] + abs (simulation_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1, index_timeslot])
                if Run_Simulations.considerMaximumNumberOfStartsHP_Combined == True:
                    if simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] > (Run_Simulations.maximumNumberOfStarts_Combined + 1):
                        total_ConstraintViolation_numberOfStarts_Combined_BT1 [index_week, index_BT1] = simulationResult_numberOfStartsCombined_BT1 [index_week, index_BT1] - (Run_Simulations.maximumNumberOfStarts_Combined + 1)
                if Run_Simulations.considerMaxiumNumberOfStartsHP_Individual  == True:
                    if simulationResult_numberOfStartsBufferStorage_BT1 [index_week, index_BT1] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]  = simulationResult_numberOfStartsBufferStorage_BT1 [index_week, index_BT1] - Run_Simulations.maximumNumberOfStarts_Individual
                    if simulationResult_numberOfStartsDHWTank_BT1 [index_week, index_BT1] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]  = total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]+  simulationResult_numberOfStartsDHWTank_BT1 [index_week, index_BT1] - Run_Simulations.maximumNumberOfStarts_Individual


        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT1  [index_week, index_BT1, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT1  [index_week, index_BT1] = simulationObjective_surplusEnergyKWH_BT1  [index_week, index_BT1] + ((simulationResult_SurplusPower_BT1  [index_week, index_BT1, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] - simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]) > simulationObjective_maximumLoad_BT1 [index_week, index_BT1]:
                    simulationObjective_maximumLoad_BT1 [index_week, index_BT1] = simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot] -  simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]
                if (simulationResult_PVGeneration_BT1  [index_week, index_BT1, index_timeslot] -  simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot]) > simulationObjective_maximumLoad_BT1 [index_week, index_BT1]:
                    simulationObjective_maximumLoad_BT1 [index_week, index_BT1] = simulationResult_PVGeneration_BT1  [index_week, index_BT1, index_timeslot] -   simulationResult_electricalLoad_BT1[index_week, index_BT1, index_timeslot]
                simulationObjective_costs_BT1  [index_week, index_BT1]  = simulationObjective_costs_BT1  [index_week, index_BT1] +  simulationResult_costs_BT1 [index_week, index_BT1, index_timeslot]


        #Building Type 2
        for index_BT2 in range (0, len(indexOfBuildingsOverall_BT2)):
            #Reading of the data
            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT2_mHP_SFH_1Minute_weeks/HH" + str(indexOfBuildingsOverall_BT2[index_BT2]) + "/HH" + str(indexOfBuildingsOverall_BT2[index_BT2]) + "_week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_weeks/Outside_Temperature_1Minute_week' +  str(currentweek) + '.csv', sep =";")

            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"
            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()



            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])

            #Wind generation

            indexBuildingForWindPowerAssignment = SetUpScenarios.numberOfBuildings_BT1 + index_BT2
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1


            bufferStorageIsHeatedUp = False
            dhwTankIsHeatedUp = False



            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):
                if index_timeslot >=1:
                    # Calculate required heating power for keeping the temperature
                    targetTemperartueValue = SetUpScenarios.initialBufferStorageTemperature
                    targetVolumeDHW = SetUpScenarios.maximumUsableVolumeDHWTank_ConventionalControl
                    if simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot - 1] > SetUpScenarios.initialBufferStorageTemperature:
                        targetTemperartueValue = simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot - 1]
                    if targetTemperartueValue >= SetUpScenarios.initialBufferStorageTemperature + 0.2:
                        targetTemperartueValue = SetUpScenarios.initialBufferStorageTemperature

                    requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel = ((targetTemperartueValue - simulationResult_BufferStorageTemperature_BT2 [index_week, index_BT2, index_timeslot - 1]) *(SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData['Space Heating [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesBufferStorage
                    requiredHeatingPowerForKeepingTheVolumeOfTheDHWStorageAtInitialLevel = ((targetVolumeDHW - simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1]) * (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData ['DHW [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesDHWTank

                    if outputVector_BT2_heatGenerationCoefficientSpaceHeating_Conventional [index_BT2, index_timeslot - 1]  > 0:
                        bufferStorageIsHeatedUp = True
                    if outputVector_BT2_heatGenerationCoefficientDHW_Conventional [index_BT2, index_timeslot - 1]  > 0:
                        dhwTankIsHeatedUp = True
                    if outputVector_BT2_heatGenerationCoefficientSpaceHeating_Conventional [index_BT2, index_timeslot - 1]  ==0:
                        bufferStorageIsHeatedUp = False
                    if outputVector_BT2_heatGenerationCoefficientDHW_Conventional [index_BT2, index_timeslot - 1]  == 0:
                        dhwTankIsHeatedUp = False


                if index_timeslot ==0:
                     bufferStorageIsHeatedUp = False
                     dhwTankIsHeatedUp = True
                     requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel = ((SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.initialBufferStorageTemperature) *(SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData['Space Heating [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesBufferStorage
                     requiredHeatingPowerForKeepingTheVolumeOfTheDHWStorageAtInitialLevel = ((SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.initialUsableVolumeDHWTank) * (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData ['DHW [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesDHWTank

                if index_timeslot >0:
                    if bufferStorageIsHeatedUp ==False and dhwTankIsHeatedUp == False:
                        if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1] <= SetUpScenarios.minimumBufferStorageTemperature_ConventionalControl:
                            bufferStorageIsHeatedUp = True
                            dhwTankIsHeatedUp = False
                            print("buffer On from OFF. Timeslot:" , index_timeslot)
                        if simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] <= SetUpScenarios.minimumUsableVolumeDHWTank_ConventionalControl:
                            bufferStorageIsHeatedUp = False
                            dhwTankIsHeatedUp = True
                            print("DHW On from OFF. Timeslot:" , index_timeslot)



                if bufferStorageIsHeatedUp == True:
                    requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel = (requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel / (cop_heatPump_SpaceHeating[index_timeslot] * SetUpScenarios.electricalPower_HP))*100
                    intendedModulationDegreeForSpaceHeating = requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel
                    intendedModulationDegreeDHW = 0
                    if requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel < SetUpScenarios.minimalModulationdDegree_HP:
                        intendedModulationDegreeForSpaceHeating = SetUpScenarios.minimalModulationdDegree_HP
                    if requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel > 100:
                        intendedModulationDegreeForSpaceHeating = 100

                if dhwTankIsHeatedUp == True:
                    requiredModulatingDegreeofTheHeatPumpForKeepingTheVolumeAtInitialLevel = (requiredHeatingPowerForKeepingTheVolumeOfTheDHWStorageAtInitialLevel / (cop_heatPump_DHW [index_timeslot] * SetUpScenarios.electricalPower_HP))*100
                    intendedModulationDegreeDHW = requiredModulatingDegreeofTheHeatPumpForKeepingTheVolumeAtInitialLevel
                    intendedModulationDegreeForSpaceHeating =0
                    if requiredModulatingDegreeofTheHeatPumpForKeepingTheVolumeAtInitialLevel < SetUpScenarios.minimalModulationdDegree_HP:
                        intendedModulationDegreeDHW = SetUpScenarios.minimalModulationdDegree_HP
                    if requiredModulatingDegreeofTheHeatPumpForKeepingTheVolumeAtInitialLevel > 100:
                        intendedModulationDegreeDHW = 100


                #Calculate hypothetical temperatures, volumes
                if index_timeslot >=1:
                    hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + (((intendedModulationDegreeForSpaceHeating/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + (((intendedModulationDegreeDHW /100) * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    hypotheticalTemperatureBufferStorageWhenHeatingWithMinimalModulation = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + (((SetUpScenarios.minimalModulationdDegree_HP/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    hypotheticalVolumeDHWTankWhenHeatingWithMinimalModulation = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + (((SetUpScenarios.minimalModulationdDegree_HP /100) * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


                if index_timeslot ==0:
                    hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation = SetUpScenarios.initialBufferStorageTemperature  + (((intendedModulationDegreeForSpaceHeating/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation = SetUpScenarios.initialUsableVolumeDHWTank + (((intendedModulationDegreeDHW /100) * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    hypotheticalTemperatureBufferStorageWhenHeatingWithMinimalModulation = SetUpScenarios.initialBufferStorageTemperature  + (((SetUpScenarios.minimalModulationdDegree_HP/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    hypotheticalVolumeDHWTankWhenHeatingWithMinimalModulation = SetUpScenarios.initialUsableVolumeDHWTank + (((SetUpScenarios.minimalModulationdDegree_HP /100) * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))



                #Adjust the intendedModulationDegrees when having reached the upper and lower limtis
                if hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation < SetUpScenarios.minimumBufferStorageTemperature_ConventionalControl:
                    intendedModulationDegreeForSpaceHeating = 100
                    intendedModulationDegreeDHW = 0
                if hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation > SetUpScenarios.maximumBufferStorageTemperature_ConventionalControl:
                    intendedModulationDegreeForSpaceHeating = 0
                    if hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation > SetUpScenarios.minimumUsableVolumeDHWTank_ConventionalControl and hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation < SetUpScenarios.maximumUsableVolumeDHWTank_ConventionalControl:
                        intendedModulationDegreeDHW = SetUpScenarios.minimalModulationdDegree_HP
                if hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation < SetUpScenarios.minimumUsableVolumeDHWTank_ConventionalControl:
                    intendedModulationDegreeForSpaceHeating = 0
                    intendedModulationDegreeDHW = 100
                if hypotheticalVolumeDHWTankWhenHeatingWithIntendedModulation > SetUpScenarios.maximumUsableVolumeDHWTank_ConventionalControl:
                    intendedModulationDegreeDHW = 0

                if hypotheticalTemperatureBufferStorageWhenHeatingWithMinimalModulation >= SetUpScenarios.maximumBufferStorageTemperature_ConventionalControl and hypotheticalVolumeDHWTankWhenHeatingWithMinimalModulation >= SetUpScenarios.maximumUsableVolumeDHWTank_ConventionalControl :
                    intendedModulationDegreeForSpaceHeating = 0
                    intendedModulationDegreeDHW = 0

                if intendedModulationDegreeForSpaceHeating > 0 and intendedModulationDegreeDHW > 0:
                    intendedModulationDegreeForSpaceHeating = 0


                # Adjust the heating at the end of the week if the storage values are too high
                if index_timeslot >= (SetUpScenarios.numberOfTimeSlotsPerWeek - 2 * Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek):
                    simulationResult_BufferStorageTemperature_BT2_Pre = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2_Pre  = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((intendedModulationDegreeDHW/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                    if bufferStorageIsHeatedUp and simulationResult_BufferStorageTemperature_BT2_Pre >SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue * 2:
                        intendedModulationDegreeForSpaceHeating =0
                    if dhwTankIsHeatedUp and simulationResult_UsableVolumeDHW_BT2_Pre > SetUpScenarios.initialUsableVolumeDHWTank + 2* SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        intendedModulationDegreeDHW =0


                #Calculate simulation values
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot - 1]  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_UsableVolumeDHW_BT2[index_week, index_BT2, index_timeslot-1] + ((intendedModulationDegreeDHW/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                    simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] = SetUpScenarios.initialUsableVolumeDHWTank + ((intendedModulationDegreeDHW/100 * cop_heatPump_DHW[index_timeslot] *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - df_buildingData ['DHW [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


                outputVector_BT2_heatGenerationCoefficientSpaceHeating_Conventional [index_BT2, index_timeslot] = intendedModulationDegreeForSpaceHeating/100
                outputVector_BT2_heatGenerationCoefficientDHW_Conventional [index_BT2, index_timeslot] = intendedModulationDegreeDHW/100


                simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + index_BT2)
                simulationResult_RESGeneration_BT2 [index_week, index_BT2, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + index_BT2) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine

                simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] = ( intendedModulationDegreeForSpaceHeating/100 + intendedModulationDegreeDHW/100 ) * SetUpScenarios.electricalPower_HP + df_buildingData ['Electricity [W]'] [index_timeslot + 1]
                simulationResult_SurplusPower_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_RESGeneration_BT2 [index_week, index_BT2, index_timeslot] - simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot]
                if simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] > simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]:
                    simulationResult_costs_BT2 [index_week, index_BT2, index_timeslot] = (simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] - simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] <= simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]:
                    simulationResult_costs_BT2 [index_week, index_BT2, index_timeslot] = (simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot] - simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)
                #Calculate the constraint violation
                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] >SetUpScenarios.maximalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] -SetUpScenarios.maximalBufferStorageTemperature
                if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] <SetUpScenarios.minimalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2, index_timeslot] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - SetUpScenarios.minimalBufferStorageTemperature

                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.maximumCapacityDHWTankOptimization:
                    simulation_ConstraintViolation_DHWTankRange_BT2  [index_week, index_BT2, index_timeslot] = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - SetUpScenarios.maximumCapacityDHWTankOptimization
                if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.minimumCapacityDHWTankOptimization:
                    simulation_ConstraintViolation_DHWTankRange_BT2  [index_week, index_BT2, index_timeslot] =  simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - SetUpScenarios.minimumCapacityDHWTankOptimization


                if intendedModulationDegreeForSpaceHeating > 0 and intendedModulationDegreeDHW >0:
                    simulation_ConstraintViolation_OnlyOneStorage_BT2 [index_week, index_BT2, index_timeslot] =1

                if (intendedModulationDegreeForSpaceHeating/100 < SetUpScenarios.minimalModulationdDegree_HP/100) and (intendedModulationDegreeForSpaceHeating/100>0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] = (SetUpScenarios.minimalModulationdDegree_HP/100) - intendedModulationDegreeForSpaceHeating

                if intendedModulationDegreeForSpaceHeating/100 > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] + intendedModulationDegreeForSpaceHeating/100 -1
                if (intendedModulationDegreeDHW/100 < (SetUpScenarios.minimalModulationdDegree_HP/100)) and (intendedModulationDegreeDHW/100 > 0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] +  (SetUpScenarios.minimalModulationdDegree_HP/100) - intendedModulationDegreeDHW/100
                if intendedModulationDegreeDHW/100 > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot] + intendedModulationDegreeDHW/100 - 1


                if index_timeslot >= 1:
                    if  outputVector_BT2_heatGenerationCoefficientSpaceHeating_Conventional [index_BT2, index_timeslot - 1] == 0 and intendedModulationDegreeForSpaceHeating/100 >0.001 :
                        simulationResult_numberOfStartsBufferStorage_BT2 [index_week, index_BT2] += 1
                    if outputVector_BT2_heatGenerationCoefficientDHW_Conventional [index_BT2, index_timeslot - 1] == 0 and intendedModulationDegreeDHW/100 >0.001 :
                        simulationResult_numberOfStartsDHWTank_BT2 [index_week, index_BT2] += 1

            # Set the values for the input parameters of the simulation (only used in the output .csv file)
            simulationInput_BT2_SpaceHeating [index_BT2, index_timeslot] = df_buildingData['Space Heating [W]'] [index_timeslot + 1]
            simulationInput_BT2_DHW [index_BT2, index_timeslot] = df_buildingData ['DHW [W]'] [index_timeslot + 1]
            simulationInput_BT2_electricityDemand [index_BT2, index_timeslot] = df_buildingData ['Electricity [W]'] [index_timeslot + 1]


            #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                total_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2] = total_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2] + abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2, index_timeslot])
                total_ConstraintViolation_DHWTankRange_BT2 [index_week, index_BT2] = total_ConstraintViolation_DHWTankRange_BT2 [index_week, index_BT2] + abs(simulation_ConstraintViolation_DHWTankRange_BT2 [index_week, index_BT2, index_timeslot])
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT2 [index_week, index_BT2] = simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue)
                    if  simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT2 [index_week, index_BT2] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue) - simulationResult_BufferStorageTemperature_BT2[index_week, index_BT2, index_timeslot]
                    if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        total_ConstraintViolation_DHWTankLastValue_BT2 [index_week, index_BT2] = simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] - ( SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue)
                    if simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot] < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue:
                        total_ConstraintViolation_DHWTankLastValue_BT2 [index_week, index_BT2] = (SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue) - simulationResult_UsableVolumeDHW_BT2 [index_week, index_BT2, index_timeslot]

                if intendedModulationDegreeForSpaceHeating > 0.0001 and intendedModulationDegreeDHW > 0.0001:
                    total_ConstraintViolation_OnlyOneStorage_BT2 [index_week, index_BT2] = total_ConstraintViolation_OnlyOneStorage_BT2 [index_week, index_BT2] + 1
                total_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2] = total_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2] + abs(simulation_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2, index_timeslot])
                if Run_Simulations.considerMaximumNumberOfStartsHP_Combined == True:
                    if simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] > (Run_Simulations.maximumNumberOfStarts_Combined + 1):
                        total_ConstraintViolation_numberOfStarts_Combined_BT2 [index_week, index_BT2] = simulationResult_numberOfStartsCombined_BT2 [index_week, index_BT2] - (Run_Simulations.maximumNumberOfStarts_Combined + 1)
                if Run_Simulations.considerMaxiumNumberOfStartsHP_Individual  == True:
                    if simulationResult_numberOfStartsBufferStorage_BT2 [index_week, index_BT2] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]  = simulationResult_numberOfStartsBufferStorage_BT2 [index_week, index_BT2] - Run_Simulations.maximumNumberOfStarts_Individual
                    if simulationResult_numberOfStartsDHWTank_BT2 [index_week, index_BT2] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]  = total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]+  simulationResult_numberOfStartsDHWTank_BT2 [index_week, index_BT2] - Run_Simulations.maximumNumberOfStarts_Individual


        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT2  [index_week, index_BT2, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT2  [index_week, index_BT2] = simulationObjective_surplusEnergyKWH_BT2  [index_week, index_BT2] + ((simulationResult_SurplusPower_BT2  [index_week, index_BT2, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] - simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]) > simulationObjective_maximumLoad_BT2 [index_week, index_BT2]:
                    simulationObjective_maximumLoad_BT2 [index_week, index_BT2] = simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot] -  simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]
                if (simulationResult_PVGeneration_BT2  [index_week, index_BT2, index_timeslot] -  simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot]) > simulationObjective_maximumLoad_BT2 [index_week, index_BT2]:
                    simulationObjective_maximumLoad_BT2 [index_week, index_BT2] = simulationResult_PVGeneration_BT2  [index_week, index_BT2, index_timeslot] -   simulationResult_electricalLoad_BT2[index_week, index_BT2, index_timeslot]
                simulationObjective_costs_BT2  [index_week, index_BT2]  = simulationObjective_costs_BT2  [index_week, index_BT2] +  simulationResult_costs_BT2 [index_week, index_BT2, index_timeslot]



         #Building Type 3
        for index_BT3 in range (0, len(indexOfBuildingsOverall_BT3)):
            #Reading of the data

            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT3_EV_SFH_1Minute_weeks/HH" + str(indexOfBuildingsOverall_BT3[index_BT3]) + "/HH" + str(indexOfBuildingsOverall_BT3[index_BT3]) + "_week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_weeks/Outside_Temperature_1Minute_week' +  str(currentweek) + '.csv', sep =";")

            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"

            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            for i in range (0, len(df_buildingData['Availability of the EV'])):
                if df_buildingData['Availability of the EV'] [i] > 0.1:
                    df_buildingData['Availability of the EV'] [i] = 1.0
                if df_buildingData['Availability of the EV'] [i] < 0.1 and df_buildingData['Availability of the EV'] [i] >0.01:
                    df_buildingData['Availability of the EV'] [i] = 0.0

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

            #Create availability array for the EV

            availabilityOfTheEV = np.zeros(( SetUpScenarios.numberOfTimeSlotsPerWeek))
            for index_timeslot_for_Availability in range (0,  SetUpScenarios.numberOfTimeSlotsPerWeek):
                availabilityOfTheEV [index_timeslot_for_Availability] = df_buildingData['Availability of the EV'] [index_timeslot_for_Availability +1]
            indexOfTheEV = SetUpScenarios.numberOfBuildings_BT1 +  index_BT3
            energyConsumptionOfEVs_Joule = SetUpScenarios.generateEVEnergyConsumptionPatterns(availabilityOfTheEV, indexOfTheEV)


            df_availabilityPatternEV = pd.DataFrame({'Timeslot': df_buildingData.index, 'Availability of the EV':df_buildingData['Availability of the EV'] })
            del df_availabilityPatternEV['Timeslot']

            df_energyConsumptionEV_Joule = pd.DataFrame({'Timeslot': df_buildingData.index, 'Energy':energyConsumptionOfEVs_Joule  })
            del df_energyConsumptionEV_Joule['Timeslot']
            df_energyConsumptionEV_Joule.index +=1


            #Wind generation

            indexBuildingForWindPowerAssignment = SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1

            #Round column and rename it
            df_buildingData['Electricity [W]'] = df_buildingData['Electricity [W]'].apply(lambda x: round(x, 2))

            # Set up inital values for the simulation
            simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, 0]= (SetUpScenarios.initialSOC_EV/100) * SetUpScenarios.capacityMaximal_EV
            simulationResult_SOCofEV_BT3 [index_week, index_BT3, 0]= SetUpScenarios.initialSOC_EV



            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):
                intendedPowerEVCharging = SetUpScenarios.chargingPowerMaximal_EV * (SetUpScenarios.modulationDegreeCharging_ConventionalControl/100) *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1]

                #Calculate hypothetical temperatures, volumes and the SOC of the EV
                if index_timeslot >=1:
                    hypotheticalEnergyLevelOfTheEV  =simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot - 1] + (  intendedPowerEVCharging *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    hypothetical_SOCofEV_BT3  = (hypotheticalEnergyLevelOfTheEV / SetUpScenarios.capacityMaximal_EV)*100


                if index_timeslot ==0:
                    hypotheticalEnergyLevelOfTheEV  = SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + ( intendedPowerEVCharging *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    hypothetical_SOCofEV_BT3  = (simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100


                # Adjust the charging Power of the EV if SOC is too high
                if hypothetical_SOCofEV_BT3 >= SetUpScenarios.initialSOC_EV:
                    intendedPowerEVCharging = 0


                #Calculate simulation values
                if index_timeslot >=1:
                    simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot]  =simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot - 1] + ( intendedPowerEVCharging *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]  = (simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalSOCDropWithNoCharging_BT3 [index_week, index_BT3] = hypotheticalSOCDropWithNoCharging_BT3 [index_week, index_BT3] + (df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]/ SetUpScenarios.capacityMaximal_EV)*100


                if index_timeslot ==0:
                    simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot]  = SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + ( intendedPowerEVCharging *  df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1] * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1])
                    simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]  = (simulationResult_energyLevelOfEV_BT3 [index_week, index_BT3, index_timeslot] / SetUpScenarios.capacityMaximal_EV)*100
                    hypotheticalSOCDropWithNoCharging_BT3 [index_week, index_BT3] = (df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]/ SetUpScenarios.capacityMaximal_EV)*100

                outputVector_BT3_chargingPowerEV_Conventional [index_BT3, index_timeslot] = intendedPowerEVCharging


                simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3)
                simulationResult_RESGeneration_BT3 [index_week, index_BT3, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT3) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine

                simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] =  intendedPowerEVCharging + df_buildingData ['Electricity [W]'] [index_timeslot + 1]
                simulationResult_SurplusPower_BT3 [index_week, index_BT3, index_timeslot] = simulationResult_RESGeneration_BT3 [index_week, index_BT3, index_timeslot] - simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot]
                if simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] > simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]:
                    simulationResult_costs_BT3 [index_week, index_BT3, index_timeslot] = (simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] - simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] <= simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]:
                    simulationResult_costs_BT3 [index_week, index_BT3, index_timeslot] = (simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot] - simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)

                #Calculate the constraint violation
                if  simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] < 0:
                    simulation_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3, index_timeslot] = simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]
                if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] >100:
                    simulation_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3, index_timeslot] =simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] - 100

                if intendedPowerEVCharging < 0:
                    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3, index_timeslot] = intendedPowerEVCharging
                if intendedPowerEVCharging > SetUpScenarios.chargingPowerMaximal_EV:
                    simulation_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3, index_timeslot] = intendedPowerEVCharging - SetUpScenarios.chargingPowerMaximal_EV

                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT3_availabilityPattern [index_BT3, index_timeslot] = df_availabilityPatternEV ["Availability of the EV"] [index_timeslot + 1]
                simulationInput_BT3_energyConsumptionOfTheEV [index_BT3, index_timeslot] = df_energyConsumptionEV_Joule["Energy"] [index_timeslot + 1]
                simulationInput_BT3_electricityDemand [index_BT3, index_timeslot] =  df_buildingData ['Electricity [W]'] [index_timeslot + 1]


            #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:

                    if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] > (SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue):
                        total_ConstraintViolation_SOCOfTheEVLastValue_BT3  [index_week, index_BT3] =  simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] - ((SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue))
                    if simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot] < (SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue):
                        total_ConstraintViolation_SOCOfTheEVLastValue_BT3  [index_week, index_BT3] = ((SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue)) - simulationResult_SOCofEV_BT3 [index_week, index_BT3, index_timeslot]



        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT3  [index_week, index_BT3, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT3  [index_week, index_BT3] = simulationObjective_surplusEnergyKWH_BT3  [index_week, index_BT3] + ((simulationResult_SurplusPower_BT3  [index_week, index_BT3, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] - simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]) > simulationObjective_maximumLoad_BT3 [index_week, index_BT3]:
                    simulationObjective_maximumLoad_BT3 [index_week, index_BT3] = simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot] -  simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]
                if (simulationResult_PVGeneration_BT3  [index_week, index_BT3, index_timeslot] -  simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot]) > simulationObjective_maximumLoad_BT3 [index_week, index_BT3]:
                    simulationObjective_maximumLoad_BT3 [index_week, index_BT3] = simulationResult_PVGeneration_BT3  [index_week, index_BT3, index_timeslot] -   simulationResult_electricalLoad_BT3[index_week, index_BT3, index_timeslot]
                simulationObjective_costs_BT3  [index_week, index_BT3]  = simulationObjective_costs_BT3  [index_week, index_BT3] +  simulationResult_costs_BT3 [index_week, index_BT3, index_timeslot]

        #Building Type 4
        for index_BT4 in range (0, len(indexOfBuildingsOverall_BT4)):
            #Reading of the data

            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT4_mHP_MFH_1Minute_Weeks/HH" + str(indexOfBuildingsOverall_BT4[index_BT4]) + "/HH" + str(indexOfBuildingsOverall_BT4[index_BT4]) + "_Week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_Weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_Week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_Weeks/Outside_Temperature_1Minute_Week' +  str(currentweek) + '.csv', sep =";")


            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"

            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()

            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')


            #Round column
            df_buildingData['Electricity [W]'] = df_buildingData['Electricity [W]'].apply(lambda x: round(x, 2))

            #Wind generation
            indexBuildingForWindPowerAssignment =  SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1

            cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP(df_outsideTemperatureData ["Temperature [C]"])

            bufferStorageIsHeatedUp = False


            #Calculate the simulation steps

            #ToDo: Add as parameter to the functiton

            updatingFrequencyEDFPrices = 1440/SetUpScenarios.timeResolution_InMinutes
            updatingFrequencyAverageTemperature = 1440 / SetUpScenarios.timeResolution_InMinutes

            helpCounterTimeSlotsForUpdatingEDFPrices  = 0
            helpCounterTimeSlotsForUpdatingAverageTemperature = 0
            helpCounterNumberOfRunningSlots = 0
            helpCounterNumberOfStandbySlots = 0

            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):

                if usePriceStorageControl == False:
                    if index_timeslot >=1:
                        # Calculate required heating power for keeping the temperature
                        targetTemperartueValue = SetUpScenarios.initialBufferStorageTemperature
                        if simulationResult_BufferStorageTemperature_BT4 [index_week, index_BT4, index_timeslot - 1] > SetUpScenarios.initialBufferStorageTemperature:
                            targetTemperartueValue = simulationResult_BufferStorageTemperature_BT4 [index_week, index_BT4, index_timeslot - 1]
                        if targetTemperartueValue >= SetUpScenarios.initialBufferStorageTemperature + 0.2:
                            targetTemperartueValue = SetUpScenarios.initialBufferStorageTemperature

                        requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel = ((targetTemperartueValue - simulationResult_BufferStorageTemperature_BT4 [index_week, index_BT4, index_timeslot - 1]) *(SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData['Space Heating [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesBufferStorage_BT4_MFH

                        if outputVector_BT4_heatGenerationCoefficientSpaceHeating_Conventional [index_BT4, index_timeslot - 1]  > 0:
                            bufferStorageIsHeatedUp = True

                        if outputVector_BT4_heatGenerationCoefficientSpaceHeating_Conventional [index_BT4, index_timeslot - 1]  ==0:
                            bufferStorageIsHeatedUp = False



                    if index_timeslot ==0:
                         bufferStorageIsHeatedUp = True
                         requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel = ((SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.initialBufferStorageTemperature) *(SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement) /SetUpScenarios.timeResolution_InMinutes * 60) + df_buildingData['Space Heating [W]'] [index_timeslot + 1] + SetUpScenarios.standingLossesBufferStorage_BT4_MFH

                    if index_timeslot >0:
                        if bufferStorageIsHeatedUp ==False:
                            if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1] <= SetUpScenarios.minimumBufferStorageTemperature_ConventionalControl:
                                bufferStorageIsHeatedUp = True



                    if bufferStorageIsHeatedUp == True:
                        requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel = (requiredHeatingPowerForKeepingTheTemperatureOfTheBufferStorageAtInitialLevel / (cop_heatPump_SpaceHeating[index_timeslot] * SetUpScenarios.electricalPower_HP_BT4_MFH))*100
                        intendedModulationDegreeForSpaceHeating = requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel
                        if requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel < SetUpScenarios.minimalModulationdDegree_HP:
                            intendedModulationDegreeForSpaceHeating = SetUpScenarios.minimalModulationdDegree_HP
                        if requiredModulatingDegreeofTheHeatPumpForKeepingTheTemperatureAtInitialLevel > 100:
                            intendedModulationDegreeForSpaceHeating = 100



                    #Calculate hypothetical temperatures, volumes
                    if index_timeslot >=1:
                        hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + (((intendedModulationDegreeForSpaceHeating/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                        hypotheticalTemperatureBufferStorageWhenHeatingWithMinimalModulation = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + (((SetUpScenarios.minimalModulationdDegree_HP/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))

                    if index_timeslot ==0:
                        hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation = SetUpScenarios.initialBufferStorageTemperature  + (((intendedModulationDegreeForSpaceHeating/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                        hypotheticalTemperatureBufferStorageWhenHeatingWithMinimalModulation = SetUpScenarios.initialBufferStorageTemperature  + (((SetUpScenarios.minimalModulationdDegree_HP/100) * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


                    #Adjust the intendedModulationDegrees when having reached the upper and lower limtis
                    if hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation < SetUpScenarios.minimumBufferStorageTemperature_ConventionalControl:
                        intendedModulationDegreeForSpaceHeating = 100
                    if hypotheticalTemperatureBufferStorageWhenHeatingWithIntendedModulation > SetUpScenarios.maximumBufferStorageTemperature_ConventionalControl:
                        intendedModulationDegreeForSpaceHeating = 0


                    # Adjust the heating at the end of the week if the storage values are too high
                    if index_timeslot >= (SetUpScenarios.numberOfTimeSlotsPerWeek - 2 * Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheWeek):
                        simulationResult_BufferStorageTemperature_BT4_Pre = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                        if simulationResult_BufferStorageTemperature_BT4_Pre >SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue * 2:
                            intendedModulationDegreeForSpaceHeating =0

                if usePriceStorageControl == True:
                    helpCounterTimeSlotsForUpdatingEDFPrices += 1
                    #Count number of running or standby slots
                    if index_timeslot >= 1:
                        if outputVector_BT4_heatGenerationCoefficientSpaceHeating_Conventional [index_BT4, index_timeslot - 1] >0.01:
                            helpCounterNumberOfRunningSlots += 1
                            helpCounterNumberOfStandbySlots = 0
                        else:
                            helpCounterNumberOfRunningSlots  = 0
                            helpCounterNumberOfStandbySlots += 1

                    #Calculate price factor

                    # Calculate empirial cumulative distribution function (ECDF) for the future prices
                    if index_timeslot == 0 or helpCounterTimeSlotsForUpdatingEDFPrices >= updatingFrequencyEDFPrices:
                        import statsmodels
                        from statsmodels.distributions.empirical_distribution import ECDF

                        electricityTarifCurrentweek = df_priceData.loc[index_timeslot: index_timeslot + (1440/SetUpScenarios.timeResolution_InMinutes) - 1, 'Price [Cent/kWh]'].values
                        ecdf_prices = ECDF(electricityTarifCurrentweek)


                    priceFactor = 1 - ecdf_prices (df_priceData.loc[index_timeslot + 1]- 0.001) #priceFactor = 1 - ecdf_prices (df_priceData.loc[index_timeslot + 1]- 0.001)


                    #Calculate the storage factor
                    if index_timeslot >=1:
                        storageFactor = 1 - (simulationResult_BufferStorageTemperature_BT4 [index_week, index_BT4, index_timeslot - 1] - SetUpScenarios.minimalBufferStorageTemperature) / (SetUpScenarios.maximalBufferStorageTemperature - SetUpScenarios.minimalBufferStorageTemperature)
                    else:
                        storageFactor = 0.5

                    #Calculate the average temperature of the current week

                    if index_timeslot == 0 or helpCounterTimeSlotsForUpdatingEDFPrices >= updatingFrequencyEDFPrices:

                        helpCounterTimeSlotsForUpdatingEDFPrices = 0
                        sumTemperature = 0
                        helpCounterTimeSlots = 0
                        for i in range (0, int((1440/SetUpScenarios.timeResolution_InMinutes))):
                            if index_timeslot + 1 + i < SetUpScenarios.numberOfTimeSlotsPerWeek:
                                sumTemperature = sumTemperature + df_outsideTemperatureData ["Temperature [C]"] [i + index_timeslot + 1]
                                helpCounterTimeSlots += 1
                        if helpCounterTimeSlots > 0:
                            averageTemperature = sumTemperature / helpCounterTimeSlots

                    #Set the modulation degree
                    intendedModulationDegreeForSpaceHeating = storageFactor * priceFactor * 100

                    # Make sure that the minimal modulation degree is not violated
                    if intendedModulationDegreeForSpaceHeating < SetUpScenarios.minimalModulationdDegree_HP and intendedModulationDegreeForSpaceHeating >= SetUpScenarios.minimalModulationdDegree_HP/2:
                        intendedModulationDegreeForSpaceHeating = SetUpScenarios.minimalModulationdDegree_HP

                    if intendedModulationDegreeForSpaceHeating < SetUpScenarios.minimalModulationdDegree_HP and intendedModulationDegreeForSpaceHeating < SetUpScenarios.minimalModulationdDegree_HP /2:
                        intendedModulationDegreeForSpaceHeating = 0


                    #Make sure that the minimal runntime and standby time are not violated
                    if intendedModulationDegreeForSpaceHeating == 0 and helpCounterNumberOfRunningSlots > 0 and helpCounterNumberOfRunningSlots < 30/SetUpScenarios.timeResolution_InMinutes:
                        intendedModulationDegreeForSpaceHeating = SetUpScenarios.minimalModulationdDegree_HP
                    if intendedModulationDegreeForSpaceHeating > 0 and helpCounterNumberOfStandbySlots >0 and helpCounterNumberOfStandbySlots < 30/SetUpScenarios.timeResolution_InMinutes:
                        intendedModulationDegreeForSpaceHeating = 0


                    #Add internal control rule for temperatures around the limits
                    if storageFactor >= 0.96 and intendedModulationDegreeForSpaceHeating < SetUpScenarios.minimalModulationdDegree_HP:
                        intendedModulationDegreeForSpaceHeating =SetUpScenarios.minimalModulationdDegree_HP
                    if storageFactor >= 0.98 and intendedModulationDegreeForSpaceHeating < SetUpScenarios.minimalModulationdDegree_HP *2:
                        intendedModulationDegreeForSpaceHeating = SetUpScenarios.minimalModulationdDegree_HP * 2
                    if storageFactor >= 1:
                        intendedModulationDegreeForSpaceHeating = 100
                    if storageFactor < 0.04:
                        intendedModulationDegreeForSpaceHeating = 0



                    #Correct constraint violations
                    if intendedModulationDegreeForSpaceHeating > 100:
                        intendedModulationDegreeForSpaceHeating = 100
                    if intendedModulationDegreeForSpaceHeating <0:
                        intendedModulationDegreeForSpaceHeating = 0


                    simulationResult_priceFactor_BT4 [index_week, index_BT4, index_timeslot] = priceFactor
                    simulationResult_storageFactor_BT4  [index_week, index_BT4, index_timeslot] =  storageFactor
                    simulationResult_averageTemperature_BT4 [index_week, index_BT4, index_timeslot] =  averageTemperature


                #Calculate simulation values
                if index_timeslot >=1:
                    simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot - 1]  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))

                if index_timeslot ==0:
                    simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] = SetUpScenarios.initialBufferStorageTemperature  + ((intendedModulationDegreeForSpaceHeating/100 * cop_heatPump_SpaceHeating[index_timeslot] *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - df_buildingData['Space Heating [W]'] [index_timeslot + 1]  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


                outputVector_BT4_heatGenerationCoefficientSpaceHeating_Conventional [index_BT4, index_timeslot] = intendedModulationDegreeForSpaceHeating/100


                simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4)
                simulationResult_RESGeneration_BT4 [index_week, index_BT4, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + SetUpScenarios.numberOfBuildings_BT3 + index_BT4) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine

                simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] = ( intendedModulationDegreeForSpaceHeating/100 ) * SetUpScenarios.electricalPower_HP_BT4_MFH + df_buildingData ['Electricity [W]'] [index_timeslot + 1]
                simulationResult_SurplusPower_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_RESGeneration_BT4 [index_week, index_BT4, index_timeslot] - simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot]
                if simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] > simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]:
                    simulationResult_costs_BT4 [index_week, index_BT4, index_timeslot] = (simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] - simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] <= simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]:
                    simulationResult_costs_BT4 [index_week, index_BT4, index_timeslot] = (simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot] - simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)


                #Calculate the constraint violation
                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] >SetUpScenarios.maximalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] -SetUpScenarios.maximalBufferStorageTemperature
                if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] <SetUpScenarios.minimalBufferStorageTemperature:
                    simulation_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4, index_timeslot] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - SetUpScenarios.minimalBufferStorageTemperature

                if (intendedModulationDegreeForSpaceHeating/100 < SetUpScenarios.minimalModulationdDegree_HP/100) and (intendedModulationDegreeForSpaceHeating/100>0.0001):
                    simulation_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4, index_timeslot] = (SetUpScenarios.minimalModulationdDegree_HP/100) - intendedModulationDegreeForSpaceHeating

                if intendedModulationDegreeForSpaceHeating/100 > 1:
                    simulation_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4, index_timeslot] =  simulation_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4, index_timeslot] + intendedModulationDegreeForSpaceHeating/100 -1


                if index_timeslot >= 1:
                    if  outputVector_BT4_heatGenerationCoefficientSpaceHeating_Conventional [index_BT4, index_timeslot - 1] == 0 and intendedModulationDegreeForSpaceHeating/100 >0.001 :
                        simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] += 1

                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT4_SpaceHeating [index_BT4, index_timeslot] = df_buildingData['Space Heating [W]'] [index_timeslot + 1]
                simulationInput_BT4_electricityDemand [index_BT4, index_timeslot] = df_buildingData ['Electricity [W]'] [index_timeslot + 1]

            #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                total_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4] = total_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4] + abs(simulation_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4, index_timeslot])
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 [index_week, index_BT4] = simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] - (SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue)
                    if  simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot] < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue :
                        total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 [index_week, index_BT4] =  (SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue) - simulationResult_BufferStorageTemperature_BT4[index_week, index_BT4, index_timeslot]

                total_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4] = total_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4] + abs(simulation_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4, index_timeslot])
                if Run_Simulations.considerMaxiumNumberOfStartsHP_MFH_Individual == True:
                    if simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] > Run_Simulations.maximumNumberOfStarts_Individual:
                        total_ConstraintViolation_numberOfStarts_Individual_BT4 [index_week, index_BT4]  = simulationResult_numberOfStartsBufferStorage_BT4 [index_week, index_BT4] - Run_Simulations.maximumNumberOfStarts_Individual


        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT4  [index_week, index_BT4, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT4  [index_week, index_BT4] = simulationObjective_surplusEnergyKWH_BT4  [index_week, index_BT4] + ((simulationResult_SurplusPower_BT4  [index_week, index_BT4, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] - simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]) > simulationObjective_maximumLoad_BT4 [index_week, index_BT4]:
                    simulationObjective_maximumLoad_BT4 [index_week, index_BT4] = simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot] -  simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]
                if (simulationResult_PVGeneration_BT4  [index_week, index_BT4, index_timeslot] -  simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot]) > simulationObjective_maximumLoad_BT4 [index_week, index_BT4]:
                    simulationObjective_maximumLoad_BT4 [index_week, index_BT4] = simulationResult_PVGeneration_BT4  [index_week, index_BT4, index_timeslot] -   simulationResult_electricalLoad_BT4[index_week, index_BT4, index_timeslot]
                simulationObjective_costs_BT4  [index_week, index_BT4]  = simulationObjective_costs_BT4  [index_week, index_BT4] +  simulationResult_costs_BT4 [index_week, index_BT4, index_timeslot]

        #Building Type 5
        for index_BT5 in range (0, len(indexOfBuildingsOverall_BT5)):

            #Reading of the data

            df_buildingData_original = pd.read_csv("C:/Users/wi9632/Desktop/Daten/DSM/BT5_BAT_SFH_1Minute_weeks/HH" + str(indexOfBuildingsOverall_BT5[index_BT5]) + "/HH" + str(indexOfBuildingsOverall_BT5[index_BT5]) + "_week" + str(currentweek) +".csv", sep =";")
            df_priceData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Price_1Minute_weeks/' + SetUpScenarios.typeOfPriceData +'/Price_' + SetUpScenarios.typeOfPriceData +'_1Minute_week' +  str(currentweek) + '.csv', sep =";")
            df_outsideTemperatureData_original = pd.read_csv('C:/Users/wi9632/Desktop/Daten/DSM/Outside_Temperature_1Minute_weeks/Outside_Temperature_1Minute_week' +  str(currentweek) + '.csv', sep =";")

            #Rename column 'Demand Electricity [W]' to 'Electricity [W]' if it exists
            if 'Demand Electricity [W]' in df_buildingData_original:
                df_buildingData_original.rename(columns={'Demand Electricity [W]': 'Electricity [W]'}, inplace=True)


            #Adjust dataframes to the current time resolution and set new index "Timeslot"

            df_buildingData_original['Time'] = pd.to_datetime(df_buildingData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_buildingData = df_buildingData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()



            arrayTimeSlots = [i for i in range (1,SetUpScenarios.numberOfTimeSlotsPerWeek + 1)]
            df_buildingData['Timeslot'] = arrayTimeSlots
            df_buildingData = df_buildingData.set_index('Timeslot')

            df_priceData_original['Time'] = pd.to_datetime(df_priceData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_priceData = df_priceData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_priceData['Timeslot'] = arrayTimeSlots
            df_priceData = df_priceData.set_index('Timeslot')

            df_outsideTemperatureData_original['Time'] = pd.to_datetime(df_outsideTemperatureData_original['Time'], format = '%d.%m.%Y %H:%M')
            df_outsideTemperatureData = df_outsideTemperatureData_original.set_index('Time').resample(str(SetUpScenarios.timeResolution_InMinutes) +'Min').mean()
            df_outsideTemperatureData['Timeslot'] = arrayTimeSlots
            df_outsideTemperatureData = df_outsideTemperatureData.set_index('Timeslot')

            #Wind generation

            indexBuildingForWindPowerAssignment = SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT5
            windProfileNominal = SetUpScenarios.calculateAssignedWindPowerNominalPerBuilding (currentweek,indexBuildingForWindPowerAssignment)
            df_windPowerAssignedNominalPerBuilding = pd.DataFrame({'Timeslot': df_buildingData.index, 'Wind [nominal]':windProfileNominal })
            del df_windPowerAssignedNominalPerBuilding['Timeslot']
            df_windPowerAssignedNominalPerBuilding.index +=1

            #Round column and rename it
            df_buildingData['Electricity [W]'] = df_buildingData['Electricity [W]'].apply(lambda x: round(x, 2))

            helpCurrentPeakLoadOfTheweek =0


            #Calculate the simulation steps
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek):

                #Assign the values for the PV generation
                simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT5)
                simulationResult_RESGeneration_BT5 [index_week, index_BT5, index_timeslot] = df_buildingData ['PV [nominal]'] [index_timeslot + 1] * SetUpScenarios.determinePVPeakOfBuildings(SetUpScenarios.numberOfBuildings_BT1 + SetUpScenarios.numberOfBuildings_BT2 + index_BT5) + df_windPowerAssignedNominalPerBuilding ["Wind [nominal]"] [index_timeslot + 1] * SetUpScenarios.maximalPowerOfWindTurbine

                #Charge battery if PV generation is higher than electrical demand
                if  df_buildingData['Electricity [W]'] [index_timeslot+1] < simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]:
                    outputVector_BT5_chargingPowerBAT_Conventional [ index_BT5, index_timeslot] =  simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot] - df_buildingData['Electricity [W]'] [index_timeslot+1]
                    # Correct the values if SOC is as its upper limit
                    if index_timeslot >= 1:
                        simulationResult_energyLevelOfBAT_BT5_hypothetical   =simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot - 1] + ((outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot]  * (SetUpScenarios.chargingEfficiency_BAT) - outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )
                        simulationResult_SOCofBAT_BT5_hypothetical  = (simulationResult_energyLevelOfBAT_BT5_hypothetical / SetUpScenarios.capacityMaximal_BAT)*100
                    if index_timeslot ==0:
                        simulationResult_energyLevelOfBAT_BT5_hypothetical   =SetUpScenarios.capacityMaximal_BAT * (SetUpScenarios.initialSOC_BAT/100) + ((outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot]  * (SetUpScenarios.chargingEfficiency_BAT) - outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )
                        simulationResult_SOCofBAT_BT5_hypothetical  = (simulationResult_energyLevelOfBAT_BT5_hypothetical / SetUpScenarios.capacityMaximal_BAT)*100
                    if simulationResult_SOCofBAT_BT5_hypothetical > 100.01:
                        outputVector_BT5_chargingPowerBAT_Conventional[index_BT5, index_timeslot] = (((100 - simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot - 1])/100) * SetUpScenarios. capacityMaximal_BAT) / (SetUpScenarios.timeResolution_InMinutes * 60)


                    #Correct the values if charging power is too high
                    if outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot] > SetUpScenarios.chargingPowerMaximal_BAT:
                        outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot] = SetUpScenarios.chargingPowerMaximal_BAT

                #Discharge the battery if PV generation is smaller than electrical demand and if the battery is not empty
                if index_timeslot >= 1:
                    if df_buildingData['Electricity [W]'] [index_timeslot+1] >= simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot] and simulationResult_energyLevelOfBAT_BT5 [index_week , index_BT5, index_timeslot - 1] > 0.1:
                        outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] = (df_buildingData['Electricity [W]'] [index_timeslot+1] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot])
                        # Correct the values if they are higher than the energy in the battery
                        if outputVector_BT5_disChargingPowerBAT_Conventional [ index_BT5, index_timeslot] > simulationResult_energyLevelOfBAT_BT5 [index_week , index_BT5, index_timeslot- 1]/ (SetUpScenarios.timeResolution_InMinutes * 60):
                            outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] = simulationResult_energyLevelOfBAT_BT5 [index_week , index_BT5, index_timeslot- 1]/ (SetUpScenarios.timeResolution_InMinutes * 60 * (1 /SetUpScenarios.dischargingEfficiency_BAT))

                if index_timeslot == 0:
                    if df_buildingData['Electricity [W]'] [index_timeslot+1] >= simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot] and SetUpScenarios.capacityMaximal_BAT * (SetUpScenarios.initialSOC_BAT/100)  > 0.1:
                        outputVector_BT5_disChargingPowerBAT_Conventional [ index_BT5, index_timeslot] = (df_buildingData['Electricity [W]'] [index_timeslot+1] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot])
                        # Correct the values if they are higher than the energy in the battery
                        if outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] > (SetUpScenarios.capacityMaximal_BAT * (simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot - 1] )) / (SetUpScenarios.timeResolution_InMinutes * 60):
                            outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] = (SetUpScenarios.capacityMaximal_BAT * (simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot - 1])) / (SetUpScenarios.timeResolution_InMinutes * 60 * (1 /SetUpScenarios.dischargingEfficiency_BAT))

                # Correct the values if disCharging power is too high
                if outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] > SetUpScenarios.chargingPowerMaximal_BAT:
                    outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] = SetUpScenarios.chargingPowerMaximal_BAT


                #Calculate the simulation values
                if index_timeslot >=1:

                    simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot]  =simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot - 1] + ((outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot]  * (SetUpScenarios.chargingEfficiency_BAT) - outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )
                    simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]  = (simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot] / SetUpScenarios.capacityMaximal_BAT)*100

                if index_timeslot ==0:
                    simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot]  =(SetUpScenarios.initialSOC_BAT/100) * SetUpScenarios.capacityMaximal_BAT + ((outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot] * (SetUpScenarios.chargingEfficiency_BAT) - outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )
                    simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]  = (simulationResult_energyLevelOfBAT_BT5 [index_week, index_BT5, index_timeslot] / SetUpScenarios.capacityMaximal_BAT)*100


                simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] =  outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot] - outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] + df_buildingData ['Electricity [W]'] [index_timeslot + 1]
                simulationResult_SurplusPower_BT5 [index_week, index_BT5, index_timeslot] = simulationResult_RESGeneration_BT5 [index_week, index_BT5, index_timeslot] - simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot]

                if simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] > simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]:
                    simulationResult_costs_BT5 [index_week, index_BT5, index_timeslot] = (simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
                if simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] <= simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]:
                    simulationResult_costs_BT5 [index_week, index_BT5, index_timeslot] = (simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot] - simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)

                # Set the values for the input parameters of the simulation (only used in the output .csv file)
                simulationInput_BT5_electricityDemand [index_BT5, index_timeslot] =  df_buildingData ['Electricity [W]'] [index_timeslot + 1]


                #Calculate the constraint violation

                if  simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] < 0:
                    simulation_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]
                if simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] >100:
                    simulation_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] =simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] - 100

                if outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot] < 0:
                    simulation_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot]
                if outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot] > SetUpScenarios.chargingPowerMaximal_BAT:
                    simulation_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = outputVector_BT5_chargingPowerBAT_Conventional [index_BT5, index_timeslot] - SetUpScenarios.chargingPowerMaximal_BAT

                if outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] < 0:
                    simulation_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot]
                if outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] > df_buildingData ['Electricity [W]'] [index_timeslot + 1]:
                    simulation_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot] = outputVector_BT5_disChargingPowerBAT_Conventional [index_BT5, index_timeslot] - df_buildingData ['Electricity [W]'] [index_timeslot + 1]


        #Calculate the total constraint violations
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if index_timeslot == SetUpScenarios.numberOfTimeSlotsPerWeek - 1:
                    if simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] > (SetUpScenarios.initialSOC_BAT + SetUpScenarios.endSOC_BATAllowedDeviationFromInitalValueUpperLimit):
                        total_ConstraintViolation_SOCOfTheBATLastValue_BT5  [index_week, index_BT5] =  simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] - ((SetUpScenarios.initialSOC_BAT + SetUpScenarios.endSOC_BATAllowedDeviationFromInitalValueUpperLimit))
                    if simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot] < (SetUpScenarios.initialSOC_BAT - SetUpScenarios.endSOC_BATAllowedDeviationFromInitalValueLowerLimit):
                        total_ConstraintViolation_SOCOfTheBATLastValue_BT5  [index_week, index_BT5] = ((SetUpScenarios.initialSOC_BAT - SetUpScenarios.endSOC_BATAllowedDeviationFromInitalValueLowerLimit)) - simulationResult_SOCofBAT_BT5 [index_week, index_BT5, index_timeslot]

                total_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5] =  total_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5] + abs(simulation_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5, index_timeslot])
                total_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5] = total_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5] + abs (simulation_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot])
                total_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5] = total_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5] + abs (simulation_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5, index_timeslot])


        # Calculate the objectives
            for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
                if simulationResult_SurplusPower_BT5  [index_week, index_BT5, index_timeslot] > 0:
                    simulationObjective_surplusEnergyKWH_BT5  [index_week, index_BT5] = simulationObjective_surplusEnergyKWH_BT5  [index_week, index_BT5] + ((simulationResult_SurplusPower_BT5  [index_week, index_BT5, index_timeslot] * SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
                if (simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] - simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]) > simulationObjective_maximumLoad_BT5 [index_week, index_BT5]:
                    simulationObjective_maximumLoad_BT5 [index_week, index_BT5] = simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot] -  simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]
                if (simulationResult_PVGeneration_BT5  [index_week, index_BT5, index_timeslot] -  simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot]) > simulationObjective_maximumLoad_BT5 [index_week, index_BT5]:
                    simulationObjective_maximumLoad_BT5 [index_week, index_BT5] = simulationResult_PVGeneration_BT5  [index_week, index_BT5, index_timeslot] -   simulationResult_electricalLoad_BT5[index_week, index_BT5, index_timeslot]
                simulationObjective_costs_BT5  [index_week, index_BT5]  = simulationObjective_costs_BT5  [index_week, index_BT5] +  simulationResult_costs_BT5 [index_week, index_BT5, index_timeslot]





        # Calculate values for all buildings combined
        for index_timeslot in range (0, SetUpScenarios.numberOfTimeSlotsPerWeek ):
            for index_BT1 in range (0, len(indexOfBuildingsOverall_BT1)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT1 [index_week, index_BT1, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT1 [index_week, index_BT1, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT1 [index_week, index_BT1, index_timeslot]
            for index_BT2 in range (0, len(indexOfBuildingsOverall_BT2)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT2 [index_week, index_BT2, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT2 [index_week, index_BT2, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT2 [index_week, index_BT2, index_timeslot]
            for index_BT3 in range (0, len(indexOfBuildingsOverall_BT3)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT3 [index_week, index_BT3, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT3 [index_week, index_BT3, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT3 [index_week, index_BT3, index_timeslot]
            for index_BT4 in range (0, len(indexOfBuildingsOverall_BT4)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT4 [index_week, index_BT4, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT4 [index_week, index_BT4, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT4 [index_week, index_BT4, index_timeslot]
            for index_BT5 in range (0, len(indexOfBuildingsOverall_BT5)):
                simulationResult_electricalLoad_combined [index_week, index_timeslot] = simulationResult_electricalLoad_combined [index_week, index_timeslot] + simulationResult_electricalLoad_BT5 [index_week, index_BT5, index_timeslot]
                simulationResult_RESGeneration_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] + simulationResult_RESGeneration_BT5 [index_week, index_BT5, index_timeslot]
                simulationResult_PVGeneration_combined [index_week, index_timeslot] = simulationResult_PVGeneration_combined [index_week, index_timeslot] + simulationResult_PVGeneration_BT5 [index_week, index_BT5, index_timeslot]



            simulationResult_SurplusEnergy_combined [index_week, index_timeslot] = simulationResult_RESGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week, index_timeslot]
            if simulationResult_electricalLoad_combined [index_week,index_timeslot] > simulationResult_PVGeneration_combined [index_week, index_timeslot]:
               simulationResult_costs_combined [index_week, index_timeslot] = (simulationResult_electricalLoad_combined [index_week, index_timeslot] - simulationResult_PVGeneration_combined [index_week, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (df_priceData ['Price [Cent/kWh]'] [index_timeslot + 1]/3600000)
            if simulationResult_electricalLoad_combined [index_week, index_timeslot] <= simulationResult_PVGeneration_combined [index_week, index_timeslot]:
               simulationResult_costs_combined [index_week, index_timeslot] = (simulationResult_PVGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week, index_timeslot]) * SetUpScenarios.timeResolution_InMinutes * 60 * (SetUpScenarios.revenueForFeedingBackElecticityIntoTheGrid_CentsPerkWh/3600000)


            #Calculate the objectives for all buidlings combined
            if simulationResult_RESGeneration_combined [index_week, index_timeslot] > simulationResult_electricalLoad_combined [index_week,index_timeslot]:
                simulationObjective_surplusEnergy_kWh_combined [index_week] =  simulationObjective_surplusEnergy_kWh_combined [index_week] +  (simulationResult_RESGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week,index_timeslot]) * ((SetUpScenarios.timeResolution_InMinutes * 60) /3600000)
            simulationObjective_costs_Euro_combined [index_week] =simulationObjective_costs_Euro_combined [index_week] + simulationResult_costs_combined [index_week, index_timeslot]
            if (simulationResult_electricalLoad_combined [index_week, index_timeslot]  > simulationResult_PVGeneration_combined [index_week, index_timeslot]) and (simulationResult_electricalLoad_combined [index_week, index_timeslot]  - simulationResult_PVGeneration_combined [index_week, index_timeslot])> simulationObjective_maximumLoad_kW_combined [index_week]:
                simulationObjective_maximumLoad_kW_combined [index_week] = simulationResult_electricalLoad_combined [index_week, index_timeslot]  - simulationResult_PVGeneration_combined [index_week, index_timeslot]
            if (simulationResult_electricalLoad_combined [index_week, index_timeslot]  <= simulationResult_PVGeneration_combined [index_week, index_timeslot]) and ( simulationResult_PVGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week, index_timeslot])> simulationObjective_maximumLoad_kW_combined [index_week]:
                simulationObjective_maximumLoad_kW_combined [index_week] = simulationResult_PVGeneration_combined [index_week, index_timeslot] - simulationResult_electricalLoad_combined [index_week, index_timeslot]

           #Calculate the combined score
            if Run_Simulations.optimization_1Objective == True:

               if Run_Simulations.optimizationGoal_minimizeSurplusEnergy == True:
                   simulationObjective_combinedScore_combined [index_week] = simulationObjective_surplusEnergy_kWh_combined [index_week]
               if Run_Simulations.optimizationGoal_minimizePeakLoad == True:
                   simulationObjective_combinedScore_combined [index_week] = simulationObjective_maximumLoad_kW_combined [index_week]
               if Run_Simulations.optimizationGoal_minimizeCosts == True:
                  simulationObjective_combinedScore_combined [index_week] = simulationObjective_costs_Euro_combined [index_week]

            if Run_Simulations.optimization_2Objective == True:

               if (Run_Simulations.optimizationGoal_minimizeSurplusEnergy == True and Run_Simulations.optimizationGoal_minimizePeakLoad == True):
                   simulationObjective_combinedScore_combined [index_week] = Run_Simulations.objective_minimizePeakLoad_weight*(simulationObjective_maximumLoad_kW_combined [index_week]/Run_Simulations.objective_minimizePeakLoad_normalizationValue) + Run_Simulations.objective_minimizeSurplusEnergy_weight * (simulationObjective_surplusEnergy_kWh_combined/Run_Simulations.objective_minimizeSurplusEnergy_normalizationValue)
               if (Run_Simulations.optimizationGoal_minimizeSurplusEnergy == True and Run_Simulations.optimizationGoal_minimizeCosts == True):
                   simulationObjective_combinedScore_combined [index_week] = Run_Simulations.objective_minimizeCosts_weight *(simulationObjective_costs_Euro_combined [index_week]/Run_Simulations.objective_minimizeCosts_normalizationValue) + Run_Simulations.objective_minimizeSurplusEnergy_weight * (simulationObjective_surplusEnergy_kWh_combined/Run_Simulations.objective_minimizeSurplusEnergy_normalizationValue)
               if (Run_Simulations.optimizationGoal_minimizePeakLoad == True and Run_Simulations.optimizationGoal_minimizeCosts == True):
                   simulationObjective_combinedScore_combined [index_week] = Run_Simulations.objective_minimizeCosts_weight *(simulationObjective_costs_Euro_combined [index_week]/Run_Simulations.objective_minimizeCosts_normalizationValue) +  Run_Simulations.objective_minimizeCosts_weight *(simulationObjective_costs_Euro_combined [index_week]/Run_Simulations.objective_minimizeCosts_normalizationValue)

            if Run_Simulations.optimization_3Objectives == True:
                simulationObjective_combinedScore_combined [index_week] = Run_Simulations.objective_minimizePeakLoad_weight*(simulationObjective_maximumLoad_kW_combined [index_week]/Run_Simulations.objective_minimizePeakLoad_normalizationValue) + Run_Simulations.objective_minimizeSurplusEnergy_weight * (simulationObjective_surplusEnergy_kWh_combined/Run_Simulations.objective_minimizeSurplusEnergy_normalizationValue) + Run_Simulations.objective_minimizeCosts_weight *(simulationObjective_costs_Euro_combined [index_week]/Run_Simulations.objective_minimizeCosts_normalizationValue)

    #Convert and round values of the objectives
    simulationObjective_maximumLoad_kW_combined [index_week] = simulationObjective_maximumLoad_kW_combined [index_week]  /1000
    simulationObjective_maximumLoad_kW_combined [index_week]  = round(simulationObjective_maximumLoad_kW_combined [index_week],2)
    simulationObjective_costs_Euro_combined [index_week] =  simulationObjective_costs_Euro_combined [index_week] /100
    simulationObjective_costs_Euro_combined [index_week] =  round(simulationObjective_costs_Euro_combined [index_week],2)
    simulationObjective_surplusEnergy_kWh_combined [index_week] =  round(simulationObjective_surplusEnergy_kWh_combined [index_week],2)

    #Calculate constraint violation for all buildings combined
    for index_BT1 in range (0, len(indexOfBuildingsOverall_BT1)):
        total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_BT1 [index_week, index_BT1]
        total_ConstraintViolation_DHWTankRange_combined [index_week] = total_ConstraintViolation_DHWTankRange_combined [index_week] + total_ConstraintViolation_DHWTankRange_BT1 [index_week, index_BT1]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] +  total_ConstraintViolation_BufferStorageTemperatureLastValue_BT1 [index_week, index_BT1]
        total_ConstraintViolation_DHWTankLastValue_combined [index_week] = total_ConstraintViolation_DHWTankLastValue_combined [index_week] + total_ConstraintViolation_DHWTankLastValue_BT1 [index_week, index_BT1]
        total_ConstraintViolation_OnlyOneStorage_combined [index_week] = total_ConstraintViolation_OnlyOneStorage_combined [index_week] + total_ConstraintViolation_OnlyOneStorage_BT1 [index_week, index_BT1]
        total_ConstraintViolation_MinimalModulationDegree_combined [index_week] = total_ConstraintViolation_MinimalModulationDegree_combined [index_week] + total_ConstraintViolation_MinimalModulationDegree_BT1 [index_week, index_BT1]
        total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week]  = total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] + total_ConstraintViolation_SOCRangeOfTheEV_BT1 [index_week, index_BT1]
        total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week]  = total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] + total_ConstraintViolation_SOCOfTheEVLastValue_BT1 [index_week, index_BT1]
        total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] = total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] +total_ConstraintViolation_ChargingPowerOfTheEV_BT1 [index_week, index_BT1]
        total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] = total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] + total_ConstraintViolation_numberOfStarts_Individual_BT1 [index_week, index_BT1]
        total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] = total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] + total_ConstraintViolation_numberOfStarts_Combined_BT1 [index_week, index_BT1]
        hypotheticalSOCDropWithNoCharging_combined [index_week] = hypotheticalSOCDropWithNoCharging_combined [index_week] +  hypotheticalSOCDropWithNoCharging_BT1 [index_week, index_BT1]
    for index_BT2 in range (0, len(indexOfBuildingsOverall_BT2)):
        total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_BT2 [index_week, index_BT2]
        total_ConstraintViolation_DHWTankRange_combined [index_week] = total_ConstraintViolation_DHWTankRange_combined [index_week] + total_ConstraintViolation_DHWTankRange_BT2 [index_week, index_BT2]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] +  total_ConstraintViolation_BufferStorageTemperatureLastValue_BT2 [index_week, index_BT2]
        total_ConstraintViolation_DHWTankLastValue_combined [index_week] = total_ConstraintViolation_DHWTankLastValue_combined [index_week] + total_ConstraintViolation_DHWTankLastValue_BT2 [index_week, index_BT2]
        total_ConstraintViolation_OnlyOneStorage_combined [index_week] = total_ConstraintViolation_OnlyOneStorage_combined [index_week] + total_ConstraintViolation_OnlyOneStorage_BT2 [index_week, index_BT2]
        total_ConstraintViolation_MinimalModulationDegree_combined [index_week] = total_ConstraintViolation_MinimalModulationDegree_combined [index_week] + total_ConstraintViolation_MinimalModulationDegree_BT2 [index_week, index_BT2]
        total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] = total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] + total_ConstraintViolation_numberOfStarts_Individual_BT2 [index_week, index_BT2]
        total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] = total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] + total_ConstraintViolation_numberOfStarts_Combined_BT2 [index_week, index_BT2]
    for index_BT3 in range (0, len(indexOfBuildingsOverall_BT3)):
        total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week]  = total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] + total_ConstraintViolation_SOCRangeOfTheEV_BT3 [index_week, index_BT3]
        total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week]  = total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] + total_ConstraintViolation_SOCOfTheEVLastValue_BT3 [index_week, index_BT3]
        total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] = total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] +total_ConstraintViolation_ChargingPowerOfTheEV_BT3 [index_week, index_BT3]
        hypotheticalSOCDropWithNoCharging_combined [index_week] = hypotheticalSOCDropWithNoCharging_combined [index_week] +  hypotheticalSOCDropWithNoCharging_BT3 [index_week, index_BT3]
    for index_BT4 in range (0, len(indexOfBuildingsOverall_BT4)):
        total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] = total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] + total_ConstraintViolation_BufferStorageTemperatureRange_BT4 [index_week, index_BT4]
        total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] =  total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] +  total_ConstraintViolation_BufferStorageTemperatureLastValue_BT4 [index_week, index_BT4]
        total_ConstraintViolation_MinimalModulationDegree_combined [index_week] = total_ConstraintViolation_MinimalModulationDegree_combined [index_week] + total_ConstraintViolation_MinimalModulationDegree_BT4 [index_week, index_BT4]
        total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] = total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] + total_ConstraintViolation_numberOfStarts_Individual_BT4 [index_week, index_BT4]
    for index_BT5 in range (0, len(indexOfBuildingsOverall_BT5)):
        total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week]  = total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week] + total_ConstraintViolation_SOCRangeOfTheBAT_BT5 [index_week, index_BT5]
        total_ConstraintViolation_SOCOfTheBATLastValue_combined [index_week]  = total_ConstraintViolation_SOCOfTheBATLastValue_combined [index_week] + total_ConstraintViolation_SOCOfTheBATLastValue_BT5 [index_week, index_BT5]
        total_ConstraintViolation_ChargingPowerOfTheBAT_combined [index_week] = total_ConstraintViolation_ChargingPowerOfTheBAT_combined [index_week] + total_ConstraintViolation_disChargingPowerOfTheBAT_BT5 [index_week, index_BT5] + total_ConstraintViolation_ChargingPowerOfTheBAT_BT5 [index_week, index_BT5]



    #Print results (constraint violations and objectives)
    print("Possible constraint violations:")
    if total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] > 0.09:
       print ("total_ConstraintViolation_BufferStorageTemperatureRange_combined: " + str(round(total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_DHWTankRange_combined [index_week] >0.1:
       print("total_ConstraintViolation_DHWTankRange_combined: " + str(round(total_ConstraintViolation_DHWTankRange_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] >0.09:
       print("total_ConstraintViolation_BufferStorageTemperatureLastValue_combined: ", str(round(total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_OnlyOneStorage_combined [index_week] >0.1:
       print("total_ConstraintViolation_OnlyOneStorage_combined: " + str(round(total_ConstraintViolation_OnlyOneStorage_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_MinimalModulationDegree_combined [index_week] >0.2:
       print("total_ConstraintViolation_MinimalModulationDegree_combined: " + str(round(total_ConstraintViolation_MinimalModulationDegree_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] >0.1:
       print("total_ConstraintViolation_SOCOfTheEVLastValue_combined: " + str(round(total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] >0.1:
       print("total_ConstraintViolation_SOCOfTheEVLastValue_combined: " + str(round(total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week] >1:
       print("total_ConstraintViolation_ChargingPowerOfTheEV_combined: " + str(round(total_ConstraintViolation_ChargingPowerOfTheEV_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_numberOfStarts_Individual_combined [index_week] >0.01:
       print("total_ConstraintViolation_numberOfStarts_Individual_combined: " + str(round(total_ConstraintViolation_numberOfStarts_Individual_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] >0.01:
       print("total_ConstraintViolation_numberOfStarts_Combined_combined: " + str(round(total_ConstraintViolation_numberOfStarts_Combined_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week] >1:
       print("total_ConstraintViolation_SOCRangeOfTheBAT_combined: " + str(round(total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_SOCOfTheBATLastValue_combined [index_week] >0.01:
       print("total_ConstraintViolation_SOCOfTheBATLastValue_combined: " + str(round(total_ConstraintViolation_SOCOfTheBATLastValue_combined [index_week], 2)) + "\n")
    if total_ConstraintViolation_ChargingPowerOfTheBAT_combined [index_week] >0.01:
       print("total_ConstraintViolation_ChargingPowerOfTheBAT_combined: " + str(round(total_ConstraintViolation_ChargingPowerOfTheBAT_combined [index_week], 2)) + "\n")



    #Calculate the negative score due to constraint violations


    #total_ConstraintViolation_BufferStorageTemperatureRange_combined
    averageDeviationPerTimeSlot_BufferStorageTemperatureRange_combined = total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] / SetUpScenarios.numberOfTimeSlotsPerWeek
    allowedTemperatureRange = SetUpScenarios.maximalBufferStorageTemperature - SetUpScenarios.minimalBufferStorageTemperature
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] = ((100/allowedTemperatureRange) * averageDeviationPerTimeSlot_BufferStorageTemperatureRange_combined)/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_DHWTankRange_combined
    averageDeviationPerTimeSlot_DHWTankRange_combined = total_ConstraintViolation_DHWTankRange_combined [index_week]  / SetUpScenarios.numberOfTimeSlotsPerWeek
    allowedVolumeRange = SetUpScenarios.maximumCapacityDHWTankOptimization -  SetUpScenarios.minimumCapacityDHWTankOptimization
    negativeScore_total_ConstraintViolation_DHWTankRange_combined [index_week] = ((100/allowedVolumeRange) * averageDeviationPerTimeSlot_DHWTankRange_combined)/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_BufferStorageTemperatureLastValue_combined
    negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] = ((100/allowedTemperatureRange) * total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week])/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_DHWTankLastValue_combined
    negativeScore_total_ConstraintViolation_DHWTankLastValue_combined [index_week] = ((100/allowedVolumeRange) * total_ConstraintViolation_DHWTankLastValue_combined [index_week] )/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_SOCOfTheEV_combined
    negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] = (total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week])/SetUpScenarios.numberOfBuildings_Total

    #total_ConstraintViolation_SOCOfTheEVLastValue_combined
    if hypotheticalSOCDropWithNoCharging_combined [index_week] == 0:
        negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] =0
    else:
        negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] = (100/hypotheticalSOCDropWithNoCharging_combined [index_week])* (total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week])
        if np.isnan(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week]) == True:
            negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] =0

    #total_ConstraintViolation_SOCOfTheBAT_combined
    negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week] = (total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week])/SetUpScenarios.numberOfBuildings_Total
    if np.isnan(negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week]) == True:
        negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week] =0



    #total_ConstraintViolation_numberOfStarts_Combined_combined
    negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined [index_week] = (total_ConstraintViolation_numberOfStarts_Combined_combined [index_week])/SetUpScenarios.numberOfBuildings_Total

     #total negative score
    negativeScore_total_overall [index_week] = Run_Simulations.weight_total_ConstraintViolation_BufferStorageTemperatureRange_combined * negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined * negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_DHWTankRange_combined * negativeScore_total_ConstraintViolation_DHWTankRange_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_DHWTankLastValue_combined * negativeScore_total_ConstraintViolation_DHWTankLastValue_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_SOCRangeOfTheEV_combined * negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_SOCOfTheEVLastValue_combined * negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week] + Run_Simulations.weight_total_ConstraintViolation_numberOfStarts_Combined_combined * negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined [index_week]  + Run_Simulations.weight_total_ConstraintViolation_SOCRangeOfTheBAT_combined * negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week]

    print("")
    print("Negative Scores")
    print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined: ", round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_DHWTankRange_combined: ", round(negativeScore_total_ConstraintViolation_DHWTankRange_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined: ", round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_DHWTankLastValue_combined: ", round(negativeScore_total_ConstraintViolation_DHWTankLastValue_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined: ", round(negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined: ", round(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined: ", round(negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined [index_week], 3))
    print("negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined: ", round(negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week], 3))
    print("")
    print("negativeScore_total_overall: ", round(negativeScore_total_overall [index_week], 3))
    print("")


    print("")
    print("Objectives" + "\n" + "\n")
    print("Consider objective Surplus Energy: " + str(Run_Simulations.optimizationGoal_minimizeSurplusEnergy))
    print("Consider objective Peak Load: " + str(Run_Simulations.optimizationGoal_minimizePeakLoad))
    print("Consider objective Costs: " + str(Run_Simulations.optimizationGoal_minimizeCosts) + "\n")
    print("Objective Surplus Energy [kWh]: " + str(round(simulationObjective_surplusEnergy_kWh_combined [index_week], 1)) )
    print("Objective Peak Load [kW]: " + str(round(simulationObjective_maximumLoad_kW_combined [index_week], 2)))
    print("Objective Costs [Euro]: " + str(round(simulationObjective_costs_Euro_combined [index_week], 2)) )
    print("Objective Score: " + str(round(simulationObjective_combinedScore_combined [index_week]/100, 2)))
    print("")


    #Write result data into files

    #BT1
    for i in range (0, SetUpScenarios.numberOfBuildings_BT1):


        df_resultingProfiles_BT1 = pd.DataFrame({'heatGenerationCoefficientSpaceHeating': outputVector_BT1_heatGenerationCoefficientSpaceHeating_Conventional[i, :],'heatGenerationCoefficientDHW': outputVector_BT1_heatGenerationCoefficientDHW_Conventional[i, :],'chargingPowerEV': outputVector_BT1_chargingPowerEV_Conventional[i, :], 'temperatureBufferStorage': simulationResult_BufferStorageTemperature_BT1[0,i, :], 'usableVolumeDHWTank': simulationResult_UsableVolumeDHW_BT1[0,i, :], 'simulationResult_SOCofEV': simulationResult_SOCofEV_BT1[0,i, :], 'simulationResult_energyLevelOfEV': simulationResult_energyLevelOfEV_BT1[0,i, :], 'simulationResult_PVGeneration': simulationResult_PVGeneration_BT1[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT1[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT1[0,i, :],  'Space Heating [W]': simulationInput_BT1_SpaceHeating [i, :], 'DHW [W]': simulationInput_BT1_DHW [i, :], 'Electricity [W]': simulationInput_BT1_electricityDemand [i, :], 'Availability of the EV': simulationInput_BT1_availabilityPattern [i, :],'Energy Consumption of the EV':simulationInput_BT1_energyConsumptionOfTheEV [i, :], 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT1[0,i, :], 'simulationResult_costs': simulationResult_costs_BT1[0,i, :]})
        #Round values
        df_resultingProfiles_BT1 ['heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_BT1 ['heatGenerationCoefficientSpaceHeating'].round(2)
        df_resultingProfiles_BT1 ['heatGenerationCoefficientDHW'] = df_resultingProfiles_BT1 ['heatGenerationCoefficientDHW'].round(2)
        df_resultingProfiles_BT1 ['chargingPowerEV'] = df_resultingProfiles_BT1 ['chargingPowerEV'].round(2)
        df_resultingProfiles_BT1 ['temperatureBufferStorage'] = df_resultingProfiles_BT1 ['temperatureBufferStorage'].round(2)
        df_resultingProfiles_BT1 ['usableVolumeDHWTank'] = df_resultingProfiles_BT1 ['usableVolumeDHWTank'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_SOCofEV'] = df_resultingProfiles_BT1 ['simulationResult_SOCofEV'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_energyLevelOfEV'] = df_resultingProfiles_BT1 ['simulationResult_energyLevelOfEV'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT1 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT1 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_costs'] = df_resultingProfiles_BT1 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT1 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT1 ['simulationResult_RESGeneration'].round(2)
        df_resultingProfiles_BT1 ['Space Heating [W]'] = df_resultingProfiles_BT1 ['Space Heating [W]'].round(1)
        df_resultingProfiles_BT1 ['DHW [W]'] = df_resultingProfiles_BT1 ['DHW [W]'].round(1)
        df_resultingProfiles_BT1 ['Electricity [W]'] = df_resultingProfiles_BT1 ['Electricity [W]'].round(1)

        df_resultingProfiles_BT1.index += 1
        df_resultingProfiles_BT1.index.name = 'timeslot'
        df_resultingProfiles_BT1.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT1), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT1.to_csv(pathForCreatingTheResultData + "/BT1_HH" + str(i + 1) + ".csv", index=True,  sep =";")


    #BT2
    for i in range (0, SetUpScenarios.numberOfBuildings_BT2):
        df_resultingProfiles_BT2 = pd.DataFrame({'heatGenerationCoefficientSpaceHeating': outputVector_BT2_heatGenerationCoefficientSpaceHeating_Conventional[i, :],'heatGenerationCoefficientDHW': outputVector_BT2_heatGenerationCoefficientDHW_Conventional[i, :], 'temperatureBufferStorage': simulationResult_BufferStorageTemperature_BT2[0,i, :], 'usableVolumeDHWTank': simulationResult_UsableVolumeDHW_BT2[0,i, :],  'simulationResult_PVGeneration': simulationResult_PVGeneration_BT2[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT2[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT2[0,i, :], 'Space Heating [W]': simulationInput_BT2_SpaceHeating [i, :], 'DHW [W]': simulationInput_BT2_DHW [i, :], 'Electricity [W]': simulationInput_BT2_electricityDemand [i, :] , 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT2[0,i, :], 'simulationResult_costs': simulationResult_costs_BT2[0,i, :]})
        #Round values
        df_resultingProfiles_BT2 ['heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_BT2 ['heatGenerationCoefficientSpaceHeating'].round(2)
        df_resultingProfiles_BT2 ['heatGenerationCoefficientDHW'] = df_resultingProfiles_BT2 ['heatGenerationCoefficientDHW'].round(2)
        df_resultingProfiles_BT2 ['temperatureBufferStorage'] = df_resultingProfiles_BT2 ['temperatureBufferStorage'].round(2)
        df_resultingProfiles_BT2 ['usableVolumeDHWTank'] = df_resultingProfiles_BT2 ['usableVolumeDHWTank'].round(2)
        df_resultingProfiles_BT2 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT2 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT2 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT2 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT2 ['simulationResult_costs'] = df_resultingProfiles_BT2 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT2 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT2 ['simulationResult_RESGeneration'].round(2)
        df_resultingProfiles_BT2 ['Space Heating [W]'] = df_resultingProfiles_BT2 ['Space Heating [W]'].round(1)
        df_resultingProfiles_BT2 ['DHW [W]'] = df_resultingProfiles_BT2 ['DHW [W]'].round(1)
        df_resultingProfiles_BT2 ['Electricity [W]'] = df_resultingProfiles_BT2 ['Electricity [W]'].round(1)

        df_resultingProfiles_BT2.index += 1
        df_resultingProfiles_BT2.index.name = 'timeslot'
        df_resultingProfiles_BT2.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT2), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT2.to_csv(pathForCreatingTheResultData + "/BT2_HH" + str(i + 1) + ".csv", index=True,  sep =";")

    #BT3
    for i in range (0, SetUpScenarios.numberOfBuildings_BT3):
        df_resultingProfiles_BT3 = pd.DataFrame({'chargingPowerEV': outputVector_BT3_chargingPowerEV_Conventional[i, :],  'simulationResult_SOCofEV': simulationResult_SOCofEV_BT3[0,i, :], 'simulationResult_energyLevelOfEV': simulationResult_energyLevelOfEV_BT3[0,i, :], 'simulationResult_PVGeneration': simulationResult_PVGeneration_BT3[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT3[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT3[0,i, :], 'Electricity [W]': simulationInput_BT3_electricityDemand [i, :], 'Availability of the EV': simulationInput_BT3_availabilityPattern [i, :],'Energy Consumption of the EV':simulationInput_BT3_energyConsumptionOfTheEV [i, :] , 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT3[0,i, :], 'simulationResult_costs': simulationResult_costs_BT3[0,i, :]})
        #Round values
        df_resultingProfiles_BT3 ['chargingPowerEV'] = df_resultingProfiles_BT3 ['chargingPowerEV'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_SOCofEV'] = df_resultingProfiles_BT3 ['simulationResult_SOCofEV'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_energyLevelOfEV'] = df_resultingProfiles_BT3 ['simulationResult_energyLevelOfEV'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT3 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT3 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_costs'] = df_resultingProfiles_BT3 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT3 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT3 ['simulationResult_RESGeneration'].round(2)
        df_resultingProfiles_BT3 ['Electricity [W]'] = df_resultingProfiles_BT3 ['Electricity [W]'].round(1)

        df_resultingProfiles_BT3.index += 1
        df_resultingProfiles_BT3.index.name = 'timeslot'
        df_resultingProfiles_BT3.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT3), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT3.to_csv(pathForCreatingTheResultData + "/BT3_HH" + str(i + 1) + ".csv", index=True,  sep =";")


    #BT4
    for i in range (0, SetUpScenarios.numberOfBuildings_BT4):
        df_resultingProfiles_BT4 = pd.DataFrame({'heatGenerationCoefficientSpaceHeating': outputVector_BT4_heatGenerationCoefficientSpaceHeating_Conventional[i, :], 'temperatureBufferStorage': simulationResult_BufferStorageTemperature_BT4[0,i, :], 'simulationResult_PVGeneration': simulationResult_PVGeneration_BT4[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT4[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT4[0,i, :] , 'Space Heating [W]': simulationInput_BT4_SpaceHeating [i, :],  'Electricity [W]': simulationInput_BT4_electricityDemand [i, :] , 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT4[0,i, :], 'simulationResult_costs': simulationResult_costs_BT4[0,i, :], 'priceFactor': simulationResult_priceFactor_BT4[0,i, :], 'storageFactor': simulationResult_storageFactor_BT4[0,i, :], 'averageTemperature': simulationResult_averageTemperature_BT4 [0,i, :]})
        #Round values
        df_resultingProfiles_BT4 ['heatGenerationCoefficientSpaceHeating'] = df_resultingProfiles_BT4 ['heatGenerationCoefficientSpaceHeating'].round(2)
        df_resultingProfiles_BT4 ['temperatureBufferStorage'] = df_resultingProfiles_BT4 ['temperatureBufferStorage'].round(2)
        df_resultingProfiles_BT4 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT4 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT4 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT4 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT4 ['simulationResult_costs'] = df_resultingProfiles_BT4 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT4 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT4 ['simulationResult_RESGeneration'].round(2)
        df_resultingProfiles_BT4 ['Space Heating [W]'] = df_resultingProfiles_BT4 ['Space Heating [W]'].round(1)
        df_resultingProfiles_BT4 ['Electricity [W]'] = df_resultingProfiles_BT4 ['Electricity [W]'].round(1)
        df_resultingProfiles_BT4 ['priceFactor'] = df_resultingProfiles_BT4 ['priceFactor'].round(2)
        df_resultingProfiles_BT4 ['storageFactor'] = df_resultingProfiles_BT4 ['storageFactor'].round(2)
        df_resultingProfiles_BT4 ['averageTemperature'] = df_resultingProfiles_BT4 ['averageTemperature'].round(1)

        df_resultingProfiles_BT4.index += 1
        df_resultingProfiles_BT4.index.name = 'timeslot'
        df_resultingProfiles_BT4.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT4), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT4.to_csv(pathForCreatingTheResultData + "/BT4_HH" + str(i + 1) + ".csv", index=True,  sep =";")

    #BT5
    for i in range (0, SetUpScenarios.numberOfBuildings_BT5):
        df_resultingProfiles_BT5 = pd.DataFrame({'chargingPowerBAT': outputVector_BT5_chargingPowerBAT_Conventional[i, :], 'disChargingPowerBAT': outputVector_BT5_disChargingPowerBAT_Conventional[i, :],  'simulationResult_SOCofBAT': simulationResult_SOCofBAT_BT5[0,i, :], 'simulationResult_energyLevelOfBAT': simulationResult_energyLevelOfBAT_BT5[0,i, :], 'simulationResult_PVGeneration': simulationResult_PVGeneration_BT5[0,i, :], 'simulationResult_RESGeneration': simulationResult_RESGeneration_BT5[0,i, :], 'simulationResult_electricalLoad': simulationResult_electricalLoad_BT5[0,i, :] , 'Electricity [W]': simulationInput_BT5_electricityDemand [i, :] , 'simulationResult_SurplusPower': simulationResult_SurplusPower_BT5[0,i, :], 'simulationResult_costs': simulationResult_costs_BT5[0,i, :], 'Outside Temperature [C]': df_outsideTemperatureData['Temperature [C]'], 'Price [Cent/kWh]': df_priceData['Price [Cent/kWh]']})
        #Round values
        df_resultingProfiles_BT5 ['chargingPowerBAT'] = df_resultingProfiles_BT5 ['chargingPowerBAT'].round(2)
        df_resultingProfiles_BT5 ['disChargingPowerBAT'] = df_resultingProfiles_BT5 ['disChargingPowerBAT'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_SOCofBAT'] = df_resultingProfiles_BT5 ['simulationResult_SOCofBAT'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_energyLevelOfBAT'] = (df_resultingProfiles_BT5 ['simulationResult_energyLevelOfBAT']/3600000).round(2)
        df_resultingProfiles_BT5 ['simulationResult_PVGeneration'] = df_resultingProfiles_BT5 ['simulationResult_PVGeneration'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_electricalLoad'] = df_resultingProfiles_BT5 ['simulationResult_electricalLoad'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_costs'] = df_resultingProfiles_BT5 ['simulationResult_costs'].round(2)
        df_resultingProfiles_BT5 ['simulationResult_RESGeneration'] = df_resultingProfiles_BT5 ['simulationResult_RESGeneration'].round(2)
        df_resultingProfiles_BT5 ['Electricity [W]'] = df_resultingProfiles_BT5 ['Electricity [W]'].round(1)

        df_resultingProfiles_BT5.index += 1
        df_resultingProfiles_BT5.index.name = 'timeslot'
        df_resultingProfiles_BT5.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_BT5), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
        df_resultingProfiles_BT5.to_csv(pathForCreatingTheResultData + "/BT5_HH" + str(i + 1) + ".csv", index=True,  sep =";")




    #Combined results for the whole residential area
    df_resultingProfiles_combined = pd.DataFrame({'simulationResult_electricalLoad_combined': simulationResult_electricalLoad_combined[0, :],'simulationResult_RESGeneration_combined': simulationResult_RESGeneration_combined[0, :],'simulationResult_PVGeneration_combined': simulationResult_PVGeneration_combined[0, :], 'simulationResult_SurplusEnergy_combined': simulationResult_SurplusEnergy_combined[0, :], 'simulationResult_costs_combined': simulationResult_costs_combined[0, :]})
    df_resultingProfiles_combined ['simulationResult_electricalLoad_combined'] =df_resultingProfiles_combined ['simulationResult_electricalLoad_combined'].round(2)
    df_resultingProfiles_combined ['simulationResult_RESGeneration_combined'] =df_resultingProfiles_combined ['simulationResult_RESGeneration_combined'].round(2)
    df_resultingProfiles_combined ['simulationResult_PVGeneration_combined'] =df_resultingProfiles_combined ['simulationResult_PVGeneration_combined'].round(2)
    df_resultingProfiles_combined ['simulationResult_SurplusEnergy_combined'] =df_resultingProfiles_combined ['simulationResult_SurplusEnergy_combined'].round(2)
    df_resultingProfiles_combined ['simulationResult_costs_combined'] =df_resultingProfiles_combined ['simulationResult_costs_combined'].round(2)



    df_resultingProfiles_combined.index.name = 'timeslot'
    df_resultingProfiles_combined.index +=1
    df_resultingProfiles_combined.insert(0, 'time of week', pd.date_range('1970-1-1', periods=len(df_resultingProfiles_combined), freq=str(SetUpScenarios.timeResolution_InMinutes) + 'min').strftime('%H:%M'))
    df_resultingProfiles_combined.to_csv (pathForCreatingTheResultData + "/wholeResidentialArea.csv", index=True,  sep =";")


    #Print results into file
    filename = pathForCreatingTheResultData + "/Results.txt"
    with open(filename, 'w') as f:
        print("Objectives" + "\n" + "\n")
        print("Consider objective Surplus Energy: " + str(Run_Simulations.optimizationGoal_minimizeSurplusEnergy), file = f)
        print("Consider objective Peak Load: " + str(Run_Simulations.optimizationGoal_minimizePeakLoad), file = f)
        print("Consider objective Costs: " + str(Run_Simulations.optimizationGoal_minimizeCosts) + "\n", file = f)
        print("Objective Surplus Energy [kWh]: " + str(round(simulationObjective_surplusEnergy_kWh_combined [index_week], 2)) , file = f)
        print("Objective Peak Load [kW]: " + str(round(simulationObjective_maximumLoad_kW_combined [index_week], 2)), file = f)
        print("Objective Costs [Euro]: " + str(round(simulationObjective_costs_Euro_combined [index_week], 2)), file = f)
        print("Objective Score: " + str(round(simulationObjective_combinedScore_combined [index_week], 2)), file = f)
        print("", file = f)
        print("", file = f)
        print("", file = f)
        print("Negative Scores", file = f)
        print("", file = f)
        print("", file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined: ", round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankRange_combined: ", round(negativeScore_total_ConstraintViolation_DHWTankRange_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankLastValue_combined: ",round(negativeScore_total_ConstraintViolation_DHWTankLastValue_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined: ",round(negativeScore_total_ConstraintViolation_SOCRangeOfTheEV_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined: ",round(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined: ",round(negativeScore_total_ConstraintViolation_SOCRangeOfTheBAT_combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined: ",round(negativeScore_total_ConstraintViolation_numberOfStarts_Combined_combined [index_week], 3), file = f)
        print("", file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_DHWTankRange_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureRange_PhysicalLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined: ", round(negativeScore_total_ConstraintViolation_DHWTankRange_PhysicalLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_BufferStorageTemperatureLastValue_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_DHWTankLastValue_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined: ",round(negativeScore_total_ConstraintViolation_SOCOfTheEVLastValue_CorrectionLimit_Combined [index_week], 3), file = f)
        print("negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined: ",round(negativeScore_total_ConstraintViolation_numberOfStarts_CorrectionLimit_Combined_Combined [index_week], 3), file = f)
        print("negativeScore_total_overall: ",round(negativeScore_total_overall [index_week], 3), file = f)
        print("", file = f)
        print("", file = f)
        print("", file = f)



    return simulationObjective_surplusEnergy_kWh_combined , simulationObjective_maximumLoad_kW_combined, simulationObjective_costs_Euro_combined, simulationObjective_combinedScore_combined, negativeScore_total_overall
    #End method



#'''


def simulateTimeSlot_WithAddtionalController_BT1 (overruleActions, action_SpaceHeating, action_DHWHeating, action_EVCharging, state_BufferStorageTemperatureLastTimeSlot,
                                                 state_usableVolumeDHWLastTimeSlot, state_SOCofEVLastTimeSlot, helpCountNumberOfStartsIndividual_SpaceHeating,
                                                 helpCountNumberOfStartsIndividual_DHW, helpCountNumberOfStarts_Combined , helpCounterNumberOfRunningSlots_SpaceHeating , helpCounterNumberOfRunningSlots_DHW ,
                                                 helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating , helpCounterNumberOfStandBySlots_DHW ,
                                                 helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, helpStoppedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit,
                                                 index_timeslot, outsideTemperature, PVGeneration, heatDemand, DHWDemand,electricityDemand, availabilityOfTheEV, priceForElectricity_CentsPerkWh, energyDemandEV, cop_SpaceHeating, cop_DHW,
                                                 helpPVGenerationPreviousTimeSlot, helpElectricalLoadPreviousTimeSlot, helpHypotheticalSOCDropNoCharging, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped,
                                                 heatingStartedPhysicalLimit_BufferStorage, heatingStartedPhysicalLimit_DHWTank,startedHeatingSpaceHeatingCorrection_end, startedHeatingDHWCorrection_end, help_bothStorageHeatedUp_lastTimeBufferStorageOverruled, help_bothStorageHeatedUp_lastTimeDHWOverruled):

    action_SpaceHeating_NotOverruled = action_SpaceHeating
    action_DHWHeating_NotOverruled = action_DHWHeating
    action_EVCharging_NotOverruled = action_EVCharging


    print("")
    print("------------------------------------------")
    print("")
    print("Beginning IC; Timeslot: ", index_timeslot + 1)
    print("")
    print("helpCountNumberOfStarts_Combined: ", helpCountNumberOfStarts_Combined)
    print(f"state_BufferStorageTemperatureLastTimeSlot: {state_BufferStorageTemperatureLastTimeSlot}")
    print(f"state_usableVolumeDHWLastTimeSlot: {state_usableVolumeDHWLastTimeSlot}")
    #Calculate the simulation steps



    if helpStartedHeatingHeatPump == True and helpCounterNumberOfRunningSlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
        helpStartedHeatingHeatPump = False
    if helpStoppedHeatingHeatPump == True and helpCounterNumberOfStandBySlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
        helpStoppedHeatingHeatPump = False

    if numberOfHeatPumpStartsReachedHardLimit == True:
        numberOfHeatPumpStartsReachedSoftLimit = False


    # Pre-Corrections of input values: too high or low input values
    if action_SpaceHeating  > 1:
        action_SpaceHeating  =1
    if action_DHWHeating  > 1:
        action_DHWHeating =1
    if action_EVCharging > SetUpScenarios.chargingPowerMaximal_EV:
        action_EVCharging = SetUpScenarios.chargingPowerMaximal_EV

    if action_SpaceHeating  < 0:
        action_SpaceHeating  =0
    if action_DHWHeating  <  0:
        action_DHWHeating =0
    if action_EVCharging < 0:
        action_EVCharging = 0



     # Pre-Corrections of input values: heating up only one storage at one time
    if action_SpaceHeating > 0.001 and action_DHWHeating  > 0.001:
        print("Pre_Correction Only one storage. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating)  + "\n")
        if help_bothStorageHeatedUp_lastTimeBufferStorageOverruled== True:
            action_DHWHeating = 0
            help_bothStorageHeatedUp_lastTimeBufferStorageOverruled = False
            help_bothStorageHeatedUp_lastTimeDHWOverruled = True
        elif help_bothStorageHeatedUp_lastTimeDHWOverruled == True:
            action_SpaceHeating = 0
            help_bothStorageHeatedUp_lastTimeBufferStorageOverruled = True
            help_bothStorageHeatedUp_lastTimeDHWOverruled = False


    #Pre-Corrections: Set small heating values to 0
    if action_SpaceHeating > 0 and action_SpaceHeating < 0.1:
        action_SpaceHeating = 0

    if action_DHWHeating > 0 and action_DHWHeating < 0.1:
        action_DHWHeating = 0


    # Pre-Corrections of input values: minimal modulation
    if action_SpaceHeating > 0.001 and action_SpaceHeating  < SetUpScenarios.minimalModulationdDegree_HP/100:
        print("Pre_Correction: Min Modulation. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + "\n")
        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100

    if action_DHWHeating > 0.001 and action_DHWHeating  < SetUpScenarios.minimalModulationdDegree_HP/100:
        print("Pre_Correction: Min Modulation. Time: " +  str(index_timeslot) + "; ANN value DHW: " + str(action_DHWHeating) + "\n")
        action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP/100




     # Pre_Corrections for the availability of the EV (charging is only possible if the EV is available at the charging station of the building)
    if action_EVCharging > 0.001 and  availabilityOfTheEV ==0:
        action_EVCharging =0
        print("Pre_Correction EV is not available for charging: " +  str(index_timeslot))

    if  helpCountNumberOfStarts_Combined >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts_BeforeConsideringMinimalRuntime:
        numberOfHeatPumpStartsReachedSoftLimit = True

    if helpCountNumberOfStarts_Combined >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts - 2:
        numberOfHeatPumpStartsReachedHardLimit = True
        numberOfHeatPumpStartsReachedSoftLimit = False


    #Calculate the hypothetical simulation values if the non-corrected actions were applied
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT1  = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT1= state_usableVolumeDHWLastTimeSlot + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        simulationResult_SOCofEV_BT1   = state_SOCofEVLastTimeSlot + (( ( action_EVCharging *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - energyDemandEV)) /SetUpScenarios.capacityMaximal_EV)*100
    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT1 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT1 = SetUpScenarios.initialUsableVolumeDHWTank + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        simulationResult_SOCofEV_BT1   = SetUpScenarios.initialSOC_EV + (( ( action_EVCharging *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - energyDemandEV)) /SetUpScenarios.capacityMaximal_EV)*100


    print("")
    print(f"action_DHWHeating: {action_DHWHeating}")
    print(f"simulationResult_UsableVolumeDHW_BT1: {simulationResult_UsableVolumeDHW_BT1}")
    print("")


    # Calculate the maximum power of the heat pump and the EV for not creating a new peak load
    if index_timeslot >=1:
        if (helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot
        if (helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot

    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP
    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP
    maximumPowerEVChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_EV

    if (action_SpaceHeating + action_DHWHeating) * SetUpScenarios.electricalPower_HP + action_EVCharging + electricityDemand > PVGeneration:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = helpCurrentPeakLoad - action_EVCharging - electricityDemand  + PVGeneration
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = helpCurrentPeakLoad - action_EVCharging - electricityDemand  + PVGeneration
        maximumPowerEVChargingForNotCreatingANewPeak = helpCurrentPeakLoad  - electricityDemand  + PVGeneration - (action_SpaceHeating + action_DHWHeating) * SetUpScenarios.electricalPower_HP

    if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek > SetUpScenarios.electricalPower_HP:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP
    if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek > SetUpScenarios.electricalPower_HP:
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP

    if  maximumPowerEVChargingForNotCreatingANewPeak >  SetUpScenarios.chargingPowerMaximal_EV:
        maximumPowerEVChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_EV

    if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP
    if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP:
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek =Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP
    if  maximumPowerEVChargingForNotCreatingANewPeak < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection *  SetUpScenarios.chargingPowerMaximal_EV:
        maximumPowerEVChargingForNotCreatingANewPeak = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.chargingPowerMaximal_EV


    #Corrections due to violations of the temperature and volume constraints
    if simulationResult_UsableVolumeDHW_BT1 <= SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
        action_DHWHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
        action_SpaceHeating = 0
        print("Correction volume too low DHW (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
    if simulationResult_UsableVolumeDHW_BT1 >= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
        helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        if helpCounterNumberOfStandBySlots_Combined >0:
            helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        if action_DHWHeating > 0.001 and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod < SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit  and (numberOfHeatPumpStartsReachedSoftLimit == False or helpStoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
           action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP/100
           print("Correction DHW too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
        else:
            action_DHWHeating = 0
            print("Correction DHW volume too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")

    if simulationResult_BufferStorageTemperature_BT1 > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:

        helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        if helpCounterNumberOfStandBySlots_Combined >0:
            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        if action_SpaceHeating > 0.001 and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod < SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and (numberOfHeatPumpStartsReachedSoftLimit == False or helpStoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
           action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
           print("Correction BufferStorage too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
        else:
           action_SpaceHeating = 0
           print("Correction BufferStorage too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")

    if simulationResult_BufferStorageTemperature_BT1 < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary and simulationResult_UsableVolumeDHW_BT1 > SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
        action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
        action_DHWHeating = 0
        print("Correction BufferStorage too low (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")


    # Corrections due to minimal modulation degree of the heat pump
    if action_SpaceHeating > 0.001 and action_SpaceHeating < SetUpScenarios.minimalModulationdDegree_HP /100:
        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP /100
        print("Correction Minimal Mod. SpaceHeating. Time: " +  str(index_timeslot) + "; ANN value: " + str(action_SpaceHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
    if action_DHWHeating > 0.001 and action_DHWHeating < SetUpScenarios.minimalModulationdDegree_HP /100:
        action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP /100
        print("Correction Minimal Mod. DHW. Time: " +  str(index_timeslot) + "; ANN value: " + str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")

    # Corrections for the SOC of the EV
    if simulationResult_SOCofEV_BT1 > 100:
        action_EVCharging = 0




    #Calculate the hypothetical simulation values if the  corrected actions were applied
    cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP_SingleTimeSlot(outsideTemperature)
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT1 = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT1 = state_usableVolumeDHWLastTimeSlot + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT1 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT1 = SetUpScenarios.initialUsableVolumeDHWTank + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))



    if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_UsableVolumeDHW_BT1 >= SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection  * 2:
        action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
        action_DHWHeating = 0
    if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_UsableVolumeDHW_BT1 < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 2:
        action_DHWHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
        action_SpaceHeating = 0
        startedHeatingSpaceHeatingCorrection_end = False
        startedHeatingDHWCorrection_end = True
    if startedHeatingDHWCorrection_end == True and simulationResult_BufferStorageTemperature_BT1 >= SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 2:
        action_DHWHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
        action_SpaceHeating = 0
    if startedHeatingDHWCorrection_end == True and simulationResult_BufferStorageTemperature_BT1 < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 2:
        startedHeatingDHWCorrection_end = False
        action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
        action_DHWHeating = 0




    #Corrections due to high number of starts of the heat pump

    #Soft Limit Reached --> Consider minimum runtimes and standbytimes of the heat pump
    if numberOfHeatPumpStartsReachedSoftLimit ==True and startedHeatingDHWCorrection_end==False and startedHeatingSpaceHeatingCorrection_end ==False:
        print("numberOfHeatPumpStartsReachedSoftLimit; Timeslot: ",index_timeslot)
        if helpStartedHeatingHeatPump == True:
            print("numberOfHeatPumpStartsReachedSoftLimit; started HP")
            if action_DHWHeating > 0.01 and simulationResult_UsableVolumeDHW_BT1 <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                action_SpaceHeating = 0
                action_DHWHeating = action_DHWHeating
            elif action_DHWHeating > 0.01 and simulationResult_UsableVolumeDHW_BT1 > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                    action_SpaceHeating = 0
                    action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                    if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                        action_DHWHeating = 0
                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                        if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                            action_SpaceHeating = 0
                            action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                        elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                            action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                            action_DHWHeating = 0
                        elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                            action_SpaceHeating = 0
                            action_DHWHeating = 0

            if action_SpaceHeating > 0.01 and simulationResult_BufferStorageTemperature_BT1 <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                action_SpaceHeating =  action_SpaceHeating
                action_DHWHeating = 0
            elif action_SpaceHeating > 0.01 and simulationResult_BufferStorageTemperature_BT1 > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                    action_DHWHeating =   0
                elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                        action_SpaceHeating = 0
                        action_DHWHeating =  SetUpScenarios.minimalModulationdDegree_HP/100
                    elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                        if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                            action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                            action_DHWHeating = 0
                        elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                            action_SpaceHeating =  0
                            action_DHWHeating =  SetUpScenarios.minimalModulationdDegree_HP/100
                        elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                            action_SpaceHeating = 0
                            action_DHWHeating = 0

            if action_DHWHeating == 0 and action_SpaceHeating ==0:
                helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                currentSOCBufferStorage_CorrectionLimits =  (state_BufferStorageTemperatureLastTimeSlot - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
                currentSOCDHWTank_CorrectionLimits = ( state_usableVolumeDHWLastTimeSlot - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary) / ( SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary )
                if currentSOCBufferStorage_CorrectionLimits < currentSOCDHWTank_CorrectionLimits:
                    if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                        action_DHWHeating = 0
                    elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod  <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                        action_SpaceHeating = 0
                        action_DHWHeating =  SetUpScenarios.minimalModulationdDegree_HP/100
                else:
                    if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod  <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                        action_SpaceHeating = 0
                        action_DHWHeating =  SetUpScenarios.minimalModulationdDegree_HP/100
                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                        action_DHWHeating = 0


        elif helpStoppedHeatingHeatPump ==True:
            print("numberOfHeatPumpStartsReachedSoftLimit; stopped HP")
            action_SpaceHeating = 0
            action_DHWHeating = 0




    # Last heating of the week if the numberOfHeatPumpStartsReachedHardLimit
    if numberOfHeatPumpStartsReachedHardLimit ==True and startedHeatingDHWCorrection_end==False and startedHeatingSpaceHeatingCorrection_end ==False:
        print("numberOfHeatPumpStartsReachedHardLimit")
        # Last heating of the week
        if lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == False:
            fractionOfweekLeft =1 - (index_timeslot / SetUpScenarios.numberOfTimeSlotsPerWeek)
            currentSOCBufferStorage_CorrectionLimits =  (state_BufferStorageTemperatureLastTimeSlot - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
            currentSOCDHWTank_CorrectionLimits = ( state_usableVolumeDHWLastTimeSlot - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary) / ( SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary )
            differenceTargetValueEndAndUpperLimit_SpaceHeating = SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - (SetUpScenarios.initialBufferStorageTemperature)
            possibleTargetTemperatureForLastHeating_SpaceHeating = SetUpScenarios.initialBufferStorageTemperature  + differenceTargetValueEndAndUpperLimit_SpaceHeating  * fractionOfweekLeft
            differenceTargetValueEndAndUpperLimit_DHW = SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - (SetUpScenarios.initialUsableVolumeDHWTank)
            possibleTargetVolumeForLastHeating_DHW = SetUpScenarios.initialUsableVolumeDHWTank  + differenceTargetValueEndAndUpperLimit_DHW  * fractionOfweekLeft
            if currentSOCBufferStorage_CorrectionLimits <= currentSOCDHWTank_CorrectionLimits:
                if state_BufferStorageTemperatureLastTimeSlot < possibleTargetTemperatureForLastHeating_SpaceHeating:
                            action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                            action_DHWHeating = 0
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                elif state_usableVolumeDHWLastTimeSlot < possibleTargetVolumeForLastHeating_DHW:
                            action_SpaceHeating = 0
                            action_DHWHeating =  maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
            elif currentSOCBufferStorage_CorrectionLimits > currentSOCDHWTank_CorrectionLimits:
                if state_usableVolumeDHWLastTimeSlot < possibleTargetVolumeForLastHeating_DHW:
                            action_SpaceHeating = 0
                            action_DHWHeating =  maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                elif state_BufferStorageTemperatureLastTimeSlot < possibleTargetTemperatureForLastHeating_SpaceHeating:
                            action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                            action_DHWHeating = 0
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
            if state_usableVolumeDHWLastTimeSlot >= possibleTargetVolumeForLastHeating_DHW and state_BufferStorageTemperatureLastTimeSlot >= possibleTargetTemperatureForLastHeating_SpaceHeating:
                action_SpaceHeating = 0
                action_DHWHeating = 0
        elif lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == True:
            action_SpaceHeating = 0
            action_DHWHeating = 0



    #Corrections for the last value of the optimization horizon
    if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek:


        helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot
        helpHypotheticalBufferStorageTemperatureWhenHeating = state_BufferStorageTemperatureLastTimeSlot
        helpHypotheticalBufferStorageTemperatureWhenNotHeating = state_BufferStorageTemperatureLastTimeSlot
        helpHypotheticalDHWVolumeWhenHeating = simulationResult_UsableVolumeDHW_BT1
        helpHypotheticalDHWVolumeWhenNotHeating = simulationResult_UsableVolumeDHW_BT1


        averageSpaceHeatingDemandLastTimeslots = 0
        averageDHWDemandLastTimeSlots = 0
        averageCOPSpaceHeatingLastTimeSlots = 0
        averageCOPDHWLastTimeSlots = 0
        helpSumSpaceHeatingDemandLastTimeslots = 0
        helpSumDHWDemandLastTimeSlots = 0
        helpSumCOPSpaceHeatingLastTimeSlots = 0
        helpSumCOPDHWLastTimeSlots = 0

        for i in range (0, Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek):
            helpSumSpaceHeatingDemandLastTimeslots = helpSumSpaceHeatingDemandLastTimeslots + heatDemand
            helpSumDHWDemandLastTimeSlots = helpSumDHWDemandLastTimeSlots + DHWDemand
            helpSumCOPSpaceHeatingLastTimeSlots = helpSumCOPSpaceHeatingLastTimeSlots + cop_SpaceHeating
            helpSumCOPDHWLastTimeSlots = helpSumCOPDHWLastTimeSlots + cop_DHW

        averageSpaceHeatingDemandLastTimeslots = helpSumSpaceHeatingDemandLastTimeslots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
        averageDHWDemandLastTimeSlots = helpSumDHWDemandLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
        averageCOPSpaceHeatingLastTimeSlots = helpSumCOPSpaceHeatingLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
        averageCOPDHWLastTimeSlots =  helpSumCOPDHWLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek


        for helpCurrentHypotheticalTimeSlot in range (0, helpTimeSlotsToEndOfweek):
            helpHypotheticalBufferStorageTemperatureWhenHeating = helpHypotheticalBufferStorageTemperatureWhenHeating + (((maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP )* averageCOPSpaceHeatingLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - averageSpaceHeatingDemandLastTimeslots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
            helpHypotheticalBufferStorageTemperatureWhenNotHeating = helpHypotheticalBufferStorageTemperatureWhenNotHeating + ((0* averageCOPSpaceHeatingLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - averageSpaceHeatingDemandLastTimeslots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
            helpHypotheticalDHWVolumeWhenHeating = helpHypotheticalDHWVolumeWhenHeating + (((maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP ) * averageCOPDHWLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - averageDHWDemandLastTimeSlots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
            helpHypotheticalDHWVolumeWhenNotHeating = helpHypotheticalDHWVolumeWhenNotHeating + ((0 * averageCOPDHWLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - averageDHWDemandLastTimeSlots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


        if helpHypotheticalBufferStorageTemperatureWhenNotHeating > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 1.0:
            action_SpaceHeating = 0
            startedHeatingDHWCorrection_end = False
            startedHeatingSpaceHeatingCorrection_end = False
            print("Correction BufferStorage too high (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
            print("helpHypotheticalBufferStorageTemperatureWhenNotHeating: ", helpHypotheticalBufferStorageTemperatureWhenNotHeating)
            print("")
        if  helpHypotheticalBufferStorageTemperatureWhenHeating < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 1.0:
            action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
            if action_SpaceHeating < action_SpaceHeating_NotOverruled:
                if action_SpaceHeating_NotOverruled <1:
                    action_SpaceHeating = action_SpaceHeating_NotOverruled
                else:
                    action_SpaceHeating = 1
            action_DHWHeating = 0
            startedHeatingDHWCorrection_end = False
            startedHeatingSpaceHeatingCorrection_end = True
            print("Correction BufferStorage too low (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
            print("helpHypotheticalBufferStorageTemperatureWhenHeating: ", helpHypotheticalBufferStorageTemperatureWhenHeating)
            print("")
        if helpHypotheticalDHWVolumeWhenNotHeating > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 1.0:
            action_DHWHeating = 0
            startedHeatingDHWCorrection_end = False
            startedHeatingSpaceHeatingCorrection_end = False
            print("Correction DHW too high (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
            print ("helpHypotheticalDHWVolumeWhenNotHeating: ", helpHypotheticalDHWVolumeWhenNotHeating)
            print("")
        if helpHypotheticalDHWVolumeWhenHeating < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 1.0:
            action_DHWHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
            if action_DHWHeating < action_DHWHeating_NotOverruled:
                if action_DHWHeating_NotOverruled <1:
                    action_DHWHeating = action_DHWHeating_NotOverruled
                else:
                    action_DHWHeating = 1
            action_SpaceHeating = 0
            startedHeatingDHWCorrection_end = True
            startedHeatingSpaceHeatingCorrection_end = False
            print("Correction DHW too low (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
            print ("helpHypotheticalDHWVolumeWhenHeating: ", helpHypotheticalDHWVolumeWhenHeating)
            print("")


    #Corrections for the violations of the physical limits of the storage systems
    helpValue_BufferStorageTemperature_CorrectedModulationDegree = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
    helpValue_UsableVolumeDHW_CorrectedModulationDegree = state_usableVolumeDHWLastTimeSlot + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

    if heatingStartedPhysicalLimit_BufferStorage == True and numberOfHeatPumpStartsReachedHardLimit == True:
        helpValue_BufferStorageTemperature_MediumModulationDegree = state_BufferStorageTemperatureLastTimeSlot  + ((0.6 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        helpValue_UsableVolumeDHW_MediumModulationDegree = state_usableVolumeDHWLastTimeSlot + ((0.6 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        if helpValue_UsableVolumeDHW_CorrectedModulationDegree >= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
            if helpValue_BufferStorageTemperature_MediumModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit and helpValue_BufferStorageTemperature_MediumModulationDegree <= SetUpScenarios.initialBufferStorageTemperature:
                action_SpaceHeating = 0.6
                action_DHWHeating = 0
            elif helpValue_BufferStorageTemperature_MediumModulationDegree < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                action_SpaceHeating = 1
                action_DHWHeating = 0
            elif helpValue_BufferStorageTemperature_MediumModulationDegree > SetUpScenarios.initialBufferStorageTemperature:
                action_SpaceHeating = 0
                action_DHWHeating = 0
                heatingStartedPhysicalLimit_BufferStorage =False

    if heatingStartedPhysicalLimit_DHWTank == True and numberOfHeatPumpStartsReachedHardLimit == True:
        helpValue_BufferStorageTemperature_MediumModulationDegree = state_BufferStorageTemperatureLastTimeSlot  + ((0.6 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        helpValue_UsableVolumeDHW_MediumModulationDegree = state_usableVolumeDHWLastTimeSlot + ((0.6 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
           if helpValue_UsableVolumeDHW_MediumModulationDegree >= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit and helpValue_UsableVolumeDHW_MediumModulationDegree <= SetUpScenarios.initialUsableVolumeDHWTank:
                action_SpaceHeating = 0
                action_DHWHeating = 0.6
           elif helpValue_UsableVolumeDHW_MediumModulationDegree < SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                action_SpaceHeating = 0
                action_DHWHeating = 1
           elif helpValue_UsableVolumeDHW_MediumModulationDegree > SetUpScenarios.initialUsableVolumeDHWTank:
                action_SpaceHeating = 0
                action_DHWHeating = 0
                heatingStartedPhysicalLimit_DHWTank =False


    if index_timeslot ==0:
        helpValue_BufferStorageTemperature_CorrectedModulationDegree =  SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        helpValue_UsableVolumeDHW_CorrectedModulationDegree =  SetUpScenarios.initialUsableVolumeDHWTank + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

    if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
        action_SpaceHeating = 0
        print("Corrections Physical limit too high value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")

    if helpValue_BufferStorageTemperature_CorrectedModulationDegree <= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
        action_SpaceHeating = 1
        action_DHWHeating = 0
        print("Corrections Physical limit too low value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
        heatingStartedPhysicalLimit_BufferStorage = True

    if helpValue_UsableVolumeDHW_CorrectedModulationDegree  >= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
        action_DHWHeating = 0
        print("Corrections Physical limit too high value DHW. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")

    if helpValue_UsableVolumeDHW_CorrectedModulationDegree  <= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
        action_SpaceHeating = 0
        action_DHWHeating = 1
        print("Corrections Physical limit too low value DHW. Time: " +  str(index_timeslot)+ "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT1) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT1) + "\n")
        heatingStartedPhysicalLimit_DHWTank = True





    #Corrections for the SOC of the EV
    if simulationResult_SOCofEV_BT1 >  100:
       action_EVCharging = 0
       print("Correction of the EV. SOC too high. Time: " +  str(index_timeslot))
    if simulationResult_SOCofEV_BT1 <  0:
       action_EVCharging = maximumPowerEVChargingForNotCreatingANewPeak

    #Corrections for the last value of the optimization horizon for the SOC
    if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek * 2:
        helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot
        helpHypotheticalEnergyEVWhenCharging = state_SOCofEVLastTimeSlot/100 * maximumPowerEVChargingForNotCreatingANewPeak
        helpHypotheticalSOCWhenCharging = (helpHypotheticalEnergyEVWhenCharging / SetUpScenarios.capacityMaximal_EV)*100
        for helpCurrentHypotheticalTimeSlot in range (0, helpTimeSlotsToEndOfweek):
            helpHypotheticalEnergyEVWhenCharging  = helpHypotheticalEnergyEVWhenCharging + (maximumPowerEVChargingForNotCreatingANewPeak *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 )
            helpHypotheticalSOCWhenCharging  = (helpHypotheticalEnergyEVWhenCharging / SetUpScenarios.capacityMaximal_EV)*100

        if simulationResult_SOCofEV_BT1 >= SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection:
            action_EVCharging = 0
            print("Correction of the EV (End of the week). SOC too high. Time: " +  str(index_timeslot))
        if helpHypotheticalSOCWhenCharging <= SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection * 0.5:
            if  action_EVCharging <=  maximumPowerEVChargingForNotCreatingANewPeak:
                action_EVCharging =  maximumPowerEVChargingForNotCreatingANewPeak
            print("Correction of the EV (End of the week). SOC too low. Time: " +  str(index_timeslot))

    if overruleActions == False:
        action_SpaceHeating = action_SpaceHeating_NotOverruled
        action_DHWHeating = action_DHWHeating_NotOverruled
        action_EVCharging = action_EVCharging_NotOverruled


    #Calculate the simulation values with the corrected input vectors
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT1 = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT1 = state_usableVolumeDHWLastTimeSlot + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        simulationResult_SOCofEV_BT1  = ((state_SOCofEVLastTimeSlot/100 * SetUpScenarios.capacityMaximal_EV + (action_EVCharging *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - energyDemandEV))  / (SetUpScenarios.capacityMaximal_EV))*100
        helpHypotheticalSOCDropNoCharging = helpHypotheticalSOCDropNoCharging + (energyDemandEV/ SetUpScenarios.capacityMaximal_EV)*100

    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT1 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT1 = SetUpScenarios.initialUsableVolumeDHWTank + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        simulationResult_SOCofEV_BT1  = ((SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + (action_EVCharging *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - energyDemandEV)) / (SetUpScenarios.capacityMaximal_EV))*100
        helpHypotheticalSOCDropNoCharging =  (energyDemandEV/ SetUpScenarios.capacityMaximal_EV)*100


    if action_SpaceHeating_NotOverruled != action_SpaceHeating:
        print("")
        print("Action overruled")
        print ("Timeslot: ", index_timeslot)
        print("state_BufferStorageTemperatureLastTimeSlot: ", state_BufferStorageTemperatureLastTimeSlot)
        print("action_SpaceHeating_NotOverruled: ", action_SpaceHeating_NotOverruled)
        print("action_SpaceHeating: ", action_SpaceHeating)
        print("simulationResult_BufferStorageTemperature_BT1: ", simulationResult_BufferStorageTemperature_BT1)
        print("")

    if action_DHWHeating_NotOverruled != action_DHWHeating:
        print("")
        print("Action overruled")
        print ("Timeslot: ", index_timeslot)
        print("state_usableVolumeDHWLastTimeSlot: ", state_usableVolumeDHWLastTimeSlot)
        print("action_DHWHeating_NotOverruled: ", action_DHWHeating_NotOverruled)
        print("action_DHWHeating: ", action_DHWHeating)
        print("simulationResult_UsableVolumeDHW_BT1: ", simulationResult_UsableVolumeDHW_BT1)
        print("")

    if action_EVCharging_NotOverruled != action_EVCharging:
        print("")
        print("Action overruled")
        print ("Timeslot: ", index_timeslot)
        print("state_SOCofEVLastTimeSlot: ", state_SOCofEVLastTimeSlot)
        print("action_EVCharging_NotOverruled: ", action_EVCharging_NotOverruled)
        print("action_EVCharging: ", action_EVCharging)
        print("simulationResult_SOCofEV_BT1: ", simulationResult_SOCofEV_BT1)
        print("")

    print("End IC; Output")
    print("action_SpaceHeating: ", action_SpaceHeating)
    print("action_DHWHeating: ", action_DHWHeating)
    print("action_EVCharging: ", action_EVCharging)
    print("")


    return action_SpaceHeating, action_DHWHeating, action_EVCharging, simulationResult_BufferStorageTemperature_BT1, simulationResult_UsableVolumeDHW_BT1, simulationResult_SOCofEV_BT1, helpCountNumberOfStartsIndividual_SpaceHeating, helpCountNumberOfStartsIndividual_DHW, helpCountNumberOfStarts_Combined , helpCounterNumberOfRunningSlots_SpaceHeating , helpCounterNumberOfRunningSlots_DHW , helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating , helpCounterNumberOfStandBySlots_DHW , helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad,  helpStartedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit, helpHypotheticalSOCDropNoCharging, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage, heatingStartedPhysicalLimit_DHWTank,startedHeatingSpaceHeatingCorrection_end, startedHeatingDHWCorrection_end, help_bothStorageHeatedUp_lastTimeBufferStorageOverruled, help_bothStorageHeatedUp_lastTimeDHWOverruled

#'''
def simulateTimeSlot_WithAddtionalController_BT2 (overruleActions, action_SpaceHeating, action_DHWHeating, state_BufferStorageTemperatureLastTimeSlot,
                                                 state_usableVolumeDHWLastTimeSlot, helpCountNumberOfStartsIndividual_SpaceHeating,
                                                 helpCountNumberOfStartsIndividual_DHW, helpCountNumberOfStarts_Combined , helpCounterNumberOfRunningSlots_SpaceHeating , helpCounterNumberOfRunningSlots_DHW ,
                                                 helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating , helpCounterNumberOfStandBySlots_DHW ,
                                                 helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, helpStoppedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit,
                                                 index_timeslot, outsideTemperature, PVGeneration, heatDemand, DHWDemand,electricityDemand, priceForElectricity_CentsPerkWh, cop_SpaceHeating, cop_DHW,
                                                 helpPVGenerationPreviousTimeSlot, helpElectricalLoadPreviousTimeSlot, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped,
                                                 heatingStartedPhysicalLimit_BufferStorage, heatingStartedPhysicalLimit_DHWTank,startedHeatingSpaceHeatingCorrection_end, startedHeatingDHWCorrection_end, help_bothStorageHeatedUp_lastTimeBufferStorageOverruled, help_bothStorageHeatedUp_lastTimeDHWOverruled):

    action_SpaceHeating_NotOverruled = action_SpaceHeating
    action_DHWHeating_NotOverruled = action_DHWHeating


    print("")
    print("------------------------------------------")
    print("")
    print("Beginning IC; Timeslot: ", index_timeslot + 1)
    print("")
    print("helpCountNumberOfStarts_Combined: ", helpCountNumberOfStarts_Combined)
    #Calculate the simulation steps



    if helpStartedHeatingHeatPump == True and helpCounterNumberOfRunningSlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
        helpStartedHeatingHeatPump = False
    if helpStoppedHeatingHeatPump == True and helpCounterNumberOfStandBySlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
        helpStoppedHeatingHeatPump = False

    if numberOfHeatPumpStartsReachedHardLimit == True:
        numberOfHeatPumpStartsReachedSoftLimit = False


    # Pre-Corrections of input values: too high or low input values
    if action_SpaceHeating  > 1:
        action_SpaceHeating  =1
    if action_DHWHeating  > 1:
        action_DHWHeating =1

    if action_SpaceHeating  < 0:
        action_SpaceHeating  =0
    if action_DHWHeating  <  0:
        action_DHWHeating =0





     # Pre-Corrections of input values: heating up only one storage at one time
    if action_SpaceHeating > 0.001 and action_DHWHeating  > 0.001:
        print("Pre_Correction Only one storage. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating)  + "\n")
        if help_bothStorageHeatedUp_lastTimeBufferStorageOverruled== True:
            action_DHWHeating = 0
            help_bothStorageHeatedUp_lastTimeBufferStorageOverruled = False
            help_bothStorageHeatedUp_lastTimeDHWOverruled = True
        elif help_bothStorageHeatedUp_lastTimeDHWOverruled == True:
            action_SpaceHeating = 0
            help_bothStorageHeatedUp_lastTimeBufferStorageOverruled = True
            help_bothStorageHeatedUp_lastTimeDHWOverruled = False


    #Pre-Corrections: Set small heating values to 0
    if action_SpaceHeating > 0 and action_SpaceHeating < 0.1:
        action_SpaceHeating = 0

    if action_DHWHeating > 0 and action_DHWHeating < 0.1:
        action_DHWHeating = 0


    # Pre-Corrections of input values: minimal modulation
    if action_SpaceHeating > 0.001 and action_SpaceHeating  < SetUpScenarios.minimalModulationdDegree_HP/100:
        print("Pre_Correction: Min Modulation. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + "\n")
        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100

    if action_DHWHeating > 0.001 and action_DHWHeating  < SetUpScenarios.minimalModulationdDegree_HP/100:
        print("Pre_Correction: Min Modulation. Time: " +  str(index_timeslot) + "; ANN value DHW: " + str(action_DHWHeating) + "\n")
        action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP/100



    if  helpCountNumberOfStarts_Combined >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts_BeforeConsideringMinimalRuntime:
        numberOfHeatPumpStartsReachedSoftLimit = True

    if helpCountNumberOfStarts_Combined >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts - 2:
        numberOfHeatPumpStartsReachedHardLimit = True
        numberOfHeatPumpStartsReachedSoftLimit = False


    #Calculate the hypothetical simulation values if the non-corrected actions were applied
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT2  = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT2= state_usableVolumeDHWLastTimeSlot + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT2 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT2 = SetUpScenarios.initialUsableVolumeDHWTank + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP
    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP


    if index_timeslot >=1:
        if (helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot
        if (helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot


    if (action_SpaceHeating + action_DHWHeating) * SetUpScenarios.electricalPower_HP + electricityDemand > PVGeneration:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = helpCurrentPeakLoad - electricityDemand  + PVGeneration
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = helpCurrentPeakLoad - electricityDemand  + PVGeneration

    if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek > SetUpScenarios.electricalPower_HP:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP
    if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek > SetUpScenarios.electricalPower_HP:
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP


    if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP
    if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP:
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek =Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP


    #Corrections due to violations of the temperature and volume constraints
    if simulationResult_UsableVolumeDHW_BT2 <= SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
        action_DHWHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
        action_SpaceHeating = 0
        print("Correction volume too low DHW (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
    if simulationResult_UsableVolumeDHW_BT2 >= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
        helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        if helpCounterNumberOfStandBySlots_Combined >0:
            helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        if action_DHWHeating > 0.001 and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod < SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit  and (numberOfHeatPumpStartsReachedSoftLimit == False or helpStoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
           action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP/100
           print("Correction DHW too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
        else:
            action_DHWHeating = 0
            print("Correction DHW volume too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")

    if simulationResult_BufferStorageTemperature_BT2 > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:

        helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        if helpCounterNumberOfStandBySlots_Combined >0:
            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        if action_SpaceHeating > 0.001 and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod < SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and (numberOfHeatPumpStartsReachedSoftLimit == False or helpStoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
           action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
           print("Correction BufferStorage too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
        else:
           action_SpaceHeating = 0
           print("Correction BufferStorage too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")

    if simulationResult_BufferStorageTemperature_BT2 < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary and simulationResult_UsableVolumeDHW_BT2 > SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary:
        action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
        action_DHWHeating = 0
        print("Correction BufferStorage too low (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")


    # Corrections due to minimal modulation degree of the heat pump
    if action_SpaceHeating > 0.001 and action_SpaceHeating < SetUpScenarios.minimalModulationdDegree_HP /100:
        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP /100
        print("Correction Minimal Mod. SpaceHeating. Time: " +  str(index_timeslot) + "; ANN value: " + str(action_SpaceHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
    if action_DHWHeating > 0.001 and action_DHWHeating < SetUpScenarios.minimalModulationdDegree_HP /100:
        action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP /100
        print("Correction Minimal Mod. DHW. Time: " +  str(index_timeslot) + "; ANN value: " + str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")



    #Calculate the hypothetical simulation values if the  corrected actions were applied
    cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP_SingleTimeSlot(outsideTemperature)
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT2 = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT2 = state_usableVolumeDHWLastTimeSlot + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT2 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT2 = SetUpScenarios.initialUsableVolumeDHWTank + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))



    if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_UsableVolumeDHW_BT2 >= SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection  * 2:
        action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
        action_DHWHeating = 0
    if startedHeatingSpaceHeatingCorrection_end == True and simulationResult_UsableVolumeDHW_BT2 < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 2:
        action_DHWHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
        action_SpaceHeating = 0
        startedHeatingSpaceHeatingCorrection_end = False
        startedHeatingDHWCorrection_end = True
    if startedHeatingDHWCorrection_end == True and simulationResult_BufferStorageTemperature_BT2 >= SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 2:
        action_DHWHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
        action_SpaceHeating = 0
    if startedHeatingDHWCorrection_end == True and simulationResult_BufferStorageTemperature_BT2 < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 2:
        startedHeatingDHWCorrection_end = False
        action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
        action_DHWHeating = 0




    #Corrections due to high number of starts of the heat pump

    #Soft Limit Reached --> Consider minimum runtimes and standbytimes of the heat pump
    if numberOfHeatPumpStartsReachedSoftLimit ==True and startedHeatingDHWCorrection_end==False and startedHeatingSpaceHeatingCorrection_end ==False:
        print("numberOfHeatPumpStartsReachedSoftLimit; Timeslot: ",index_timeslot)
        if helpStartedHeatingHeatPump == True:
            print("numberOfHeatPumpStartsReachedSoftLimit; started HP")
            if action_DHWHeating > 0.01 and simulationResult_UsableVolumeDHW_BT2 <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                action_SpaceHeating = 0
                action_DHWHeating = action_DHWHeating
            elif action_DHWHeating > 0.01 and simulationResult_UsableVolumeDHW_BT2 > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                    action_SpaceHeating = 0
                    action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                    if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                        action_DHWHeating = 0
                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                        if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                            action_SpaceHeating = 0
                            action_DHWHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                        elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                            action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                            action_DHWHeating = 0
                        elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                            action_SpaceHeating = 0
                            action_DHWHeating = 0

            if action_SpaceHeating > 0.01 and simulationResult_BufferStorageTemperature_BT2 <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                action_SpaceHeating =  action_SpaceHeating
                action_DHWHeating = 0
            elif action_SpaceHeating > 0.01 and simulationResult_BufferStorageTemperature_BT2 > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                    action_DHWHeating =   0
                elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                        action_SpaceHeating = 0
                        action_DHWHeating =  SetUpScenarios.minimalModulationdDegree_HP/100
                    elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary:
                        if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                            action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                            action_DHWHeating = 0
                        elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                            action_SpaceHeating =  0
                            action_DHWHeating =  SetUpScenarios.minimalModulationdDegree_HP/100
                        elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and helpValue_UsableVolumeDHW_WhenHeatingWithMinMod > SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                            action_SpaceHeating = 0
                            action_DHWHeating = 0

            if action_DHWHeating == 0 and action_SpaceHeating ==0:
                helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                helpValue_UsableVolumeDHW_WhenHeatingWithMinMod = state_usableVolumeDHWLastTimeSlot + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
                currentSOCBufferStorage_CorrectionLimits =  (state_BufferStorageTemperatureLastTimeSlot - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
                currentSOCDHWTank_CorrectionLimits = ( state_usableVolumeDHWLastTimeSlot - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary) / ( SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary )
                if currentSOCBufferStorage_CorrectionLimits < currentSOCDHWTank_CorrectionLimits:
                    if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                        action_DHWHeating = 0
                    elif helpValue_UsableVolumeDHW_WhenHeatingWithMinMod  <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                        action_SpaceHeating = 0
                        action_DHWHeating =  SetUpScenarios.minimalModulationdDegree_HP/100
                else:
                    if helpValue_UsableVolumeDHW_WhenHeatingWithMinMod  <= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
                        action_SpaceHeating = 0
                        action_DHWHeating =  SetUpScenarios.minimalModulationdDegree_HP/100
                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                        action_DHWHeating = 0


        elif helpStoppedHeatingHeatPump ==True:
            print("numberOfHeatPumpStartsReachedSoftLimit; stopped HP")
            action_SpaceHeating = 0
            action_DHWHeating = 0




    # Last heating of the week if the numberOfHeatPumpStartsReachedHardLimit
    if numberOfHeatPumpStartsReachedHardLimit ==True and startedHeatingDHWCorrection_end==False and startedHeatingSpaceHeatingCorrection_end ==False:
        print("numberOfHeatPumpStartsReachedHardLimit")
        # Last heating of the week
        if lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == False:
            fractionOfweekLeft =1 - (index_timeslot / SetUpScenarios.numberOfTimeSlotsPerWeek)
            currentSOCBufferStorage_CorrectionLimits =  (state_BufferStorageTemperatureLastTimeSlot - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary) / (SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary)
            currentSOCDHWTank_CorrectionLimits = ( state_usableVolumeDHWLastTimeSlot - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary) / ( SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - SetUpScenarios.minimumUsableVolumeDHWTank_CorrectionNecessary )
            differenceTargetValueEndAndUpperLimit_SpaceHeating = SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - (SetUpScenarios.initialBufferStorageTemperature)
            possibleTargetTemperatureForLastHeating_SpaceHeating = SetUpScenarios.initialBufferStorageTemperature  + differenceTargetValueEndAndUpperLimit_SpaceHeating  * fractionOfweekLeft
            differenceTargetValueEndAndUpperLimit_DHW = SetUpScenarios.maximumUsableVolumeDHWTank_CorrectionNecessary - (SetUpScenarios.initialUsableVolumeDHWTank)
            possibleTargetVolumeForLastHeating_DHW = SetUpScenarios.initialUsableVolumeDHWTank  + differenceTargetValueEndAndUpperLimit_DHW  * fractionOfweekLeft
            if currentSOCBufferStorage_CorrectionLimits <= currentSOCDHWTank_CorrectionLimits:
                if state_BufferStorageTemperatureLastTimeSlot < possibleTargetTemperatureForLastHeating_SpaceHeating:
                            action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                            action_DHWHeating = 0
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                elif state_usableVolumeDHWLastTimeSlot < possibleTargetVolumeForLastHeating_DHW:
                            action_SpaceHeating = 0
                            action_DHWHeating =  maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
            elif currentSOCBufferStorage_CorrectionLimits > currentSOCDHWTank_CorrectionLimits:
                if state_usableVolumeDHWLastTimeSlot < possibleTargetVolumeForLastHeating_DHW:
                            action_SpaceHeating = 0
                            action_DHWHeating =  maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
                elif state_BufferStorageTemperatureLastTimeSlot < possibleTargetTemperatureForLastHeating_SpaceHeating:
                            action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP
                            action_DHWHeating = 0
                            lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
            if state_usableVolumeDHWLastTimeSlot >= possibleTargetVolumeForLastHeating_DHW and state_BufferStorageTemperatureLastTimeSlot >= possibleTargetTemperatureForLastHeating_SpaceHeating:
                action_SpaceHeating = 0
                action_DHWHeating = 0
        elif lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == True:
            action_SpaceHeating = 0
            action_DHWHeating = 0



    #Corrections for the last value of the optimization horizon
    if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek:


        helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot
        helpHypotheticalBufferStorageTemperatureWhenHeating = state_BufferStorageTemperatureLastTimeSlot
        helpHypotheticalBufferStorageTemperatureWhenNotHeating = state_BufferStorageTemperatureLastTimeSlot
        helpHypotheticalDHWVolumeWhenHeating = simulationResult_UsableVolumeDHW_BT2
        helpHypotheticalDHWVolumeWhenNotHeating = simulationResult_UsableVolumeDHW_BT2


        averageSpaceHeatingDemandLastTimeslots = 0
        averageDHWDemandLastTimeSlots = 0
        averageCOPSpaceHeatingLastTimeSlots = 0
        averageCOPDHWLastTimeSlots = 0
        helpSumSpaceHeatingDemandLastTimeslots = 0
        helpSumDHWDemandLastTimeSlots = 0
        helpSumCOPSpaceHeatingLastTimeSlots = 0
        helpSumCOPDHWLastTimeSlots = 0

        for i in range (0, Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek):
            helpSumSpaceHeatingDemandLastTimeslots = helpSumSpaceHeatingDemandLastTimeslots + heatDemand
            helpSumDHWDemandLastTimeSlots = helpSumDHWDemandLastTimeSlots + DHWDemand
            helpSumCOPSpaceHeatingLastTimeSlots = helpSumCOPSpaceHeatingLastTimeSlots + cop_SpaceHeating
            helpSumCOPDHWLastTimeSlots = helpSumCOPDHWLastTimeSlots + cop_DHW

        averageSpaceHeatingDemandLastTimeslots = helpSumSpaceHeatingDemandLastTimeslots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
        averageDHWDemandLastTimeSlots = helpSumDHWDemandLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
        averageCOPSpaceHeatingLastTimeSlots = helpSumCOPSpaceHeatingLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek
        averageCOPDHWLastTimeSlots =  helpSumCOPDHWLastTimeSlots / Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek


        for helpCurrentHypotheticalTimeSlot in range (0, helpTimeSlotsToEndOfweek):
            helpHypotheticalBufferStorageTemperatureWhenHeating = helpHypotheticalBufferStorageTemperatureWhenHeating + (((maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP )* averageCOPSpaceHeatingLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - averageSpaceHeatingDemandLastTimeslots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
            helpHypotheticalBufferStorageTemperatureWhenNotHeating = helpHypotheticalBufferStorageTemperatureWhenNotHeating + ((0* averageCOPSpaceHeatingLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - averageSpaceHeatingDemandLastTimeslots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
            helpHypotheticalDHWVolumeWhenHeating = helpHypotheticalDHWVolumeWhenHeating + (((maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP ) * averageCOPDHWLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - averageDHWDemandLastTimeSlots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
            helpHypotheticalDHWVolumeWhenNotHeating = helpHypotheticalDHWVolumeWhenNotHeating + ((0 * averageCOPDHWLastTimeSlots *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - averageDHWDemandLastTimeSlots  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


        if helpHypotheticalBufferStorageTemperatureWhenNotHeating > SetUpScenarios.initialBufferStorageTemperature + SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 1.0:
            action_SpaceHeating = 0
            startedHeatingDHWCorrection_end = False
            startedHeatingSpaceHeatingCorrection_end = False
            print("Correction BufferStorage too high (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
            print("helpHypotheticalBufferStorageTemperatureWhenNotHeating: ", helpHypotheticalBufferStorageTemperatureWhenNotHeating)
            print("")
        if  helpHypotheticalBufferStorageTemperatureWhenHeating < SetUpScenarios.initialBufferStorageTemperature - SetUpScenarios.endBufferStorageTemperatureAllowedDeviationFromInitalValue_ForCorrection * 1.0:
            action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
            if action_SpaceHeating < action_SpaceHeating_NotOverruled:
                if action_SpaceHeating_NotOverruled <1:
                    action_SpaceHeating = action_SpaceHeating_NotOverruled
                else:
                    action_SpaceHeating = 1
            action_DHWHeating = 0
            startedHeatingDHWCorrection_end = False
            startedHeatingSpaceHeatingCorrection_end = True
            print("Correction BufferStorage too low (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
            print("helpHypotheticalBufferStorageTemperatureWhenHeating: ", helpHypotheticalBufferStorageTemperatureWhenHeating)
            print("")
        if helpHypotheticalDHWVolumeWhenNotHeating > SetUpScenarios.initialUsableVolumeDHWTank + SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 1.0:
            action_DHWHeating = 0
            startedHeatingDHWCorrection_end = False
            startedHeatingSpaceHeatingCorrection_end = False
            print("Correction DHW too high (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
            print ("helpHypotheticalDHWVolumeWhenNotHeating: ", helpHypotheticalDHWVolumeWhenNotHeating)
            print("")
        if helpHypotheticalDHWVolumeWhenHeating < SetUpScenarios.initialUsableVolumeDHWTank - SetUpScenarios.endUsableVolumeDHWTankAllowedDeviationFromInitialValue_ForCorrection * 1.0:
            action_DHWHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP
            if action_DHWHeating < action_DHWHeating_NotOverruled:
                if action_DHWHeating_NotOverruled <1:
                    action_DHWHeating = action_DHWHeating_NotOverruled
                else:
                    action_DHWHeating = 1
            action_SpaceHeating = 0
            startedHeatingDHWCorrection_end = True
            startedHeatingSpaceHeatingCorrection_end = False
            print("Correction DHW too low (End of the week). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
            print ("helpHypotheticalDHWVolumeWhenHeating: ", helpHypotheticalDHWVolumeWhenHeating)
            print("")


    #Corrections for the violations of the physical limits of the storage systems
    helpValue_BufferStorageTemperature_CorrectedModulationDegree = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
    helpValue_UsableVolumeDHW_CorrectedModulationDegree = state_usableVolumeDHWLastTimeSlot + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

    if heatingStartedPhysicalLimit_BufferStorage == True and numberOfHeatPumpStartsReachedHardLimit == True:
        helpValue_BufferStorageTemperature_MediumModulationDegree = state_BufferStorageTemperatureLastTimeSlot  + ((0.6 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        helpValue_UsableVolumeDHW_MediumModulationDegree = state_usableVolumeDHWLastTimeSlot + ((0.6 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        if helpValue_UsableVolumeDHW_CorrectedModulationDegree >= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
            if helpValue_BufferStorageTemperature_MediumModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit and helpValue_BufferStorageTemperature_MediumModulationDegree <= SetUpScenarios.initialBufferStorageTemperature:
                action_SpaceHeating = 0.6
                action_DHWHeating = 0
            elif helpValue_BufferStorageTemperature_MediumModulationDegree < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
                action_SpaceHeating = 1
                action_DHWHeating = 0
            elif helpValue_BufferStorageTemperature_MediumModulationDegree > SetUpScenarios.initialBufferStorageTemperature:
                action_SpaceHeating = 0
                action_DHWHeating = 0
                heatingStartedPhysicalLimit_BufferStorage =False

    if heatingStartedPhysicalLimit_DHWTank == True and numberOfHeatPumpStartsReachedHardLimit == True:
        helpValue_BufferStorageTemperature_MediumModulationDegree = state_BufferStorageTemperatureLastTimeSlot  + ((0.6 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        helpValue_UsableVolumeDHW_MediumModulationDegree = state_usableVolumeDHWLastTimeSlot + ((0.6 * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))
        if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
           if helpValue_UsableVolumeDHW_MediumModulationDegree >= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit and helpValue_UsableVolumeDHW_MediumModulationDegree <= SetUpScenarios.initialUsableVolumeDHWTank:
                action_SpaceHeating = 0
                action_DHWHeating = 0.6
           elif helpValue_UsableVolumeDHW_MediumModulationDegree < SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
                action_SpaceHeating = 0
                action_DHWHeating = 1
           elif helpValue_UsableVolumeDHW_MediumModulationDegree > SetUpScenarios.initialUsableVolumeDHWTank:
                action_SpaceHeating = 0
                action_DHWHeating = 0
                heatingStartedPhysicalLimit_DHWTank =False


    if index_timeslot ==0:
        helpValue_BufferStorageTemperature_CorrectedModulationDegree =  SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        helpValue_UsableVolumeDHW_CorrectedModulationDegree =  SetUpScenarios.initialUsableVolumeDHWTank + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

    if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
        action_SpaceHeating = 0
        print("Corrections Physical limit too high value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")

    if helpValue_BufferStorageTemperature_CorrectedModulationDegree <= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
        action_SpaceHeating = 1
        action_DHWHeating = 0
        print("Corrections Physical limit too low value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
        heatingStartedPhysicalLimit_BufferStorage = True

    if helpValue_UsableVolumeDHW_CorrectedModulationDegree  >= SetUpScenarios.maximumUsableVolumeDHWTank_PhysicalLimit:
        action_DHWHeating = 0
        print("Corrections Physical limit too high value DHW. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")

    if helpValue_UsableVolumeDHW_CorrectedModulationDegree  <= SetUpScenarios.minimumUsableVolumeDHWTank_PhysicalLimit:
        action_SpaceHeating = 0
        action_DHWHeating = 1
        print("Corrections Physical limit too low value DHW. Time: " +  str(index_timeslot)+ "; ANN value SpaceHeating: " + str(action_SpaceHeating) + ", ANN value DHW: "+ str(action_DHWHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT2) +"; DHW Tank: " + str(simulationResult_UsableVolumeDHW_BT2) + "\n")
        heatingStartedPhysicalLimit_DHWTank = True


    if overruleActions == False:
        action_SpaceHeating = action_SpaceHeating_NotOverruled
        action_DHWHeating = action_DHWHeating_NotOverruled


    #Calculate the simulation values with the corrected input vectors
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT2 = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT2 = state_usableVolumeDHWLastTimeSlot + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))

    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT2 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        simulationResult_UsableVolumeDHW_BT2 = SetUpScenarios.initialUsableVolumeDHWTank + ((action_DHWHeating * cop_DHW *  SetUpScenarios.electricalPower_HP * SetUpScenarios.timeResolution_InMinutes * 60 - DHWDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesDHWTank * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.temperatureOfTheHotWaterInTheDHWTank * SetUpScenarios.densityOfWater * SetUpScenarios.specificHeatCapacityOfWater))


    if action_SpaceHeating_NotOverruled != action_SpaceHeating:
        print("")
        print("Action overruled")
        print ("Timeslot: ", index_timeslot)
        print("state_BufferStorageTemperatureLastTimeSlot: ", state_BufferStorageTemperatureLastTimeSlot)
        print("action_SpaceHeating_NotOverruled: ", action_SpaceHeating_NotOverruled)
        print("action_SpaceHeating: ", action_SpaceHeating)
        print("simulationResult_BufferStorageTemperature_BT2: ", simulationResult_BufferStorageTemperature_BT2)
        print("")

    if action_DHWHeating_NotOverruled != action_DHWHeating:
        print("")
        print("Action overruled")
        print ("Timeslot: ", index_timeslot)
        print("state_usableVolumeDHWLastTimeSlot: ", state_usableVolumeDHWLastTimeSlot)
        print("action_DHWHeating_NotOverruled: ", action_DHWHeating_NotOverruled)
        print("action_DHWHeating: ", action_DHWHeating)
        print("simulationResult_UsableVolumeDHW_BT2: ", simulationResult_UsableVolumeDHW_BT2)
        print("")


    print("End IC; Output")
    print("action_SpaceHeating: ", action_SpaceHeating)
    print("action_DHWHeating: ", action_DHWHeating)
    print("")


    return action_SpaceHeating, action_DHWHeating, simulationResult_BufferStorageTemperature_BT2, simulationResult_UsableVolumeDHW_BT2, helpCountNumberOfStartsIndividual_SpaceHeating, helpCountNumberOfStartsIndividual_DHW, helpCountNumberOfStarts_Combined , helpCounterNumberOfRunningSlots_SpaceHeating , helpCounterNumberOfRunningSlots_DHW , helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating , helpCounterNumberOfStandBySlots_DHW , helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad,  helpStartedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage, heatingStartedPhysicalLimit_DHWTank,startedHeatingSpaceHeatingCorrection_end, startedHeatingDHWCorrection_end, help_bothStorageHeatedUp_lastTimeBufferStorageOverruled, help_bothStorageHeatedUp_lastTimeDHWOverruled



def simulateTimeSlot_WithAddtionalController_BT3 (overruleActions,  action_EVCharging, state_SOCofEVLastTimeSlot, helpCurrentPeakLoad,
                                                 index_timeslot, outsideTemperature, PVGeneration, electricityDemand, availabilityOfTheEV, energyDemandEV, priceForElectricity_CentsPerkWh, helpPVGenerationPreviousTimeSlot, helpElectricalLoadPreviousTimeSlot, helpHypotheticalSOCDropNoCharging ):


    action_EVCharging_NotOverruled = action_EVCharging


    print("")
    print("------------------------------------------")
    print("")
    print("Beginning IC; Timeslot: ", index_timeslot + 1)
    print("")

    #Calculate the simulation steps



    # Pre-Corrections of input values: too high or low input values

    if action_EVCharging > SetUpScenarios.chargingPowerMaximal_EV:
        action_EVCharging = SetUpScenarios.chargingPowerMaximal_EV

    if action_EVCharging < 0:
        action_EVCharging = 0



     # Pre_Corrections for the availability of the EV (charging is only possible if the EV is available at the charging station of the building)
    if action_EVCharging > 0.001 and  availabilityOfTheEV ==0:
        action_EVCharging =0
        print("Pre_Correction EV is not available for charging: " +  str(index_timeslot))



    #Calculate the hypothetical simulation values if the non-corrected actions were applied
    if index_timeslot >=1:
        simulationResult_SOCofEV_BT3   = state_SOCofEVLastTimeSlot + (( ( action_EVCharging *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - energyDemandEV)) /SetUpScenarios.capacityMaximal_EV)*100
    if index_timeslot ==0:
        simulationResult_SOCofEV_BT3   = SetUpScenarios.initialSOC_EV + (( ( action_EVCharging *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - energyDemandEV)) /SetUpScenarios.capacityMaximal_EV)*100



    # Calculate the maximum power of the heat pump and the EV for not creating a new peak load
    if index_timeslot >=1:
        if (helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot
        if (helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot

    maximumPowerEVChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_EV

    if action_EVCharging + electricityDemand > PVGeneration:
        maximumPowerEVChargingForNotCreatingANewPeak = helpCurrentPeakLoad  - electricityDemand  + PVGeneration


    if  maximumPowerEVChargingForNotCreatingANewPeak >  SetUpScenarios.chargingPowerMaximal_EV:
        maximumPowerEVChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_EV


    if  maximumPowerEVChargingForNotCreatingANewPeak < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection *  SetUpScenarios.chargingPowerMaximal_EV:
        maximumPowerEVChargingForNotCreatingANewPeak = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.chargingPowerMaximal_EV


    # Corrections for the SOC of the EV
    if simulationResult_SOCofEV_BT3 > 100:
        action_EVCharging = 0


    #Corrections for the last value of the optimization horizon
    if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek:


        helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot


    #Corrections for the SOC of the EV
    if simulationResult_SOCofEV_BT3 >  100:
       action_EVCharging = 0
       print("Correction of the EV. SOC too high. Time: " +  str(index_timeslot))
    if simulationResult_SOCofEV_BT3 <  0:
       action_EVCharging = maximumPowerEVChargingForNotCreatingANewPeak

    #Corrections for the last value of the optimization horizon for the SOC
    if index_timeslot >= SetUpScenarios.numberOfTimeSlotsPerWeek - Run_Simulations.timeslotsForCorrectingActionsBeforeTheAndOfTheweek * 2:
        helpTimeSlotsToEndOfweek = SetUpScenarios.numberOfTimeSlotsPerWeek - index_timeslot
        helpHypotheticalEnergyEVWhenCharging = state_SOCofEVLastTimeSlot/100 * maximumPowerEVChargingForNotCreatingANewPeak
        helpHypotheticalSOCWhenCharging = (helpHypotheticalEnergyEVWhenCharging / SetUpScenarios.capacityMaximal_EV)*100
        for helpCurrentHypotheticalTimeSlot in range (0, helpTimeSlotsToEndOfweek):
            helpHypotheticalEnergyEVWhenCharging  = helpHypotheticalEnergyEVWhenCharging + (maximumPowerEVChargingForNotCreatingANewPeak *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 )
            helpHypotheticalSOCWhenCharging  = (helpHypotheticalEnergyEVWhenCharging / SetUpScenarios.capacityMaximal_EV)*100

        if simulationResult_SOCofEV_BT3 >= SetUpScenarios.initialSOC_EV + SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection:
            action_EVCharging = 0
            print("STSIC: Correction of the EV (End of the week). SOC too high. Time: " +  str(index_timeslot))
        if helpHypotheticalSOCWhenCharging <= SetUpScenarios.initialSOC_EV - SetUpScenarios.endSOC_EVAllowedDeviationFromInitalValue_ForCorrection * 0.5:
            if  action_EVCharging <=  maximumPowerEVChargingForNotCreatingANewPeak:
                action_EVCharging =  maximumPowerEVChargingForNotCreatingANewPeak
            print("STSIC: Correction of the EV (End of the week). SOC too low. Time: " +  str(index_timeslot))

    if overruleActions == False:
        action_EVCharging = action_EVCharging_NotOverruled


    #Calculate the simulation values with the corrected input vectors
    if index_timeslot >=1:
        simulationResult_SOCofEV_BT3  = ((state_SOCofEVLastTimeSlot/100 * SetUpScenarios.capacityMaximal_EV + (action_EVCharging *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - energyDemandEV))  / (SetUpScenarios.capacityMaximal_EV))*100
        helpHypotheticalSOCDropNoCharging = helpHypotheticalSOCDropNoCharging + (energyDemandEV/ SetUpScenarios.capacityMaximal_EV)*100

    if index_timeslot ==0:
        simulationResult_SOCofEV_BT3  = ((SetUpScenarios.initialSOC_EV/100 * SetUpScenarios.capacityMaximal_EV + (action_EVCharging *  availabilityOfTheEV * (SetUpScenarios.chargingEfficiency_EV/100) * SetUpScenarios.timeResolution_InMinutes * 60 - energyDemandEV)) / (SetUpScenarios.capacityMaximal_EV))*100
        helpHypotheticalSOCDropNoCharging =  (energyDemandEV/ SetUpScenarios.capacityMaximal_EV)*100



    if action_EVCharging_NotOverruled != action_EVCharging:
        print("")
        print("Action overruled")
        print ("Timeslot: ", index_timeslot)
        print("state_SOCofEVLastTimeSlot: ", state_SOCofEVLastTimeSlot)
        print("action_EVCharging_NotOverruled: ", action_EVCharging_NotOverruled)
        print("action_EVCharging: ", action_EVCharging)
        print("simulationResult_SOCofEV_BT3: ", simulationResult_SOCofEV_BT3)
        print("")

    print("End IC; Output")

    print("action_EVCharging: ", action_EVCharging)
    print("")


    return action_EVCharging, simulationResult_SOCofEV_BT3,  helpCurrentPeakLoad,  helpHypotheticalSOCDropNoCharging



#'''

def simulateTimeSlot_WithAddtionalController_BT4 (overruleActions, action_SpaceHeating, state_BufferStorageTemperatureLastTimeSlot
                                                 ,helpCountNumberOfStartsIndividual_SpaceHeating,
                                                  helpCountNumberOfStarts_Combined , helpCounterNumberOfRunningSlots_SpaceHeating ,
                                                 helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating ,
                                                 helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad, helpStartedHeatingHeatPump, helpStoppedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit,
                                                 index_timeslot, outsideTemperature, PVGeneration, heatDemand, electricityDemand, priceForElectricity_CentsPerkWh, cop_SpaceHeating,
                                                 helpPVGenerationPreviousTimeSlot, helpElectricalLoadPreviousTimeSlot, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped,
                                                 heatingStartedPhysicalLimit_BufferStorage,startedHeatingSpaceHeatingCorrection_end, building_heated_up_last_timeslot_but_temperature_dropped):

    action_SpaceHeating_NotOverruled = action_SpaceHeating

    '''
    print("")
    print("------------------------------------------")
    print("")
    print("Beginning IC; Timeslot: ", index_timeslot + 1)
    print("")
    print("helpCountNumberOfStarts_Combined: ", helpCountNumberOfStarts_Combined)
    '''
    #Calculate the simulation steps



    if helpStartedHeatingHeatPump == True and helpCounterNumberOfRunningSlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
        helpStartedHeatingHeatPump = False
    if helpStoppedHeatingHeatPump == True and helpCounterNumberOfStandBySlots_Combined >=Run_Simulations.minimalRunTimeHeatPump:
        helpStoppedHeatingHeatPump = False

    if numberOfHeatPumpStartsReachedHardLimit == True:
        numberOfHeatPumpStartsReachedSoftLimit = False


    # Pre-Corrections of input values: too high input values or too low
    if action_SpaceHeating  > 1:
        action_SpaceHeating  = 1

    if action_SpaceHeating  < 0:
        action_SpaceHeating  = 0


    #Pre-Corrections: Set small heating values to 0
    if action_SpaceHeating > 0 and action_SpaceHeating < 0.1:
        action_SpaceHeating = 0


    # Pre-Corrections of input values: minimal modulation
    if action_SpaceHeating > 0.001 and action_SpaceHeating  < SetUpScenarios.minimalModulationdDegree_HP/100:
        print("Pre_Correction: Min Modulation. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + "\n")
        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100




    if  helpCountNumberOfStarts_Combined >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts_BeforeConsideringMinimalRuntime:
        numberOfHeatPumpStartsReachedSoftLimit = True

    if helpCountNumberOfStarts_Combined >= (Run_Simulations.maximumNumberOfStarts_Combined + 1) + Run_Simulations.additionalNumberOfAllowedStarts - 2:
        numberOfHeatPumpStartsReachedHardLimit = True
        numberOfHeatPumpStartsReachedSoftLimit = False


    #Calculate the hypothetical simulation values if the non-corrected actions were applied
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT4  = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT4 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


    maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP_BT4_MFH
    maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP_BT4_MFH

    if index_timeslot >=1:
        if (helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot
        if (helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot

    if (action_SpaceHeating) * SetUpScenarios.electricalPower_HP_BT4_MFH + electricityDemand > PVGeneration:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = helpCurrentPeakLoad - electricityDemand  + PVGeneration
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = helpCurrentPeakLoad - electricityDemand  + PVGeneration

    if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek > SetUpScenarios.electricalPower_HP_BT4_MFH:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = SetUpScenarios.electricalPower_HP_BT4_MFH
    if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek > SetUpScenarios.electricalPower_HP_BT4_MFH:
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek = SetUpScenarios.electricalPower_HP_BT4_MFH


    if maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP_BT4_MFH:
        maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP_BT4_MFH
    if maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP_BT4_MFH:
        maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek =Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.electricalPower_HP_BT4_MFH


    #Corrections due to violations of the temperatur constraints

    if simulationResult_BufferStorageTemperature_BT4 > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:

        helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        if helpCounterNumberOfStandBySlots_Combined >0:
            helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((Run_Simulations.numberOfTimeSlotHeatingWithMinModulationDegreeWhenStartingToHeat * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
        if action_SpaceHeating > 0.001 and helpValue_BufferStorageTemperature_WhenHeatingWithMinMod < SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit and (numberOfHeatPumpStartsReachedSoftLimit == False or helpStoppedHeatingHeatPump ==False) and numberOfHeatPumpStartsReachedHardLimit == False:
           action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
           action_SpaceHeating = 0
           print("Correction BufferStorage too high (Correction necessary) with min mod. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) +  "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4)  + "\n")
        else:
           action_SpaceHeating = 0
           print("Correction BufferStorage too high (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4) + "\n")

    if simulationResult_BufferStorageTemperature_BT4 < SetUpScenarios.minimumBufferStorageTemperature_CorrectionNecessary :
        action_SpaceHeating = 0.8 #maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP_BT4_MFH
        if building_heated_up_last_timeslot_but_temperature_dropped == True:
            action_SpaceHeating = 1.0

        print("Correction BufferStorage too low (Correction necessary). Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4) + "\n")


    # Corrections due to minimal modulation degree of the heat pump
    if action_SpaceHeating > 0.001 and action_SpaceHeating < SetUpScenarios.minimalModulationdDegree_HP /100:
        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP /100
        print("Correction Minimal Mod. SpaceHeating. Time: " +  str(index_timeslot)  + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4) + "\n")


    #Calculate the hypothetical simulation values if the  corrected actions were applied
    cop_heatPump_SpaceHeating, cop_heatPump_DHW = SetUpScenarios.calculateCOP_SingleTimeSlot(outsideTemperature)
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT4 = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT4 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


    if startedHeatingSpaceHeatingCorrection_end == True :
        action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_EndOfTheweek / SetUpScenarios.electricalPower_HP_BT4_MFH



    #Corrections due to high number of starts of the heat pump

    #Soft Limit Reached --> Consider minimum runtimes and standbytimes of the heat pump
    if numberOfHeatPumpStartsReachedSoftLimit ==True  and startedHeatingSpaceHeatingCorrection_end ==False:
        print("numberOfHeatPumpStartsReachedSoftLimit; Timeslot: ",index_timeslot)
        if helpStartedHeatingHeatPump == True:
            print("numberOfHeatPumpStartsReachedSoftLimit; started HP")

            if action_SpaceHeating > 0.01 and simulationResult_BufferStorageTemperature_BT4 <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                action_SpaceHeating =  action_SpaceHeating
            elif action_SpaceHeating > 0.01 and simulationResult_BufferStorageTemperature_BT4 > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary:
                    if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                        action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                    elif helpValue_BufferStorageTemperature_WhenHeatingWithMinMod > SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                        action_SpaceHeating =  0



            if action_SpaceHeating ==0:
                helpValue_BufferStorageTemperature_WhenHeatingWithMinMod = state_BufferStorageTemperatureLastTimeSlot  + ((1 * SetUpScenarios.minimalModulationdDegree_HP/100 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))
                if helpValue_BufferStorageTemperature_WhenHeatingWithMinMod <= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
                    action_SpaceHeating = SetUpScenarios.minimalModulationdDegree_HP/100
                else:
                    action_SpaceHeating = 0



        elif helpStoppedHeatingHeatPump ==True:
            print("numberOfHeatPumpStartsReachedSoftLimit; stopped HP")
            action_SpaceHeating = 0




    # Last heating of the week if the numberOfHeatPumpStartsReachedHardLimit
    if numberOfHeatPumpStartsReachedHardLimit ==True and startedHeatingSpaceHeatingCorrection_end ==False:
        print("numberOfHeatPumpStartsReachedHardLimit")
        # Last heating of the week
        if lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == False:
            fractionOfweekLeft =1 - (index_timeslot / SetUpScenarios.numberOfTimeSlotsPerWeek)
            differenceTargetValueEndAndUpperLimit_SpaceHeating = SetUpScenarios.maximumBufferStorageTemperature_CorrectionNecessary - (SetUpScenarios.initialBufferStorageTemperature)
            possibleTargetTemperatureForLastHeating_SpaceHeating = SetUpScenarios.initialBufferStorageTemperature  + differenceTargetValueEndAndUpperLimit_SpaceHeating  * fractionOfweekLeft
            if state_BufferStorageTemperatureLastTimeSlot < possibleTargetTemperatureForLastHeating_SpaceHeating:
                action_SpaceHeating = maximumPowerHeatPumpForNotCreatingANewPeak_DuringTheweek / SetUpScenarios.electricalPower_HP_BT4_MFH
                lastHeatingAfterHeatPumpStartsReachedHardLimitStarted = True
            if state_BufferStorageTemperatureLastTimeSlot >= possibleTargetTemperatureForLastHeating_SpaceHeating:
                action_SpaceHeating = 0

        elif lastHeatingAfterHeatPumpStartsReachedHardLimitStopped == True:
            action_SpaceHeating = 0





    #Corrections for the violations of the physical limits of the storage systems
    helpValue_BufferStorageTemperature_CorrectedModulationDegree = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))

    if heatingStartedPhysicalLimit_BufferStorage == True and numberOfHeatPumpStartsReachedHardLimit == True:
        helpValue_BufferStorageTemperature_MediumModulationDegree = state_BufferStorageTemperatureLastTimeSlot  + ((0.6 * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))

        if helpValue_BufferStorageTemperature_MediumModulationDegree >= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit and helpValue_BufferStorageTemperature_MediumModulationDegree <= SetUpScenarios.initialBufferStorageTemperature:
            action_SpaceHeating = 0.6
        elif helpValue_BufferStorageTemperature_MediumModulationDegree < SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
            action_SpaceHeating = 1
        elif helpValue_BufferStorageTemperature_MediumModulationDegree > SetUpScenarios.initialBufferStorageTemperature:
            action_SpaceHeating = 0
            heatingStartedPhysicalLimit_BufferStorage =False



    if index_timeslot ==0:
        helpValue_BufferStorageTemperature_CorrectedModulationDegree =  SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))

    if helpValue_BufferStorageTemperature_CorrectedModulationDegree >= SetUpScenarios.maximumBufferStorageTemperature_PhysicalLimit:
        action_SpaceHeating = 0
        print("Corrections Physical limit too high value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating) + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4)  + "\n")

    if helpValue_BufferStorageTemperature_CorrectedModulationDegree <= SetUpScenarios.minimumBufferStorageTemperature_PhysicalLimit:
        action_SpaceHeating = 1
        print("Corrections Physical limit too low value Space Heating. Time: " +  str(index_timeslot) + "; ANN value SpaceHeating: " + str(action_SpaceHeating)  + "; BufferStorage: " + str(simulationResult_BufferStorageTemperature_BT4) + "\n")
        heatingStartedPhysicalLimit_BufferStorage = True






    if overruleActions == False:
        action_SpaceHeating = action_SpaceHeating_NotOverruled


    #Calculate the simulation values with the corrected input vectors
    if index_timeslot >=1:
        simulationResult_BufferStorageTemperature_BT4 = state_BufferStorageTemperatureLastTimeSlot  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))

    if index_timeslot ==0:
        simulationResult_BufferStorageTemperature_BT4 = SetUpScenarios.initialBufferStorageTemperature  + ((action_SpaceHeating * cop_SpaceHeating *  SetUpScenarios.electricalPower_HP_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60  - heatDemand  * SetUpScenarios.timeResolution_InMinutes * 60 - SetUpScenarios.standingLossesBufferStorage_BT4_MFH * SetUpScenarios.timeResolution_InMinutes * 60) / (SetUpScenarios.capacityOfBufferStorage_BT4_MFH * SetUpScenarios.densityOfCement * SetUpScenarios.specificHeatCapacityOfCement))


    if action_SpaceHeating_NotOverruled != action_SpaceHeating:
        print("")
        print("Action overruled")
        print ("Timeslot: ", index_timeslot)
        print("state_BufferStorageTemperatureLastTimeSlot: ", round(state_BufferStorageTemperatureLastTimeSlot,1 ))
        print("action_SpaceHeating_NotOverruled: ",  round(action_SpaceHeating_NotOverruled,2 ))
        print("action_SpaceHeating: ",  round(action_SpaceHeating,2 ))
        print("simulationResult_BufferStorageTemperature_BT4: ",  round(simulationResult_BufferStorageTemperature_BT4,1 ))
        print("")



    '''
    print("End IC; Output")
    print("action_SpaceHeating: ", action_SpaceHeating)
    print("")
    '''

    return action_SpaceHeating, simulationResult_BufferStorageTemperature_BT4, helpCountNumberOfStartsIndividual_SpaceHeating, helpCountNumberOfStarts_Combined , helpCounterNumberOfRunningSlots_SpaceHeating  , helpCounterNumberOfRunningSlots_Combined , helpCounterNumberOfStandBySlots_SpaceHeating  , helpCounterNumberOfStandBySlots_Combined, helpCurrentPeakLoad,  helpStartedHeatingHeatPump, numberOfHeatPumpStartsReachedSoftLimit, numberOfHeatPumpStartsReachedHardLimit, lastHeatingAfterHeatPumpStartsReachedHardLimitStarted, lastHeatingAfterHeatPumpStartsReachedHardLimitStopped, heatingStartedPhysicalLimit_BufferStorage,startedHeatingSpaceHeatingCorrection_end


#'''

def simulateTimeSlot_WithAddtionalController_BT5 (overruleActions,  action_chargingPowerBat, action_disChargingPowerBat, state_SOCofBATLastTimeSlot, helpCurrentPeakLoad,
                                                 index_timeslot, outsideTemperature, PVGeneration, electricityDemand,  priceForElectricity_CentsPerkWh, helpPVGenerationPreviousTimeSlot, helpElectricalLoadPreviousTimeSlot ):


    action_chargingPowerBat_NotOverruled = action_chargingPowerBat
    action_disChargingPowerBat_NotOverruled = action_disChargingPowerBat



    #Calculate the simulation steps



    # Pre-Corrections of input values: too high or low input values
    if action_chargingPowerBat > SetUpScenarios.chargingPowerMaximal_BAT:
        action_chargingPowerBat = SetUpScenarios.chargingPowerMaximal_BAT

    if action_disChargingPowerBat > SetUpScenarios.chargingPowerMaximal_BAT:
        action_disChargingPowerBat = SetUpScenarios.chargingPowerMaximal_BAT

    if action_chargingPowerBat < 0:
        action_chargingPowerBat = 0

    if action_disChargingPowerBat < 0:
        action_disChargingPowerBat = 0


    # Pre-Corrections: No charging and discharging of the BAT at the same timeslot
    if action_chargingPowerBat > 0.01 and action_disChargingPowerBat >0.01:
        if action_chargingPowerBat >action_disChargingPowerBat:
            action_disChargingPowerBat = 0

        if action_chargingPowerBat <= action_disChargingPowerBat:
            action_chargingPowerBat = 0



    #Calculate the hypothetical simulation values if the non-corrected actions were applied
    if index_timeslot >=1:
        state_SOCofBAT = state_SOCofBATLastTimeSlot + (((action_chargingPowerBat * (SetUpScenarios.chargingEfficiency_BAT) - action_disChargingPowerBat *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )/ SetUpScenarios.capacityMaximal_BAT)*100
    if index_timeslot ==0:
        state_SOCofBAT = SetUpScenarios.initialSOC_BAT+ (((action_chargingPowerBat * (SetUpScenarios.chargingEfficiency_BAT) - action_disChargingPowerBat *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )/ SetUpScenarios.capacityMaximal_BAT)*100


    # Calculate the maximum power of the BAT for not creating a new peak load
    if index_timeslot >=1:
        if (helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpElectricalLoadPreviousTimeSlot - helpPVGenerationPreviousTimeSlot
        if (helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot) > helpCurrentPeakLoad:
            helpCurrentPeakLoad = helpPVGenerationPreviousTimeSlot - helpElectricalLoadPreviousTimeSlot

    maximumPowerBATChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_BAT

    if action_chargingPowerBat + electricityDemand > PVGeneration:
        maximumPowerBATChargingForNotCreatingANewPeak = helpCurrentPeakLoad  - electricityDemand  + PVGeneration


    if  maximumPowerBATChargingForNotCreatingANewPeak >  SetUpScenarios.chargingPowerMaximal_BAT:
        maximumPowerBATChargingForNotCreatingANewPeak = SetUpScenarios.chargingPowerMaximal_BAT


    if  maximumPowerBATChargingForNotCreatingANewPeak < Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection *  SetUpScenarios.chargingPowerMaximal_BAT:
        maximumPowerBATChargingForNotCreatingANewPeak = Run_Simulations.minimalModulationDegreeOfTheMaximumPowerInCaseOfANecessaryCorrection * SetUpScenarios.chargingPowerMaximal_BAT




    # Corrections for the SOC of the BAT
    if state_SOCofBAT > 100.01:
        action_chargingPowerBat = 0

    if state_SOCofBAT < -0.01:
        action_disChargingPowerBat = 0


    if overruleActions == False:
        action_chargingPowerBat = action_chargingPowerBat_NotOverruled
        action_disChargingPowerBat = action_disChargingPowerBat_NotOverruled


    #Calculate the simulation values with the corrected input vectors
    if index_timeslot >=1:
        state_SOCofBAT = state_SOCofBATLastTimeSlot + (((action_chargingPowerBat * (SetUpScenarios.chargingEfficiency_BAT) - action_disChargingPowerBat *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )/ SetUpScenarios.capacityMaximal_BAT)*100
    if index_timeslot ==0:
        state_SOCofBAT = SetUpScenarios.initialSOC_BAT+ (((action_chargingPowerBat * (SetUpScenarios.chargingEfficiency_BAT) - action_disChargingPowerBat *(1 /SetUpScenarios.dischargingEfficiency_BAT)) * SetUpScenarios.timeResolution_InMinutes * 60 )/ SetUpScenarios.capacityMaximal_BAT)*100



    if action_chargingPowerBat_NotOverruled != action_chargingPowerBat or action_disChargingPowerBat_NotOverruled != action_disChargingPowerBat:
        print("")
        print("Action overruled")
        print ("Timeslot: ", index_timeslot)
        print("state_SOCofBATLastTimeSlot: ", state_SOCofBATLastTimeSlot)
        print("action_chargingPowerBat_NotOverruled: ", action_chargingPowerBat_NotOverruled)
        print("action_chargingPowerBat: ", action_chargingPowerBat)
        print("action_disChargingPowerBat_NotOverruled: ", action_disChargingPowerBat_NotOverruled)
        print("action_disChargingPowerBat: ", action_disChargingPowerBat)
        print("state_SOCofBAT: ", state_SOCofBAT)
        print("")



    return action_chargingPowerBat,action_disChargingPowerBat, state_SOCofBAT,  helpCurrentPeakLoad





#'''






if __name__ == "__main__":
    print("In IC Simulation")


    if Run_Simulations.run_simulateWeeks_WithAddtionalController_Schedule == True:
        useInternalControllerToOverruleActions = Run_Simulations.useInternalControllerToOverruleActions_simulateWeeks_WithAddtionalController_Schedule
        inputVector_BT1_heatGenerationCoefficientSpaceHeating, inputVector_BT1_heatGenerationCoefficientDHW, inputVector_BT1_chargingPowerEV, inputVector_BT2_heatGenerationCoefficientSpaceHeating, inputVector_BT2_heatGenerationCoefficientDHW, inputVector_BT3_chargingPowerEV, inputVector_BT4_heatGenerationCoefficientSpaceHeating = ANN.generateActionsForAllTimeslotWithANN()
        outputVector_BT1_heatGenerationCoefficientSpaceHeating_corrected, outputVector_BT1_heatGenerationCoefficientDHW_corrected, outputVector_BT1_chargingPowerEV_corrected, outputVector_BT2_heatGenerationCoefficientSpaceHeating_corrected, outputVector_BT2_heatGenerationCoefficientDHW_corrected, outputVector_BT3_chargingPowerEV_corrected, outputVector_BT4_heatGenerationCoefficientSpaceHeating_corrected = simulateWeeks_WithAddtionalController_Schedule (useInternalControllerToOverruleActions, inputVector_BT1_heatGenerationCoefficientSpaceHeating, inputVector_BT1_heatGenerationCoefficientDHW, inputVector_BT1_chargingPowerEV, inputVector_BT2_heatGenerationCoefficientSpaceHeating, inputVector_BT2_heatGenerationCoefficientDHW, inputVector_BT3_chargingPowerEV, inputVector_BT4_heatGenerationCoefficientSpaceHeating )
        print("End of method: simulateWeeks_WithAddtionalController_Schedule()")

    if Run_Simulations.run_simulateWeeks_ConventionalControl == True:
        outputVector_BT1_heatGenerationCoefficientSpaceHeating_Conventional, outputVector_BT1_heatGenerationCoefficientDHW_Conventional, outputVector_BT1_chargingPowerEV_Conventional, outputVector_BT2_heatGenerationCoefficientSpaceHeating_Conventional, outputVector_BT2_heatGenerationCoefficientDHW_Conventional, outputVector_BT3_chargingPowerEV_Conventional, outputVector_BT4_heatGenerationCoefficientSpaceHeating_Conventional = simulateWeeks_ConventionalControl()
        print("End of method: simulateWeeks_ConventionalControl()")





