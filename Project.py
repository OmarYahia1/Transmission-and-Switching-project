
import numpy as np
import pandas as pd

#user inputs
cityArea = 1000
popDensity = 100
avgCalls = 5/(60*24)
avgCallDuration = 2
availableChannels = 200
maxChannels = 100
CI = 6.5
pblock = "2%"
slotsperChannel = 8
slotsperSub = 2

users = cityArea * popDensity #total number of users in a city
aUser = avgCalls * avgCallDuration #erlang for a user

reuseFactor = [3,4,7,9,12,13,16,19,21]
n10 = [1,1,1,1,1,1,1,1,1]
n120 = [3,2,2,2,2,2,2,2,2]
n180 = [4,3,3,3,3,3,3,3,3]
n360 = [6,6,6,6,6,6,6,6,6]


x = 0
# 3N/n > C/I
for i in reuseFactor :
    
    a = (3*i)/n10[x]
    b = (3*i)/n120[x]
    c =(3*i)/n180[x]
    d = (3*i)/n360[x]
    x = x + 1
    if ( a > CI ):
        N10 = i
    if ( b > CI):
        N120 = i
    if ( c > CI):
        N180 = i
    if ( d > CI):
        N = i

trunks10 = np.floor((availableChannels/N10)*(slotsperChannel/slotsperSub))
sector10 = np.floor(trunks10/36)
trunks120 = np.floor((availableChannels/N120)*(slotsperChannel/slotsperSub))
sector120 = np.floor(trunks120/3)
trunks180 = np.floor((availableChannels/N180)*(slotsperChannel/slotsperSub))
sector180 = np.floor(trunks180/2)
trunks = np.floor((availableChannels/N)*(slotsperChannel/slotsperSub))
#sector10 = trunks10/36

erlangTable = pd.read_csv("Erlang.csv")

asector120 = float(erlangTable[pblock][sector120])
asector10 = float(erlangTable[pblock][sector10])
asector180 = float(erlangTable[pblock][sector180])
acell360 = float(erlangTable[pblock][trunks])

subsperCell10 = np.floor((36*asector10)/aUser)
subsperCell120 =np.floor((3*asector120)/aUser)
subsperCell180 = np.floor((2*asector180)/aUser)
subsperCell360 = np.floor(acell360/aUser)

cells10 = np.ceil(users/subsperCell10)
cells120 = np.ceil(users/subsperCell120)
cells180 = np.ceil(users/subsperCell180)
cells360 = np.ceil(users/subsperCell360)

maximum = []
maximum.append(cells10)
maximum.append(cells120)
maximum.append(cells180)
maximum.append(cells360)
maxCells = np.max(maximum)
print("Number of cells using 10 degree sectoring "+str(cells10))
print("Number of cells using 120 degree sectoring "+str(cells120))
print("Number of cells using 180 degree sectoring "+str(cells180))
print("Number of cells using 360 degree sectoring "+str(cells360))
print("Maximum number of cells "+str(maxCells))