import ns_detector
import serial, keyboard
import threading, time

D = ns_detector.ns_detector()

def communicator():
    last = False
    portx = "COM7"
    bps = 9600
    timex = 0.1
    ser = serial.Serial(portx, bps, timeout=timex)
    while True:
        busy = ser.read().decode()
        if busy == "t":
            keyboard.press("home")
        elif busy == "f":
            keyboard.release("home")
        if D.RECV:
            if not last:
                ser.write("t\n".encode())
                last = True
        else:
            if last:
                ser.write("f\n".encode())
                last = False

def main():
    communication = threading.Thread(target=communicator, name="Communicator")
    communication.daemon = True
    communication.start()


main()