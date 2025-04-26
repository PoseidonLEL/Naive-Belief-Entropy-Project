import numpy as np, pandas as pd
from os.path import exists
import BNL_Vector
import warnings
from multiprocessing import Pool,cpu_count
warnings.filterwarnings("ignore", message="invalid value encountered in scalar divide")

'''
Limited Object Validator Association - Neighbor Model | Love-A-Neighbor Model
'''


class LOVA:
    
    '''----INITIAL OBJECT DEFINITION & BOOTUP----'''
    
    
    def __init__(self, fileName, batch_length):
        self.fileName = fileName
        self.BL = batch_length
        self.memoryPool = self.callMemoryFile()
        self.HashMap = self.HashMapSetup()
    
    def HashMapSetup(self): #Boots up HashMap
        return {x:i for (i,x) in enumerate(self.memoryPool[0])}
    
    
    
    '''----HIGH LEVEL MEMORY & DATA STRUCTURE MANAGEMENT----'''
    
    
    def callMemoryFile(self): #Reads Memory Pool from Storage and loads contents into RAM
        newDF = pd.DataFrame()
        if(not exists(self.fileName)):
            newDF['Object'] = [" "]
            newDF['AValue'] = [0.0]
            newDF['Environment1'] = [1.0]
            newDF.to_csv(fr'{self.fileName}', index=False)
        newDF = pd.read_csv(f"{self.fileName}")
        return [newDF['Object'].to_numpy(),
                newDF['AValue'].to_numpy(dtype=np.float32),
                newDF['Environment1'].to_numpy(dtype=np.float32)]
    
    
    #MAIN DISK BANDWIDTH BOTTLENECK
    #Rewrites Memory Pool in Storage with the current version of the Memory Pool in RAM
    def updateMemoryFile(self):
        pd.DataFrame({'Object': self.memoryPool[0], 
                      'AValue': self.memoryPool[1],
                      'Environment1':self.memoryPool[2]}).to_csv(fr'{self.fileName}', mode='w', index=False)
    
    
    #MAIN MEMORY BANDWIDTH BOTTLENECK
    def writeToMemoryPool(self,Object,AValue,Environment1):#Rewrites Memory Pool in RAM 
        (self.memoryPool[0],
         self.memoryPool[1],
         self.memoryPool[2]) = (np.array(Object),
                                np.array(AValue),
                                np.array(Environment1))
    def writeToMemoryPoolAPPEND(self,Object,AValue,Environment1): 
        (self.memoryPool[0],
         self.memoryPool[1],
         self.memoryPool[2]) = (np.append(self.memoryPool[0],Object),
                                np.append(self.memoryPool[1],AValue),
                                np.append(self.memoryPool[2],Environment1))
        
        
        
    #Adds new Memory Entry to Memory Dataframe, then writes it to Memory Pool
    #instVal serves as an external value passed by External Data Functions
    # Function is messy because I had to do a patch on Data Structure Logic Handling.
    def newMemory(self,memory,instVal=None):
        if(memory not in self.HashMap):

            c = instVal!=None
            if(len(self.HashMap)==1):
                self.writeToMemoryPoolAPPEND(memory,np.float32(instVal if c else 0),np.float32(1))
            else:
                evaluation = self.crossAssociate(memory,self.memoryPool[0],self.memoryPool[1])
                self.writeToMemoryPoolAPPEND( memory, np.mean((instVal, evaluation),dtype=np.float32) if c else np.float32(evaluation), np.float32(1) )
            del c
            self.HashMap[memory]=len(self.HashMap)

        else: 
            self.convert(memory,instVal)
            
    
    
    
    
    
    '''----LOW LEVEL MODEL ABSTRACTION----'''
    
    

    #Gets distance value for all Data Strings in relation to the Input String
    def massFuzz(self,array,inputV):
        return BNL_Vector.massBNL(inputV,array,self.BL)

    
    #When a new Data Entry is added, it will gain its favorability value by cross referencing
    #   its own properties with the current data entries.
    def crossAssociate(self,nInput,objectValue,aValue):
        compareVect = self.massFuzz(objectValue,nInput)**2
        evaluation = np.sum(compareVect*aValue)/np.sum(compareVect) # Weighted Average Calculation
        return evaluation if not np.isnan(evaluation) else np.float32(0.0) #Handling divide-by-zero issues
    
    
    #Once an existing Data Entry is changed, it affects all other data entries
    #   based on how relevant each entry is to the entry that was originally changed.
    #Will also change Habituation factors of all other Data Entries in a similar way.
    def updateOps(self,groundZero,simList,envList,diff):
        compareVect = self.massFuzz(self.memoryPool[0],groundZero)**2
        simVector = simList + ((diff/envList)*compareVect) # Habituative Distance Calculation
        envVector = np.add(envList,compareVect)
        return (simVector,envVector)
    

    
    #Will change a specific Data Entries Favorability Value to a given extent. 
    #  Doing so will also instate a Habituative effect onto the data value.
    def convert(self,nInput,Eintensity):
        tempPlace = self.HashMap[nInput]
        reeval = np.mean((Eintensity,self.memoryPool[1][tempPlace]),dtype=np.float32) if Eintensity!=None else self.memoryPool[1][tempPlace] #Favor Reevaluation 
        stimulusChange = reeval - self.memoryPool[1][tempPlace]  #Stimulus Change
        (param1,param2) = self.updateOps(nInput,self.memoryPool[1],self.memoryPool[2],stimulusChange)
        self.writeToMemoryPool(self.memoryPool[0],param1,param2)
        
        
        
        
        
    '''----EXTENSIONS TO USER-END FUNCTIONALITY----'''

    #Get memorypool as a pandas Dataframe.
    def toDataframe(self):
        return pd.DataFrame(data={'Experience':self.memoryPool[0].copy(),
                              'Favor Value':self.memoryPool[1].copy(),
                              'Habit Value':self.memoryPool[2].copy()})

    #Checks if a given Experience String exists within the current dataset.
    def existingMemory(self, entry):
        return 1 if entry in self.HashMap else 0
    
    #Replaces current dataset in Memory with an input dataset provided by user.
    def fit_dataset(self,matrix=None):
        if (matrix!=None):
            self.writeToMemoryPool(np.object_(matrix[0]),np.float32(matrix[1]),np.float32(matrix[2]))
            self.HashMap = self.HashMapSetup()

    #Returns entire memory pool or a specific column
    def getBrain(self, column=None):
        return self.memoryPool if column==None else self.memoryPool[column]
    
    #Returns long term neutrality value
    def getMentalState(self):
        return np.sum(self.memoryPool[1]*self.memoryPool[2])/np.sum(self.memoryPool[2])
    
    
    #Returns a sorted list of the top best or worst memories. Will give as many as requested.
    def favoritism(self,side=1,amount=3):
        return (pd.DataFrame({'A0': self.memoryPool[0],
                              'A1': self.memoryPool[1]})).sort_values(by='A1',
                                ascending=False if side==1 else True).head(amount if amount>=0 else len(self.HashMap)).to_numpy()    
    
    #Obtain the favorability value for a hypothetical Experience String
    def getFavorValue(self, memString):
        return (self.memoryPool[1][self.HashMap[memString]],1) if memString in self.HashMap else (self.crossAssociate(memString,
                                                                                                  self.memoryPool[0],
                                                                                                  self.memoryPool[1]),0)
    
    #Obtain the habit value for a hypothetical Experience String
    def getHabitValue(self, memString):
        return self.memoryPool[2][self.HashMap[memString]] if memString in self.HashMap else np.float32(0)


    #Give the algorithm a segment of a memory string (or a full memory string) and 
    #   it will return all memories that are relevant to the segment/string
    def remindOf(self,memSeg,side=1,amount=1):
        return (pd.DataFrame({'A0':self.memoryPool[0],
                              'A1':self.massFuzz(self.memoryPool[0],memSeg),
                              'A2':self.memoryPool[1]})).sort_values(by='A1',
                                ascending=False if side==1 else True).head(amount if amount>=0 else len(self.HashMap)).to_numpy()


    #Pass a set of entries into the function and it will return a sorted list of recommendations based on the current policy.
    def get_recommendation(self,array,amount=0):
        if(cpu_count()<8):
            return f"COMMAND REJECTED: CPU requires at least 8 available threads. Your CPU only has {cpu_count()} threads lmao."
            
        comp = len(self.HashMap)*len(array) #Approximating the number of processes that CPU will run based on dataset size & input array size
        if(comp>150000):
            with Pool(4 if comp<360000 else 8) as p:
                weights = [x[0] for x in (p.map(self.getFavorValue,array))]
        else:
            weights = [self.getFavorValue(i)[0] for i in array]
        return (pd.DataFrame({'Object': array,
                              'Favor Value': weights })).sort_values(by='Favor Value', ascending=False).head(amount if amount>0 else len(array)).to_numpy()
