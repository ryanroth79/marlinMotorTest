import tkinter as tk
from tkinter import *
from tkinter import ttk
import serial
import time

def readAllLines():
    while True:
      buff = ser.readline()
      if(len(buff) == 0):
          break
      print(buff)

root = tk.Tk()
root.title("As the motor turns")
speedVar = tk.IntVar()
distanceVar = tk.IntVar()
cyclesVar = tk.IntVar()
OptionList = [
"Clockwise",
"Counter-Clockwise"
] 
directionVar = tk.StringVar()
directionVar.set(OptionList[0])

def runCycles():
  speed = speedVar.get()
  distance = distanceVar.get()
  cycles = cyclesVar.get()
  fwdCommand = "G1 F" + str(speed) + " X" + str(distance) + " H0 \r\n"
  revCommand = "G1 F" + str(speed) + " X-" + str(distance) + " H0 \r\n"
  print(fwdCommand)
  print(revCommand)
  
  for c in range(cycles):
    var.set(c+1)
    root.update()
    ser.write(fwdCommand.encode())
    print(ser.readline())
    
    time.sleep(0.1)
    ser.write(revCommand.encode())
    print(ser.readline())

def runPositionCW():
  speed = speedVar.get()
  distance = distanceVar.get()
  cycles = cyclesVar.get()
  fwdCommand = "G1 F" + str(speed) + " X" + str(distance) + " H0 \r\n"
  ser.write(fwdCommand.encode())
  print(fwdCommand)
  print(ser.readline())
        
def runPositionCCW():
  speed = speedVar.get()
  distance = distanceVar.get()
  cycles = cyclesVar.get()
  revCommand = "G1 F" + str(speed) + " X-" + str(distance) + " H0 \r\n"
  ser.write(revCommand.encode())
  print(revCommand)
  print(ser.readline())
  

tabControl = ttk.Notebook(root)
cycleTab = ttk.Frame(tabControl)
posTab = ttk.Frame(tabControl)

## Cycle Tab
tabControl.add(cycleTab, text = "Cycle")
var = tk.StringVar()
label = tk.Label( cycleTab, textvariable=var).grid(row=5, column=2, columnspan=1)

speedSlider = tk.Scale(cycleTab, from_=0, to_=40000, variable = speedVar,
                                 orient=tk.HORIZONTAL, resolution = 100, label = "Speed",
                                 width=45, length=400).grid(row=0, column=0, columnspan=2)

distanceSlider = tk.Scale(cycleTab, from_=0, to_=500, variable = distanceVar,
                                 orient=tk.HORIZONTAL, resolution = 1, label = "Distance",
                                 width=45, length=400).grid(row=1, column=0, columnspan=2)

cyclesSlider = tk.Scale(cycleTab, from_=1, to_=1000, variable = cyclesVar,
                                 orient=tk.HORIZONTAL, resolution = 1, label = "Cycles",
                                 width=45, length=400).grid(row=3, column=0, columnspan=2)

goButton = tk.Button(cycleTab, text = "CYCLE", command = runCycles).grid(row = 4, column=1)
goRoundButton = tk.Button(cycleTab, text = "GO Right", command = runPositionCW).grid(row = 5, column=2)
goBackButton = tk.Button(cycleTab, text = "GO Left", command = runPositionCCW).grid(row = 5, column=3)

## Position Tab

tabControl.add(posTab, text = "Position")



tabControl.pack(expand=1, fill="both")

## Main Section
ser = serial.Serial("/dev/ttyUSB0")
ser.baudrate = 250000
ser.timeout = 1
readAllLines()
ser.write("M119\r\n".encode())
readAllLines()
ser.write("M92 X16.00\r\n".encode()) # Try and set 1 mm = 1 step
readAllLines()
root.mainloop()
