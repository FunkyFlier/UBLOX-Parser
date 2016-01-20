import serial
import time
import struct

ublox = serial.Serial('COM9',115200)
ublox.close()
ublox.open()
inByte = 0xAA
print format(inByte,'02x')
 
while True:
    #print ublox.inWaiting()
    if ublox.inWaiting() > 0:
        numBytes = ublox.inWaiting()
        print numBytes
        inList = ublox.read(1)
        #print type(inList)
        #print int(inList,16)
        inByte = struct.unpack('b',inList[0:1])
        print type(inByte[0])
        print hex(inByte[0])
        #restult = bytearray.fromhex(inList)
        #print format(inList[0],'02x')
        #inByte = inList.decode('hex')
        #format(inByte,'02x')
        #print format(inByte,'02x')
#         for i in range(0,numBytes):
#             inByte = ublox.read(1)
#             print format(inBye,'02x')
#       
    time.sleep(0.1)    