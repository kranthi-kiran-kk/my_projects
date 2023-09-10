import shutil
import sqlite3
from os import listdir
import os
import csv
from application_logging.logger import App_Logger


class dBOperation:
    """
    This class shall be used for handling all the SQL operations.

    """

    def __init__(self):
        self.path = 'Prediction_Database/'
        self.bad_file_path = "Prediction_Raw_Files_Validated/Bad_Raw"
        self.good_file_path = "Prediction_Raw_Files_Validated/Good_Raw"
        self.database_log = "Prediction_Logs/DataBaseConnectionLog.txt"
        self.logger = App_Logger()

    def data_base_connection(self, database_name):

        """
        Method Name: data_base_connection
        Description: This method creates the database with the given name and if database already exists \
        then opens the connection to the DB.
        Output: Connection to the DB
        On Failure: Raise ConnectionError
        """
        try:
            conn = sqlite3.connect(self.path + database_name + '.db')
            file = open(self.database_log, 'a+')
            self.logger.log(file, f"Opened {database_name} database successfully")
            file.close()
        except ConnectionError as cex:
            file = open(self.database_log, 'a+')
            self.logger.log(file, f"Error while connecting to database: {cex}")
            file.close()
            raise ConnectionError
        return conn

    def create_table_db(self, database_name, column_names):

        """
           Method Name: create_table_db
           Description: This method creates a table in the given database which will be used to \
           insert the Good data after raw data validation.
           Output: None
           On Failure: Raise Exception

        """
        conn = self.data_base_connection(database_name)
        try:

            conn.execute('DROP TABLE IF EXISTS Good_Raw_Data;')

            for key in column_names.keys():
                column_type = column_names[key]

                # we will remove the column of string datatype before loading as it is not needed for training
                # in try block we check if the table exists, if yes then add columns to the table
                # else in catch block we create the table
                try:
                    conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" \
                    {dataType}'.format(column_name=key, dataType=column_type))
                except Exception:
                    conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} \
                    {dataType})'.format(column_name=key, dataType=column_type))

            conn.close()

            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Tables created successfully!!")
            file.close()

            file = open(self.database_log, 'a+')
            self.logger.log(file, f"Closed {database_name} database successfully")
            file.close()

        except Exception as e:
            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()

            file = open(self.database_log, 'a+')
            self.logger.log(file, "Closed %s database successfully" % database_name)
            file.close()
            raise e
        finally:
            if conn is not None:
                conn.close()

    def insert_into_table_good_data(self, database):

        """
           Method Name: insert_into_table_good_data
           Description: This method inserts the Good data files from the Good_Raw folder into the
                        above created table.
           Output: None
           On Failure: Raise Exception

        """

        conn = self.data_base_connection(database)
        good_file_path = self.good_file_path
        bad_file_path = self.bad_file_path
        only_files = [f for f in listdir(good_file_path)]
        log_file = open("Prediction_Logs/DbInsertLog.txt", 'a+')

        for file in only_files:
            try:

                with open(good_file_path + '/' + file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=list_))
                                self.logger.log(log_file, f" {file}: File loaded successfully!!")
                                conn.commit()
                            except Exception:
                                raise RuntimeError

            except Exception as e:

                conn.rollback()
                self.logger.log(log_file, "Error while creating table: %s " % e)
                shutil.move(good_file_path + '/' + file, bad_file_path)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()
                raise e

        conn.close()
        log_file.close()

    def selecting_data_from_table_into_csv(self, database):
        """
        Method Name: selecting_data_from_table_into_csv
        Description: This method exports the data in GoodData table as a CSV file. in a given location.
                    above created .
        Output: None
        On Failure: Raise Exception

        """

        file_from_db = 'Prediction_FileFromDB/'
        file_name = 'InputFile.csv'
        log_file = open("Prediction_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = self.data_base_connection(database)
            sql_select = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sql_select)

            results = cursor.fetchall()

            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            # Make the CSV output directory
            if not os.path.isdir(file_from_db):
                os.makedirs(file_from_db)

            # Open CSV file for writing.
            csv_file = csv.writer(open(file_from_db + file_name, 'w', newline=''),
                                  delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csv_file.writerow(headers)
            csv_file.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")

        except Exception as ex:
            self.logger.log(log_file, f"File exporting failed. Error : {ex}")
            raise RuntimeError
