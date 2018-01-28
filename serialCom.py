# ==== Imports
import serial

# ==== Variables
ser = serial.Serial("COM5", 9600)


def connect(port):
    
    serin = ser.read()
        
    ser.write("1".encode())

    while ser.read() == '1':
        ser.read()
        
if __name__ == "__main__":
    connect("COM5")