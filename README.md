# Naive-Belief-Entropy-LOVA
## Belief Entropy: A process in which the impression toward a perceived environment by a group of agents begins approaching a mutual equilibrium as those agent interact with each other. 
LOVA is a specialized type of Content-Based Recommender System that uses sets of defined objects within an environment to develop a _favorability policy_ for events that may occur within its environment.

LOVA "naively" follows the rules of Belief Entropy.

## Notable Points:

- The main purpose of LOVA is to provide associative alignment to a unique dataset of stored memories. Each memory is associated with all others under a given weight, based on a custom similarity. 
- When a new memory is added, its favor value is evaluated based on its weighted similarity to all previous memories and their own favor values. 
- When an existing memory's favor value is changed, it also changes the favor values for all the other memories in the dataset. The magnitude that each favor value will change is based on their similarity value with the origin memory, as well as the magnitude of the origin memory's change.
- Habituation is simutalted in LOVA, meaning that the change in a memory's favor value will decrease each time said memory is repeatedly changed.
- An Agent within an environment is meant to attach itself directly to its respective LOVA Model. The agent may use LOVA's policy to decide how to act within its environment, based on how favorable each incoming event is perceived to be.

__The LOVA Model is built to enable Off-Policy Learning in situations where multiple objects are involved in singular independent events. As well as multiple of LOVA Agents in an environment.__ 
**LOVA Agents have the unique ability to interact with other LOVA Agents within their respective environments, and each interaction the other LOVA Agents may affect the policy of each other agent.**

## Attributes:

- fileName (str) (passed in): Name of the data file that the model instance reads from. Will create new file if none is found.
    
- batch_length (int) (passed in): The length of each substring in regards to each data entry.
    
- memoryPool (Array) (internal): The main data set, pulled from the data file or other provided dataset and loaded into memory.
    
- HashMap (Dictionary) (internal): A dictionary used for keeping track of dataset indices.


## Main Methods:

- init(self, fileName, batch_length): Initializes LOVA instance & memory with data file and batch length.
    
- HashMapSetup(self): Internal function used to generate HashMap from dataset entries.
    
- callMemoryFile(self): Internal function used to call a data file with the provided file name.
    
- updateMemoryFile(self): User function used to write the current memory into the data file.
    
- writeToMemoryPool(self,Object,AValue,Environment1): Internal function used to update the current memory.
    
- newMemory(self,memory,instVal): User function for adding to the current memory.
    
- massFuzz(self,array,inputV): Internal function used to get similarity value for all data entries in relation to a new entry being added.
  - Uses custom string similarity metric (BNL).
        
- crossAssociate(self,nInput,objectValue,aValue): Internal function used to give a new data entry its favor value by cross referencing its own properties with the current data entries.
    
- convert(self,nInput,Eintensity): Internal function used to change a specific data entry's favor value to a given extent. Doing so will also instate a Habituative effect onto the data value.
