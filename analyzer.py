import csv 
import time

class anomaly_analyzer():
    def __init__(self):
        self.lock = None
    def run(self,lock):
        self.lock = lock
        while True:
            time.sleep(1)
            self.analyze_frequency()
    def analyze_frequency(self):
        IP = 0
        Timestamp = 1 
        lis = []
        IPs_list = []

        def read_data_from_csv():
            self.lock.acquire()
            with open('ssh_logs.csv') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in reader:
                    if row[IP] != 'IP': #remove header of csv file
                        lis.append(csv_data_holder(row[IP],row[Timestamp]))
                        IPs_list.append(row[IP])
            self.lock.release()
            lis.sort(key=lambda x: str(x))
       
        read_data_from_csv()

        def devide_to_lists_by_IPs():
            lists_of_IPs_and_timestamps = []
            _IPs_list = set(IPs_list)
            for k in _IPs_list:
                t = list(filter(lambda x:str(x) == k,lis))
                lists_of_IPs_and_timestamps.append(t)

            for i in lists_of_IPs_and_timestamps:
                for j in i:
                    print str(j)
                print '====================================='
        
        devide_to_lists_by_IPs()



class csv_data_holder():
    def __init__(self,ip,timestamp):
        self.IP = ip
        self.timestamp = timestamp
    def __str__(self):
        return self.IP