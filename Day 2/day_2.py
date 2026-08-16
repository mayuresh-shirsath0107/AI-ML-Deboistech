''' Day 2: Python Fundamentals
   Date:10/08/2026
   Name: Mayuresh Suresh Shirsath
   Cohort: AI/ML 
   Description : Topics that are covered on day 2
   Topics : 1) Arithmatic Operators,2)String Concatination ,3) String Replication ,4) variable naming rule , 5) comments, 6) print function , 
   7) input function, 8) len function , 9)type conversion, 10) round() function, 11)  abs() function 12)comparison (relational) operators ,
  13)Boolean Operator  , 14) Minor project'''

"""Arithmetic Operations"""

A=2
B=3
print(A**B) #Exponent

print(B//A) #Inter division

print(B/A) #Division

print(B*A) #Multiplication

print(A+B) #Addition

print(B-A) #Substraction


"""String Concatenation"""

A="My Name "
B="Mayuresh"

D=A+B
print(D)



"""String Replication"""

X="Replicate "
print(X*3)

"""Lets change the value of Variable"""

var1=3.14
print(var1)
var1="String"
print(var1)



"""Type Conversion"""

A=1234
print(str(A)) #Integer to String

B="32.22"
print(float(B)) #String to Float

"""round() Approximation"""

A=12.8743
print(round(A))

"""abs() Absolute value                     
*converts negative value into positive
"""

A=-323
print(abs(A))

"""Comparison operations"""

A=int(input("Enter the number: "))
B=int(input("Enter the number: "))

if A==B:
  print("equals to each other")
elif A>=B:
  print("A is greter ")
else:
  print("A is smaller")

"""Boolean operators

and : TRUE when both values are true
or : TRUE when atleast one value is true
not : converts TRUE into FALSE and FALSE into TRUE
"""

""" MINI project on ALl Python operators """

print("System : You are locked inside Python Vault")
print("Your Mission: Collect enough power to escape the vault.")

#level 1
energy=10
print("LEVEL 1 — ENERGY CORE")
print(f"You start with {energy} energy.")

found = int(input("You found an energy crystal worth: "))

energy = energy + found

print("Energy collected!")
print(f"Your energy is now: {energy}")

#level 2
print("LEVEL 2 — POWER BOOST")

boost = int(input("Choose your power multiplier (1–5): "))

powered_energy = energy * boost

print("POWER ACTIVATED!")
print(f"Your energy became: {powered_energy}")

#level 3
print("LEVEL 3 — LASER WALL")

laser_cost = int(input("How much energy does the laser wall cost? "))

remaining = powered_energy - laser_cost

print("Laser wall disabled!")
print(f"Energy remaining: {remaining}")

#level 4
print("LEVEL 4 — TEAM UP")

team_size = int(input("How many hackers are in your team? "))

share = remaining / team_size

print(f"Each hacker gets {share:.2f} energy.")

#level 5
print("LEVEL 5 — BUILD THE SQUAD")

energy_per_hacker = int(input("Energy required per hacker: "))

full_hackers = remaining // energy_per_hacker

print(f"You can fully power {full_hackers} hackers.")

#level 6
leftover = remaining % energy_per_hacker

print(f"Energy left unused: {leftover}")

#level 7
print("LEVEL 7 — THE FINAL VAULT")

power_level = int(input("Enter your final power level: "))

final_power = power_level ** 2

print(f"Your final power is: {final_power}")

#escape
print("\n" + "=" * 45)
print("VAULT UNLOCKED!")
print("=" * 45)

print(f"""
🏆 MISSION COMPLETE!

🔋 Final energy      : {remaining}
👥 Full hackers      : {full_hackers}
♻️ Leftover energy   : {leftover}
⚡ Final power       : {final_power}

You didn't just learn operators.
You used them to build something. 🐍

WELCOME TO PYTHON.
""")
