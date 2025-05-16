
# Project 2
# The goal of this project is to write a console-based database application in Python, this 
# time using an N-tier design. The database used for this project consists of information 
# pertaining to registered lobbyists in Chicago, their employers, their clients, and their 
# compensation.
import sqlite3
import objecttier


def command1():
    print()
    name = input("Enter lobbyist name (first or last, wildcards _ and % supported): ")
    print()
    #name = input()  # Get input from the user
    lobbyists = objecttier.get_lobbyists(dbConn, name)  # Fetch the matching lobbyists
    num_matching_lobbyists = len(lobbyists)  # Count the number of rows in the result
    print(f"Number of lobbyists found: {num_matching_lobbyists}")
    print()
    
    if len(lobbyists) <= 100:
        for lobbyist in lobbyists:
            # Print lobbyist details
            print(f"{lobbyist.Lobbyist_ID} : {lobbyist.First_Name} {lobbyist.Last_Name} Phone: {lobbyist.Phone}")
            
    elif len(lobbyists) > 100 :
        # Limit display if too many results
        print("There are too many lobbyists to display, please narrow your search and try again...")
        print()
    else:
        print("No lobbyists found matching the criteria.")

# Command 2: Display details for a specific lobbyist by ID.
def command2():
    print()
    print("Enter Lobbyist ID: ")
    number = input()
    lobbyist_id = f"{number}"
    lobbyist = objecttier.get_lobbyist_details(dbConn, lobbyist_id)
    if not lobbyist:
        print("No lobbyist with that ID was found.")
        return
    else:
        # Print detailed information about the lobbyist
        print(f"{lobbyist.Lobbyist_ID} :")
        print(f"  Full Name: {lobbyist.Salutation} {lobbyist.First_Name} {lobbyist.Middle_Initial} {lobbyist.Last_Name} {lobbyist.Suffix}")
        print(f"  Address: {lobbyist.Address_1} {lobbyist.Address_2} , {lobbyist.City} , {lobbyist.State_Initial} {lobbyist.Zip_Code} {lobbyist.Country}")
        print(f"  Email: {lobbyist.Email}")
        print(f"  Phone: {lobbyist.Phone}")
        print(f"  Fax: {lobbyist.Fax}")
        print(f"  Years Registered: {', '.join(map(str, lobbyist.Years_Registered))}, ")
        print(f"  Employers: {', '.join(map(str,lobbyist.Employers))}, ")
        print(f"  Total Compensation: ${lobbyist.Total_Compensation:,.2f}")
        

# Command 3: Display top N lobbyists based on total compensation for a given year.
def command3():
    print()
    value = input("Enter the value of N: ")

    # Validate input for N
    if value.isdigit():
        N = int(value)
        if N <= 0:
            print("Please enter a positive value for N...")
            print()
            return
    else:
        print("Please enter a positive value for N...")
        return

    # Prompt for the year after validating N
    year = input("Enter the year: ")
    print()
    # Validate year input
    if not year:
        print("Year input is required.")
        return

    # Fetch top N lobbyists for the given year
    total = objecttier.get_top_N_lobbyists(dbConn, N, year)

    # Check if results were found and display them
    if total:
        for i in range(min(N, len(total))):
            print(f"{i+1} . {total[i].First_Name} {total[i].Last_Name}")
            print(f"  Phone: {total[i].Phone}")
            print(f"  Total Compensation: ${total[i].Total_Compensation:,.2f}")
            print(f"  Clients: {', '.join(map(str,total[i].Clients))}, ")
    else:
        return
    
# Command 4: Register a lobbyist for a given year.
def command4():
    print()
    year = input("Enter year: ")
    lobbyist_id = input("Enter the lobbyist ID: ")

    # Attempt to add the year to the lobbyist's record
    success = objecttier.add_lobbyist_year(dbConn, lobbyist_id, year)
    print()
    # Handle success or failure
    if success == 0 or success == -1:
        print("No lobbyist with that ID was found.")
    else:
        print("Lobbyist successfully registered.")
    print()
# Command 5: Set the salutation for a lobbyist.
def command5():
    print()
    lobbyist_id = input("Enter the lobbyist ID: ")
    salutation = input("Enter the salutation: ")

    # Attempt to update the lobbyist's salutation
    success = objecttier.set_salutation(dbConn, lobbyist_id, salutation)
    print()
    # Handle success or failure
    if not success:
        print("No lobbyist with that ID was found.")
    else:
        print("Salutation successfully set.")
    print()

# Main function: Entry point of the application.
print('** Welcome to the Chicago Lobbyist Database Application **')
def print_stats(dbConn):
    # format specifier "," to automatically insert comma every 3 digit from right
    print("General Statistics:")
    print(f"  Number of Lobbyists: {objecttier.num_lobbyists(dbConn):,}")
    print(f"  Number of Employers: {objecttier.num_employers(dbConn):,}")
    print(f"  Number of Clients: {objecttier.num_clients(dbConn):,}")
print()
# Establish database connection
dbConn = sqlite3.connect('Chicago_Lobbyists.db')
print_stats(dbConn)
print()
# Command loop
y = input("Please enter a command (1-5, x to exit): ")
while (y!="x"):
    if (y=='1'):
        command1()
        print()
    elif (y == '2'):
        command2()
    elif (y == '3'):
        command3()
    elif (y == '4'):
        command4()
    elif (y == '5'):
        command5()
    else:
        print("**Error, unknown command, try again...")
        
    
    # Prompt for next command
    y = input("Please enter a command (1-5, x to exit): ")