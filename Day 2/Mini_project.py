
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