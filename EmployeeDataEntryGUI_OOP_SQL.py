
import sqlite3
from tkinter import *

class Application(Frame):
    EmployeeData = []
    RecordNumber = 0

    def __init__(self, master):
        """ Initialize Frame. """
        super(Application, self).__init__(master)  
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        #Screen elements declarations
        #labels
        self.label10 = Label(self, text="Employee ID", bg="light grey").grid(row = 0, column = 0, sticky = W)
        self.label1 = Label(self, text="First Name", bg="light grey").grid(row = 1, column = 0, sticky = W)
        self.label2 = Label(self, text="Last Name", bg="light grey").grid(row = 2, column = 0, sticky = W)
        self.label3 = Label(self, text="Address", bg="light grey").grid(row = 3, column = 0, sticky = W)
        self.label4 = Label(self, text="City", bg="light grey").grid(row = 4, column = 0, sticky = W)
        self.label5 = Label(self, text="State", bg="light grey").grid(row = 5, column = 0, sticky = W)
        self.label6 = Label(self, text="Zip", bg="light grey").grid(row = 6, column = 0, sticky = W)
        self.label7 = Label(self, text="PhoneNumber", bg="light grey").grid(row = 7, column = 0, sticky = W)
        self.label8 = Label(self, text="HourlyRate", bg="light grey").grid(row = 8, column = 0, sticky = W)
        self.label9 = Label(self, text="NormalHours", bg="light grey").grid(row = 9, column = 0, sticky = W)
        #textboxes
        self.entryID = Entry(self)
        self.entryID.grid(row = 0, column = 1, sticky = W) 
        self.entryFN = Entry(self)
        self.entryFN.grid(row = 1, column = 1, sticky = W) 
        self.entryLN = Entry(self)
        self.entryLN.grid(row = 2, column = 1, sticky = W)
        self.entryAddress = Entry(self)
        self.entryAddress.grid(row = 3, column = 1, sticky = W)
        self.entryCity = Entry(self)
        self.entryCity.grid(row = 4, column = 1, sticky = W) 
        self.entryState = Entry(self)
        self.entryState.grid(row = 5, column = 1, sticky = W)
        self.entryZip = Entry(self)
        self.entryZip.grid(row = 6, column = 1, sticky = W)
        self.entryPhone = Entry(self)
        self.entryPhone.grid(row = 7, column = 1, sticky = W) 
        self.entryRate = Entry(self)
        self.entryRate.grid(row = 8, column = 1, sticky = W)
        self.entryHours = Entry(self)
        self.entryHours.grid(row = 9, column = 1, sticky = W)
        #buttons
        self.btnClose = Button(self,text="Close",command=self.close,fg="Blue").grid(row = 10, column = 0, sticky = W)
        self.btnClear = Button(self,text="Clear",fg="Blue",command=self.clear_text).grid(row = 10, column = 1, sticky = W)
        self.btnSave = Button(self,text="Save",fg="Blue",command=self.saveData).grid(row = 10, column = 2, sticky = W)
        self.btnLoadData = Button(self,text="Load Data",fg="Blue",command=self.loadData).grid(row = 10, column = 3, sticky = W)

        self.btnFirst = Button(self,text="First",fg="Blue",command=self.moveFirst).grid(row = 11, column = 0, sticky = W)
        self.btnLast = Button(self,text="Last",fg="Blue",command=self.moveLast).grid(row = 11, column = 1, sticky = W)
        self.btnNext = Button(self,text="Next",fg="Blue",command=self.moveNext).grid(row = 11, column = 2, sticky = W)
        self.btnPrevious = Button(self,text="Previous",fg="Blue",command=self.movePrevious).grid(row = 11, column = 3, sticky = W)

    #Event handler functions
    def close(self):
        root.destroy()
        
    def clear_text(self):
        self.entryID.delete(0, END)
        self.entryFN.delete(0, END)
        self.entryLN.delete(0, END)
        self.entryAddress.delete(0, END)
        self.entryCity.delete(0, END)
        self.entryState.delete(0, END)
        self.entryZip.delete(0, END)
        self.entryPhone.delete(0, END)
        self.entryRate.delete(0, END)
        self.entryHours.delete(0, END)
        self.entryID.focus_set()
        
    def saveData(self):
        SQL = self.buildInsertSQL()
        self.executeSQL(SQL)
        print(SQL)
        
    def buildInsertSQL(self):
        SQL = "INSERT INTO Employees (EMPID,FirstName,LastName,Address) VALUES (" + self.entryID.get() + ",'" + self.entryFN.get() + "','" + self.entryLN.get() + "','" + self.entryAddress.get() + "')"
        print(SQL) 
        return SQL

    def executeSQL(self,SQL):
        conn = sqlite3.connect(r'C:\Fullerton College Classes\Python\DatabaseLecture\XYZCorp.db')
        cur = conn.cursor()
    
        cur.execute(SQL)
        conn.commit()
        conn.close()

    def loadData(self):
        Application.EmployeeData = []
        self.loadDataFromDB()
        self.displayDataOnForm()

    def loadDataFromDB(self):
        conn = sqlite3.connect(r'C:\Fullerton College Classes\Python\DatabaseLecture\XYZCorp.db')
        cur = conn.cursor()
    
        cur.execute("select * from Employee")
    
        row = cur.fetchone()
    
        while row != None:
            TempList = [row[0],row[1],row[2],row[3]]
            Application.EmployeeData.append(TempList)
            row = cur.fetchone()
            
        conn.close()

    def createDataList(self):
        Application.EmployeeData= [self.entryID.get(),self.entryFN.get(),self.entryLN.get(),self.entryAddress.get(),self.entryCity.get(),self.entryState.get(),self.entryZip.get(),self.entryPhone.get(),self.entryRate.get(),self.entryHours.get()]
        
    def displayDataOnForm(self):
        self.clear_text()
        self.entryID.insert(0,Application.EmployeeData[Application.RecordNumber][0])
        self.entryFN.insert(0,Application.EmployeeData[Application.RecordNumber][1])
        self.entryLN.insert(0,Application.EmployeeData[Application.RecordNumber][2])
        self.entryAddress.insert(0,Application.EmployeeData[Application.RecordNumber][3])
        self.entryCity.insert(0,Application.EmployeeData[Application.RecordNumber][4])
        self.entryState.insert(0,Application.EmployeeData[Application.RecordNumber][5])
        self.entryZip.insert(0,Application.EmployeeData[Application.RecordNumber][6])
        self.entryPhone.insert(0,Application.EmployeeData[Application.RecordNumber][7])
        self.entryRate.insert(0,Application.EmployeeData[Application.RecordNumber][8])
        self.entryHours.insert(0,Application.EmployeeData[Application.RecordNumber][9])

    def moveLast(self):
        Application.RecordNumber = len(Application.EmployeeData) - 1
        self.displayDataOnForm()
        
    def moveFirst(self):
        Application.RecordNumber = 0
        self.displayDataOnForm()

    def moveNext(self):
        Application.RecordNumber += 1
        if Application.RecordNumber > len(Application.EmployeeData) -1:
            Application.RecordNumber = len(Application.EmployeeData) - 1
        self.displayDataOnForm()
        
    def movePrevious(self):
        Application.RecordNumber -= 1
        if Application.RecordNumber < 0:
            Application.RecordNumber = 0
        self.displayDataOnForm()


root = Tk()
root.title("Employee Data Entry")
root.configure(background = "light grey")
root.geometry("500x450")
app = Application(root)
root.mainloop()
