from time import perf_counter
        
        
    def exportCalibrations(stepsNum): # function used to perform calculations
        for stepsNum in range (1, 661, 10):

            f = open("Graphs/Graphs" + str(stepsNum) + ".csv", "w")
        
            xs = []
            ys = []
            
            writer = csv.writer(f)
            
            count = 1
            while(count < 10):
                start = perf_counter()
                self.stepper.step(stepsNum, count)
                y = perf_counter() - start
                print("Speed: ", count, "Steps: ", stepsNum, " Time: ", y)
                self.stepper.resetPosition()
                xs.append(count)
                ys.append(y)
                buf = [str(count), str(y)]
                writer.writerow(buf)
                count += 0.5
            
            f.close()
            
            
            
            
    def parseCalibrations(stepsNum): # Code for creating speed plot from previously created data
        target = 0.25
        tol = 0.03
        print("For speeds at:", target , "with a tolerance of:", tol)   
        for stepsNum in range (341, 661, 10):
            with open("Graphs/Graphs" + str(stepsNum) + ".csv", newline = '') as csvfile:
                read = csv.reader(csvfile, delimiter = ',')
                x = []
                y = []
                for row in read:                    
                    if (abs(float(row[1]) - target) < tol):
                        x.append(float(row[0]))
                        y.append(float(row[1]))
                
                index = 0
                minVal = 5
                
                yDiffs = []
                if (len(y) > 0):
                    for i in range(len(y)):
                        yDiffs.append(abs(y[i] - target))
                        if (yDiffs[i] < minVal):
                            minVal = yDiffs[i]
                            index = i
                    
#                     print("Steps: " + str(stepsNum) + ", Speed:", int(x[index]))
                    print(str(stepsNum) + ", " + str(float(x[index])))
                else:
                    print(str(stepsNum) + ", x") 
                    print("Steps: " + str(stepsNum) + ", Speed:", 0)