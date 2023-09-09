import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operations import file_methods


class KMeansClustering:
    """
    This class shall  be used to divide the data into clusters before training.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def elbow_plot(self, data):
        """
        Method Name: elbow_plot
        Description: This method saves the plot to decide the optimum number of clusters to the file.
        Output: A picture saved to the directory
        On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')
        # initializing an empty list
        wcss = []
        try:
            for i in range(1, 11):
                # initializing the KMeans object
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
                # fitting the data to the KMeans Algorithm
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)
            # creating the graph between WCSS and the number of clusters
            plt.plot(range(1, 11), wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            # saving the elbow plot locally
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')
            # finding the value of the optimum cluster programmatically
            kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger_object.log(self.file_object, f"The optimum number of clusters is: {str(kn.knee)} . \
                                Exited the elbow_plot method of the KMeansClustering class")
            return kn.knee

        except Exception as ex:
            self.logger_object.log(self.file_object, f"Exception occurred in elbow_plot method of the \
            KMeansClustering class. Exception message: {str(ex)} Finding the number of \
            clusters failed. Exited the elbow_plot method of the KMeansClustering class")
            raise RuntimeError

    def create_clusters(self, data, number_of_clusters):
        """
        Method Name: create_clusters
        Description: Create a new dataframe consisting of the cluster information.
        Output: A dataframe with cluster column
        On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, "Entered the create_clusters method of the KMeansClustering class")
        try:
            kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            #  divide data into clusters
            y_kmeans = kmeans.fit_predict(data)

            file_op = file_methods.File_Operation(self.file_object, self.logger_object)
            # saving the KMeans model to directory passing 'Model' as the functions need three parameters
            # save_model = file_op.save_model(kmeans, 'KMeans')
            _ = file_op.save_model(kmeans, 'KMeans')
            # create a new column in dataset for storing the cluster information
            data['Cluster'] = y_kmeans
            self.logger_object.log(self.file_object, "successfully created '+str(kn.knee)+ 'clusters. \
            Exited the create_clusters method of the KMeansClustering class")
            return data
        except Exception as ex:
            self.logger_object.log(self.file_object, f"Exception occurred in create_clusters method of\
            the KMeansClustering class. Exception message: {str(ex)} Fitting the data to clusters failed.\
            Exited the create_clusters method of the KMeansClustering class")
            raise RuntimeError
