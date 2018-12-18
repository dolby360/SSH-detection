import csv 
import time
from decimal import Decimal 

class anomaly_analyzer():
    def __init__(self):
        self.lock = None
    def run(self,lock):
        self.lock = lock
        while True:
            time.sleep(1)
            self.analyze_frequency()
            self.net_analyzer()

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
            self.lists_of_IPs_and_timestamps = []
            _IPs_list = set(IPs_list)
            for k in _IPs_list:
                t = list(filter(lambda x:str(x) == k,lis))
                self.lists_of_IPs_and_timestamps.append(t)

            # for i in self.lists_of_IPs_and_timestamps:
            #     for j in i:
            #         print str(j) + '   '  + str(j.get_timestamp())
            #     print '====================================='
        
        devide_to_lists_by_IPs()

        
        for listItem in self.lists_of_IPs_and_timestamps:
            b = 0
            for j in range(0,len(listItem) - 1):
                b += (listItem[j+1].get_timestamp() - listItem[j].get_timestamp())
            avg = int(b/len(listItem))
            if avg < 5 and len(listItem) > 2:
                print 'Computer with ip: ' + listItem[0].get_IP() + ' try to make SSH connection every: ' + str(avg) + ' seconds' 
                #Block the IP
                # import subprocess
                # subprocess.Popen("sudo iptables -A INPUT -s " +listItem[0].get_IP()+ " -p TCP -j DROP")

    def net_analyzer(self):
        lis = []
        IPs_list = []
        IP = 0
        Timestamp = 1 
        def read_data_from_csv():
            with open('IPs_database.csv') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in reader:
                    if row[IP] != 'IP': #remove header of csv file
                        lis.append(csv_data_holder(row[IP],row[Timestamp]))
            lis.sort(key=lambda x: str(x))
       
        read_data_from_csv()

        IPs_list = list(map(lambda x:str(x),list(set(lis))))
        #print IPs_list

        def save_ip_history():
            
            for i in self.lists_of_IPs_and_timestamps: ## All data from ssh_logs.csv!!!!
                item = i[len(i) - 1]  # Because lists_of_IPs_and_timestamps is a list of lists we take the last item because it is the must relevant 
                if item.get_IP() not in IPs_list:
                    with open('IPs_database.csv', 'a') as csvfile:
                        row = item.get_IP() + ',' + str(item.get_timestamp()) + '\n'
                        csvfile.write(row)
                else: # All of this else is just to update the IP with latest timestamp
                    for k in range(0,len(lis)):
                        if item.get_IP() == lis[k].get_IP(): 
                            # if item.get_IP() == '10.0.0.36':
                            #     print item.get_IP()
                            #     print lis[k].get_IP()
                            #     print item.get_timestamp()
                            #     print lis[k].get_timestamp()
                            #     print '-----------------------------------'
                            if item.get_timestamp() > lis[k].get_timestamp():  #if the new ip have an update timestamp
                                f = open('IPs_database.csv', "w+")
                                f.close()
                                with open('IPs_database.csv', 'a') as csvfile:
                                    row = 'IP,timestamp,counter\n' 
                                    csvfile.write(row)         


        save_ip_history()
        

class csv_data_holder():
    def __init__(self,ip,timestamp):
        self.IP = ip
        self.timestamp = timestamp
    def __str__(self):
        return self.IP
    def get_timestamp(self):
        return Decimal(self.timestamp)
    def get_IP(self):
        return self.IP