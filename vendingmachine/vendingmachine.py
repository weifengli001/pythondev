"""
CPSC-442X Python Programming
Assignment 1: Vending Machine
Author: Weifeng Li
UBID: 984558

"""
#Global varable
paid_amount = 0.0#The total amount of insert coins
total = 0 #The total costs
change = 0 # change
drinks = {"Water" : 1, "Soda" : 1.5, "Juice" : 3} # The drinks dictionary stores drinks and their price
snackes = {"Chips" : 1.25, "Peanuts" : 0.75, "Cookie" : 1} #The snackes dictionary stores snackes and their price

"""
entering function
parameter: factor, is the value of the coin
"""
def vending(factor = 0.25):
    global paid_amount, total, change
    print("Welco to the UB vending machine.")
    cnt = input("Enter the number of quarters you wish to insert: ")
    paid_amount = int(cnt) * factor
    change = paid_amount - total
    print("You entered ", paid_amount, " dollars.")
    main_menu()

#main menu
def main_menu():
    global paid_amount, total, change
    while True:
        print("------------------------------------")
        print("Select category: ")
        print("1. Drinks")
        print("2. Snacks")
        print("3. Exit")
        selection = input("Select an option: ")
        if(selection == '1'):
            drinks_menu()
        elif(selection == '2'):
            snackes_menu()
        elif(selection == '3'):
            #change = paid_amount - total
            print("Paid amount: ", paid_amount, ", total purchase: ", total, ", change: ", change)
            return
        else:
            print("Invalid selection.")

#drinks menu
def drinks_menu():
    global paid_amount, total, change
    while True:
        print("-------------------------------------")
        print(" Juice ($3)")
        print(" Water ($1)")
        print(" Soda ($1.5)")
        drink = input("Enter your drink selection (x to exit): ")
        if(drink == 'x'):
            break
        elif(drinks.get(drink) == None):
            print("Invalid selection.")
        else:
            if(drinks[drink] > change):
                print("You don't have enough money to buy", drink)
            else:
                total += drinks[drink]
                change -= drinks[drink]

#snackes menu
def snackes_menu():
    global paid_amount, total, change
    while True:
        print("-----------------------------------------")
        print(" Chips: ($1.25)")
        print(' Peanuts: ($0.75)')
        print(" Cookie: ($1)")
        snack = input("Enter your snack selection (x to exit): ")
        if(snack == 'x'):
            break
        elif(snackes.get(snack) == None):
            print("Invalid selection.")
        else:
            if(snackes[snack] > change):
                print("You don't hava enough money to buy", snack)
            else:
                total += snackes[snack]
                change -= snackes[snack]

vending()
