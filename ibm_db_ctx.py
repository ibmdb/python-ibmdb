import ibm_db

class Db2connect:
    """Context manager to handle connections to DB2."""
    #__cxn: Optional['IBM_DBConnection'] 
    
    def __init__(self, dsn: str, username: str, password: str) -> None:
        """Instantiate a DB2 connection."""
        #print("init method called")
        self.__dsn = dsn
        self.__username = username
        self.__password = password
        self.__cxn = None

    def __enter__(self) -> 'IBM_DBConnection':
        """Connect to DB2."""
        self.__cxn = ibm_db.connect(self.__dsn, '', '')
        #print("enter method called")
        return self.__cxn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Disconnect from DB2."""
        #print("exit method called")
        ibm_db.close(self.__cxn)
        self.__cxn = None      
  
"""connection_str = config.database
with DB2connect(connection_str,'','') as conn:
   print("with block ")
   print("connect")
   print(conn)
   #run query 
   stmt = ibm_db.prepare(conn, "SELECT * from animals WHERE weight < 10.0")
   result = ibm_db.execute(stmt)
   print (result)

   
print("after with connect object :", conn)
#run some query expected some errors
stmt = ibm_db.prepare(conn, "SELECT * from animals WHERE weight < 10.0")
result = ibm_db.execute(stmt)
"""