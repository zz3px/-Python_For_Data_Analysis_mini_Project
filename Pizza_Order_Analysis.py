##
## File: zz3px-homework03-solns.py (STAT 3250)
## Topic: Homework 3 Solutions
## Name: Zhiwei Zhang
##
import numpy as np
import pandas as pd 
from pandas import DataFrame
from scipy import stats
import scipy.stats as st
ff = pd.read_csv('fastfood.csv')
#%%
# Problem 1
# Determine the mean time required to fill an order for all stores. 
# Then calculate a 95% confidence interval for the mean,
mean = np.mean(ff.secs)
n = len(ff.secs)
std = np.std(ff.secs,ddof=1)
t = stats.t.isf(0.025,n-1)
conf = {"lower": mean-t*std/(n**(1/2)),"upper":mean+t*std/(n**(1/2))}
conf
"""
{'lower': 215.45240997615664, 'upper': 217.20180588217139}
"""
#%%
# Problem 2
# What percentage of orders took longer than that (4 mins) to fill?
target = 4*60
sum(ff.secs > target)/n
"""
# Output: percentage of orders took longer than 4 mins to fill
 0.32228182833439695
"""
#%%
# Problem 3
# Find the 5th and 95th percentiles for order fill time.
np.sort(ff.secs)[n*0.05-1]
np.sort(ff.secs)[n*0.95-1]
"""
52       # Output: 5th percentile for order
519      # Output: 95% percentile for order
"""
#%%
# Problem 4
# Determine the mean time for each day of the week.
group = ff['secs'].groupby(ff['dayofweek'])
group.mean()
"""
# Output: mean time for each day of week
dayofweek
Fri     216.234941
Mon     216.774747
Thur    216.605129
Tues    215.742300
Wed     216.282449
"""
#%%
# Problem 5
# Identify all stores with average order fill time 2 standard deviations below the mean average fill time for the 892 stores. 
# Similarly, identify all stores with average order fill time 2 standard deviations above the mean average fill time for the 892 stores.
# For each, sort the store number from smallest to largest.
storemean = ff['secs'].groupby(ff['storenum']).mean()
mean = np.mean(storemean)  # mean of 892 stores average
std = np.std(storemean)

hp = list()
for name, group in ff['secs'].groupby(ff['storenum']):
    if group.mean () <= mean-2*std:
        hp.append(name)
np.sort(hp)

lp = list()
for name, group in ff['secs'].groupby(ff['storenum']):
    if group.mean() >= (mean + 2*std):
        lp.append(name)
np.sort(lp)

"""
# Output: high performance stores
[ 27,  43,  53, 122, 201, 243, 312, 500, 511, 514, 550, 570, 651,
       699, 722, 852, 859]
       
# Output: low performance stores
[ 30,  47,  59, 128, 149, 154, 155, 231, 233, 281, 318, 387, 392,
       402, 422, 452, 474, 528, 614, 621, 657, 718, 723, 725, 726, 887]
"""
#%%
# Problem 6
# Find the 10 “fastest” stores, those with the 10 lowest mean order time. 
# Repeat for the 10 “slowest” stores, those with the 10 highest mean order times. 
# Find 95% confidence intervals for each of these groups. 
# (The confidence intervals should use the data from the original set, not the mean store data.)
storemean = ff['secs'].groupby(ff['storenum']).mean()
data = DataFrame(storemean)
top10 = data.sort_index(by = 'secs')[:10]
group1 = np.array(top10.index)
bottom10 = data.sort_index(by='secs',ascending = False)[:10]
group2 = np.array(bottom10.index)
   
c1 = list()
for i in group1:  
    for j in ff.secs[ff.storenum == i]:
        c1.append(j)   # all secs for 10 fastest stores in original data
  
c2 = list()
for i in group2: 
    for j in ff.secs[ff.storenum == i]:
        c2.append(j)

n1=len(c1)
n2=len(c2)
mean1 = np.mean(c1)
mean2 = np.mean(c2)
std1 = np.std(c1,ddof=1)
std2 = np.std(c2,ddof=1) 
t1 = stats.t.isf(0.025,n1-1)    
t2 = stats.t.isf(0.025,n2-1)

upper1 = mean1+t1*std1/(n1**(1/2)) # upper bound
upper2 = mean2+t2*std2/(n2**(1/2)) 
lower1 = mean1-t1*std1/(n1**(1/2)) # lower bound
lower2 = mean2-t2*std2/(n2**(1/2))
conf = {'upper':[upper1,upper2],'lower':[lower1,lower2]}  
cf = DataFrame(conf)       # to make results dataframe
cf = cf.set_index([['10 fastest','10 slowest']])
cf  

"""
# Output: 10 fastest stores:
[243, 511, 550, 122, 570, 514,  27, 201, 699, 651]

# Output: 10 slowest stores:
[657, 231, 149, 422, 887, 528, 621, 281, 723, 387]

# 95% confidence interval for each group:
                 lower       upper
10 fastest  175.091408  189.498785
10 slowest  243.227632  261.856638
"""
#%%
# Problem 7
# Repeat the previous question for each day of the week, excluding the confidence intervals
# List any stores that appear on more than one “highest” list, and do the same for any stores on more then one “lowest” list.

toplist = list()
bottomlist = list()
for i in pd.unique(ff.dayofweek):
    x = ff[ff.dayofweek== i]
    y = DataFrame(x['secs'].groupby(x['storenum']).mean())
    top = y.sort_index(by='secs')[:10]
    bottom = y.sort_index(by='secs',ascending = False)[:10]
    print('Top 10 stores on', i , np.array(top.index))
    print('Bottom 10 stores on', i , np.array(bottom.index))
    toplist.append(np.array(top.index))
    bottomlist.append(np.array(bottom.index)) 
    

top = np.concatenate((toplist[0],toplist[1],toplist[2],toplist[3],toplist[4]),axis=0)
T = np.sort(top)
TOP = list()
for i in range(0,len(T)-1):
    if T[i] == T[i+1]:
        TOP.append(T[i])
TOP

bottom = np.concatenate((bottomlist[0],bottomlist[1],bottomlist[2],bottomlist[3],bottomlist[4]),axis=0)
B = np.sort(bottom)
BOTTOM = list()
for i in range(0,len(B)-1):
    if B[i] == B[i+1]:
        BOTTOM.append(B[i])
BOTTOM    
"""
# Output:
Top 10 stores on Tues [888 171 312 434 837 202 543 159 800 225]
Bottom 10 stores on Tues [186 152 614 281 102 508 438 446 112  26]

Top 10 stores on Mon [786 805 122 265 819 752 570 743  18   5]
Bottom 10 stores on Mon [505 487 718 725  29 857  48 190  21 507]

Top 10 stores on Thur [ 84 346 551 629 684 586 597 259 355 234]
Bottom 10 stores on Thur [828 644 149 613 700 270 176 128 698 654]

Top 10 stores on Fri [399 466 770  50 658 825 617 454 717 243]
Bottom 10 stores on Fri [ 30 422 452 231 738 541  71 149 174   6]

Top 10 stores on Wed [653 106 134  27 514 301 667 225 182 734]
Bottom 10 stores on Wed [611 363 818 621 359 884 207 657 253  28]

# Outout:

[225] appears on more than one highest list

[149] appears on more than one slowest list

"""

#%%
# Problem 8
# Use the median in place of the mean, and identify the 10 top and bottom 10 stores.
# Identify the stores that are “highest” for both the mean and median, then do the same for “lowest.”
storemedian = ff['secs'].groupby(ff['storenum']).median()
data = DataFrame(storemedian)

top10 = data.sort_index(by = 'secs')[:10]
group3 = np.array(top10.index)
bottom10 = data.sort_index(by='secs',ascending = False)[:10]
group4 = np.array(bottom10.index)

np.intersect1d(group1,group3)  #find intersection
np.intersect1d(group2,group4)
"""
# Output: top ten stores using median
[243, 312,  27, 722, 852, 122, 596, 160, 454, 298]

# Output: bottom ten stores using median
[657, 149, 233, 875,  59, 726, 304, 242, 161, 438]

# Output: fastest for both the mean and median
[27, 122, 243]

# Output: slowest for both the mean and median
[149, 657]
"""
