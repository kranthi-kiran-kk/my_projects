from os import listdir
import pandas
from application_logging.logger import App_Logger


class DataTransform:
    """

     This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

     """

    def __init__(self):
        self.good_data_path = "Training_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()

    def replace_missing_with_null(self):
        """
        Method Name: replace_missing_with_null
        Description: This method replaces the missing values in columns with "NULL" to
                     store in the table. We are using substring in the first column to
                     keep only "Integer" data for ease up the loading.
                     This column is anyway going to be removed during training.

        """

        log_file = open("Training_Logs/dataTransformLog.txt", 'a+')
        try:
            only_files = [f for f in listdir(self.good_data_path)]
            for file in only_files:
                csv = pandas.read_csv(self.good_data_path + "/" + file)
                csv.fillna('NULL', inplace=True)
                csv['Wafer'] = csv['Wafer'].str[6:]
                csv.to_csv(self.good_data_path + "/" + file, index=None, header=True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % file)
        except Exception as ex:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % ex)
            log_file.close()
            raise ex
        log_file.close()
