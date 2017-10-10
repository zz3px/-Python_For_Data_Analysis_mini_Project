##
## File: zz3px-homework04-solns.py (STAT 3250)
## Topic: Homework 6 Solutions
## Name: Zhiwei Zhang
##
import pandas as pd
import numpy as np
from pandas import DataFrame

# 1. What proportion of requests were successful? (The requester received pizza.)
received = list()
pizza = open("pizza_requests.txt",'r')
for line in pizza:
    if 'requester_received_pizza' in line:
        received.append((line.split(',')[1]).split(" ")[1])

received.count('true')/len(received)*100
print("24.634103332745546% ofthe requestes were successful")

#%%
# 2. What is the mean number of subReddits subscribed to, and how many distinct subReddits are there among all the requests?  
pizza = open("pizza_requests.txt",'r')
flag = 0
result = list()
temp = list()        
for line in pizza:
	line = line.split("\n")[0]
	if "requester_subreddits_at_request" in line:
		if "}" in line:
			flag = 0
			result.append(temp)
			temp = []
			continue
		else:
			flag = 1 #after this line, we need to add the strings into our temp list
			continue
	if flag == 1:
		if '}' in line:
			flag = 0
			result.append(temp)
			temp=[]
		else:
			temp.append(line.split("\"")[1])
number = list()
for i in result:
    number.append(len(i))
ave = np.mean(number)
print("The mean number of subReddits subscribed to is:", ave)

pizza = open("pizza_requests.txt",'r')
unique = list()
count = 0
for line in pizza:
    if line[0] ==' ' and '}' not in line:
        if line not in unique:
            unique.append(line)
            count+=1
len(unique)
print("9915 distinct subReddits are there among all the requests")

#%%
# 3. Find the median account age at the time of request for all requests
age = list()
pizza = open("pizza_requests.txt",'r')
for line in pizza:
    if'requester_account_age_in_days_at_request' in line:
        age.append((line.split(',')[1]).split(" ")[1])
age = [float(i) for i in age]
median = np.median(age)
print('the median account age at the time of request for all requests is:',155.64759259259259)


#%%
# 4. Divide the requests into those with account age greater than the median found in the previous question, 
# and those with account age less than the median. Find a 95% confidence interval for the difference in
# proportion of successful pizza requests between the two groups. (Either order for the proportions is fine.)
data = {'success':received,'age':age}
combine = DataFrame(data,columns=['success','age'])
gr = combine.success[combine.age>median]
le = combine.success[combine.age<median]
pg = sum(gr=='true')/len(gr) #proportion of greater than median, success
pl = sum(le=='true')/len(le)

se = ((pg*(1-pg))/len(gr) + (pl*(1-pl))/len(le))**0.5
lower = (pg-pl)-1.96*se
upper = (pg-pl)+1.96*se
# Confidence interval
cf = [lower,upper]
print("The 95% confidence interval for the difference in proportion of successful pizza requests between the two groups is:",cf )


#%%
## 5. How many users made more than one pizza request? If one or more, then what was the maximum number of requests from a user?
user = list()
pizza = open("pizza_requests.txt",'r')
for line in pizza:
    if'requester_username' in line:
        user.append((line.split(',')[1]).split(" ")[1])

[x for x in user if user.count(x)>=2]
print("No user made more than one pizza request")      
        
        
#%%         
# 6. Find the mean number of requester upvotes at retrieval.
upvotes1 = list()
pizza = open("pizza_requests.txt",'r')
for line in pizza:
    if'requester_upvotes_minus_downvotes_at_retrieval' in line:
        upvotes1.append((line.split(',')[1]).split(" ")[1])
upvotes1 = [int(i) for i in upvotes1]

pizza = open("pizza_requests.txt",'r')
upvotes2 = list()
for line in pizza:
    if'requester_upvotes_plus_downvotes_at_retrieval' in line:
        upvotes2.append((line.split(',')[1]).split(" ")[1])
upvotes2 = [int(i) for i in upvotes2]

upvotes = list()
for i in range(len(upvotes1)):
    upvotes.append((upvotes1[i]+upvotes2[i])/2)
    
mean = np.mean(upvotes)
print("The mean number of requester upvotes at retrieval is:", mean)

#%%
# 7. Determine the percentage of request texts that mentioned the word “student”.
text=list()
pizza = open("pizza_requests.txt",'r')
for line in pizza:
    if"request_text" in line:
        text.append((line.split(',',1)[1]))
text = DataFrame(text,columns=['t'])

l = list(range(len(text)))[::2]
ct = 0
for i in l:
    if text.t[i].count('student')>0:
        ct = ct + 1
p = ct/(len(text)/2)
print("The percentage of request texts that mentioned the word student is:",p)


#%%
f = open('homework6-output-Zhang-Zhiwei.txt','w')
print("Homework 6 Output (Zhiwei Zhang):",file=f)
print(" ",file = f)
print("Problem 1:",file = f)
print("24.634103332745546% ofthe requestes were successful",file = f)

print(" ",file = f)
print("Problem 2:",file = f)
print("The mean number of subReddits subscribed to is: 17.9698465879",file = f)
print("9915 distinct subReddits are among all the requests", file =f)


print(" ",file = f)
print("Problem 3:",file = f)
print('the median account age at the time of request for all requests is: 155.64759259259259', file = f)


print(" ",file = f)
print("Problem 4:",file = f)
print("The 95% confidence interval for the difference in proportion of successful pizza requests between the two groups is:[0.022047288214369135, 0.066841600674519774]", file = f)



print(" ",file = f)
print("Problem 5:",file = f)
print("No user made more than one pizza request",file = f )  


print(" ",file = f)
print("Problem 6:",file = f)
print("The mean number of requester upvotes at retrieval is: 5171.3452653852937", file = f)


print(" ",file = f)
print("Problem 7:",file = f)
print("The percentage of request texts that mentioned the word student is:7.617704108622818%",file = f)
f.close()







