# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:39:11 2021

@author: Haniel Chang
"""

# =============================================================================
# Global variables. array holds the addresses with values as strings. numlist 
# is used when a list is need to create an array. Container will hold the 
# result of revesrsing the process back to a multi-dimensinoal container
array = []
numlist = []
container = {}
prevAddr = []

       

# =============================================================================
# This function converts the multi-dim container to 1D list. It  
def createList(key, val):          
    
    if (isinstance(val, dict)):    
        for i in val:
            base = "'" + key
            inner_key = i
            inner_val = val[i]
            
            if (isinstance(inner_val, int)):
                s = base + '/' + inner_key + "':" + str(inner_val)
                array.append(s)                
            else:
                if (isinstance(inner_val, list)): 
                    addr = 0
                    for k in inner_val:
                        s = base + '/' + inner_key + '/' + str(addr) + "':" + str(k)
                        array.append(s)
                        addr += 1
                else:
                    if (isinstance(inner_val, dict)):
                        s = base + '/' + inner_key
                        k = inner_val.keys()
                        v = inner_val.values()
                        inner_key2 = next(iter(k))
                        inner_val2 = next(iter(v))
                        s1, s2 = createList(inner_key2, inner_val2)
                        s = s + '/' + s1 + "'" + ':' + str(s2)
                        array.append(s)
              
    else:
         return key, val
     
# =============================================================================
# This function reverses the action of function createList.
# The 'j' for loop removes 
# apostrophes from paths to facilitate conversion. The 'k' for loop 
# determines if there is a digit within a path to confirm if a list will be
# needed to store integer values (namely 5,6, and 7 in this example). 
# key_val is the list containing path and value. CurAddr holds
# the components of the path separated into strings.
def createDict(string):
        global prevAddr
        global numlist
        key_val = string.split(':')
        CurAddr  = key_val[0].split('/')
        value = int(key_val[1])
        size = len(CurAddr)
        
        
        for j in range(size):
            CurAddr[j] = CurAddr[j].replace("'","")
        
        for k in CurAddr:
            if k.isdigit():
                numlist.append(value)
                CurAddr.remove(k)
                size -= 1            
        
        if (not container):
            createNewKey(CurAddr, size, value)
        else:
            if (prevAddr[0] == CurAddr[0]):
                maxIndex = min(len(prevAddr), len(CurAddr))
                for i in range(maxIndex): 
                    if prevAddr[i] != CurAddr[i]:
                        newKey = CurAddr[i]
                        prevKey = CurAddr[i - 1]
                        container[prevKey].update({newKey:value})
            else:
                createNewKey(CurAddr, size, value)
                numlist = []
        if (prevAddr == CurAddr):
            i1 = prevAddr[0]
            i2 = prevAddr[1]
            container[i1][i2] = numlist
        prevAddr = CurAddr
        return
# ============================================================================= 
# This function will create a new key when needed. It creates a dict within
# a dict using the first 2 elements received by the call. It modifies global
# variable container as needed.
def createNewKey(address, size, val):       
     ind = 0
     K1 = address[ind]
     ind += 1
     K2 = address[ind]
     container.setdefault(K1, {})[K2] = val
     if (ind + 1 != size ):
         for i in range(ind + 1, size, 1):
             container[K1][K2] = {address[i]:val}
     return
# =============================================================================
# Main body code where the function calls are made. I have chosen to hard code
# the example container given in the assessment problem.
    
D = {'one':{'two': 3,'four': [5,6,7]}, 'eight':{'nine':{'ten':11}}}
print('The value of the container is: ')
print(D)

for i in D:        
    createList(i ,D[i])
                
print()
print('When container is converted to 1D array, we get:')        
for i in array:
    print(i)

print()
for i in array:
    createDict(i)
print('When we take the 1D array and reverse the process, we get:')
print(str(container))
            
            

