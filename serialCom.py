# ==== Imports
import serial

# ==== Variables

def connect(port):
    ser = serial.Serial(port, 9600)
    
    try:
        serin = ser.read()
            
        ser.write("1".encode())

        while ser.read() == '1':
            ser.read()
            
        return True
    except:
        return False
        
if __name__ == "__main__":
    connect("COM5")