import pickle
import os
import shutil


class File_Operation:
    """
        This class shall be used to save the model after training
        and load the saved model for prediction.

    """
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory = 'models/'

    def save_model(self, model, filename):
        """
            Method Name: save_model
            Description: Save the model file to directory
            Outcome: File gets saved
            On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, "Entered the save_model method of the File_Operation class")
        try:
            # create separate directory for each cluster
            path = os.path.join(self.model_directory, filename)
            # remove previously existing models for each clusters
            if os.path.isdir(path):
                # remove previously existing models for each clusters
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path + '/' + filename+'.sav', 'wb') as f:
                # save the model to file
                pickle.dump(model, f)
            self.logger_object.log(self.file_object, f"Model File {filename} saved. \
                                   Exited the save_model method of the Model_Finder class")

        except Exception as e:
            self.logger_object.log(self.file_object, f"Exception occurred in save_model method of\
                            the Model_Finder class. Exception message: {str(e)}")
            self.logger_object.log(self.file_object, f"Model File {filename} could not be saved. \
                                        Exited the save_model method of the Model_Finder class")
            raise RuntimeError

    def load_model(self, filename):
        """
        Method Name: load_model
        Description: load the model file to memory
        Output: The Model file loaded in memory
        On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, "Entered the load_model method of the File_Operation class")
        try:
            with open(self.model_directory + filename + '/' + filename + '.sav', 'rb') as f:
                self.logger_object.log(self.file_object, f"Model File {filename} loaded. \
                Exited the load_model method of the Model_Finder class")
                return pickle.load(f)
        except Exception as ex:
            self.logger_object.log(self.file_object, f"Exception occurred in load_model method of the\
                                    Model_Finder class. Exception message: {str(ex)}")
            self.logger_object.log(self.file_object, f"Model File {filename} could not be saved. \
            Exited the load_model method of the Model_Finder class")
            raise RuntimeError

    def find_correct_model_file(self, cluster_number):
        """
        Method Name: find_correct_model_file
        Description: Select the correct model based on cluster number
        Output: The Model file
        On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, "Entered the find_correct_model_file \
                                            method of the File_Operation class")
        model_name = None
        try:
            folder_name = self.model_directory
            list_of_files = os.listdir(folder_name)
            for file in list_of_files:
                if file.index(str(cluster_number)) != -1:
                    model_name = file.split('.')[0]
            self.logger_object.log(self.file_object,
                                   "Exited the find_correct_model_file method of the Model_Finder class.")
            return model_name
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   f"Exception occurred in find_correct_model_file \
                                   method of the Model_Finder class. Exception message: {str(e)}.\
            'Exited the find_correct_model_file method of the Model_Finder class with Failure")
            raise RuntimeError
