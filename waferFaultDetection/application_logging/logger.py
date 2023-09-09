from datetime import datetime


class App_Logger:

    def __init__(self):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

    def log(self, file_object, log_message,):
        # file_object.write(str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message +"\n")
        file_object.write(f"{str(self.date)}/{str(self.current_time)}'\t\t' {log_message} '\n'")
