from sklearn.preprocessing import StandardScaler
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import mean_squared_error
import numpy as np

# Define the file paths
MLSupvervised_input_data_file_path = r"C:\Users\wi9632\Desktop\MLSupvervised_input_data.csv"
MLSupervised_output_data_file_path = r"C:\Users\wi9632\Desktop\MLSupervised_output_data.csv"

# Read MLSupvervised_input_data and MLSupvervised_input_data from a CSV file as a NumPy array
MLSupvervised_input_data = np.loadtxt(MLSupvervised_input_data_file_path, delimiter=";", dtype=np.float64)
MLSupervised_output_data = np.loadtxt(MLSupervised_output_data_file_path, delimiter=";", dtype=np.float64)

#Standardize the data
scaler_standardized_X = StandardScaler()
MLSupvervised_input_data = scaler_standardized_X.fit_transform(MLSupvervised_input_data)

scaler_standardized_Y = StandardScaler()
MLSupervised_output_data = scaler_standardized_Y.fit_transform(MLSupervised_output_data.reshape(-1, 1))

#Split data
index_X_Train_End = int(0.7 * len(MLSupvervised_input_data))
index_X_Validation_End = int(1.0 * len(MLSupvervised_input_data))

X_train = MLSupvervised_input_data[0: index_X_Train_End]
X_valid = MLSupvervised_input_data[index_X_Train_End: index_X_Validation_End]
Y_train = MLSupervised_output_data[0: index_X_Train_End]
Y_valid = MLSupervised_output_data[index_X_Train_End: index_X_Validation_End]

X_train_valid = np.concatenate((X_train, X_valid))
Y_train_valid = np.concatenate((Y_train, Y_valid))
Y_train_valid = Y_train_valid.ravel()

# define the model
changingParameter_max_samples = [1.0]
changingParameter_max_features = [0.4, 0.6, 0.8, 1]
changingParameter_n_estimators = [5, 20, 50, 100, 200, 1000]  # Number of trees in the forest
changingParameter_max_depth = [3, 5, None]
numberOfDifferentConfigurations = len(changingParameter_max_samples) * len(changingParameter_max_features) * len(
    changingParameter_n_estimators) * len(changingParameter_max_depth)

currentBestParameter_max_samples = -1
currentBestParameter_max_features = -1
currentBestParameter_n_estimators = -1
currentBestParameter_max_depth = -1
currentBestRMSE = 999999999

rmse_forEachConfiguration = np.zeros(numberOfDifferentConfigurations)
currentIndexLoop = 0

# Loop for hyperparameter tuning on the validation dataset
for max_samples_iteration in changingParameter_max_samples:
    for max_features_iteration in changingParameter_max_features:
        for n_estimators_iteration in changingParameter_n_estimators:
            for max_depth_iteration in changingParameter_max_depth:

                print(f"Run {currentIndexLoop + 1} from {numberOfDifferentConfigurations}")
                model = RandomForestRegressor(n_estimators=n_estimators_iteration, max_samples=max_samples_iteration,
                                              max_features=max_features_iteration, criterion='squared_error',
                                              max_depth=max_depth_iteration)

                cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
                n_scores = cross_val_score(model, X_train_valid, Y_train_valid, scoring='neg_mean_squared_error', cv=cv,
                                           n_jobs=-1, error_score='raise')
                mean_rmse = round(n_scores.mean() * (-1), 3)
                print(f"mean_rmse: {mean_rmse}")

                # Check if the current configuration is better then the previously best configuration
                if currentBestRMSE > mean_rmse:
                    currentBestRMSE = mean_rmse
                    currentBestParameter_max_samples = max_samples_iteration
                    currentBestParameter_max_features = max_features_iteration
                    currentBestParameter_n_estimators = n_estimators_iteration
                    currentBestParameter_max_depth = max_depth_iteration
                    bestTrainedModel = model
                currentIndexLoop += 1
                print("")

                if currentIndexLoop == numberOfDifferentConfigurations:
                    # Print best results
                    print(f"Best Configuration")
                    print(f"currentBestParameter_max_samples: {currentBestParameter_max_samples}")
                    print(f"currentBestParameter_max_features: {currentBestParameter_max_features}")
                    print(f"currentBestParameter_n_estimators: {currentBestParameter_n_estimators}")
                    print(f"currentBestParameter_max_depth: {currentBestParameter_max_depth}")
                    print(f"currentBestRMSE: {currentBestRMSE}")

                    # Train tree with default values
                    model_default = RandomForestRegressor()
                    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
                    n_scores = cross_val_score(model_default, X_train_valid, Y_train_valid,
                                               scoring='neg_mean_squared_error', cv=cv, n_jobs=-1, error_score='raise')
                    mean_rmse_default = round(n_scores.mean() * (-1), 3)
                    print(f"mean_rmse Default: {mean_rmse_default}")
                    print(f"")



