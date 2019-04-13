
"""
simple students database that collect the information of students and calculate the average of their exams,
then add to database.. by the way, I am using PostgreSQL database.
"""

import psycopg2 as ps

def create_db():
    """
    first, let's connect our database and create a table
    """
    conn = ps.connect("dbname='student' user='postgres' password='000' host='localhost' port='5432'")

    #cursor
    cur = conn.cursor()

    #let's create student table
    cur.execute(" CREATE TABLE IF NOT EXISTS students(StudentID integer PRIMARY KEY, StudentName Text NOT NULL,Surname Text NOT NULL)")
    conn.commit()
    # and courses table
    cur.execute(" CREATE TABLE IF NOT EXISTS Courses(CourseID integer PRIMARY KEY, ID integer REFERENCES students(StudentID) ON DELETE CASCADE,CourseName TEXT NOT NULL,Quiz REAL NOT NULL,VizeNot REAL NOT NULL, FinalNot REAL NOT NULL,average REAL)")
    conn.commit()
    conn.close()

# to insert our students table

def insertStudents(id,name,surname):
    con = ps.connect("dbname='student' user='postgres' password='000' host='localhost' port='5432'")
    cur = con.cursor()
    #cur.execute("INSERT INTO store(item,quatity,price) values('%s',%s,%s) "% (item,quatity,price))
    # to avoid sql injections we use like this
    cur.execute("INSERT INTO students(StudentID,StudentName,Surname) values(%s,%s,%s) ",(id,name,surname))
    con.commit()
    con.close()

# let's insert student courses
def insertCourses(studentID,id,course,quiz,vize,final,average):
    con = ps.connect("dbname='student' user='postgres' password='000' host='localhost' port='5432'")
    cur = con.cursor()
    # inserting the parameters
    cur.execute("INSERT INTO Courses(CourseID,ID,CourseName,Quiz,VizeNot,FinalNot,average) values(%s,%s,%s,%s,%s,%s,%s) ",(id,studentID,course,quiz,vize,final,average))
    con.commit()
    con.close()


# Deleting student note: before we have to delete student courses table

def deleteDatabase_student(id):
    con = ps.connect("dbname='student' user='postgres' password='000' host='localhost' port='5432'")
    cur = con.cursor()
    cur.execute('DELETE FROM Courses WHERE ID=%s',(id,))
    con.commit()
    cur.execute('DELETE FROM students WHERE StudentID=%s',(id,))
    con.commit()
    con.close()


# let's view our students and their courses

def viewStudents():
    con = ps.connect("dbname='student' user='postgres' password='000' host='localhost' port='5432'")
    cur = con.cursor()
    cur.execute('select * from students inner join Courses on students.studentid = Courses.id')
    rows = cur.fetchall()
    print('studentid | studentname| surname| courseid | id | coursename | quiz | vizenot | finalnot |average')
    print()
    for row in rows:
            print(row,'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')
    con.close()
    
# let's update our course table
def updateDatabase_courses(columnname,option,id,av):
    con = ps.connect("dbname='student' user='postgres' password='000' host='localhost' port='5432'")
    cur = con.cursor()
    #cur.execute('UPDATE Courses SET CourseName=%s,Quiz=%s,VizeNot=%s,FinalNot=%s,average=%s WHERE CourseID=%s',(coursename,quiz,vize,final,average,id))
    cur.execute('UPDATE Courses SET '+ columnname+'=%s,average=%s WHERE CourseID=%s',(option,av,id))
    con.commit()
    con.close()

# let's update our students table

def updateDatabase_student(id,name,surname):
    con = ps.connect("dbname='student' user='postgres' password='000' host='localhost' port='5432'")
    cur = con.cursor()
    cur.execute('UPDATE students SET StudentName=%s,Surname=%s WHERE StudentID=%s',(name,surname,id))
    con.commit()
    con.close()





"""
    know let's start our project of that user can enter student and edit,
    and I used couple of function I hope I will change these to class..

"""







def addStudent():
    name = input('Enter student name:')
    surname = input('enter student surname:')
    ID = input('Enter Student ID: ')
    #insert to the database
    insertStudents(ID,name,surname)


# add course from user
def addCourse(studentId):
    courses = int(input('How many Courses you want to add: '))

    for i in range(courses):
        name = input('course name:')
        id = input('course id:')
        quiz = float(input('add quiz not:'))
        vize = float(input('add vize not:'))
        final = float(input('add final not:'))
        av = quiz*0.20 + vize*0.30 + final*0.50
        insertCourses(studentId,id,name,quiz,vize,final,av)

    
# let's update our student from user
def updateStudent(id):
    name = input('Enter student name:')
    surname = input('enter student surname:')
    #add to the database
    updateDatabase_student(id,name,surname)


# let's update student's courses that we want
def updateCourse(id):
    orginalAv = 0
    try:
        coursename = input('input course name:')
        option = int(input('which one you want to update(quiz:1,vize:2,final:3,courseName:4):'))
        changeto = input('What you want to changed it:')
        #first let's connect to the database to change average of student if user change one of student puans
        con = ps.connect("dbname='student' user='postgres' password='000' host='localhost' port='5432'")
        cur = con.cursor()
        cur.execute('select quiz, vizenot,finalnot,average from Courses where coursename=%s',(coursename,))
        rows = cur.fetchall()
        for quiz,vize,final,ave in rows: 
            orginalAv = ave

            if option ==1:
                changeto= float(changeto)
                av = float(changeto*0.20 + vize*0.30 + final*0.50)
                quiz = 'Quiz'
                updateDatabase_courses(quiz,changeto,id,av)

            elif option ==2:
                changeto= float(changeto)
                av = float(quiz*0.20 + changeto*0.30 + final*0.50)
                vize = 'VizeNot'
                updateDatabase_courses(vize,changeto,id,av)
                
                #updating student
            elif option ==3:
                changeto= float(changeto)
                av = float(quiz*0.20 + vize*0.30 + changeto*0.50)
                final = 'FinalNot'
                updateDatabase_courses(final,changeto,id,av)
                
            #updating student course
            elif option ==4:
                name = 'CourseName'
                updateDatabase_courses(name,changeto,id,orginalAv)
        con.close()
    except:
        print('course not exist')


# let's delete the student that user user entered

def deleteStudent(id):
    deleteDatabase_student(id)

    


# print on screen the options of user
def switch_demo(argument):
    switcher = {
        1: "Insert Students",
        2: "Insert Courses",
        3: "Update Student",
        4: "Update Course",
        5: "Delete Student",
        6: "View Students and Courses",
    }
    for i in switcher:
        print(i,': ', switcher[i])
    print()
    return switcher.get(argument, "Invalid month")
    


def continou():
    quit = input('you want to continou?(y,n):')
    if quit=='y':
        return True
    else:
        return False
""" let's build our project that user can add and edit student"""

while True:
    create_db()
    switch_demo(1)
    option = int(input('choose an Option: '))
   
    if switch_demo(option) =='Invalid month' :
        print('Wrong option try Again..')
    else:
        #adding student
        if option ==1:
            addStudent()
        
        #adding course
        elif option ==2:
            id = int(input('which student Id:'))
            addCourse(id)
        
        #updating student
        elif option ==3:
            id = int(input('which student Id:'))
            updateStudent(id)
        
        #updating student course
        if option ==4:
            id = int(input('which student Id:'))
            updateCourse(id)
        
        #deleting student with his courses
        elif option ==5:
            id = int(input('which student Id:'))
            deleteStudent(id)
        
        #showing all students in data with courses
        elif option ==6:
            viewStudents()
        
    if continou()==False:
        break