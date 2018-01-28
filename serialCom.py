# ==== Imports
import serial

# ==== Variables
ser = serial.Serial()

def connect(port):
    ser.port = port
    ser.baudrate = 9600
    ser.open()
    
    try:
        serin = ser.read()
            
        ser.write("8".encode())

        return True
    except:
        return False
        
def sendBraille(list):
    #⠠⠓⠑⠇⠇⠕⠀⠠⠸⠺
    #list = ['6', '1-2-5', '1-5', '1-2-3', '1-2-3', '1-3-5', '', '6', '4-5-6', '2-4-5-6']
    
    for l in list:
        parse = l.split('-')
        #print(parse)
        parse.append('0')
        
        for p in parse:
            ser.write(p.encode())
            #print(p)
            ser.read()
            
    ser.write('0'.encode())
    ser.write('9'.encode())    
        
if __name__ == "__main__":
    connect("COM5")
    sendBraille()