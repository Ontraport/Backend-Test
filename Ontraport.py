### TAKE ONE DICT AS INPUT, OUTPUT THE OTHER DICT, THEN VICE VERSA FOR PART TWO ###
# {
#     'one':
#     {
#         'two': 3,
#         'four': [ 5,6,7]
#     },
#     'eight':
#     {
#         'nine':
#         {
#             'ten':11
#         }
#     }
# }

# {
#     'one/two':3,
#     'one/four/0':5,
#     'one/four/1':6,
#     'one/four/2':7,
#     'eight/nine/ten':11
# }

### PART ONE - FLATTEN ###
def flatten(c, char_key=''):
    """Take a nested dictionary and return a flattened dictionary"""
    #return dictionary
    ret = {}
    #loop over key, value pairs, the initial key is stored by joining a default char_key & key
    for k,v in c.items():
        key = char_key+k
        #if value is dictionary, recursively update ret using a new char_key seperator until a non-dict value is found     
        if isinstance(v, dict):
            ret.update(flatten(v, key+'/'))
        #values are assigned based on the type, list or int
        elif isinstance(v, list):
            for idx, num in enumerate(v):
                u=({key+'/'+str(idx):num})
                ret.update(u)
        else:
            ret[key] = v
    return ret

container1 = {
                'one':
                {
                    'two':3,
                    'four':[5,6,7]
                },
                'eight':
                {
                    'nine':
                    {
                        'ten':11
                    }
                }
            }
print (flatten(container1))


### PART TWO - EXPAND ###
def expand(c):
    """Take a flattened dictionary and return a nested dictionary"""
    #return dictionary
    ret = {}
    for k, v in c.items():
        cur = ret
        #create list of keys, iterate through all keys except the last bc value assignment is handled later
        keys = k.split('/')
        for idx, key in enumerate(keys[:-1]):
            if key not in cur:
                if keys[idx+1].isnumeric():
                    cur[key]=[]
                else:
                    cur[key]={}  
            #update current location in dict and keep previous copy to use for isinstance(v, list)
            prev=cur
            cur=cur[key]
        #assign values
        if keys[-1].isalpha():
            cur[keys[-1]]=v
        else:
            prev[key].append(v)
    return ret

container2 = {
                'one/two':3,
                'one/four/0':5,
                'one/four/1':6,
                'one/four/2':7,
                'eight/nine/ten':11
            }
print(expand(container2))
