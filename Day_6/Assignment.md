#                                                   **Assignment : Day 6**

## Handling any arguments : *args, **kwargs
```python
def decorator(function): # (function) is actually a base function we want to decorate .....eg.add()
  def wrapper(*args,**kwargs):  #args and kwargs sllos the function to accept any arguments (numbers and key words )
    print("And the addition is ....") #Before the function 
    
    result = function(*args,**kwargs) #uses original function again in result
    print(result)
    
    print("Is the answer correct.?") #After the function
    return result
  return wrapper


@decorator #Its just a shortcut for decorator call 
def add(a,b): #giving function add and attributes(a,b) which are *args
  return a+b
add(10,20)  
```

### Example : timing.py
```python
import time
from functools import wraps
def show_time(function): #it is our decorator 
   @wraps(function) #@wraps keeps the original function as it is (preserve)
   def wrapper(*args, ** kwargs):
       start - time.time() # checks the time before function starts
       result = function(*args, ** kwargs)
       print(f'Time: {time.time() -start :. 4f}s') #Calculate the time it takes to run the function 
       return result
   return wrapper
@show_time #calls the decorator
def train_one_epoch()
```
## Context Manager 

Manual 
  ```python
  file = oepn('data.txt') #open file 
  content = file.read()#work on file
  file.close() #close the file .....
  ```
### **Now if ```content = file.read()``` crashes then this file will never close**

thats why we use ``` with ``` to make file handling automatic

```python
with open('data.txt') as file:
    content = file.read()
``` 
now file will always be close even if exception occurs 

## ' __enter__ ()' and ' __exit__() '

```python
class MyContext:
    def __enter__(self): #takes self arguments and open the file
        print("Entering")
        return self #return original argument
    def __exit__(self, exc_type, exc_value, tb): #close the file
        print("Leaving")
with MyContext(): #calling function using with ....#no manual open and close needed
    print("Inside")
```
output
```python
Entering
Inside
Leaving
```

### **_Timer(example)_**

```python
import time
from contextlib import contextmanager

#it is a decorator which helps to create context manager without defining class for it

@contextmanager
def timer():    
    start = time.time() # Records the starting time

    try:
        yield #yeild will pause the function at start ..and give controls to with block

    finally: #this code block will execute even if any exception occurs
        print(f"Time: {time.time() - start:.4f}s") #it will execute after the with block

def train_one_epoch():
    time.sleep(3) #give argument in time (seconds) to sleep 


with timer():
    train_one_epoch()
```
output
```python
Time: 2.0001s
```