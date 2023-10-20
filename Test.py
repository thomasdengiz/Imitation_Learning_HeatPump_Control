import os
import pandas as pd
import SetUpScenarios

input_dir = r"C:\Users\wi9632\Desktop\Daten\DSM\Training_Data\Weeks_BT4_New\kWh25\Min_Costs_Scaled_PV_0_kWp_30_Min"
output_dir = r"C:\Users\wi9632\Desktop\Daten\DSM\Training_Data\Weeks_BT4_New\kWh25\Min_Costs_Scaled_PV_0_kWp_30_Min_A"

for subfolder in os.listdir(input_dir):
    subfolder_path = os.path.join(input_dir, subfolder)
    if os.path.isdir(subfolder_path):
        for week_folder in os.listdir(subfolder_path):
            week_folder_path = os.path.join(subfolder_path, week_folder)
            if os.path.isdir(week_folder_path):
                input_file_path = os.path.join(week_folder_path, "BT4_HH1.csv")
                if os.path.exists(input_file_path):
                    # Read the input file
                    df = pd.read_csv(input_file_path, sep=";")

                    # Perform some manipulations on the dataframe
                    # ...                      # Calculate price factor
                    updatingFrequencyEDFPrices = 1440 / SetUpScenarios.timeResolution_InMinutes
                    updatingFrequencyAverageTemperature = 1440 / SetUpScenarios.timeResolution_InMinutes

                    helpCounterTimeSlotsForUpdatingEDFPrices = 0

                    # define empty lists for the new columns
                    price_factors = []
                    storage_factors = []
                    avg_temperatures = []

                    # Calculate empirial cumulative distribution function (ECDF) for the future prices
                    for index_timeslot in df.index:
                        helpCounterTimeSlotsForUpdatingEDFPrices += 1
                        if index_timeslot == 0 or helpCounterTimeSlotsForUpdatingEDFPrices >= updatingFrequencyEDFPrices:
                            import statsmodels
                            from statsmodels.distributions.empirical_distribution import ECDF

                            electricityTarifCurrentDay = df.loc[index_timeslot: index_timeslot + (1440 / SetUpScenarios.timeResolution_InMinutes) - 1, 'Price [Cent/kWh]'].values
                            ecdf_prices = ECDF(electricityTarifCurrentDay)

                        priceFactor = 1 - ecdf_prices(df.loc[index_timeslot, 'Price [Cent/kWh]']- 0.001)

                        # Calculate the storage factor
                        if index_timeslot >=1:
                            storageFactor = 1 - (df.loc[index_timeslot - 1, 'temperatureBufferStorage']  - SetUpScenarios.minimalBufferStorageTemperature) / (SetUpScenarios.maximalBufferStorageTemperature - SetUpScenarios.minimalBufferStorageTemperature)
                        else:
                            storageFactor = 0.5

                        # Calculate the average temperature of the current day
                        if index_timeslot == 0 or helpCounterTimeSlotsForUpdatingEDFPrices >= updatingFrequencyEDFPrices:
                            helpCounterTimeSlotsForUpdatingEDFPrices = 0
                            sumTemperature = 0
                            helpCounterTimeSlots = 0
                            for i in range(0, int((1440 / SetUpScenarios.timeResolution_InMinutes))):
                                if index_timeslot + 1 + i < SetUpScenarios.numberOfTimeSlotsPerWeek:
                                    sumTemperature = sumTemperature + df.loc[i + index_timeslot + 1, 'Outside Temperature [C]']
                                    helpCounterTimeSlots += 1
                            if helpCounterTimeSlots > 0:
                                averageTemperature = sumTemperature / helpCounterTimeSlots


                        price_factors.append(priceFactor)
                        storage_factors.append(storageFactor)
                        avg_temperatures.append(averageTemperature)


                    # Add new columns to the dataframe

                    df["PriceFactor"] = price_factors
                    df["StorageFactor"] = storage_factors
                    df["AverageTemperature"] = avg_temperatures

                    df["PriceFactor"] = df["PriceFactor"].round(2)
                    df["StorageFactor"] = df["StorageFactor"].round(2)
                    df["AverageTemperature"] = df["AverageTemperature"].round(1)

                    # Create the output directory if it doesn't exist
                    output_subfolder_path = os.path.join(output_dir, subfolder, week_folder)
                    if not os.path.exists(output_subfolder_path):
                        os.makedirs(output_subfolder_path)

                    # Write the updated dataframe to a new csv file
                    output_file_path = os.path.join(output_subfolder_path, "BT4_HH1.csv")
                    df.to_csv(output_file_path, sep=";", index=False)








