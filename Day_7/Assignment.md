# _Assigment of Day 7_

## _Get request and reading it back_
```python
response = requests.get('https://google.com') #we are requesting to fetch data of Google.com web page 
response.status_code #it shows the status of our request 
```
output
```python
200 #means we successulyy fetched data
```
.                                                                                  
.                                                                                                
.                                                                                             
```python
response.text #this is the data we fetched in script form 
```
output
```python
'<html>....</html>
```

```python
response.raise_for_status()
#raises an error automatically on 404 , 500 ,etc
```
Basically _get request_ is used to get data or fetch data of a web page or https URL from the server ...                         
it is strictly _read only_ data means user can't do any changes in it                                                     

## _post request_
```python
response = requests.post(
    url,json=data
)
```
**the _post_ request sends the data to the server or in easier way ..uploads the data**                                      
it is exactly opposite of _get_ request                                                                     
it is also used to calling **_API_** model
```python
requests.post(api_url,json=data)
```

## _JSON_

```python
response = requests.get('https://google.com/data') #Sends http request to the server
data = response.json() # after fetching data from the server ...it converts raw text string into json file
data['name'] #from that json file ..python gives the target value as output
```
outpu
```python
'Mayuresh'
```
**now whats actually _JSON_ means .......**
JSON is a translator for python or any other programming language which translate raw text string data into dictionary (key:value)pair format which makes python to understand and fetch data .....                                   
eg...{'name':'Mayuresh','id':101,etc...} converts into                                                             
```python
 {
    'name':'Mayuresh'
    'id': 101
   }
```
it is more structured and map form of data.....

## Worked example : Students_marks
```python
marks = np.array([86,90,78,92,86]) #created an array and store it in variable 'marks'
print("Marks:", marks) # gets marks from the array
print("Total:", np.sum(marks)) #does the total sum of elements in array....#Total sum of marks
print("Average:", np.mean(marks)) #Gets the average marks using mean function on array
print("Highest:", np.max) #gets the maximum value from the array ....#Highest marks from the array
```
output
```python
Marks: [86 90 78 92 86]
Total: 432
Average: 86.4
Highest: 92
```