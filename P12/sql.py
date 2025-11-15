#Here we will be creating a student db and storing data using sqllite3
import sqlite3

conn = sqlite3.connect('student.db')

#cursor object : to create record, insert records, update, delete..
cur = conn.cursor()

cur.execute('''
CREATE TABLE STUDENT(NAME VARCHAR(30), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT);
            ''')

cur.execute('''INSERT INTO STUDENT VALUES ('ABHISHEK', '10', 'B', 89)''')
cur.execute('''INSERT INTO STUDENT VALUES ('BACCHAN', '11', 'B', 99)''')
cur.execute('''INSERT INTO STUDENT VALUES ('CHIRAG', '12', 'B', 59)''')
cur.execute('''INSERT INTO STUDENT VALUES ('DEEPAK', '8', 'B', 69)''')
cur.execute('''INSERT INTO STUDENT VALUES ('GOLI', '9', 'B', 89)''')
cur.execute('''INSERT INTO STUDENT VALUES ('TAPPU', '9', 'B', 19)''')

print("Inserted Records are: ")

data = cur.execute(''' SELECT * FROM STUDENT ''')

for stu in data:
    print(stu)

conn.commit()
conn.close()