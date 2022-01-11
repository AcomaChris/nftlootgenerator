# Loot object generator.
# Returns a loot object string for use on card.

import time
import sympy
import random
import uuid

#############################
# Declare required variables.
#############################

debug_recordtime = False # Switch to True to record and print loot generation time out.

test_prime = 6242950767904892547110745313203633592441 # For large digitl prime number testing.
test_contract_id = "0x06012c8cf97bead5deae237070f9587f8e7a266d"

if(debug_recordtime) : t0 = time.time()

###########################################################
# Utility functions to help define loot rarity and effects.
###########################################################

def IsPrimeNumber(token_id):
    return sympy.isprime(token_id)

def CreateUniqueID(contract_id, token_id):
    print(f"Contract ID: {hex(int(contract_id[2:], 16))} + Token ID: {token_id}")
    seed_number = hex(int(contract_id[2:], 16) + token_id)
    print(f"Seed Number: {seed_number}")
    pass

def GetRarity(token_id):
    pass

def GiveLootObject(colour, rarity):
    return 'I am a loot object'

CreateUniqueID(test_contract_id, 1024)

# Print out the total time at the end of the operation.
if(debug_recordtime): 
    t1 = time.time()
    totaltime = t1 - t0
    print(f"Time to process =  + {totaltime}")