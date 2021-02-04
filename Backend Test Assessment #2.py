# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:39:11 2021

@author: Haniel Chang
"""

# =============================================================================
# Global variables. array holds the addresses with values as strings. numlist 
# is used when a list is need to create an array. Container will hold the 
# result of revesrsing the process back to a multi-dimensinoal container
import collections
array = []
numlist = []
container = {}
prevAddr = []

       

# =============================================================================
# This function converts the multi-dim container to 1D list. It  
def convertToList(key, val):          
    
    if isinstance(val, dict):    
        for i in val:
            base = "'" + key
            inner_key = i
            inner_val = val[i]
            
            if isinstance(inner_val, int):
                createIntAddress(base, inner_key, inner_val)
            else:
                if isinstance(inner_val, list): 
                      createListAddress(base, inner_key, inner_val)           
                else:
                    if isinstance(inner_val, dict):
                        createNestedAddress(base, inner_key, inner_val)                    
    else:
         return 
  
# =============================================================================
# This function creates an address if an integer is found        
def createIntAddress(b, ik, iv):
    path = b + '/' + ik + "':"
    value = str(iv)
    s = path + value
    array.append(s) 

# =============================================================================
# This function creates an address if a list of integers is found    
def createListAddress(b, ik, iv):
    addr = 0
    for k in iv:
        index = str(addr)
        path = b + '/' + ik + '/' + index + "':"
        value = str(k)
        s =  path + value
        array.append(s)
        addr += 1
# =============================================================================
# This function creates an address if a nested dictionary is found
def createNestedAddress(b, ik, iv):        
        s = b + '/' + ik
        while isinstance(iv, dict):
            nextKey = iv.keys()
            nextVal = iv.values()
            ik = next(iter(nextKey))
            iv = next(iter(nextVal))
            if isinstance(ik, str):
                s = s + '/' + ik
            if isinstance(iv, int):
                s = s + "'" + ':' + str(iv)
            elif isinstance(iv, list):
                addr = 0
                for i in iv:
                    index = str(addr)
                    t = s + '/' + index + "'" + ":" + str(i)
                    array.append(t)
                    addr += 1
                return
        array.append(s)    
# =============================================================================
# This function reverses the action of function convertToList.
# The 'j' for loop removes 
# apostrophes from paths to facilitate conversion. The 'k' for loop 
# determines if there is a digit within a path to confirm if a list will be
# needed to store integer values (namely 5,6, and 7 in this example). 
# key_val is the list containing path and value. CurAddr holds
# the components of the path separated into strings.
def convertToDict(string):
        global prevAddr
        global numlist
        key_val = string.split(':')
        CurAddr  = key_val[0].split('/')
        value = key_val[1]
        if value.isdigit():
            value = int(value)
        size = len(CurAddr)
        
        
        for j in range(size):
            CurAddr[j] = CurAddr[j].replace("'","")
        
        for k in CurAddr:
            if k.isdigit():
                if len(prevAddr) == 0:
                    numlist.append(value)
                CurAddr.remove(k)
                size -= 1 
        
        items_prevAddr = collections.Counter(prevAddr)
        items_curAddr = collections.Counter(CurAddr)        
        if len(prevAddr) != 0 and len(CurAddr) != 0:
            if items_prevAddr != items_curAddr:
                numlist = []
                numlist.append(value)
            else:
              numlist.append(value)
        
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
#                numlist = []
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
     newDict = {}
     ind = 0
     K1 = address[ind]
     ind += 1
     K2 = address[ind]
     newDict.setdefault(K1, {})[K2] = val
     if (ind != size - 1 ):
         start = {address[size - 1]:val}
         newDict = start
         for i in range(size - 2 , -1, -1):             
             newDict = {address[i]:newDict}
     container.update(newDict)
     return
# =============================================================================
# Main body code where the function calls are made. I have chosen to hard code
# the example container given in the assessment problem.
    
D = {'one':{'two': 3,'four': [5,6,7]}, 'eight':{'nine':{'ten':11}}}
print('The value of the container is: ')
print(D)

for i in D:        
    convertToList(i ,D[i])
                
print()
print('When container is converted to 1D array, we get:')        
for i in array:
    print(i)

print()
for i in array:
    convertToDict(i)
print('When we take the 1D array and reverse the process, we get:')
print(str(container))
            
            

