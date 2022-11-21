import serial
ser=serial.Serial(port='COM4',baudrate=9600,parity=serial.PARITY_NONE,\
                  stopbits=serial.STOPBITS_ONE,\
                  bytesize=serial.EIGHTBITS,\
                  )

while 1:
    if ser.readable():
        res=ser.readline()
        ready=res.decode()[:len(res)-2]
        ready=ready.split()
        print(ready[0],ready[1],ready[2])
        #judge=input()
        
