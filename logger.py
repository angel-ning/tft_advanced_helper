import time

class Logger:
    def __init__(self, filepath):
        self.log_file = open(filepath, 'w', encoding='utf8')

    def write_log(self, message):
        # We are using a different format for the timestamp here
        timestamp = time.strftime('%Y/%m/%d %H:%M:%S')
        formatted_message = '[{}] {}'.format(timestamp, message)
        print(formatted_message)
        self.log_file.write(formatted_message + '\n')

    def close_log(self):
        if self.log_file:
            self.log_file.close()
