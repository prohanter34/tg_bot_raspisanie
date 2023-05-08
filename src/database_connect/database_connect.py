import psycopg2
from src.database_connect.util import utils
import os

conn = psycopg2.connect(
    database="raspisanie1",
    user="postgres",
    password="erwerwre",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()



def check_data(shift):
    cursor.execute("SELECT EXTRACT (DOW FROM NOW())")
    records = list(cursor.fetchall())
    return utils.dowTransform(int(records[0][0]) + shift)

def check_data_week(shift):
    if shift == 0:
        cursor.execute("SELECT EXTRACT (WEEK FROM NOW())")
    elif shift == 1:
        cursor.execute("SELECT EXTRACT (WEEK FROM NOW() + INTERVAL '1 WEEK')")
    records = list(cursor.fetchall())
    return records[0][0]

def timeTableOfDay(shift):
    if shift == 0:
        cursor.execute("SELECT NOW()::DATE")
    elif shift == 1:
        cursor.execute("SELECT NOW()::DATE + INTERVAL '1 DAY'")
    data = list(cursor.fetchall())[0][0]
    cursor.execute("SELECT * FROM timetable "
                   "JOIN subjects on timetable.subject_name = subjects.id WHERE day='{}'".format(data))
    records = list(cursor.fetchall())
    print(records)
    records = idToTeacher(records)
    print(records)
    return records


def timeTableOfDayWeek(dayOfWeek):
    week = check_data_week(0)
    cursor.execute("SELECT * FROM timetable JOIN "
                   "subjects on timetable.subject_name = subjects.id WHERE extract(week from day)='{}' "
                   "AND extract(dow from day)='{}';".format(week, dayOfWeek))
    records = list(cursor.fetchall())
    records = idToTeacher(records)
    return records


def timeTableOfWeek(shift):
    week = check_data_week(shift)
    timeTable = []
    for dayOfWeek in range(1, 7):
        cursor.execute("SELECT * FROM timetable "
                       "JOIN subjects on timetable.subject_name = subjects.id WHERE"
                       " extract(week from day)='{}' AND extract(dow from day)='{}';".format(week, dayOfWeek))
        records = list(cursor.fetchall())
        records = idToTeacher(records)
        timeTable.append(records)
    return timeTable


def idToTeacher(array):
    output = []
    for i in array:
        cursor.execute("SELECT * FROM teachers WHERE id='{}'".format(i[5]))
        records = list(cursor.fetchall())
        i = (i[0], i[1], i[7], i[3], str(i[4])[0:5], records[0][1])
        output.append(i)
    return output

