from customtkinter import (
    CTk,
    CTkFrame,
    CTkButton,
    CTkCheckBox,
    CTkEntry,
    CTkScrollableFrame,
    CTkImage,
    CTkToplevel,
    CTkLabel,
)
from tkinter import END, IntVar
from PIL import Image


task_data = []

def displayDB():
    print("=" * 50)
    for item in task_data:
        print(f"{item['task']} [{item['status']}]: {item['description']}")

class TaskManager:
    def __init__(self, masterFrame: CTkScrollableFrame):
        self.taskList = dict()
        self.master = masterFrame
        self.hideCompleted = False

    def addTask(self, taskString: str, taskStatus: int = 0, initialize: bool = False, taskDesc: str = ""):
        if not len(taskString.strip()):
            return

        deleteButton.configure(state="normal")
        taskInput.delete(0, END)
        descInput.delete(0, END)

        if len(taskString) > 26:
            taskItem = CTkScrollableFrame(master=self.master, orientation="horizontal", height=60)
        else:
            taskItem = CTkFrame(master=self.master)

        taskCheck = CTkCheckBox(master=taskItem, text=taskString, font=("monospace", 15))
        descLabel = CTkLabel(master=taskItem, text=taskDesc, font=("monospace", 12), anchor="w")
        descLabel.grid(row=1, column=0, padx=20, sticky="w")

        editButton = CTkButton(master=taskItem, text="Edit", width=50,
                               command=lambda: self.editDescription(taskCheck.__hash__()))
        editButton.grid(row=0, column=1, rowspan=2, padx=10)

        checkbox_var = IntVar()
        checkbox_var.set(taskStatus)
        taskCheck.configure(command=lambda: self.update(self.taskList[taskCheck.__hash__()]), variable=checkbox_var)
        taskCheck.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        taskItem.pack(padx=10, pady=10, fill="x")

        self.taskList[taskCheck.__hash__()] = [taskItem, taskCheck, taskString, descLabel, taskDesc]

        if not initialize:
            task_data.append({"task": taskString, "status": 0, "description": taskDesc})
            displayDB()

    def update(self, taskItem):
        for item in task_data:
            if item["task"] == taskItem[2]:
                item["status"] = taskItem[1].get()
                break
        displayDB()

        if self.hideCompleted and taskItem[1].get():
            taskItem[0].forget()
            if isinstance(taskItem[0], CTkScrollableFrame):
                taskItem[0]._parent_frame.forget()
        elif not self.hideCompleted:
            taskItem[0].pack(padx=10, pady=10, fill="x")

    def editDescription(self, task_id):
        taskItem = self.taskList[task_id]
        oldDesc = taskItem[4]

        editWin = CTkToplevel()
        editWin.title("Edit Description")
        editWin.resizable(False, False)
        label = CTkLabel(master=editWin, text="Edit Description:")
        label.pack(padx=10, pady=10)

        entry = CTkEntry(master=editWin, width=300)
        entry.insert(0, oldDesc)
        entry.pack(padx=10, pady=10)

        def save():
            newDesc = entry.get()
            taskItem[3].configure(text=newDesc)
            taskItem[4] = newDesc
            for item in task_data:
                if item["task"] == taskItem[2]:
                    item["description"] = newDesc
                    break
            displayDB()
            editWin.destroy()

        saveBtn = CTkButton(master=editWin, text="Save", command=save)
        saveBtn.pack(padx=10, pady=10)

    def showOrHideCompleted(self, status: bool):
        self.hideCompleted = status
        for item in self.taskList.values():
            self.update(item)

def proceedDeleting(option: str, warning: CTkToplevel):
    if option == "delete":
        deleteButton.configure(state="disabled")
        task_data.clear()
        for taskItem in taskManager.taskList.values():
            taskItem[0].destroy()
            if isinstance(taskItem[0], CTkScrollableFrame):
                taskItem[0]._parent_frame.destroy()
        taskManager.taskList = dict()
    warning.destroy()
    app.update()

def deleteData():
    deleteWarning = CTkToplevel()
    deleteWarning.resizable(False, False)
    deleteWarning.grab_set()
    warningLabel = CTkLabel(master=deleteWarning, text="⚠️This will erase all data⚠️")
    warningLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    proceedButton = CTkButton(master=deleteWarning, text="Proceed",
                              command=lambda: proceedDeleting("delete", deleteWarning))
    proceedButton.grid(row=1, column=0, padx=10, pady=10)
    cancelButton = CTkButton(master=deleteWarning, text="Cancel",
                             command=lambda: proceedDeleting("cancel", deleteWarning))
    cancelButton.grid(row=1, column=1, padx=10, pady=10)

def close_connection():
    app.destroy()


app = CTk()
app.title("Personal Task Manager")
app.geometry("370x600")
app.minsize(370, 600)
app.resizable(False, True)
app.iconbitmap("./images/taskManagerIcon.ico")

mainFrame = CTkFrame(master=app)
mainFrame.pack(padx=10, pady=10, expand=True, fill="both")

taskManagerFrame = CTkFrame(master=mainFrame)
taskManagerFrame.pack(padx=10, pady=10, fill="x")

taskInput = CTkEntry(master=taskManagerFrame, width=225, placeholder_text="Task name")
taskInput.grid(row=0, column=0, padx=10, pady=5)

descInput = CTkEntry(master=taskManagerFrame, width=225, placeholder_text="Description (optional)")
descInput.grid(row=1, column=0, padx=10, pady=5)

def handle_enter(event=None):
    taskManager.addTask(taskInput.get(), taskDesc=descInput.get())

taskInput.bind("<Return>", handle_enter)
descInput.bind("<Return>", handle_enter)

taskListFrame = CTkScrollableFrame(master=mainFrame)
taskListFrame.pack(padx=10, pady=10, expand=True, fill="both")

taskManager = TaskManager(taskListFrame)

addTaskButton = CTkButton(master=taskManagerFrame, text="ADD", width=60,
                          command=lambda: taskManager.addTask(taskInput.get(), taskDesc=descInput.get()))
addTaskButton.grid(row=0, column=1, padx=10, pady=10, rowspan=2)

hideCompletedCheck = CTkCheckBox(master=taskManagerFrame, text="Hide Completed", font=("monospace", 15))
hideCompletedCheck.configure(command=lambda: taskManager.showOrHideCompleted(hideCompletedCheck.get()))
hideCompletedCheck.grid(row=2, column=0, padx=10, pady=10)

deleteButton = CTkButton(master=taskManagerFrame, text=None, width=60,
                         image=CTkImage(Image.open("./images/bin.png")),
                         command=deleteData)
deleteButton.grid(row=2, column=1, padx=10, pady=10)


for row in task_data:
    taskManager.addTask(row["task"], row["status"], True, taskDesc=row["description"])

app.protocol("WM_DELETE_WINDOW", close_connection)
app.mainloop()
