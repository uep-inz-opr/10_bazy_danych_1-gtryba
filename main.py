import csv, sqlite3
from datetime import datetime
sqlite_con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) # change to 'sqlite:///your_filename.db'sqlite_con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) # change to 'sqlite:///your_filename.db'
cur = sqlite_con.cursor()

#Tworzymy pusta tabele polaczenia
cur.execute('''CREATE TABLE polaczenia (from_subscriber data_type INTEGER, 
                  to_subscriber data_type INTEGER, 
                  datetime data_type timestamp, 
                  duration data_type INTEGER , 
                  celltower data_type INTEGER);''') # use your column names here

with open('polaczenia_duze.csv','r') as fin: 
    # csv.DictReader uses first line in file for column headings by default
    reader = csv.reader(fin, delimiter = ";") # comma is default delimiter
    next(reader, None)  # skip the headers
    rows = [x for x in reader]
    #print(rows)
    cur.executemany("INSERT INTO polaczenia (from_subscriber, to_subscriber, datetime, duration , celltower) VALUES (?, ?, ?, ?, ?);", rows)
    sqlite_con.commit()

# sqlite_con
# cursor = sqlite_con.cursor()
# cursor.execute("Select datetime from polaczenia limit 3;")
# cursor.fetchall()
# print(cursor.fetchall())

#To samo co ostatnio, usunieta funkcja mogrify
class ReportGenerator:
  def __init__(self,connection, escape_string = "(%s)"):
    self.connection = connection
    self.report_text = None
    self.escape_string = escape_string

  def generate_report(self, user_id):
    cursor = self.connection.cursor()
    sql_query = f"Select sum(duration) from polaczenia where from_subscriber ={self.escape_string}"
    args = (user_id,)
    cursor.execute(sql_query, args)
    result = cursor.fetchone()[0]
    self.report_text = f"Łączny czas trwania dla użytkownika {user_id} to {result}"

  def get_report(self):	
    return self.report_text

  def get_duration(self):
      cursor = self.connection.cursor()
      query = f"Select sum(duration) from polaczenia"
      cursor.execute(query)
      result = cursor.fetchone()
      wynik = result[0]
      print(wynik)


# rg = ReportGenerator(sqlite_con, escape_string="?")
# rg.generate_report(283)
# rg.get_report()

# cursor.execute("Select datetime as '[timestamp]' from polaczenia limit 5;")
# result = cursor.fetchall()
# print(result)
#[x[0].isoformat() for x in result]

if __name__ == "__main__":
    nazwa_pliku = input()
    rg = ReportGenerator(sqlite_con, escape_string="?")
    rg.get_duration()
    rg.get_report()

