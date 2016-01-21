import serial
import time
import struct


ublox = serial.Serial('COM15',38400)
ublox.close()
ublox.open()

ubloxState = 0
inByte   = 0x00
summingByte = 0x00

sumRcvdA = 0x00
sumRcvdB = 0x00

sumCalcA = 0x00
sumCalcB = 0x00

def GetGPSByte():
    inList = ublox.read(1)
    gpsByte = struct.unpack('B',inList[0:1])
    return gpsByte[0]


while True:
    while ublox.inWaiting() > 0:
        if ubloxState == 0:#check first byte
            inByte = GetGPSByte()
            if inByte == 0xB5:
                ubloxState = 1    
            print "0"
        elif ubloxState == 1:#check second byte
            inByte = GetGPSByte()
            if inByte == 0x62:
                ubloxState = 2
            else:
                ubloxState = 0
            sumCalcA = 0x00
            sumCalcB = 0x00
            print "1"
        elif ubloxState == 2:#check message type
            inByte = GetGPSByte()
            sumCalcA += inByte
            sumCalcB += sumCalcA
            if inByte == 0x01:
                ubloxState = 3
            else:
                ubloxState = 0
            print "2"
        elif ubloxState == 3:#check message number
            inByte = GetGPSByte()
            sumCalcA += inByte
            sumCalcB += sumCalcA
            if inByte == 0x07:
                ubloxState = 4
            else:
                ubloxState = 0
            print "3"
        elif ubloxState == 4:#get packet length
            if ublox.inWaiting() >= 2:
                print "4"
                lengthList = ublox.read(2)
                packetLength = struct.unpack('H',lengthList[0:2])
                
                inByteList = struct.unpack('B',lengthList[0:1])
                sumCalcA += inByteList[0]
                sumCalcB += sumCalcA
                
                inByteList = struct.unpack('B',lengthList[1:2])
                sumCalcA += inByteList[0]
                sumCalcB += sumCalcA
                print(packetLength)
                if packetLength[0] == 92:
                    ubloxState = 5
                else:
                    ubloxState = 0
            
        elif ubloxState == 5:#get GPS packet
            print ublox.inWaiting()
            if ublox.inWaiting() >= 92:
                print "5"
                ubloxList = ublox.read(92)
                ubloxState = 6
            
        elif ubloxState == 6:#get first sum
            sumRcvdA = GetGPSByte()
            
            ubloxState = 7
            print "6"
        elif ubloxState == 7:#get second sum then generate and check
            sumRcvdB = GetGPSByte()
            for i in range(0,92):
                #print i
                summingByte = struct.unpack('B',ubloxList[i:i+1])
                print format(summingByte[0],'02x')
                sumCalcA += summingByte[0]
                sumCalcB += sumCalcA
            sumCalcA = sumCalcA & 0xFF
            sumCalcB = sumCalcB & 0xFF
            print (sumCalcA,sumCalcB,sumRcvdA,sumRcvdB)
            if (sumCalcA == sumRcvdA) and (sumCalcB == sumRcvdB):
                print "sums match"
                #print ubloxList
                #unpack the data from the list
                ubloxTouple = struct.unpack('LHBBBBBBLlBBBBllllLLlllllLLH',ubloxList[0:78])
                print ubloxTouple
            ubloxState = 0
            print "7"
            
#     while ublox.inWaiting() < 200:
#         print ublox.inWaiting()
#         time.sleep(0.05)
#     if ublox.inWaiting() > 0:
#         numBytes = ublox.inWaiting()
#         inList = ublox.read(1)
#         inByte = struct.unpack('B',inList[0:1])
#         print hex(inByte[0])

    #time.sleep(0.1)    
    
