import tkinter
import serial
import time

window = tkinter.Tk()
window.geometry("800x480")
window.wm_title("Spin me right round...")
speedVar = tkinter.IntVar()
distanceVar = tkinter.IntVar()
cyclesVar = tkinter.IntVar()

def readAllLines():
    while True:
      buff = ser.readline()
      if(len(buff) == 0):
          break
      print(buff)
      
ser = serial.Serial("com3")
ser.baudrate = 250000
ser.timeout = 1
readAllLines()
ser.write("M119\r\n".encode())
readAllLines()
      
var = tkinter.StringVar()
label = tkinter.Label( window, textvariable=var).grid(row=5, column=2, columnspan=1)

speedSlider = tkinter.Scale(window, from_=0, to_=25000, variable = speedVar,
                                 orient=tkinter.HORIZONTAL, resolution = 100, label = "Speed",
                                 width=45, length=200).grid(row=0, column=0, columnspan=2)

distanceSlider = tkinter.Scale(window, from_=0, to_=500, variable = distanceVar,
                                 orient=tkinter.HORIZONTAL, resolution = 1, label = "Distance",
                                 width=45, length=200).grid(row=1, column=0, columnspan=2)

cyclesSlider = tkinter.Scale(window, from_=1, to_=1000, variable = cyclesVar,
                                 orient=tkinter.HORIZONTAL, resolution = 1, label = "Cycles",
                                 width=45, length=200).grid(row=3, column=0, columnspan=2)


def doIt():
  speed = speedVar.get()
  distance = distanceVar.get()
  cycles = cyclesVar.get()
  fwdCommand = "G0 F" + str(speed) + " X" + str(distance) + " \r\n"
  revCommand = "G0 F" + str(speed) + " X-" + str(distance) + " \r\n"
  print(fwdCommand)
  print(revCommand)
  
  for c in range(cycles):
    var.set(c+1)
    window.update()
    ser.write(fwdCommand.encode())
    print(ser.readline())
    
    time.sleep(0.1)
    ser.write(revCommand.encode())
    print(ser.readline())





goButton = tkinter.Button(text = "GO",
                          command = doIt).grid(row = 4, column=1)

window.mainloop()
