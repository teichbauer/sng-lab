import struct

shared = {
    "AverageCurrent":   0,
    "AverageVoltage1":  0,
    "AverageVoltage2":  0,
    "AveragePressure1": 0,
    "AveragePressure2": 0,
    "SumCurrent":       0,
    "SumVoltage1":      0,
    "SumVoltage2":      0,
    "SumPressure1":     0,
    "SumPressure2":     0,
    "CntCurrent":       0,
    "CntVoltage1":      0,
    "CurrentEventId":   0,
    "LastFrameId":      0,
}

def msg_verifier(msg):
    info = {}
    errs = []
    # verify [0]
    if msg[0]!= 0x68:
        errs.append(f"invalid msg header (should be 0x68): {hex(msg[0])}")
    
    # verify [-1]
    if msg[-1] != 0x16:
        errs.append(f"invalid message end-byte(should be 0x16): {hex(msg[-1])}")
    
    # verify sum 
    data_length = len(msg) - 3
    sum = 0
    should_be_sum = msg[-2]
    for i in range(data_length):
        sum += msg[i]
    if msg[-2] != sum % 256:
        errs.append(f"check sum (should be{hex(should_be_sum)}): {hex(sum)}")
    
    # ?? why in server.py:211 msg[1 + msg[2]*256 ?? is it "small endian" ??
    info["data length"]     = struct.unpack('!H',msg[1:3])[0]
    info["control code"]    = msg[3]
    info["frame type"]      = msg[4]

    if len(errs) != 0:
        [print(msg) for msg in errs]
        return info, errs
    return info, None
    
class Averager:
    def __init__(self):
        self.init()

    def init(self):
        self.av_dic = {
            "current": [],
            "voltage1": [],
            "voltage2": [],
            "pressure1": [],
            "pressure2": [],
        }

    def add(self, name, value):
        self.av_dic[name].append(value)

    def get_av(self,name):
        return sum(self.av_dic[name]) / len(self.av_dic[name])