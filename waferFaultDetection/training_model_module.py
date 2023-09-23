"""
This is the module for Training the Machine Learning Model.

"""

# Doing the necessary imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from data_ingestion import data_loader
from data_preprocessing import preprocessing
from data_preprocessing import clustering
from best_model_finder import tuner
from file_operations import file_methods
from application_logging import logger


# Creating the common Logging object
class trainModel:

    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')

    def training_model(self):
        # Logging the start of Training
        self.log_writer.log(self.file_object, 'Start of Training')
        try:
            # Getting the data from the source
            data_getter = data_loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            """doing the data preprocessing"""

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            # remove the unnamed column as it doesn't contribute to prediction.
            data = preprocessor.remove_columns(data, ['Wafer'])

            # create separate features and labels
            x, y = preprocessor.separate_label_feature(data, label_column_name='Output')

            # check if missing values are present in the dataset
            is_null_present = preprocessor.is_null_present(x)

            # if missing values are there, replace them appropriately.
            if is_null_present:
                # missing value imputation
                x = preprocessor.impute_missing_values(x)

            # check further which columns do not contribute to predictions
            # if the standard deviation for a column is zero, it means that the column has constant values,
            # and they are giving the same output both for good and bad sensors
            # prepare the list of such columns to drop
            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(x)

            # drop the columns obtained above
            x = preprocessor.remove_columns(x, cols_to_drop)

            """ Applying the clustering approach"""
            # object initialization.
            kmeans = clustering.KMeansClustering(self.file_object, self.log_writer)
            # using the elbow plot to find the number of optimum clusters
            number_of_clusters = kmeans.elbow_plot(x)
            # Divide the data into clusters
            x = kmeans.create_clusters(x, number_of_clusters)
            # create a new column in the dataset consisting of the corresponding cluster assignments.
            x['Labels'] = y

            # getting the unique clusters from our dataset
            list_of_clusters = x['Cluster'].unique()

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""

            for i in list_of_clusters:
                # filter the data for one cluster
                cluster_data = x[x['Cluster'] == i]

                # Prepare the feature and Label columns
                cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis=1)
                cluster_label = cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label,
                                                                    test_size=1 / 3, random_state=355)
                # object initialization
                model_finder = tuner.Model_Finder(self.file_object, self.log_writer)
                # getting the best model for each of the clusters
                le = LabelEncoder()
                y_train = le.fit_transform(y_train)
                best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)
                # saving the best model to the directory.
                file_op = file_methods.File_Operation(self.file_object, self.log_writer)
                _ = file_op.save_model(best_model, best_model_name+str(i))

            # logging the successful Training
            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()

        except Exception:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise RuntimeError
