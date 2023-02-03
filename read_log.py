import pandas as pd 
import time

class ReadLogSTARCCM:
    
    def __init__(self):
        print("RUNNING HERE")
        time.sleep(5)
        self.dict_complete = {}
        print("RUNNING HERE 2")
        time.sleep(5)
        self.dict_time = {}
        self.time = []
        self.time_final = []

    def open_file(self, filename):
        self.filename = filename
        self.file = open(filename + ".log")
    
    def removes_trailing_spaces(self, f):
        for line in f:
            line = line.lstrip()
            if line:
                print(line)

    def detect_variables(self):
        for line in self.file:

            line = line.lstrip()
            if line:
                delimiter = ")"
                line_parentheses_split = [e+delimiter for e in line.split(delimiter) if e]
                line_spaces_split = line_parentheses_split[0].split(" ")
                line_parentheses_split.pop(0)
                line_total = line_spaces_split+ line_parentheses_split
                line_final_split = list(filter(("").__ne__, line_total))
                if (len(line_final_split) > 0):
                    line_final_split.pop(len(line_final_split) - 1)

                for i in range(0, len(line_final_split)):
                    counter = 0
                    passed = 0
                    corrected = 0
                    for j in line_final_split[i]:
                        if j == "(":
                            passed = 1
                        if passed == 1:
                            counter += 1
                        if j == ")":
                            if len(line_final_split[i]) == counter:
                                line_final_split[i-1] = line_final_split[i-1] + line_final_split[i]
                                line_final_split.pop(i)
                                corrected = 1
                    if corrected == 1:
                        break

                if bool(self.dict_complete) == False:
                    if all(x in line_final_split for x in ['Iteration', 'Continuity', 'X-momentum']):
                        for i in range(0, len(line_final_split)):
                            self.dict_complete[line_final_split[i]] = []

                self.delete_log_that_is_not_data(line_final_split)

                    
    def delete_log_that_is_not_data(self, line):
        if_pass = 0

        try:
            line = [ float(x) for x in line ]
        except:
            if_pass = 1

        if if_pass == 0:
            if (len(line) == len(self.dict_complete)):
                counter = 0
                for key in self.dict_complete.keys():
                    self.dict_complete[key].append(line[counter])
                    counter = counter + 1
        else:
            pass

    def detect_time(self):
        for line in self.file:
            print(line)
            line = line.lstrip()
            print(line)
            if line:
                line_spaces_split = line.split(" ")
                line_final_split = list(filter(("").__ne__, line_spaces_split))

                if(line_final_split[0] == 'TimeStep'):
                    self.time.append(line_final_split[3])
            
        for x in self.time:
            self.time_final.append(x.replace("\n", "").replace(".",","))
        
        self.dict_time["Time"] = self.time_final
        

    def to_xlsx(self):
        self.dict_time.update(self.dict_complete)
        df_complete = pd.DataFrame.from_dict(self.dict_time)
        df_complete.index += 1 
        df_complete.to_excel(self.filename + ".xlsx")

read = ReadLogSTARCCM()

# read_filename = input("Digite o nome do arquivo de log do STAR-CCM+ com a extensão .log: ")

read.open_file("WEGDOE31")
read.detect_time()
read.open_file("WEGDOE31")
read.detect_variables()

read.to_xlsx()
