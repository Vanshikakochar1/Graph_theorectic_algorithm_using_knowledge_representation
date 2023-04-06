import pandas as pd
import numpy as np
import io

df = pd.read_csv(r"C:\Users\Zeke Henry\Downloads\Minor Project.csv")
#Eliminating the timestamp column
df = df.drop('Timestamp', axis=1)
total_cols=len(df.columns)

print(df)
#Adding the dataset the
dnew=[]
count=0
for i in df.columns:
  dnew.append('data'+(str)(count+1))
  count+=1

for i in range(len(df.columns)):
    df.set_axis(dnew, axis=1,inplace=True)
print(df)

list1=[]
for i in range(len(df.columns)):
  list1.append(df.columns)

global_eps=1/len(list1)

from itertools import combinations
combs = list(combinations(df.columns, 2))

jarray=[]
for col1, col2 in combs:
    re = len(set(df[col1]).intersection(df[col2]))
    fe=len(set(df[col1]).union(df[col2]))
    jaccardval=float(re/fe)
    jarray.append(jaccardval)

dataf = pd.DataFrame(index=['data1', 'data2', 'data3', 'data4'], columns=['data1', 'data2', 'data3', 'data4'])
dataf1 = pd.DataFrame(index=[list1[0]], columns=[list1[0]])
ds = pd.DataFrame(dataf1)
flag = 0
for i in range(len(ds)):
  for j in range(i):
    ds.iloc[j, i] = jarray[flag]
    ds.iloc[i, j] = jarray[flag]
    flag += 1
    if i == j + 1:
      ds.iloc[j + 1, i] = 0
      ds.iloc[0, 0] = 0

print(ds)

def max_value(x):
  temp = [0, 0, [], 0]
  xrow = 0
  ycol = 0
  for i in range(0, len(ds)):
    if ds.iloc[x, i] >= temp[0] and ds.iloc[x, i] != 1:
      temp[0] = ds.iloc[x, i]
      temp[1] = x
      temp[2].append(i)
  return temp


def findconcept(x, y):
    max1 = max_value(x)
    max2 = max_value(y)
    if max1[0] == max2[0] and max1[1] in max2[2] and max2[1] in max1[2]:
        return "This is a concept"
    else:
        return "This is not a concept"


for i in range(1, len(ds)):
    for j in range(i):
        print(j + 1, i + 1, findconcept(j, i))


def summation(x,y):
  sum=0.0
  for i in range(0,len(ds)):
        sum=sum+ds.iloc[i,y]
  return sum

def coalition(x,y):
    num=ds.iloc[x,y]
    sum = summation(x,y)
    # for i in range(0,len(ds)):
    #     sum=sum+ds.iloc[i,y]
    col=num/sum
    return col

coalist=[]
for i in range(1, len(ds)):
    for j in range(i):
        if (findconcept(j,i)=="This is a concept"):
            coalist.append(coalition(j,i))
            #print(j + 1, i + 1, findconcept(j, i))
print(coalist)

def concept3(x,y,z):
    var1 = x-1
    var2 = y-1
    var3 = z-1
    num1=ds.iloc[var1,var2]+ds.iloc[var2,var3]+ds.iloc[var1,var3]
    den=summation(var1,var2)+ summation(var2,var3) + summation(var1,var3)
    concept_3 = num1 / den
    return concept_3


highest=0.0
for i in range(0,len(ds)):
    for j in range(0,i):
      if(j==i):
        continue
      for k in range(0,j):
        if(k==i or k==j):
          continue
        else:
          print(k+1, j+1, i+1, concept3(k,j,i))
          if(concept3(k,j,i)>=highest):
            highest=concept3(k,j,i)

coalist.append(highest)

def concept4(m,n,o,p):
    var1 = m-1
    var2 = n-1
    var3 = o-1
    var4 = p-1
    num1=ds.iloc[var1,var2]+ds.iloc[var2,var3]+ds.iloc[var1,var3]+ds.iloc[var1,var4]+ds.iloc[var2,var4]+ds.iloc[var3,var4]
    den=summation(var1,var2)+ summation(var2,var3) + summation(var1,var3) + summation(var1,var4)+summation(var2,var4)+summation(var3,var4)
    concept_4 = num1 / den
    return concept_4


highest=0.0

for f in range(0,len(ds)):
  for i in range(0,f):
    for j in range(0,i):
      if(j==i):
        continue
      for k in range(0,j):
        if(k==i or k==j):
          continue
        else:
          print(k+1, j+1, i+1, f+1 ,concept4(k,j,i,f))
          if(concept4(k,j,i,f)>=highest):
            highest=concept4(k,j,i,f)

coalist.append(highest)

def stop_criteria(eps, n):
  espilon=eps
  coal_check=n
  perc_diff= 1-(min(coal_check)/max(coal_check))
  if perc_diff<=eps:
    return True
  else:
    return False

if (stop_criteria(0.25,coalist)) == True:
  print("Stopping coalition check")
else:
  print("Values yet to reach stopping condition, continue?")
