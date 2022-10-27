import sqlite3


def exit( window ):
    window.destroy()

def getALLStudent():
    conn = sqlite3.connect("Student.db")
    cmd = "SELECT * FROM Student"
    cursor = conn.execute(cmd)
    student = []
    for row in cursor:
        student.append(row)
    conn.close()
    return student