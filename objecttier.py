#
# objecttier
#
# Builds Lobbyist-related objects from data retrieved through 
# the data tier.
#

import datatier

# Define the Lobbyist class with attributes and properties for basic lobbyist information
class Lobbyist:
    def __init__(self, id, fname, lname, phone):
        self._Lobbyist_ID = id
        self._First_Name = fname
        self._Last_Name = lname
        self._Phone = phone

    @property
    def Lobbyist_ID(self):
        return self._Lobbyist_ID

    @property
    def First_Name(self):
        return self._First_Name
    
    @property
    def Last_Name(self):
        return self._Last_Name
    
    @property
    def Phone(self):
        return self._Phone
    
# Define the LobbyistDetails class to hold detailed information about a lobbyist
class LobbyistDetails:
    def __init__(self, id, sal, fname, lname, minitial, suf, add1, add2, city, state, zip, country, email, phone, fax, years, emp, total):
        self._Lobbyist_ID = id
        self._First_Name = fname
        self._Last_Name = lname
        self._Phone = phone
        self._Salutation = sal
        self._Middle_Initial = minitial
        self._Suffix = suf
        self._Address_1 = add1
        self._Address_2 = add2
        self._City = city
        self._State_Initial = state
        self._Zip_Code = zip
        self._Country = country
        self._Email = email
        self._Fax = fax
        self._Years_Registered = years
        self._Employers = emp
        self._Total_Compensation = total

    @property
    def Lobbyist_ID(self):
        return self._Lobbyist_ID

    @property
    def First_Name(self):
        return self._First_Name
        
    @property
    def Last_Name(self):
        return self._Last_Name
        
    @property
    def Phone(self):
        return self._Phone
    @property
    def Salutation(self):
        return self._Salutation

    @property
    def Middle_Initial(self):
        return self._Middle_Initial
        
    @property
    def Suffix(self):
        return self._Suffix
        
    @property
    def Address_1(self):
        return self._Address_1

    @property
    def Address_2(self):
        return self._Address_2

    @property
    def City(self):
        return self._City

    @property
    def State_Initial(self):
        return self._State_Initial

    @property
    def Zip_Code(self):
        return self._Zip_Code

    @property
    def Country(self):
        return self._Country

    @property
    def Email(self):
        return self._Email

    @property
    def Fax(self):
        return self._Fax

    @property
    def Years_Registered(self):
        return self._Years_Registered

    @property
    def Employers(self):
        return self._Employers

    @property
    def Total_Compensation(self):
        return self._Total_Compensation
        

# Define the LobbyistClients class for holding a lobbyist's clients along with their basic information and total compensation
class LobbyistClients:
    def __init__(self, id, fname, lname, phone, total, clients):
        self._Lobbyist_ID = id
        self._First_Name = fname
        self._Last_Name = lname
        self._Phone = phone
        self._Total_Compensation = total
        self._Clients = clients

            
    @property
    def Lobbyist_ID(self):
        return self._Lobbyist_ID

    @property
    def First_Name(self):
        return self._First_Name
            
    @property
    def Last_Name(self):
        return self._Last_Name

    @property
    def Phone(self):
        return self._Phone
    @property
    def Total_Compensation(self):
        return self._Total_Compensation

    @property
    def Clients(self):
        return self._Clients

# Define a function to count the number of lobbyists in the database
def num_lobbyists(dbConn):
    lobbyistNumSQL = """SELECT COUNT(Lobbyist_ID) FROM LobbyistInfo"""
    result = datatier.select_one_row(dbConn, lobbyistNumSQL)
    return result[0] if result is not None else -1


# Define a function to count the number of employers in the database
def num_employers(dbConn):
    numEmployerSQL = """SELECT COUNT(Employer_Name) FROM EmployerInfo"""
    result = datatier.select_one_row(dbConn, numEmployerSQL)
    return result[0] if result is not None else -1

# Define a function to count the number of lobbyists in the database
def num_clients(dbConn):
    numClientsSQL = """SELECT COUNT(Client_ID) FROM ClientInfo"""
    result = datatier.select_one_row(dbConn, numClientsSQL)
    return result[0] if result is not None else -1

# Define a function to retrieve lobbyists based on a pattern matching their first or last name
def get_lobbyists(dbConn, pattern):
    getLobbyistSQL = """SELECT Lobbyist_ID, First_Name, Last_Name, Phone
                        FROM LobbyistInfo
                        WHERE First_Name LIKE ? OR Last_Name LIKE ?
                        ORDER BY Lobbyist_ID ASC"""
    # The pattern should be included twice in the parameters list, once for each LIKE clause
    param = [pattern, pattern]

    # Call the select_n_rows function from the datatier module with the SQL statement and the formatted parameters
    rows = datatier.select_n_rows(dbConn, getLobbyistSQL, param)

    if rows is None:
      return []

    lobbyists = []
    for row in rows:
      lobbyist = Lobbyist(row[0], row[1], row[2], row[3])  
      lobbyists.append(lobbyist)

    return lobbyists

# Define a function to retrieve detailed information for a specific lobbyist by their ID
def get_lobbyist_details(dbConn, lobbyist_id):
        LobbyistDetailSQL1 = """ 
                                Select LobbyistInfo.Lobbyist_ID, LobbyistInfo.Salutation, LobbyistInfo.First_Name, LobbyistInfo.Middle_Initial, 
                                LobbyistInfo.Last_Name,LobbyistInfo.Suffix, LobbyistInfo.Address_1,LobbyistInfo.Address_2, 
                                LobbyistInfo.City, LobbyistInfo.State_Initial, LobbyistInfo.ZipCode, LobbyistInfo.Country, LobbyistInfo.Email, 
                                LobbyistInfo.Phone,LobbyistInfo.Fax
                                from LobbyistInfo
                                where LobbyistInfo.Lobbyist_ID = ?
                                """
        LobbyistDetailSQL2 = """ select LobbyistInfo.Lobbyist_ID, Employer_Name
                                from LobbyistInfo
                                join LobbyistAndEmployer
                                on LobbyistInfo.Lobbyist_ID = LobbyistAndEmployer.Lobbyist_ID
                                join LobbyistYears
                                on LobbyistInfo.Lobbyist_ID = LobbyistYears.Lobbyist_ID
                                join EmployerInfo
                                on LobbyistAndEmployer.Employer_ID = EmployerInfo.Employer_ID
                                where LobbyistInfo.Lobbyist_ID = ?
                                group by Employer_Name
                                """
        LobbyistDetailSQL3 = """ Select sum(Compensation_Amount)
                                from Compensation
                                join LobbyistInfo
                                on Compensation.Lobbyist_ID = LobbyistInfo.Lobbyist_ID
                                where LobbyistInfo.Lobbyist_ID = ?
                                group by LobbyistInfo.Lobbyist_ID
                                """
        LobbyistDetailSQL4 = """ Select LobbyistInfo.Lobbyist_ID, Year
                                from LobbyistInfo
                                join LobbyistYears
                                on LobbyistInfo.Lobbyist_ID = LobbyistYears.Lobbyist_ID
                                where LobbyistInfo.Lobbyist_ID = ?
                                """

        # Fetching basic info
        basic_info = datatier.select_one_row(dbConn, LobbyistDetailSQL1, [lobbyist_id])
        if not basic_info:
            return None  

        # Fetching employer names
        employer_rows = datatier.select_n_rows(dbConn, LobbyistDetailSQL2, [lobbyist_id])
        empSet = [row[1] for row in employer_rows]  
        empList = sorted(list(empSet))
        # Fetching total compensation
        comp_row = datatier.select_one_row(dbConn, LobbyistDetailSQL3, [lobbyist_id])
        compAmount = float(comp_row[0]) if comp_row and comp_row[0] is not None else 0.0

        # Fetching years registered
        year_rows = datatier.select_n_rows(dbConn, LobbyistDetailSQL4, [lobbyist_id])
        yearList = [row[1] for row in year_rows]  

        # Constructing the LobbyistDetails object
        
        lobbyist_details = LobbyistDetails(
            id=basic_info[0], 
            sal=basic_info[1], 
            fname=basic_info[2], 
            lname=basic_info[4], 
            minitial=basic_info[3], 
            suf=basic_info[5], 
            add1=basic_info[6], 
            add2=basic_info[7], 
            city=basic_info[8], 
            state=basic_info[9], 
            zip=basic_info[10], 
            country=basic_info[11], 
            email=basic_info[12], 
            phone=basic_info[13], 
            fax=basic_info[14], 
            years=yearList, 
            emp=empList, 
            total=compAmount
        )

        return lobbyist_details

# Define a function to retrieve the top N lobbyists based on their total compensation for a given year
def get_top_N_lobbyists(dbConn, N, year):
    # SQL to get the top N lobbyists based on total compensation for a given year
    query_lobbyists = """
                    SELECT LobbyistInfo.Lobbyist_ID, LobbyistInfo.First_Name, LobbyistInfo.Last_Name, LobbyistInfo.Phone, SUM(Compensation.Compensation_Amount) AS Total
                    FROM LobbyistInfo 
                    JOIN Compensation ON LobbyistInfo.Lobbyist_ID = Compensation.Lobbyist_ID
                    WHERE strftime('%Y', Compensation.Period_Start) = ?
                    GROUP BY LobbyistInfo.Lobbyist_ID
                    ORDER BY Total DESC 
                    LIMIT ?
                """
    params_lobbyists = [year, N]
    top_lobbyists = datatier.select_n_rows(dbConn, query_lobbyists, params_lobbyists)

    if not top_lobbyists:
        return []

    top_lobbyist_clients = []

    for lobbyist in top_lobbyists:
        lobbyist_id, first_name, last_name, phone, total_compensation = lobbyist
        total_compensation = float(total_compensation) if total_compensation else 0.0

        # SQL to get the list of clients for each top lobbyist in the specified year
        query_clients = """
                        SELECT ClientInfo.Client_Name
                        FROM Compensation
                        JOIN ClientInfo ON Compensation.Client_ID = ClientInfo.Client_ID
                        WHERE Compensation.Lobbyist_ID = ? AND strftime('%Y', Compensation.Period_Start) = ?
                        GROUP BY ClientInfo.Client_ID
                        ORDER BY ClientInfo.Client_Name
                        """
        params_clients = [lobbyist_id, year]
        clients = datatier.select_n_rows(dbConn, query_clients, params_clients)

        client_names = [client[0] for client in clients]

        # Create an instance of LobbyistClients for each lobbyist and append to the list
        lobbyist_client_instance = LobbyistClients(lobbyist_id, first_name, last_name, phone, total_compensation, client_names)
        top_lobbyist_clients.append(lobbyist_client_instance)

    return top_lobbyist_clients

# Define a function to add a registration year for a lobbyist in the database
def add_lobbyist_year(dbConn, lobbyist_id, year):
   SQLCheck = "SELECT COUNT(*) FROM LobbyistInfo WHERE Lobbyist_ID = ?"
   ParamCheck = [lobbyist_id]
   result = datatier.select_one_row(dbConn, SQLCheck, ParamCheck)

   if not result or result[0] == 0:
      return 0

   sqlYears = "INSERT INTO LobbyistYears (Lobbyist_ID, Year) VALUES (?, ?)"
   param = [lobbyist_id, year]
   check1 = datatier.perform_action(dbConn, sqlYears, param)
   
   if check1:
      return 1
   else:
      return 0

# Define a function to set or update the salutation for a lobbyist
def set_salutation(dbConn, lobbyist_id, salutation):
    salutationSQL = "UPDATE LobbyistInfo SET Salutation = ? WHERE Lobbyist_ID = ?"
    param = [salutation, lobbyist_id]
    result = datatier.perform_action(dbConn, salutationSQL, param)
    if result == 1:
        return 1
    else: 
        return 0