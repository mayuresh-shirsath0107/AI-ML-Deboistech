''' Day 1: Python Fundamentals
   Date:09/08/2026
   Name: Mayuresh Suresh Shirsath
   Cohort: AI/ML
   Contact no : 9145506307
   Email :mayuresh0107@gmail.com
   Description : Topics which are covered on day 1
   Topics : 1) virtual environment ,2) vscode/jupyter notebook/kaggle ,3) commands ,4) DataTypes, 5) dictionary, 6) List , 
   7) Indexing, 8) Slicing , 9)Conditional Statements, 10)For loop, 11) While loop'''

#Datatype 
x=int(input("enter a valid number :"))
print(x)

#string to integer conversion
y="1234"
x=int(y)
print(x)
print(type(x))

#string to int using build in function
#Dictionary
dict={"number": 1234,
      "name": "aditya"}
print(dict['name'])

#List
lst =[1,2,3,4,"A","B",2.15,3.33,dict]
print(lst)

#indexing
print(lst[1])

#slicing
print(lst[:3])

list=["sakshi",2.5,1000,True,dict]
print(list[1])

A="lets go outside"
#Task 1:print first 6 characters from the String
print(A[:6])

#Task 2:print full string except fist 2 characters
print(A[2:])

#Task 3:print middle word from the string
print(A[5:7])

#Conditional Statement (IF , ELIF , ELSE)
sub1=int(input("enter marks of subject 1: "))
sub2=int(input("enter marks of subject 2: "))
sub3=int(input("enter marks of subject 3: "))

marks=sub1+sub2+sub3
if marks>=200:
  print("grade A")
elif marks>=100:
  print("grade B")
else:
  print("grade F")

#For loop examples
#Type 1
for i in range(1,11):
  print(i)

#Type 2
for i in range(0,101,5):
  print(i)

#While Loop
numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
target = int(input("Find number between 1 to 20 : "))
i = 0
while i < len(numbers):
    if numbers[i] == target:
        print("Number found at: ",numbers[i])
        break  
    
    i = i+1
    
    

