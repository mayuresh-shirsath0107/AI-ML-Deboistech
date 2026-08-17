#                                       BankAccount Class&#x20;

---

## Code Explanation

### 1. Creating the Class

```python
class BankAccount:
```

A class named `BankAccount` is created. It acts as a blueprint for creating bank account objects.

---

### 2. Constructor Method

```python
def __init__(self, owner, balance):
    self.owner = owner
    self.balance = balance
```

The `__init__()` method is called automatically when a new object is created.

#### Parameters:

- `owner` → Name of the account holder.
- `balance` → Initial account balance.

#### Example:

```python
acc = BankAccount("Mayuresh", 10000)
```

This creates an account for **Mayuresh** with an initial balance of **₹10,000**.

---

### 3. Deposit Method

```python
def deposit(self, amount):
    self.balance += amount
```

This method adds the deposited amount to the current balance.

#### Example:

```python
acc.deposit(1500)
```

Calculation:

```text
10000 + 1500 = 11500
```

New Balance = **₹11,500**

---

### 4. Withdraw Method

```python
def withdraw(self, amount):
    if amount <= self.balance:
        self.balance -= amount
    else:
        print("insufficient balance")
```

This method withdraws money only if enough balance is available.

#### Example:

```python
acc.withdraw(2000)
```

Calculation:

```text
11500 - 2000 = 9500
```

New Balance = **₹9,500**

If the withdrawal amount is greater than the available balance, the program displays:

```text
insufficient balance
```

---

### 5. Show Balance Method

```python
def show_balance(self):
    print(f"Balance:{self.balance}")
```

This method displays the current account balance.

#### Example:

```python
acc.show_balance()
```

Output:

```text
Balance:9500
```

##
