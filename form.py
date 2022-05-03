from tkinter import *
import tkinter.font as font
import model

root = Tk()
root.geometry('400x500')
speedDiff = 0
accelaration = 0
throttle = 0

def submitData():
    speedDiff = int (speedEntry.get())
    accelaration = int (accelarationEntry.get())
    print(speedDiff)
    print(accelaration)
    controller = model.CruiseController()
    throttle = controller.get_throttle(speed_diff=  speedDiff, acc=  accelaration)
    # Label(root, text= f"\n\nThrottle: {throttle}", font=font.Font(family='Helvetica')).pack()
    # throttleLabel.pack_forget()
    global throttleLabel 
    throttleLabel["text"] = f"\n\nThrottle: {throttle}" # = Label(root, text= f"\n\nThrottle: {throttle}", font=font.Font(family='Helvetica'))

    # throttleLabel.pack() 

    print(throttle)

    return None

# # creating a label widget
myLabel = Label(root, text="Enter Speed:\n", font=font.Font(family='Helvetica'))
# # shoving it onto the screen
myLabel.pack()
speedEntry = Entry(root, width = 20)
speedEntry.pack()

# Button(root, text="Submit Speed", command=submitSpeed).pack()


Label(root, text="\n\nEnter Accelaration:\n", font=font.Font(family='Helvetica')).pack()
accelarationEntry = Entry(root, width = 20)
accelarationEntry.pack()
Label(root, text="\n\n\n\n\n\n").pack()


Button(root, text="Submit", command=submitData, width=25, background="lightgreen", font=font.Font(family='Helvetica')).pack()

throttleLabel = Label(root, text= f"\n\nThrottle: {throttle}", font=font.Font(family='Helvetica'))


throttleLabel.pack()


# Run the interface
root.mainloop()