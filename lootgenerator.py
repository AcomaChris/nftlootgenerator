# Loot object generator.
# Returns a loot object string for use on card.

import time
import sympy

#############################
# Declare required variables.
#############################

debug_recordtime = False # Switch to True to record and print loot generation time out.

test_prime = 6242950767904892547110745313203633592441 # For large digitl prime number testing.

if(debug_recordtime) : t0 = time.time()

###########################################################
# Utility functions to help define loot rarity and effects.
###########################################################

def IsPrimeNumber(token_id):
 return sympy.isprime(token_id)

def CreateUniqueID(token_id):
    pass

def GetRarity(token_id):
    pass

def GiveLootObject(colour, rarity):
    return 'I am a loot object'

# Print out the total time at the end of the operation.
if(debug_recordtime): 
    t1 = time.time()
    totaltime = t1 - t0
    print(f"Time to process =  + {totaltime}")