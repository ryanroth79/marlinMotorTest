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

ser = ""
root = tk.Tk()
root.title("As the motor turns")
speedVar = tk.IntVar()
distanceVar = tk.IntVar()
cyclesVar = tk.StringVar()
OptionList = [
"Clockwise",
"Counter-Clockwise"
] 
directionVar = tk.StringVar()
directionVar.set(OptionList[0])

def runCycles():
  speed = speedVar.get()
  distance = distanceVar.get()
  cycles = int(cyclesVar.get())
  print(cycles)
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

## Main Section
def initSystem():
    global ser
    print(serialPort.get())
    ser = serial.Serial(serialPort.get())
    ser.baudrate = 250000
    ser.timeout = 1
    readAllLines()
    ser.write("M119\r\n".encode())
    readAllLines()
    ser.write("M92 X16.00\r\n".encode()) # Try and set 1 mm = 1 step
    readAllLines()
    ser.write("M203 X800\r\n".encode()) # Set Max Speeds
    readAllLines()
    ser.write("M201 X4000\r\n".encode()) # Set Max Acceleration
    readAllLines()

tabControl = ttk.Notebook(root)
cycleTab = ttk.Frame(tabControl)
posTab = ttk.Frame(tabControl)

## Cycle Tab
tabControl.add(cycleTab, text = "Cycle")
#lazily adding the serial port entry here....
serialPort = tk.StringVar(value = "/dev/ttyUSB0")
spBox = tk.Entry(cycleTab, textvariable = serialPort, ).grid(row=0, column=1, columnspan=1)
initButton = tk.Button(cycleTab, text="Init System", command = initSystem).grid(row=0, column = 2)

var = tk.StringVar()
label = tk.Label( cycleTab, textvariable=var).grid(row=5, column=2, columnspan=1)

speedSlider = tk.Scale(cycleTab, from_=0, to_=50000, variable = speedVar,
                                 orient=tk.HORIZONTAL, resolution = 100, label = "Speed",
                                 width=45, length=400).grid(row=2, column=0, columnspan=2)

distanceSlider = tk.Scale(cycleTab, from_=0, to_=500, variable = distanceVar,
                                 orient=tk.HORIZONTAL, resolution = 1, label = "Distance",
                                 width=45, length=400).grid(row=3, column=0, columnspan=2)

tk.Label(cycleTab, text="Number of cycles").grid(row=4, column = 0)
cycles = tk.Entry(cycleTab, textvariable = cyclesVar).grid(row=4, column=1, columnspan=1)

goButton = tk.Button(cycleTab, text = "CYCLE", command = runCycles).grid(row = 5, column=1)
goRoundButton = tk.Button(cycleTab, text = "GO Right", command = runPositionCW).grid(row = 6, column=2)
goBackButton = tk.Button(cycleTab, text = "GO Left", command = runPositionCCW).grid(row = 6, column=3)

## Position Tab

tabControl.add(posTab, text = "Position")



tabControl.pack(expand=1, fill="both")



root.mainloop()
