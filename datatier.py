import sqlite3


def select_one_row(dbConn, sql, parameters = None):
    if (parameters == None):
       parameters = []
    dbCursor = dbConn.cursor()

    try:
       dbCursor.execute(sql, parameters)
       row = dbCursor.fetchone()
       return row if row is not None else()
    except Exception as err:
       print("select_one_row failed:", err)
       return None
    finally:
       dbCursor.close()

def select_n_rows(dbConn, sql, parameters = None):
    if (parameters == None):
       parameters = []
    dbCursor = dbConn.cursor()

    try:
       dbCursor.execute(sql, parameters)
       rows = dbCursor.fetchall()
       return rows
    except Exception as err:
       print("select_n_rows failed:", err)
       return None
    finally:
       dbCursor.close()


def perform_action(dbConn, sql, parameters = None):
    if (parameters == None):
        parameters = []
    dbCursor = dbConn.cursor()

    try:
       dbCursor.execute(sql, parameters)
       dbConn.commit()
       return dbCursor.rowcount
    except Exception as err:
       print("perform_action failed:", err)
       return -1
    finally:
       dbCursor.close()