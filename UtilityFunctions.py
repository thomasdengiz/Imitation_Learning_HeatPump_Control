# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 10:13:57 2022

@author: wi9632
"""
# This method calculates the drifting features between training, validation, and test dataset (covariateShift) 
# using a RandomForestClassifier and the AOC_ROC values of the classificaiton

def printDriftingFeatures(training_data, validation_data, test_data):
    ## importing libraries
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import LabelEncoder
    
    pd.options.mode.chained_assignment = None  # default='warn'
    
    
    treshold_AOC_ROC_ForIdentifyingDriftingFeature = 0.8
    
    
    ## reading files
    train =  training_data.copy()
    valid =  validation_data.copy()
    test =  test_data.copy()
    
    #Define the data for the new train and test dataset
    for iteration in range (0, 3):
        
        if iteration ==0:
            train_new =  train
            test_new =  valid
            print("\nROC-AUC values for the different features between Training and Validation dataset\n")
        if iteration ==1:
            train_new = train
            test_new = test
            print("\nROC-AUC values for the different features between Training and Test dataset\n")
        if iteration ==2:
            train_new = valid
            test_new = test
            print("\nROC-AUC values for the different features between Validation and Test dataset\n")
            
    
        ## label encoding
        number = LabelEncoder()
        for i in train_new.columns:
            if (train_new[i].dtype == 'object'):
              train_new[i] = number.fit_transform(train_new[i].astype('str'))
              train_new[i] = train_new[i].astype('object')
        
        for i in test.columns:
            if (test_new[i].dtype == 'object'):
              test_new[i] = number.fit_transform(test_new[i].astype('str'))
              test_new[i] = test_new[i].astype('object')
        
        ## creating a new feature origin
        train_new['origin'] = 0
        test_new['origin'] = 1
        #training = train_new.drop('price_doc',axis=1) #droping target variable
        
        ## taking sample from training and test data
        training = train_new.sample(int (len(train_new)/2), random_state=12)
        testing = test_new.sample(int (len(test_new)/2), random_state=11)
        
        ## combining random samples
        combi = training.append(testing)
        combi_copy = combi.copy()
        y = combi['origin']
        combi.drop('origin',axis=1,inplace=True)
        
        ## modelling
        model = RandomForestClassifier(n_estimators = 100, max_depth = 10,min_samples_leaf = 5)
        drop_list = []
    
        for i in combi.columns:
            score = cross_val_score(model,pd.DataFrame(combi[i]),y,cv=10,scoring='roc_auc')
            if (np.mean(score) >= treshold_AOC_ROC_ForIdentifyingDriftingFeature):
                drop_list.append(i)
                print(f"{i}: {round((np.mean(score)), 2)}   --> Drifting feature")
            else:
                print(f"{i}: {round((np.mean(score)), 2)}")
                
                
def calculate_Kullback_Leibler_Divergence (training_data, validation_data, test_data):
    import scipy
    from scipy.stats import norm
    from scipy.stats import rv_histogram
    import numpy as np
    import pandas as pd
    

    features_overall = list(training_data.columns.values)
    
    for currentFeature in features_overall:

        data_train = training_data[[currentFeature]].values
        data_valid = validation_data[[currentFeature]].values
        data_test = test_data[[currentFeature]].values
        
        #Make distribution objects of the histograms
        histogram_dist_train = rv_histogram(np.histogram(data_train, bins='auto'))
        histogram_dist_valid = rv_histogram(np.histogram(data_valid, bins='auto'))
        histogram_dist_test = rv_histogram(np.histogram(data_test, bins='auto'))
        
        
        #Generate arrays of pdf evaluations
        X1 = np.linspace(np.min(data_train), np.max(data_train), 10000)
        X2 = np.linspace(np.min(data_valid), np.max(data_valid), 10000)
        X3 = np.linspace(np.min(data_test), np.max(data_test), 10000)
        rvs_train = [histogram_dist_train.pdf(x) for x in X1]
        rvs_valid = [histogram_dist_valid.pdf(x) for x in X2]
        rvs_test = [histogram_dist_test.pdf(x) for x in X3]
        
        #Calculate the Kullback–Leibler divergence between the different datasets
        entropy_train_valid = scipy.special.rel_entr(rvs_train, rvs_valid)  
        entropy_train_test = scipy.special.rel_entr(rvs_train, rvs_test) 
        entropy_valid_test = scipy.special.rel_entr(rvs_valid, rvs_test) 
         
        kl_div_train_valid = np.sum(entropy_train_valid)
        kl_div_train_test = np.sum(entropy_train_test)
        kl_div_valid_test = np.sum(entropy_valid_test)
        
        
        #Print the values of the Kullback–Leibler divergence
        currentFeature
        print(f"\n\nFeature {currentFeature}")
        print("Kullback-Leibler divergence without normal distribution/n")
        print(f"Kullback–Leibler divergence between training and validation dataset: {round(kl_div_train_valid, 2)}")
        print(f"Kullback–Leibler divergence between training and test dataset: {round(kl_div_train_test, 2)}")
        print(f"Kullback–Leibler divergence between validation and test dataset: {round(kl_div_valid_test, 2)} \n\n")
        
        
        #Make normal distribution objects from data mean and standard deviation
        norm_dist_train = norm(data_train.mean(), data_train.std())
        norm_dist_valid = norm(data_valid.mean(), data_valid.std())
        norm_dist_test = norm(data_test.mean(), data_test.std())
        
        #Generate arrays of pdf evaluations
        X1 = np.linspace(np.min(data_train), np.max(data_train), 10000)
        X2 = np.linspace(np.min(data_valid), np.max(data_valid), 10000)
        X3 = np.linspace(np.min(data_test), np.max(data_test), 10000)
        rvs_train = [norm_dist_train.pdf(x) for x in X1]
        rvs_valid = [norm_dist_valid.pdf(x) for x in X2]
        rvs_test = [norm_dist_test.pdf(x) for x in X3]
        
        #Calculate the Kullback–Leibler divergence between the different datasets
        entropy_train_valid = scipy.special.rel_entr(rvs_train, rvs_valid)  
        entropy_train_test = scipy.special.rel_entr(rvs_train, rvs_test) 
        entropy_valid_test = scipy.special.rel_entr(rvs_valid, rvs_test) 
         
        kl_div_train_valid = np.sum(entropy_train_valid)
        kl_div_train_test = np.sum(entropy_train_test)
        kl_div_valid_test = np.sum(entropy_valid_test)
        
        
        #Print the values of the Kullback–Leibler divergence
        print(f"Feature {currentFeature}")
        print("Kullback-Leibler divergence with normal distribution/n")
        print(f"Kullback–Leibler divergence between training and validation dataset: {round(kl_div_train_valid, 2)}")
        print(f"Kullback–Leibler divergence between training and test dataset: {round(kl_div_train_test, 2)}")
        print(f"Kullback–Leibler divergence between validation and test dataset: {round(kl_div_valid_test, 2)}")   
    

    
# This method plots the combined histograms of the pandas-dataframes for the training_data, validation_data and test_data.
#If plotSingleHistograms==True, the single histograms for each feature for the training, validation and test dataset are also plotted        
def plotHistograms  (training_data, validation_data, test_data, plotSingleHistograms):

    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import rv_histogram
    import numpy as np
    
    sns.set_style('ticks')
    
    features_overall = list(training_data.columns.values)
    print(features_overall)
    
    for currentFeature in features_overall:
        
        data_train = training_data[[currentFeature]].values
        data_valid = validation_data[[currentFeature]].values
        data_test = test_data[[currentFeature]].values
        
        #Make distribution objects of the histograms
        histogram_dist_train = rv_histogram(np.histogram(data_train, bins='auto'))
        histogram_dist_valid = rv_histogram(np.histogram(data_valid, bins='auto'))
        histogram_dist_test = rv_histogram(np.histogram(data_test, bins='auto'))
        

    
        if plotSingleHistograms ==True:
            displot_dataTrain=sns.displot(data_train, bins='auto', kde=False)
            displot_dataTrain._legend.remove()
            plt.ylabel('Count')
            plt.xlabel('Training Data')
            plt.title(f"{currentFeature}\nHistogram Training Data", fontsize = 18)
            plt.show()
            
            displot_dataValid =sns.displot(data_valid, bins='auto', kde=False)
            displot_dataValid._legend.remove()
            plt.ylabel('Count')
            plt.xlabel('Validation Data')
            plt.title(f"{currentFeature}\nHistogram Validation Data", fontsize = 18)
            plt.show()
            
            displot_dataTest =sns.displot(data_test, bins='auto', kde=False)
            displot_dataTest._legend.remove()
            plt.ylabel('Count')
            plt.xlabel('Test Data')
            plt.title(f"{currentFeature}\nHistogram Test Data", fontsize = 18)
            plt.show()
        

        
        #Plot desity functions of the histograms for training and validation data

        
        
        # Plot histograms and normal distribution in a combined plot for training and validation data
        X1 = np.linspace(data_train.min(), data_train.max(), 1000)
        X2 = np.linspace(data_valid.min(), data_valid.max(), 1000)
        X3 = np.linspace(data_test.min(), data_test.max(), 1000)
        fig, ax = plt.subplots(1,2, figsize=(12,6))
        ax[0].plot(X1, histogram_dist_train.pdf(X1), label='train')
        ax[0].plot(X2, histogram_dist_valid.pdf(X2), label='valid')
        ax[0].plot(X3, histogram_dist_test.pdf(X3), label='test')
        ax[0].set_title(f'{currentFeature}\nHistogram distributions', fontsize = 14)
        ax[0].legend()
        #Try to plot figure 1 onto the right side of the combined figure
        sns.kdeplot(data=data_train.squeeze(), color='cornflowerblue', label='train', fill=False, ax=ax[1])
        sns.kdeplot(data=data_valid.squeeze(),  color='orange', label='valid', fill=False, ax=ax[1])
        sns.kdeplot(data=data_test.squeeze(),  color='green', label='test', fill=False, ax=ax[1])
        ax[1].set_title(f'{currentFeature}\nKernel density estimation', fontsize = 14)
        ax[1].legend()
        plt.show()
        
        '''
        # Plot histograms and normal distribution in a combined plot for training and validation data
        X1 = np.linspace(data_train.min(), data_train.max(), 1000)
        X2 = np.linspace(data_valid.min(), data_valid.max(), 1000)
        X3 = np.linspace(data_test.min(), data_test.max(), 1000)
        fig, ax = plt.subplots(1,2, figsize=(12,6))
        ax[0].plot(X1, histogram_dist_train.pdf(X1), label='train')
        ax[0].plot(X2, histogram_dist_valid.pdf(X2), label='valid')
        ax[0].plot(X3, histogram_dist_test.pdf(X3), label='test')
        ax[0].set_title(f'{currentFeature}\nHistogram distributions', fontsize = 14)
        ax[0].legend()
        ax[1].plot(X1, norm_dist_train.pdf(X1), label='train')
        ax[1].plot(X2, norm_dist_valid.pdf(X2), label='valid')
        ax[1].plot(X3, norm_dist_test.pdf(X3), label='test')
        ax[1].set_title(f'{currentFeature}\nNormal distributions', fontsize = 14)
        ax[1].legend()
        '''
        
    plt.close()
    
def calculateCorrelationBetweenInputFeaturesAndOutputLabels (input_features_training_data, input_features_validation_data, input_features_test_data, input_labels_training_data, input_labels_validation_data, input_labels_test_data):
    import scipy.stats
    
    inputFeatures = list(input_features_training_data.columns.values)
    inputLabels = list(input_labels_training_data.columns.values)
    
    print("Correlation Analysis (Pearson) \n")
    for feature_1 in inputFeatures:
        for feature_2 in inputLabels:

            correlation =round(scipy.stats.pearsonr(input_features_training_data[feature_1], input_labels_training_data[feature_2])[0],2)
            print(f"Training Data: {feature_1} and {feature_2} = {correlation}")
            correlation =round(scipy.stats.pearsonr(input_features_validation_data[feature_1], input_labels_validation_data[feature_2])[0],2)
            print(f"Validation Data: {feature_1} and {feature_2} = {correlation}")
            correlation =round(scipy.stats.pearsonr(input_features_test_data[feature_1], input_labels_test_data[feature_2])[0],2)
            print(f"Test Data: {feature_1} and {feature_2} = {correlation}")
            print("")

        print("")
        
   