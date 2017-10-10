##
## File: zz3px-homework04-solns.py (STAT 3250)
## Topic: Homework 4 Solutions
## Name: Zhiwei Zhang
##
import pandas as pd 
import numpy as np
from pandas import DataFrame
from scipy import stats
import scipy.stats as st
zipcode = pd.read_csv('zipcodes.txt',  converters={'Zipcode':str})
genres = pd.read_csv('genres.txt',sep='|',names=['movieid','movietitle','releasedate','videoreleasedate','IMDbURL','unknown',
'Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery',
'Romance','Sci-Fi','Thriller','War','Western'])
reviews = pd.read_csv('reviews.txt', sep='\t',header= None, names = ['reviewerid','movieid','rating','timestamp'])
reviewers = pd.read_csv('reviewers.txt',sep='|',header=None,names=['reviewerid','age','gender','occupation','zipcode'],converters={'zipcode':str})

f = open('homework4-output-Zhang-Zhiwei.txt','w')
print("Homework 4 Output (Zhiwei Zhang):",file=f)
#%%
print("Problem 1:",file=f)
## 1. Which percentage of each rating was given?
rating = reviews['reviewerid'].groupby(reviews['rating'])
rate = np.array(rating.count())
for i in (range(0,5)):   
    print(100* rate[i]/sum(rate),"% was given by rating" , i+1, file = f)  # sumrate=100000

"""
6.11 % was given by rating 1
11.37 % was given by rating 2
27.145 % was given by rating 3
34.174 % was given by rating 4
21.201 % was given by rating 5
"""
#%%
print(" ",file = f)
print("Problem 2:",file=f)
## 2. Which reviewers were the top-10 in terms of number of movies reviewed? (Provide the reviewer number
## and the number of movies reviewed. If there is a tie for 10th place, include all that tied.)
group = reviews['movieid'].groupby(reviews['reviewerid'])
number = DataFrame(group.count())  #943 reviewers
a = number.sort_index(by = 'movieid',ascending=False)[:10]
print("Top-10 reviewers in terms of number of movies reviewed",file=f)
print(a,file=f)
"""
# output: top-10 reviewers in terms of number of movies reviewed
 
     number of movies reviewed

reviewerid         
405             737
655             685
13              636
450             540
276             518
416             493
537             490
303             484
234             480
393             448
"""
#%%
print(" ",file = f)
print("Problem 3:",file=f)
## 3. Find a 95% confidence interval for the average rating among all reviewers, and a 95% confidence
## interval for the average rating among the top-10 reviewers. Does there appear to be evidence that the
## two groups differs?
topgroup = np.array(a.index)
top10rating = list()
for i in topgroup:  
    for j in reviews.rating[reviews.reviewerid == i]:
        top10rating.append(j)  
top10rating

n1 = len(reviews)
mean1 = np.mean(reviews.rating)
std1 = np.std(reviews.rating,ddof=1)
t1 = stats.t.isf(0.025,n1-1)

n2 = len(top10rating)  #5521
mean2 = np.mean(top10rating)
std2 = np.std(top10rating,ddof=1)   
t2 = stats.t.isf(0.025,n2-1)

upper1 = mean1+t1*std1/(n1**(1/2)) # upper bound
upper2 = mean2+t2*std2/(n2**(1/2)) 
lower1 = mean1-t1*std1/(n1**(1/2)) # lower bound
lower2 = mean2-t2*std2/(n2**(1/2))
conf = {'upper':[upper1,upper2],'lower':[lower1,lower2]}  
cf = DataFrame(conf)       # to make results dataframe
cf = cf.set_index([['all reviewers','top-10 reviewers']])
print("95% confidence interval for the average rating among all reviewers and among the top-10 reviewers",file=f)
print(cf,file = f)
print("Based on the 95% confidence intervals, the two groups do differ in the average rating.",'\n',"Two intervals are not overlapping at all and the interval of the average rating among",'\n',"all reviewers is above the interval of the average rating among the top-10 reviewers.",file=f)

"""
# Output: 95% confidence interval for two groups
                     lower     upper
all reviewers     3.522883  3.536837
top-10 reviewers  3.073829  3.138837

Based on the 95% confidence intervals, the two groups do differ in the average rating. 
Two intervals are not overlappying at all and the interval of the average rating among all reviewers is above the interval
of the average rating among the top-10 reviewers.
"""
#%%
print(" ",file = f)
print("Problem 4:",file=f)
## 4. Which movies were the top-10 based on of number of times reviewed? (Provide the movie title and
## the number of times reviewed. If there is a tie for 10th place, include all that tied.)

group = reviews['reviewerid'].groupby(reviews['movieid'])
number = DataFrame(group.count())  #1682
a = number.sort_index(by = 'reviewerid',ascending=False)[:10]
movieid = np.array(a.index)
print(" top-10 movies based on of number of times reviewed",file=f)
for i in movieid:
        print("Number of times reviewed:",a.reviewerid[i]," /  Movie Title: ",genres.movietitle[i-1],file = f)

"""
top-10 movies based on number of times reviewed
Number of times reviewed: 583  /  Movie Title:  Star Wars (1977)
Number of times reviewed: 509  /  Movie Title:  Contact (1997)
Number of times reviewed: 508  /  Movie Title:  Fargo (1996)
Number of times reviewed: 507  /  Movie Title:  Return of the Jedi (1983)
Number of times reviewed: 485  /  Movie Title:  Liar Liar (1997)
Number of times reviewed: 481  /  Movie Title:  English Patient, The (1996)
Number of times reviewed: 478  /  Movie Title:  Scream (1996)
Number of times reviewed: 452  /  Movie Title:  Toy Story (1995)
Number of times reviewed: 431  /  Movie Title:  Air Force One (1997)
Number of times reviewed: 429  /  Movie Title:  Independence Day (ID4) (1996)
"""

#%%
print(" ",file = f)
print("Problem 5:",file=f)
#5. Which genre occurred most often, based on the number of reviews. Which was least often?
group = reviews['reviewerid'].groupby(reviews['movieid'])
number = list((group.count())) # how many times being reviewed for each movie
subset = genres.ix[:,6:]  # all the genre columns
func = lambda x: np.asarray(x) * np.asarray(number)
result = subset.apply(func)

c = list()
for i in (range(0,18)):
    c.append(sum(np.array(result[[i]])))
    print(result[[i]].columns.values,":",sum(np.array(result[[i]])))
max(c)
min(c)
print("Drama occurred most often:","39895",file=f)
print("Documentary occursed least often","758",file=f)
"""
# Output: the number of times each genre occurred based on the number of reviews.

['Action'] : [25589]
['Adventure'] : [13753]
['Animation'] : [3605]
['Childrens'] : [7182]
['Comedy'] : [29832]
['Crime'] : [8055]
['Documentary'] : [758]
['Drama'] : [39895]
['Fantasy'] : [1352]
['Film-Noir'] : [1733]
['Horror'] : [5317]
['Musical'] : [4954]
['Mystery'] : [5245]
['Romance'] : [19461]
['Sci-Fi'] : [12730]
['Thriller'] : [21872]
['War'] : [9398]
['Western'] : [1854]

Drama occurred most often: 39895
Documentary occursed least often :758
"""
#%%
print(" ",file = f)
print("Problem 6:",file=f)
## 6. What percentage of reviews involved movies classified in at least two genres?
subset = genres.ix[:,6:]
twogenres = list()
for i in range(0,1682):
    if (sum(subset.ix[i])) >= 2:
        twogenres.append(i+1)  # get movieid for movies in at least two genres

group = reviews['reviewerid'].groupby(reviews['movieid'])
number = list(group.count())

x = list()
for i in twogenres:
    x.append(number[i-1])

sum(x)/100000
print("69.938% of reviews involved movies classified in at least two genres",file=f)
"""
# Output: 69.938% of reviews involved movies classified in at least two genres
0.69938
"""
#%%
print(" ",file = f)
print("Problem 7:",file=f)
## 7. Give a 95% confidence interval for the average rating for male reviewers, and do the same for female reviewers.
new = pd.merge(reviews[['rating','reviewerid']],reviewers[['gender','reviewerid']],on='reviewerid')
male = np.sum(new.gender=='M')
female = np.sum(new.gender=='F')
umale = np.mean(new.rating[new.gender=='M'])
ufemale =np.mean(new.rating[new.gender=='F']) 
stdm = np.std(new.rating[new.gender=='M'],ddof=1)  
stdf = np.std(new.rating[new.gender=='F'],ddof=1) 
tm = stats.t.isf(0.025,male-1)
tf = stats.t.isf(0.025,female-1)

upperm = umale+tm*stdm/(male**(1/2)) # upper bound
upperf = ufemale+tf*stdf/(female**(1/2)) 
lowerm = umale-tm*stdm/(male**(1/2))  # lower bound
lowerf = ufemale-tf*stdf/(female**(1/2))
conf = {'upper':[upperm,upperf],'lower':[lowerm,lowerf]}  
cf = DataFrame(conf)       # to make results dataframe
cf = cf.set_index([['male reviewers','female reviewers']])
cf 
print("95% confidence intervals for the average rating for male and female reviewers",file=f)
print(cf,file=f)

"""
# Output: 95% confidence intervals for the average rating for male and female reviewers
                     lower     upper
male reviewers    3.521309  3.537269
female reviewers  3.517202  3.545813
"""
#%%
print(" ",file = f)
print("Problem 8:",file=f)
## 8. Which state/territory/Canada/unknown produced the top-5 most reviews?
import re
group = reviews['movieid'].groupby(reviews['reviewerid'])
reviewsnumber = DataFrame(group.count())
reviewsnumber['reviewerid']=reviewsnumber.index
new = zipcode[['Zipcode','State']]  # only 2 columns
unique = new.drop_duplicates(subset=['Zipcode'])

reviewers['Location']=" "
for i in range(0,943):  
    z = reviewers.loc[i,'zipcode']
    if re.search('[a-zA-Z]+',z):
        reviewers = reviewers.set_value(i,'Location','Canada') 
    elif sum(z == unique.Zipcode) == 1:    
        reviewers = reviewers.set_value(i,'Location',unique.get_value(unique.index[unique['Zipcode']==z].tolist()[0],'State'))
    else: 
        reviewers = reviewers.set_value(i,'Location','unknown') 

merged = pd.merge(reviewers,reviewsnumber, on='reviewerid')
count = DataFrame( merged['movieid'].groupby(merged['Location']).sum())
top5 = count.sort_index(by='movieid',ascending = False)[0:5]
print("CA, MN, NY,IL,TX produced the top-5 most reviews",file=f)
print(top5,file = f)
"""
# Output: CA, MN, NY,IL,TX produced the top-5 most reviews

       number of reviews
Location         
CA          13842 
MN           7635
NY           6882
IL           5740
TX           5042
"""
#%%
print(" ",file = f)
print("Problem 9:",file=f)
## 9. What percentage of movies have exactly 1 review? 2 reviews? 3 reviews? Continue to 20 reviews.
group = reviews['reviewerid'].groupby(reviews['movieid'])
a = np.sort(list(group.count()))
print("% of movies have exactly 1 review? 2 reviews? 3 reviews? Continue to 20 reviews.",file=f)
for i in range(1,21):
    print(100*sum(a==i)/len(a), "percentage of movies has exactly",i," reviews",file=f)

"""
# output: % of movies have exactly 1 review? 2 reviews? 3 reviews? Continue to 20 reviews.
8.38287752675 percentage of movies has exactly 1  reviews
4.04280618312 percentage of movies has exactly 2  reviews
3.56718192628 percentage of movies has exactly 3  reviews
3.8049940547 percentage of movies has exactly 4  reviews
3.03210463734 percentage of movies has exactly 5  reviews
2.31866825208 percentage of movies has exactly 6  reviews
2.6159334126 percentage of movies has exactly 7  reviews
1.78359096314 percentage of movies has exactly 8  reviews
1.96195005945 percentage of movies has exactly 9  reviews
1.96195005945 percentage of movies has exactly 10  reviews
1.18906064209 percentage of movies has exactly 11  reviews
1.66468489893 percentage of movies has exactly 12  reviews
1.48632580262 percentage of movies has exactly 13  reviews
0.832342449465 percentage of movies has exactly 14  reviews
1.3079667063 percentage of movies has exactly 15  reviews
1.12960760999 percentage of movies has exactly 16  reviews
0.594530321046 percentage of movies has exactly 17  reviews
1.42687277051 percentage of movies has exactly 18  reviews
1.07015457788 percentage of movies has exactly 19  reviews
0.713436385256 percentage of movies has exactly 20  reviews
"""
#%%
print(" ",file = f)
print("Problem 10:",file=f)
## 10. Which genre had the highest average review, and which had the lowest average review?
Action = list()
Adventure = list()
Animation = list()
Childrens = list()
Comedy = list()
Crime = list()
Documentary  = list()
Drama = list()
Fantasy = list()
FilmNoir  = list()
Horror = list()
Musical = list()
Mystery = list()
Romance = list()
SciFi = list()
Thriller = list()
War = list()
Western = list ()
genres=genres.set_index(genres.movieid)
for i in range(1,1683):
    if genres.loc[i,'Action'] == 1:
        Action.append(i)
    if genres.loc[i,'Adventure'] == 1:
        Adventure.append(i)
    if genres.loc[i,'Animation'] == 1:
        Animation.append(i)
    if genres.loc[i,'Childrens'] == 1:
        Childrens.append(i)
    if genres.loc[i,'Comedy'] == 1:
        Comedy.append(i)
    if genres.loc[i,'Crime'] == 1:
        Crime.append(i) 
    if genres.loc[i,'Documentary'] == 1:
        Documentary .append(i)
    if genres.loc[i,'Drama'] == 1:
        Drama.append(i) 
    if genres.loc[i,'Fantasy'] == 1:
       Fantasy.append(i) 
    if genres.loc[i,'Film-Noir'] == 1:
        FilmNoir.append(i) 
    if genres.loc[i,'Horror'] == 1:
        Horror.append(i) 
    if genres.loc[i,'Musical'] == 1:
        Musical.append(i) 
    if genres.loc[i,'Mystery'] == 1:
        Mystery.append(i) 
    if genres.loc[i,'Romance'] == 1:
        Romance.append(i) 
    if genres.loc[i,'Sci-Fi'] == 1:
        SciFi .append(i) 
    if genres.loc[i,'Thriller'] == 1:
        Thriller.append(i) 
    if genres.loc[i,'War'] == 1:
        War.append(i) 
    if genres.loc[i,'Western'] == 1:
        Western.append(i)     
action = list()
for i in Action:
    action.append(list(reviews.rating[reviews.movieid==i]))
adventure = list()
for i in Adventure:
    adventure.append(list(reviews.rating[reviews.movieid==i]))
animation = list()
for i in Animation:
    animation.append(list(reviews.rating[reviews.movieid==i]))
chil = list()
for i in Childrens:
    chil.append(list(reviews.rating[reviews.movieid==i]))
comedy = list()
for i in Comedy:
    comedy.append(list(reviews.rating[reviews.movieid==i]))
crime = list()
for i in Crime:
    crime.append(list(reviews.rating[reviews.movieid==i]))
doc = list()
for i in Documentary:
    doc.append(list(reviews.rating[reviews.movieid==i]))
drama = list()
for i in Drama:
    drama.append(list(reviews.rating[reviews.movieid==i]))
fan = list()
for i in Fantasy:
    fan.append(list(reviews.rating[reviews.movieid==i]))
noir = list()
for i in FilmNoir:
    noir.append(list(reviews.rating[reviews.movieid==i]))
horror = list()
for i in Horror:
    horror.append(list(reviews.rating[reviews.movieid==i]))
mus = list()
for i in Musical:
    mus.append(list(reviews.rating[reviews.movieid==i]))
mys = list()
for i in Mystery:
    mys.append(list(reviews.rating[reviews.movieid==i]))
rom = list()
for i in Romance:
    rom.append(list(reviews.rating[reviews.movieid==i]))
sci = list()
for i in SciFi:
    sci.append(list(reviews.rating[reviews.movieid==i]))
thri = list()
for i in Thriller:
    thri.append(list(reviews.rating[reviews.movieid==i]))        
war = list()
for i in War:
    war.append(list(reviews.rating[reviews.movieid==i]))    
west = list()
for i in Western:
    west.append(list(reviews.rating[reviews.movieid==i]))    
    

print('Action has average review: ', np.mean(np.concatenate(action)))
print('Adventure has average review: ', np.mean(np.concatenate(adventure)))
print('Animationhas average review: ', np.mean(np.concatenate(animation)))
print('Childrens has average review: ', np.mean(np.concatenate(chil)))
print('Comedy has average review: ', np.mean(np.concatenate(comedy)))
print('Crime has average review: ', np.mean(np.concatenate(crime)))
print('Documentary has average review: ', np.mean(np.concatenate(doc)))
print('Drama has average review: ', np.mean(np.concatenate(drama)))
print('Fantasy has average review: ', np.mean(np.concatenate(fan)))
print('Film-Noir has average review: ', np.mean(np.concatenate(noir)))
print('Horror has average review: ', np.mean(np.concatenate(horror)))
print('Musical has average review: ', np.mean(np.concatenate(mus)))
print('Mystery has average review: ', np.mean(np.concatenate(mys)))
print('Romance has average review: ', np.mean(np.concatenate(rom)))
print('Sci-Fi has average review: ', np.mean(np.concatenate(sci)))
print('Thriller has average review: ', np.mean(np.concatenate(thri)))
print('War has average review: ', np.mean(np.concatenate(war)))
print('Western has average review: ', np.mean(np.concatenate(west)))

print("War has the highest average reviews: 3.92152336988",file=f)
print("Fantasy has the lowest average reviews:  3.21523668639",file=f)
"""
War has the highest average reviews: 3.92152336988
Fantasy has the lowest average reviews:  3.21523668639
"""

#%%
print(" ",file = f)
print("Problem 11:",file=f)
## 11. Repeat the previous question, for reviewers age 30 and under and then for reviewers over 30.
over = DataFrame(reviewers[reviewers.age > 30]['reviewerid'])
under = DataFrame(reviewers[reviewers.age <= 30]['reviewerid'])
review1 = pd.merge(over,reviews,on='reviewerid')
review2 = pd.merge(under, reviews, on='reviewerid')

action2 =list()
for i in Action:
    action2.append(list(review1.rating[review1.movieid==i]))
adventure2 = list()
for i in Adventure:
    adventure2.append(list(review1.rating[review1.movieid==i]))
animation2 = list()
for i in Animation:
    animation2.append(list(review1.rating[review1.movieid==i]))
chil2 = list()
for i in Childrens:
    chil2.append(list(review1.rating[review1.movieid==i]))
comedy2 = list()
for i in Comedy:
    comedy2.append(list(review1.rating[review1.movieid==i]))
crime2 = list()
for i in Crime:
    crime2.append(list(review1.rating[review1.movieid==i]))
doc2 = list()
for i in Documentary:
    doc2.append(list(review1.rating[review1.movieid==i]))
drama2 = list()
for i in Drama:
    drama2.append(list(review1.rating[review1.movieid==i]))
fan2 = list()
for i in Fantasy:
    fan2.append(list(review1.rating[review1.movieid==i]))
noir2 = list()
for i in FilmNoir:
    noir2.append(list(review1.rating[review1.movieid==i]))
horror2 = list()
for i in Horror:
    horror2.append(list(review1.rating[review1.movieid==i]))
mus2 = list()
for i in Musical:
    mus2.append(list(review1.rating[review1.movieid==i]))
mys2 = list()
for i in Mystery:
    mys2.append(list(review1.rating[review1.movieid==i]))
rom2 = list()
for i in Romance:
    rom2.append(list(review1.rating[review1.movieid==i]))
sci2 = list()
for i in SciFi:
    sci2.append(list(review1.rating[review1.movieid==i]))
thri2 = list()
for i in Thriller:
    thri2.append(list(review1.rating[review1.movieid==i]))     
war2 = list()
for i in War:
    war2.append(list(review1.rating[review1.movieid==i]))
west2 = list()
for i in Western:
    west2.append(list(review1.rating[review1.movieid==i])) 
    

print('Action has average review: ', np.mean(np.concatenate(action2)))
print('Adventure has average review: ', np.mean(np.concatenate(adventure2)))
print('Animationhas average review: ', np.mean(np.concatenate(animation2)))
print('Childrens has average review: ', np.mean(np.concatenate(chil2)))
print('Comedy has average review: ', np.mean(np.concatenate(comedy2)))
print('Crime has average review: ', np.mean(np.concatenate(crime2)))
print('Documentary has average review: ', np.mean(np.concatenate(doc2)))
print('Drama has average review: ', np.mean(np.concatenate(drama2)))
print('Fantasy has average review: ', np.mean(np.concatenate(fan2)))
print('Film-Noir has average review: ', np.mean(np.concatenate(noir2)))
print('Horror has average review: ', np.mean(np.concatenate(horror2)))
print('Musical has average review: ', np.mean(np.concatenate(mus2)))
print('Mystery has average review: ', np.mean(np.concatenate(mys2)))
print('Romance has average review: ', np.mean(np.concatenate(rom2)))
print('Sci-Fi has average review: ', np.mean(np.concatenate(sci2)))
print('Thriller has average review: ', np.mean(np.concatenate(thri2)))
print('War has average review: ', np.mean(np.concatenate(war2)))
print('Western has average review: ', np.mean(np.concatenate(west2)))



action3 =list()
for i in Action:
    action3.append(list(review2.rating[review2.movieid==i]))
adventure3 = list()
for i in Adventure:
    adventure3.append(list(review2.rating[review2.movieid==i]))
animation3 = list()
for i in Animation:
    animation3.append(list(review2.rating[review2.movieid==i]))
chil3 = list()
for i in Childrens:
    chil3.append(list(review2.rating[review2.movieid==i]))
comedy3 = list()
for i in Comedy:
    comedy3.append(list(review2.rating[review2.movieid==i]))
crime3 = list()
for i in Crime:
    crime3.append(list(review2.rating[review2.movieid==i]))
doc3 = list()
for i in Documentary:
    doc3.append(list(review2.rating[review2.movieid==i]))
drama3 = list()
for i in Drama:
    drama3.append(list(review2.rating[review2.movieid==i]))
fan3 = list()
for i in Fantasy:
    fan3.append(list(review2.rating[review2.movieid==i]))
noir3 = list()
for i in FilmNoir:
    noir3.append(list(review2.rating[review2.movieid==i]))
horror3 = list()
for i in Horror:
    horror3.append(list(review2.rating[review2.movieid==i]))
mus3 = list()
for i in Musical:
    mus3.append(list(review2.rating[review2.movieid==i]))
mys3 = list()
for i in Mystery:
    mys3.append(list(review2.rating[review2.movieid==i]))
rom3 = list()
for i in Romance:
    rom3.append(list(review2.rating[review2.movieid==i]))
sci3 = list()
for i in SciFi:
    sci3.append(list(review2.rating[review2.movieid==i]))
thri3 = list()
for i in Thriller:
    thri3.append(list(review2.rating[review2.movieid==i]))  
war3 = list()
for i in War:
    war3.append(list(review2.rating[review2.movieid==i]))
west3 = list()
for i in Western:
    west3.append(list(review2.rating[review2.movieid==i]))
    

print('Action has average review: ', np.mean(np.concatenate(action3)))
print('Adventure has average review: ', np.mean(np.concatenate(adventure3)))
print('Animationhas average review: ', np.mean(np.concatenate(animation3)))
print('Childrens has average review: ', np.mean(np.concatenate(chil3)))
print('Comedy has average review: ', np.mean(np.concatenate(comedy3)))
print('Crime has average review: ', np.mean(np.concatenate(crime3)))
print('Documentary has average review: ', np.mean(np.concatenate(doc3)))
print('Drama has average review: ', np.mean(np.concatenate(drama3)))
print('Fantasy has average review: ', np.mean(np.concatenate(fan3)))
print('Film-Noir has average review: ', np.mean(np.concatenate(noir3)))
print('Horror has average review: ', np.mean(np.concatenate(horror3)))
print('Musical has average review: ', np.mean(np.concatenate(mus3)))
print('Mystery has average review: ', np.mean(np.concatenate(mys3)))
print('Romance has average review: ', np.mean(np.concatenate(rom3)))
print('Sci-Fi has average review: ', np.mean(np.concatenate(sci3)))
print('Thriller has average review: ', np.mean(np.concatenate(thri3)))
print('War has average review: ', np.mean(np.concatenate(war3)))
print('Western has average review: ', np.mean(np.concatenate(west3)))


print("For reviewers age over 30",'\n','Film-Noir has the highest average review: 3.99805447471','\n','Horror has the lowest average review: 3.28520017994',file=f)
print(" ",file=f)
print('For reviewers age 30 and under','\n','Filr-Noir has the highest average review: 3.80992907801','\n','Fantasy has the lowest average review: 3.09078590786',file=f)

"""
For reviewers age over 30
Film-Noir has the highest average review: 3.99805447471
Horror has the lowest average review: 3.28520017994

For reviewers age 30 and under
Filr-Noir has the highest average review: 3.80992907801
Fantasy has the lowest average review: 3.09078590786
"""

#%%
print(" ",file = f)
print("Problem 12(a):",file=f)
## 12. Suppose that a “positive review” is one with a rating of 4 or 5.
# (a) Find a 95% confidence interval for pf − pm, where pf is the proportion of positive reviews from
# females and pm is the proportion of positive reviews from males. Is there evidence that the proportions differ?

id = list(reviews.reviewerid[reviews.rating >=4 ])
reviewers = reviewers.set_index(reviewers.reviewerid)
gender1 = list()
for i in id:
    a = reviewers.loc[i,'gender']
    gender1.append(a)
    
gender2 = list()
for i in list(reviews.reviewerid):
    b = reviewers.loc[i,'gender']
    gender2.append(b)

gender1 = np.array(gender1)
gender2 = np.array(gender2)  # f & m list
female = sum(gender1 =='F') 
male = sum(gender1 == 'M')
pf = sum(gender1=='F')/sum(gender2=='F')
pm = sum(gender1=='M')/sum(gender2=='M')

diff = pf - pm
std = ((pm*(1-pm)/male + pf*(1-pf)/female))**(1/2)
zvalue = st.norm.ppf(.975)
upper = diff + zvalue * std
lower = diff - zvalue * std
conf = {'lower': [lower],'upper':[upper]}
conf = DataFrame(conf)
conf = conf.set_index([['confidence interval']])
print('95% confidence interval for difference between proportion of positive reviews from females and from males',file=f)
print(conf,file=f)
print("There is no evidence that the proportions differ",'\n',"The confidence interval includes 0, which suggests that there is no difference between the proportion",file=f)

"""
# output: 95% confidence interval for pf − pm
                         lower     upper
confidence interval   -0.008183  0.010744
"""
#%%print(" ",file = f)
print(" ",file=f)
print("Problem 12(b):",file=f)
#(b) The states California, New York, Texas, Florida, and Illinois have the largest populations. Group
#these as the “large states” and group the rest as “the rest”. Find a 95% confidence interval for
#pl −pr, where pl is the proportion of positive reviews from reviewers in large states, and pr is the
#proportion of positive reviews from reviewers in the rest. Is there evidence that the proportions differ?
# CA NY TX FL IL    
aa = pd.merge(reviewers[['reviewerid','Location']], reviews,on="reviewerid")  #location is created in question 8
positive = aa[aa.rating>=4]

large = sum(positive.Location=='CA')+sum(positive.Location=='NY')+sum(positive.Location=='TX')+sum(positive.Location=='FL')+sum(positive.Location=='IL')
totallarge = sum(aa.Location =='CA')+sum(aa.Location=='NY')+sum(aa.Location=='TX')+sum(aa.Location=='FL')+sum(aa.Location=='IL')  

rest = len(positive)-large
totalrest = 100000 - totallarge

pl = large/totallarge
pr = rest/totalrest

diff = pl - pr
std = ((pl*(1-pl)/large + pr*(1-pr)/rest))**(1/2)
zvalue = st.norm.ppf(.975)
upper = diff + zvalue * std
lower = diff - zvalue * std
conf = {'lower': [lower],'upper':[upper]}
conf = DataFrame(conf)
conf = conf.set_index([['confidence interval']])
print("95% confid ence interval for difference between proportion of positive reviews from large states and the rest",file=f)
print(conf,file=f)
print("The confidence interval is negative which might indicate that there is a difference between propotion of positive reviews from large states and from the rests",'\n',"However, the difference between the boundaries are pretty small which might suggest that the difference is not significant",file=f)

f.close()
"""
# Output: 95% confidence interval for pl −pr
                        lower     upper
confidence interval  -0.033508 -0.01576

"""


