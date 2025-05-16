# Chicago Lobbyist Database Application

This is a console-based Python application that uses an N-tier design to manage and interact with a SQLite database containing information about registered lobbyists in Chicago. The application allows users to search, update, and view statistics on lobbyists, their employers, clients, and compensation.

## Project Structure

- `main.py` — Console application for user interaction.
- `objecttier.py` — Logic for database access and object creation (data access layer).
- `Chicago_Lobbyists.db` — SQLite database file with all relevant data.


## Features

### Command 1: Search Lobbyists
- Search for lobbyists by first or last name using wildcards (`%`, `_`).
- Displays a list of matches (up to 100 results).

### Command 2: View Lobbyist Details
- Input a Lobbyist ID to view full profile information including:
  - Full name
  - Address, email, and contact info
  - Years registered
  - Employers
  - Total compensation

### Command 3: Top N Lobbyists by Compensation
- Enter a year and number `N` to view the top-paid lobbyists for that year.
- Lists full name, contact info, compensation, and associated clients.

### Command 4: Register Lobbyist for a New Year
- Add a registration year to a specific lobbyist.

### Command 5: Update Salutation
- Set or update the salutation (e.g., Mr., Ms., Dr.) for a lobbyist.

## Setup & Running the App

### Requirements:
- Python 3.6+
- `sqlite3` (built-in module)

### How to Run:
1. Ensure `main.py`, `objecttier.py`, and `Chicago_Lobbyists.db` are in the same directory.
2. Open terminal or command prompt.
3. Run the app:
   ```bash
   python main.py
