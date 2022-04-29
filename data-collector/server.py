import socket
import os
import math
import threading
import time
import datetime
from dict2bytes import decode_bytes
import pdb      # python debugger module pdb
from pprint import pprint

# global variable
global	g_uiSpotCnt
g_uiSpotCnt = 0

global	g_uiCurrentSpotCur
g_uiCurrentSpotCur = 0

global	g_uiCurrentSpotVolt1
g_uiCurrentSpotVolt1 = 0

global	g_uiCurrentSpotVolt2
g_uiCurrentSpotVolt2 = 0

global	g_uiCurrentSpotPress1
g_uiCurrentSpotPress1 = 0

global	g_uiCurrentSpotPress2
g_uiCurrentSpotPress2 = 0

global	g_uiSpotCur
g_uiSpotCur = []

global	g_uiSpotVolt1
g_uiSpotVolt1 = []  

global	g_uiSpotVolt2
g_uiSpotVolt2 = []

global	g_uiSpotPress1  
g_uiSpotPress1 = []

global	g_uiSpotPress2
g_uiSpotPress2 = []

global g_uiAverageCurrent
g_uiAverageCurrent = 0

global g_uiAverageVoltage1
g_uiAverageVoltage1 = 0

global g_uiAverageVoltage2
g_uiAverageVoltage2 = 0

global g_uiAveragePressure1
g_uiAveragePressure1 = 0

global g_uiAveragePressure2
g_uiAveragePressure2 = 0

global g_uiOldAverageCurrent
g_uiOldAverageCurrent = 0

global g_uiOldAverageVoltage1
g_uiOldAverageVoltage1 = 0

global g_uiOldAverageVoltage2
g_uiOldAverageVoltage2 = 0

global g_uiOldAveragePressure1
g_uiOldAveragePressure1 = 0

global g_uiOldAveragePressure2
g_uiOldAveragePressure2 = 0

global uiCntCurrent
uiCntCurrent = 0

global uiCntVoltage1
uiCntVoltage1 = 0

global uiCntVoltage2
uiCntVoltage2 = 0

global uiCntPressure1
uiCntPressure1 = 0

global uiCntPressure2
uiCntPressure2 = 0

global uiSumCurrent
uiSumCurrent = 0

global uiSumVoltage1
uiSumVoltage1 = 0

global uiSumVoltage2
uiSumVoltage2 = 0

global uiSumPressure1
uiSumPressure1 = 0

global uiSumPressure2
uiSumPressure2 = 0

global uiMaxCurrent
uiMaxCurrent = 0

global uiWholeSpotCount
uiWholeSpotCount = 0

global	uiDuration
uiDuration = 0

global dSpotTimeStamp
dSpotTimeStamp = 0

global dLastTimeStamp
dLastTimeStamp = 0

global g_strIP

global strFileName

global g_frameBase
g_frameBase = 1

global	uiTriggerThresholdCurrent
uiTriggerThresholdCurrent	= 1000
global	uiTriggerThresholdVoltage
uiTriggerThresholdVoltage	= 500
global	uiTriggerThresholdPressure1
uiTriggerThresholdPressure1 = 300
global	uiTriggerThresholdPressure2
uiTriggerThresholdPressure2 = 300

global   dAvgCurrent
dAvgCurrent = 0.0
global   dAvgVoltage1
dAvgVoltage1 = 0.0
global   dAvgVoltage2
dAvgVoltage2 = 0.0
global   dAvgPressure1
dAvgPressure1 = 0.0
global   dAvgPressure2
dAvgPressure2 = 0.0

global	g_uiCurrentEventId
g_uiCurrentEventId = 0

global    g_uiLastFrameId
g_uiLastFrameId = 0

# server listening on this port
PORT = 5050
SERVER = "139.24.167.26"
#SERVER = "10.0.0.3"
ADDR = (SERVER, PORT)

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(
    socket.AF_INET,         # socket family/category: IPv4
    socket.SOCK_STREAM      # type of socket
    )

server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg = conn.recv(1024)   # receive byte-array
        if msg:
#            pdb.set_trace()
#            now = datetime.datetime.now() 
            print('%s total byte length: %d'%(datetime.datetime.now(),len(msg)))           
            if len(msg) < 1024:
			
#                print(msg.hex(), sep=' ')
                print(msg.hex())
                s = 0
                while s < len(msg):
#                    print('BYTE[%04d] = 0x%02x'%(s,msg[s]))
                    s = s+1
                print('%s total received collector data %d bytes'%(datetime.datetime.now(),len(msg)))
				
                if msg[0] == 0x68:
                    print('%s received message header 0x%x'%(datetime.datetime.now(),msg[0]))
                else:
                    print('%s received invalid message header 0x%x, not 0x68'%(datetime.datetime.now(),msg[0]))
				
                if msg[len(msg)-1] == 0x16:
                    print('%s received message end 0x%x'%(datetime.datetime.now(),msg[len(msg)-1]))
                else:
                    print('%s Received invalid message end 0x%x, not 0x16'%(datetime.datetime.now(),msg[len(msg)-1]))				

                sum = 0
                for x in range(0,len(msg)-3):
                    sum = sum + msg[x]	

#                print('%s the sum of message: %d'%(datetime.datetime.now(),sum))
                print('%s the check sum: %d'%(datetime.datetime.now(),sum%256))	
                if msg[len(msg)-2] == sum%256:
                    print('%s the checksum and the value of checksum byte are same, both 0x%x'%(datetime.datetime.now(),msg[len(msg)-2]))
                else:
                    print('%s the checksum and the value of checksum byte are mismatch, one is 0x%02x and another is 0x%02x'%(datetime.datetime.now(),sum%256,msg[len(msg)-2]))		

                print('%s the data length: %d'%(datetime.datetime.now(),msg[1]+256*msg[2]))
                print('%s the control code: 0x%02x'%(datetime.datetime.now(),msg[3]))
                print('%s the frame type: 0x%02x '%(datetime.datetime.now(),msg[4]))
#                print('%s 0x00 - event description'%(datetime.datetime.now()))
#                print('%s 0x01 - spot current'%(datetime.datetime.now()))
#                print('%s 0x02 - spot voltage1'%(datetime.datetime.now()))
#                print('%s 0x03 - spot voltage2'%(datetime.datetime.now()))
#                print('%s 0x04 - spot pressure1'%(datetime.datetime.now()))
#                print('%s 0x05 - spot pressure2'%(datetime.datetime.now()))
					
                if msg[4] == 0:	
                    dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                    print('%s received spot event description message'%(datetime.datetime.now()))
                    time_stamp = datetime.datetime.now()
#                    print('%s received spot event description message: timestamp <%s>'%(datetime.datetime.now(),dt_ms))
                    global strFileName
                    strFileName = dt_ms 
                    f = open(strFileName+ ".json", "w")
                    f.write("[\n")
                    f1 = open(strFileName+"_current.json", "w")
                    f1.write("[\n")
                    f1.close()
                    f2 = open(strFileName+"_voltage1.json", "w")
                    f2.write("[\n")
                    f2.close()	
                    f3 = open(strFileName+"_voltage2.json", "w")
                    f3.write("[\n")
                    f3.close()	
                    f4 = open(strFileName+"_pressure1.json", "w")
                    f4.write("[\n")
                    f4.close()		
                    f5 = open(strFileName+"_pressure2.json", "w")
                    f5.write("[\n")
                    f5.close()
                    f.write("{\"receive time stamp\":\"" + str(time_stamp) + "\"},\n")
                    print('%s parsed spot time: %s %02d:%02d:%02d'%(datetime.datetime.now(),datetime.date.today(),msg[7]-int(msg[7]/16)*6,msg[6]-int(msg[6]/16)*6,msg[5]-int(msg[5]/16)*6))
                    spot_time = ("%s %02d:%02d:%02d")%(datetime.date.today(),msg[7]-int(msg[7]/16)*6,msg[6]-int(msg[6]/16)*6,msg[5]-int(msg[5]/16)*6)
                    f.write("{\"spot time\":\"" + str(spot_time) + "\"},\n")					
                    if msg[8] == 0:
                        print('%s parsed trigger type: %d - reserved'%(datetime.datetime.now(),msg[8]))
                    elif msg[8] == 1:
                        print('%s parsed trigger type: %d - current'%(datetime.datetime.now(),msg[8]))
                    elif msg[8] == 2:
                        print('%s parsed trigger type: %d - voltage1'%(datetime.datetime.now(),msg[8]))
                    elif msg[8] == 3:
                        print('%s parsed trigger type: %d - voltage2'%(datetime.datetime.now(),msg[8]))
                    elif msg[8] == 4:
                        print('%s parsed trigger type: %d - pressure1'%(datetime.datetime.now(),msg[8]))
                    elif msg[8] == 5:
                        print('%s parsed trigger type: %d - pressure2'%(datetime.datetime.now(),msg[8]))
                    trigger_type = ("%d")%(msg[8])
                    f.write("{\"trigger type\":\"" + str(trigger_type) + "\"},\n")
                    print('%s parsed spot duration: %d'%(datetime.datetime.now(),msg[9]*256+msg[10]))
                    spot_duration = ("%d")%(msg[9]*256+msg[10])
                    f.write("{\"spot duration\":\"" + str(spot_duration) + "\"},\n")
                    global g_frameBase
                    g_frameBase = msg[9] + math.ceil(msg[10]/256)
                    print('%s parsed frame base : %d'%(datetime.datetime.now(),g_frameBase))					
                    print('%s parsed event index: %d'%(datetime.datetime.now(),msg[11]*256+msg[12]))
                    event_index = ("%d")%(msg[11]*256+msg[12])
                    f.write("{\"event index\":\"" + str(event_index) + "\"},\n")
                    print('%s parsed frame id: %d'%(datetime.datetime.now(),msg[13]*256+msg[14]))
                    frame_id = ("%d")%(msg[13]*256+msg[14])
                    f.write("{\"frame id\":\"" + str(frame_id) + "\"},\n")
                    print('%s parsed sensor status: %d'%(datetime.datetime.now(),msg[15]*256+msg[16]))
                    sensor_status = ("%d")%(msg[15]*256+msg[16])
                    f.write("{\"sensor status\":\"" + str(sensor_status) + "\"},\n")
                    print('%s parsed inlet pressure: %d'%(datetime.datetime.now(),msg[17]*256+msg[18]))
                    inlet_pressure = ("%d")%(msg[17]*256+msg[18])
                    f.write("{\"inlet pressure\":\"" + str(inlet_pressure) + "\"},\n")
                    print('%s parsed return pressure: %d'%(datetime.datetime.now(),msg[19]*256+msg[20]))
                    return_pressure = ("%d")%(msg[19]*256+msg[20])
                    f.write("{\"return pressure\":\"" + str(return_pressure) + "\"},\n")
                    print('%s parsed water flow1: %.3f'%(datetime.datetime.now(),(msg[21]*256+msg[22])*0.001))
                    water_flow1 = ("%.3f")%((msg[21]*256+msg[22])*0.001)
                    f.write("{\"water flow1\":\"" + str(water_flow1) + "\"},\n")
                    print('%s parsed water flow2: %.3f'%(datetime.datetime.now(),(msg[23]*256+msg[24])*0.001))
                    water_flow2 = ("%.3f")%((msg[23]*256+msg[24])*0.001)
                    f.write("{\"water flow2\":\"" + str(water_flow2) + "\"},\n")
                    print('%s parsed water flow3: %.3f'%(datetime.datetime.now(),(msg[25]*256+msg[26])*0.001))
                    water_flow3 = ("%.3f")%((msg[25]*256+msg[26])*0.001)
                    f.write("{\"water flow3\":\"" + str(water_flow3) + "\"},\n")
                    print('%s parsed temperature1: %.1f'%(datetime.datetime.now(),(msg[27]*256+msg[28])*0.1))
                    temperature1 = ("%.1f")%((msg[27]*256+msg[28])*0.1)
                    f.write("{\"temperature1\":\"" + str(temperature1) + "\"},\n")
                    print('%s parsed temperature2: %.1f'%(datetime.datetime.now(),(msg[29]*256+msg[30])*0.1))
                    temperature2 = ("%.1f")%((msg[29]*256+msg[30])*0.1)
                    f.write("{\"temperature2\":\"" + str(temperature2) + "\"},\n")
                    print('%s parsed temperature3: %.1f'%(datetime.datetime.now(),(msg[31]*256+msg[32])*0.1))
                    temperature3 = ("%.1f")%((msg[31]*256+msg[32])*0.1)
                    f.write("{\"temperature3\":\"" + str(temperature3) + "\"},\n")
                    print('%s parsed temperature4: %.1f'%(datetime.datetime.now(),(msg[33]*256+msg[34])*0.1))
                    temperature4 = ("%.1f")%((msg[33]*256+msg[34])*0.1)
                    f.write("{\"temperature4\":\"" + str(temperature4) + "\"},\n")
                    print('%s parsed temperature5: %.1f'%(datetime.datetime.now(),(msg[35]*256+msg[36])*0.1))
                    temperature5 = ("%.1f")%((msg[35]*256+msg[36])*0.1)
                    f.write("{\"temperature5\":\"" + str(temperature5) + "\"},\n")
                    print('%s parsed temperature6: %.1f'%(datetime.datetime.now(),(msg[37]*256+msg[38])*0.1))
                    temperature6 = ("%.1f")%((msg[37]*256+msg[38])*0.1)
                    f.write("{\"temperature6\":\"" + str(temperature6) + "\"},\n")
                    print('%s parsed temperature7: %.1f'%(datetime.datetime.now(),(msg[39]*256+msg[40])*0.1))
                    temperature7 = ("%.1f")%((msg[39]*256+msg[40])*0.1)
                    f.write("{\"temperature7\":\"" + str(temperature7) + "\"},\n")
                    print('%s parsed temperature8: %.1f'%(datetime.datetime.now(),(msg[41]*256+msg[42])*0.1))
                    temperature8 = ("%.1f")%((msg[41]*256+msg[42])*0.1)
                    f.write("{\"temperature8\":\"" + str(temperature8) + "\"},\n")
                    print('%s parsed X axis angle: %.1f'%(datetime.datetime.now(),(msg[43]*256+msg[44])*0.1))
                    Xaxis_angle = ("%.1f")%((msg[43]*256+msg[44])*0.1)
                    f.write("{\"X axis angle\":\"" + str(Xaxis_angle) + "\"},\n")
                    print('%s parsed Y axis angle: %.1f'%(datetime.datetime.now(),(msg[45]*256+msg[46])*0.1))
                    Yaxis_angle = ("%.1f")%((msg[45]*256+msg[46])*0.1)
                    f.write("{\"Y axis angle\":\"" + str(Yaxis_angle) + "\"},\n")
                    print('%s parsed Z axis angle: %.1f'%(datetime.datetime.now(),(msg[47]*256+msg[48])*0.1))
                    Zaxis_angle = ("%.1f")%((msg[47]*256+msg[48])*0.1)
                    f.write("{\"Z axis angle\":\"" + str(Zaxis_angle) + "\"},\n")
                    print('%s parsed work piece id: %c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c'%(datetime.datetime.now(),msg[49],msg[50],msg[51],msg[52],msg[53],msg[54],msg[55],msg[56],msg[57],msg[58],msg[59],msg[60],msg[61],msg[62],msg[63],msg[64],msg[65],msg[66],msg[67],msg[68],msg[69],msg[70],msg[71],msg[72],msg[73],msg[74],msg[75],msg[76],msg[77],msg[78],msg[79],msg[80],msg[81],msg[82],msg[83],msg[84],msg[85],msg[86],msg[87],msg[88],msg[89],msg[90],msg[91],msg[92],msg[93],msg[94],msg[95],msg[96],msg[97],msg[98]))
                    work_piece = ("%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c")%(msg[49],msg[50],msg[51],msg[52],msg[53],msg[54],msg[55],msg[56],msg[57],msg[58],msg[59],msg[60],msg[61],msg[62],msg[63],msg[64],msg[65],msg[66],msg[67],msg[68],msg[69],msg[70],msg[71],msg[72],msg[73],msg[74],msg[75],msg[76],msg[77],msg[78],msg[79],msg[80],msg[81],msg[82],msg[83],msg[84],msg[85],msg[86],msg[87],msg[88],msg[89],msg[90],msg[91],msg[92],msg[93],msg[94],msg[95],msg[96],msg[97],msg[98])
                    f.write("{\"work piece\":\"" + str(work_piece) + "\"}\n]")
                    ack_list = [0x68, 0x05, 0x00, 0x04, msg[12], msg[11], msg[14], msg[13], (0x68+0x05+0x00+0x04+msg[12]+msg[11]+msg[14]+msg[13])%256, 0x16]
                    ack = ''.join(format(x, '02x') for x in ack_list)
                    print('%s the string of acknowledge: %s'%(datetime.datetime.now(),str(ack)))
                    ack_bytes = bytes.fromhex(ack)
                    conn.send(ack_bytes)
					
                    global g_uiAverageCurrent
                    g_uiAverageCurrent = 0

                    global g_uiAverageVoltage1
                    g_uiAverageVoltage1 = 0

                    global g_uiAverageVoltage2
                    g_uiAverageVoltage2 = 0

                    global g_uiAveragePressure1
                    g_uiAveragePressure1 = 0

                    global g_uiAveragePressure2
                    g_uiAveragePressure2 = 0
					
                    global uiSumCurrent
                    uiSumCurrent = 0

                    global uiSumVoltage1
                    uiSumVoltage1 = 0

                    global uiSumVoltage2
                    uiSumVoltage2 = 0

                    global uiSumPressure1
                    uiSumPressure1 = 0

                    global uiSumPressure2
                    uiSumPressure2 = 0		

                    global uiCntCurrent
                    uiCntCurrent = 0

                    global uiCntVoltage1
                    uiCntVoltage1 = 0

                    global uiCntVoltage2
                    uiCntVoltage2 = 0

                    global uiCntPressure1
                    uiCntPressure1 = 0

                    global uiCntPressure2
                    uiCntPressure2 = 0
					
                    global uiWholeSpotCount
                    uiWholeSpotCount = msg[9]*256+msg[10]	

                    global	g_uiCurrentEventId
                    g_uiCurrentEventId = msg[11]*256+msg[12]	

                    global    g_uiLastFrameId
                    g_uiLastFrameId = msg[13]*256+msg[14]
                    f.close()					

                if msg[4] == 1:
                    print('%s received spot current data message'%(datetime.datetime.now()))				
                    print('%s parsed spot event index 0x%x'%(datetime.datetime.now(),msg[5]*256+msg[6]))
                    print('%s the spot current telegram contains data count is <%d>'%(datetime.datetime.now(),msg[9]*256+msg[10]))
                    print('%s the spot current telegram sampling rate is <%d>'%(datetime.datetime.now(),msg[11]*256+msg[12]))
                    print('%s the old total of spot current array is <%d>'%(datetime.datetime.now(),uiCntCurrent))
#                    print('%s the current spot event index is <%d>'%(datetime.datetime.now(),g_uiCurrentEventId))					
                    f1 = open(strFileName+"_current.json", "a")

                    if(msg[5]*256+msg[6]) == g_uiCurrentEventId:
                        print('%s the event index of current frame <%d> is equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))
                    else:
                        print('%s the event index of current frame <%d> is not equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))

#                    global    g_uiLastFrameId						
                    if(msg[7]*256+msg[8]) == g_uiLastFrameId + 1:
                        print('%s the current frame <%d> is next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
                    else:
                        print('%s the current frame <%d> is not next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
					
                    g_uiLastFrameId = msg[7]*256+msg[8]

                    ack_list = [0x68, 0x05, 0x00, 0x04, msg[6], msg[5], msg[8], msg[7], (0x68+0x05+0x00+0x04+msg[6]+msg[5]+msg[8]+msg[7])%256, 0x16]
                    ack = ''.join(format(x, '02x') for x in ack_list)
                    print('%s the string of acknowledge: %s'%(datetime.datetime.now(),str(ack)))
                    ack_bytes = bytes.fromhex(ack)
                    conn.send(ack_bytes)
                   
                    for x in range(0,msg[9]*256+msg[10],1):
                        uiCntCurrent = uiCntCurrent + 1
                        uiSumCurrent = uiSumCurrent+msg[13+x]*256+msg[13+x+1]
                        spot_current = ("%d")%(msg[13+x]*256+msg[13+x+1])
                        if uiCntCurrent == uiWholeSpotCount or uiCntCurrent == (uiWholeSpotCount + 1):
                            f1.write("{\"current\":\"" + str(spot_current) + "\"}\n")
                        else:
                            f1.write("{\"current\":\"" + str(spot_current) + "\"},\n")
							
                    print('%s the current/total count <%d/%d> and current sum <%d>'%(datetime.datetime.now(),uiCntCurrent,uiWholeSpotCount,uiSumCurrent))		

                    f1.close()
						
                    if uiCntCurrent == uiWholeSpotCount or uiCntCurrent == (uiWholeSpotCount + 1) or (g_uiLastFrameId%g_frameBase == 0 and g_frameBase > 1):
                        g_uiAverageCurrent = int(uiSumCurrent/uiCntCurrent)
                        print('%s the average current <%d>'%(datetime.datetime.now(),g_uiAverageCurrent))		
                        f1 = open(strFileName+"_current.json", "a")
                        f1.write("]")
                        f1.close()

                if msg[4] == 2:
                    print('%s received spot voltage1 data message'%(datetime.datetime.now()))				
                    print('%s parsed spot event index 0x%x'%(datetime.datetime.now(),msg[5]*256+msg[6]))
                    print('%s the spot voltage1 telegram contains data count is <%d>'%(datetime.datetime.now(),msg[9]*256+msg[10]))
                    print('%s the spot voltage1 telegram sampling rate is <%d>'%(datetime.datetime.now(),msg[11]*256+msg[12]))
                    print('%s the old total of spot voltage1 array is <%d>'%(datetime.datetime.now(),uiCntVoltage1))
#                    print('%s the current spot event index is <%d>'%(datetime.datetime.now(),g_uiCurrentEventId))					
                    f2 = open(strFileName+"_voltage1.json", "a")					

                    if(msg[5]*256+msg[6]) == g_uiCurrentEventId:
                        print('%s the event index of current frame <%d> is equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))
                    else:
                        print('%s the event index of current frame <%d> is not equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))

#                    global    g_uiLastFrameId						
                    if(msg[7]*256+msg[8]) == g_uiLastFrameId + 1:
                        print('%s the current frame <%d> is next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
                    else:
                        print('%s the current frame <%d> is not next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
					
                    g_uiLastFrameId = msg[7]*256+msg[8]

                    ack_list = [0x68, 0x05, 0x00, 0x04, msg[6], msg[5], msg[8], msg[7], (0x68+0x05+0x00+0x04+msg[6]+msg[5]+msg[8]+msg[7])%256, 0x16]
                    ack = ''.join(format(x, '02x') for x in ack_list)
                    print('%s the string of acknowledge: %s'%(datetime.datetime.now(),str(ack)))
                    ack_bytes = bytes.fromhex(ack)
                    conn.send(ack_bytes)
                   
                    for x in range(0,msg[9]*256+msg[10],1):
                        uiCntVoltage1 = uiCntVoltage1 + 1
                        uiSumVoltage1 = uiSumVoltage1+msg[13+x]*256+msg[13+x+1]
                        spot_voltage1 = ("%d")%(msg[13+x]*256+msg[13+x+1])
                        if uiCntVoltage1 == uiWholeSpotCount or uiCntVoltage1 == (uiWholeSpotCount + 1):
                            f2.write("{\"voltage1\":\"" + str(spot_voltage1) + "\"}\n")
                        else:
                            f2.write("{\"voltage1\":\"" + str(spot_voltage1) + "\"},\n")

                    print('%s the current/total count <%d/%d> and current sum <%d>'%(datetime.datetime.now(),uiCntVoltage1,uiWholeSpotCount,uiSumVoltage1))		

                    f2.close()					
						
                    if uiCntVoltage1 == uiWholeSpotCount or uiCntVoltage1 == (uiWholeSpotCount + 1) or (g_uiLastFrameId%g_frameBase == 0 and g_frameBase > 1):
                        g_uiAverageVoltage1 = int(uiSumVoltage1/uiCntVoltage1)
                        print('%s the average voltage1 <%d>'%(datetime.datetime.now(),g_uiAverageVoltage1))			
                        f2 = open(strFileName+"_voltage1.json", "a")
                        f2.write("]")
                        f2.close()					
						

                if msg[4] == 3:
                    print('%s received spot voltage2 data message'%(datetime.datetime.now()))				
                    print('%s parsed spot event index 0x%x'%(datetime.datetime.now(),msg[5]*256+msg[6]))
                    print('%s the spot voltage2 telegram contains data count is <%d>'%(datetime.datetime.now(),msg[9]*256+msg[10]))
                    print('%s the spot voltage2 telegram sampling rate is <%d>'%(datetime.datetime.now(),msg[11]*256+msg[12]))
                    print('%s the old total of spot voltage2 array is <%d>'%(datetime.datetime.now(),uiCntVoltage2))
#                    print('%s the current spot event index is <%d>'%(datetime.datetime.now(),g_uiCurrentEventId))					
                    f3 = open(strFileName+"_voltage2.json", "a")					

                    if(msg[5]*256+msg[6]) == g_uiCurrentEventId:
                        print('%s the event index of current frame <%d> is equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))
                    else:
                        print('%s the event index of current frame <%d> is not equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))

#                    global    g_uiLastFrameId						
                    if(msg[7]*256+msg[8]) == g_uiLastFrameId + 1:
                        print('%s the current frame <%d> is next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
                    else:
                        print('%s the current frame <%d> is not next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
					
                    g_uiLastFrameId = msg[7]*256+msg[8]

                    ack_list = [0x68, 0x05, 0x00, 0x04, msg[6], msg[5], msg[8], msg[7], (0x68+0x05+0x00+0x04+msg[6]+msg[5]+msg[8]+msg[7])%256, 0x16]
                    ack = ''.join(format(x, '02x') for x in ack_list)
                    print('%s the string of acknowledge: %s'%(datetime.datetime.now(),str(ack)))
                    ack_bytes = bytes.fromhex(ack)
                    conn.send(ack_bytes)
                   
                    for x in range(0,msg[9]*256+msg[10],1):
                        uiCntVoltage2 = uiCntVoltage2 + 1
                        uiSumVoltage2 = uiSumVoltage2+msg[13+x]*256+msg[13+x+1]
                        spot_voltage2 = ("%d")%(msg[13+x]*256+msg[13+x+1])
                        if uiCntVoltage2 == uiWholeSpotCount or uiCntVoltage2 == (uiWholeSpotCount + 1):
                            f3.write("{\"voltage2\":\"" + str(spot_voltage2) + "\"}\n")
                        else:
                            f3.write("{\"voltage2\":\"" + str(spot_voltage2) + "\"},\n")

                    print('%s the current/total count <%d/%d> and current sum <%d>'%(datetime.datetime.now(),uiCntVoltage2,uiWholeSpotCount,uiSumVoltage2))			

                    f3.close()					
						
                    if uiCntVoltage2 == uiWholeSpotCount or uiCntVoltage2 == (uiWholeSpotCount + 1) or (g_uiLastFrameId%g_frameBase == 0 and g_frameBase > 1):
                        g_uiAverageVoltage2 = int(uiSumVoltage2/uiCntVoltage2)
                        print('%s the average voltage2 <%d>'%(datetime.datetime.now(),g_uiAverageVoltage2))			
                        f3 = open(strFileName+"_voltage2.json", "a")
                        f3.write("]")
                        f3.close()					

                if msg[4] == 4:
                    print('%s received spot pressure1 data message'%(datetime.datetime.now()))				
                    print('%s parsed spot event index 0x%x'%(datetime.datetime.now(),msg[5]*256+msg[6]))
                    print('%s the spot pressure1 telegram contains data count is <%d>'%(datetime.datetime.now(),msg[9]*256+msg[10]))
                    print('%s the spot pressure1 telegram sampling rate is <%d>'%(datetime.datetime.now(),msg[11]*256+msg[12]))
                    print('%s the old total of spot pressure1 array is <%d>'%(datetime.datetime.now(),uiCntPressure1))
#                    print('%s the current spot event index is <%d>'%(datetime.datetime.now(),g_uiCurrentEventId))						
                    f4 = open(strFileName+"_pressure1.json", "a")				

                    if(msg[5]*256+msg[6]) == g_uiCurrentEventId:
                        print('%s the event index of current frame <%d> is equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))
                    else:
                        print('%s the event index of current frame <%d> is not equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))

#                    global    g_uiLastFrameId						
                    if(msg[7]*256+msg[8]) == g_uiLastFrameId + 1:
                        print('%s the current frame <%d> is next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
                    else:
                        print('%s the current frame <%d> is not next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
					
                    g_uiLastFrameId = msg[7]*256+msg[8]

                    ack_list = [0x68, 0x05, 0x00, 0x04, msg[6], msg[5], msg[8], msg[7], (0x68+0x05+0x00+0x04+msg[6]+msg[5]+msg[8]+msg[7])%256, 0x16]
                    ack = ''.join(format(x, '02x') for x in ack_list)
                    print('%s the string of acknowledge: %s'%(datetime.datetime.now(),str(ack)))
                    ack_bytes = bytes.fromhex(ack)
                    conn.send(ack_bytes)
                   
                    for x in range(0,msg[9]*256+msg[10],1):
                        uiCntPressure1 = uiCntPressure1 + 1
                        uiSumPressure1 = uiSumPressure1+msg[13+x]*256+msg[13+x+1]
                        spot_pressure1 = ("%d")%(msg[13+x]*256+msg[13+x+1])
                        if uiCntPressure1 == uiWholeSpotCount or uiCntPressure1 == (uiWholeSpotCount + 1):
                            f4.write("{\"pressure1\":\"" + str(spot_pressure1) + "\"}\n")
                        else:
                            f4.write("{\"pressure1\":\"" + str(spot_pressure1) + "\"},\n")

                    print('%s the current/total count <%d/%d> and current sum <%d>'%(datetime.datetime.now(),uiCntPressure1,uiWholeSpotCount,uiSumPressure1))			

                    f4.close()											
						
                    if uiCntPressure1 == uiWholeSpotCount or uiCntPressure1 == (uiWholeSpotCount + 1):
                        g_uiAveragePressure1 = int(uiSumPressure1/uiCntPressure1)
                        print('%s the average pressure1 <%d>'%(datetime.datetime.now(),g_uiAveragePressure1))			
                        f4 = open(strFileName+"_pressure1.json", "a")
                        f4.write("]")
                        f4.close()						


                if msg[4] == 5:
                    print('%s received spot pressure2 data message'%(datetime.datetime.now()))				
                    print('%s parsed spot event index 0x%x'%(datetime.datetime.now(),msg[5]*256+msg[6]))
                    print('%s the spot pressure2 telegram contains data count is <%d>'%(datetime.datetime.now(),msg[9]*256+msg[10]))
                    print('%s the spot pressure2 telegram sampling rate is <%d>'%(datetime.datetime.now(),msg[11]*256+msg[12]))
                    print('%s the old total of spot pressure2 array is <%d>'%(datetime.datetime.now(),uiCntPressure2))
#                    print('%s the current spot event index is <%d>'%(datetime.datetime.now(),g_uiCurrentEventId))							
                    f5 = open(strFileName+"_pressure2.json", "a")								

                    if(msg[5]*256+msg[6]) == g_uiCurrentEventId:
                        print('%s the event index of current frame <%d> is equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))
                    else:
                        print('%s the event index of current frame <%d> is not equal to current event index <%d>'%(datetime.datetime.now(),msg[5]*256+msg[6],g_uiCurrentEventId))

#                    global    g_uiLastFrameId						
                    if(msg[7]*256+msg[8]) == g_uiLastFrameId + 1:
                        print('%s the current frame <%d> is next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
                    else:
                        print('%s the current frame <%d> is not next to last frame <%d>'%(datetime.datetime.now(),msg[7]*256+msg[8],g_uiLastFrameId))
					
                    g_uiLastFrameId = msg[7]*256+msg[8]

                    ack_list = [0x68, 0x05, 0x00, 0x04, msg[6], msg[5], msg[8], msg[7], (0x68+0x05+0x00+0x04+msg[6]+msg[5]+msg[8]+msg[7])%256, 0x16]
                    ack = ''.join(format(x, '02x') for x in ack_list)
                    print('%s the string of acknowledge: %s'%(datetime.datetime.now(),str(ack)))
                    ack_bytes = bytes.fromhex(ack)
                    conn.send(ack_bytes)
                   
                    for x in range(0,msg[9]*256+msg[10],1):
                        uiCntPressure2 = uiCntPressure2 + 1
                        uiSumPressure2 = uiSumPressure2+msg[13+x]*256+msg[13+x+1]
                        spot_pressure2 = ("%d")%(msg[13+x]*256+msg[13+x+1])
                        if uiCntPressure2 == uiWholeSpotCount or uiCntPressure2 == (uiWholeSpotCount + 1):
                            f5.write("{\"pressure2\":\"" + str(spot_pressure2) + "\"}\n")
                        else:
                            f5.write("{\"pressure2\":\"" + str(spot_pressure2) + "\"},\n")

                    print('%s the current/total count <%d/%d> and current sum <%d>'%(datetime.datetime.now(),uiCntPressure2,uiWholeSpotCount,uiSumPressure2))			

                    f5.close()						
						
                    if uiCntPressure2 == uiWholeSpotCount or uiCntPressure2 == (uiWholeSpotCount + 1) or (g_uiLastFrameId%g_frameBase == 0 and g_frameBase > 1):
                        g_uiAveragePressure2 = int(uiSumPressure2/uiCntPressure2)
                        print('%s the average pressure2 <%d>'%(datetime.datetime.now(),g_uiAveragePressure2))			
                        f5 = open(strFileName+"_pressure2.json", "a")
                        f5.write("]")
                        f5.close()							
						
#                decoded_msg = msg.decode(FORMAT)
#                print(decoded_msg)
#                if decoded_msg == DISCONNECT_MESSAGE:
#                    connected = False
            else:
#                dic_obj = decode_bytes(msg)
#                print(f"[{addr}]:")
#                pprint(dic_obj)
                print()

                # save data into a file under ./datafiles/
#                timestamp_str = dic_obj["time-stamp"].strip()
#                timestamp_str = timestamp_str[0:10] + '-' + timestamp_str[-4:]
#                fname =  timestamp_str + ".txt"
#                with open(fname, 'w') as outfile:
#                    pprint(dic_obj, outfile)

#                conn.send(str(dic_obj).encode())
                print("aknowledgement sent.")
    conn.close()

def start():
    server.listen(1)
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()    # wait for a new connection to come
        thread = threading.Thread(
            target=handle_client, 
            args = (conn, addr)
        )
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

        # for testing purpose
        # in real server, we will never call join() and break
        thread.join()
        print(f"[STOPPED]")
        break

print("[STARTING] server is starting...")
start()



