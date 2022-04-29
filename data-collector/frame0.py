from datetime import datetime
import struct


class Frame0:
    def __init__(self, shared):
        self.name = "event description"
        self.shared = shared
        self.dic = { 'spot time': datetime.now().isoformat() }

    def collect_shared(self, msg):
        # get shared.frameBase (?? never used? didn't appeared in logs.txt ??)
        # ------------------------------------------------------
        # originally done with:  msg[9] + math.ceil(msg[10]/256)
        self.shared["frameBase"] = msg[9] + int(bool(msg[10]))

        # get WholeSpotCount : msg[9]*256+msg[10]
        self.shared["WholeSpotCount"] = struct.unpack('!H', msg[9:11])[0]

        # get CurrentEventId : msg[11]*256+msg[12]
        self.shared["CurrentEventId"] = struct.unpack('!H', msg[11:13])[0]

        # get LastFrameId : msg[13]*256+msg[14]
        self.shared["LastFrameId"] = struct.unpack('!H', msg[13:15])[0]


    def parse(self, msg):
        self.collect_shared(msg)

        # get trigger type
        trggr_type = msg[8]
        self.dic["trigger type"] = f"{trggr_type}: event description"
        
        # get spot duration
        spot_duration = struct.unpack('!H', msg[9:11])[0] # msg[9]*256+msg[10]
        self.dic["spot duration"] = f"{spot_duration}"

        # get event index (msg[11]*256+msg[12])
        self.dic["event index"] = struct.unpack('!H', msg[11:13])[0]

        # get frame id (msg[13]*256+msg[14])
        self.dic["frame id"] = struct.unpack('!H', msg[13:15])[0]
        
        # get sensor status (msg[15]*256+msg[16])
        self.dic["sensor status"] = struct.unpack('!H', msg[15:17])[0]

        # get inlet pressure (msg[17]*256+msg[18])
        self.dic["inlet pressure"] = struct.unpack('!H',msg[17:19])[0]

        # get return pressure (msg[19]*256+msg[20])
        self.dic["return pressure"] = struct.unpack('!H',msg[19:21])[0]

        # get water flow1 : (msg[21]*256+msg[22])*0.001
        self.dic["water flow1"] = struct.unpack('!H',msg[21:23])[0] * 0.001
        
        # get water flow2 : (msg[23]*256+msg[24])*0.001
        self.dic["water flow2"] = struct.unpack('!H',msg[23:25])[0] * 0.001
        
        # get water flow3 : (msg[25]*256+msg[26])*0.001
        self.dic["water flow3"] = struct.unpack('!H',msg[25:27])[0] * 0.001

        # get temperature1 : (msg[27]*256+msg[28])*0.1
        self.dic["temperature1"] = struct.unpack('!H',msg[27:29])[0] * 0.1

        # get temperature2 : (msg[29]*256+msg[30])*0.1
        self.dic["temperature2"] = struct.unpack('!H',msg[29:31])[0] * 0.1

        # get temperature3 : (msg[31]*256+msg[32])*0.1
        self.dic["temperature3"] = struct.unpack('!H',msg[31:33])[0] * 0.1

        # get temperature4 : (msg[33]*256+msg[34])*0.1
        self.dic["temperature4"] = struct.unpack('!H',msg[33:35])[0] * 0.1

        # get temperature5 : (msg[35]*256+msg[36])*0.1
        self.dic["temperature5"] = struct.unpack('!H',msg[35:37])[0] * 0.1

        # get temperature6 : (msg[37]*256+msg[38])*0.1
        self.dic["temperature6"] = struct.unpack('!H',msg[37:39])[0] * 0.1

        # get temperature7 : (msg[39]*256+msg[40])*0.1
        self.dic["temperature7"] = struct.unpack('!H',msg[39:41])[0] * 0.1

        # get temperature8 : (msg[41]*256+msg[42])*0.1
        self.dic["temperature8"] = struct.unpack('!H',msg[41:43])[0] * 0.1

        # get X axis angle : (msg[43]*256+msg[44])*0.1
        self.dic["X axis angle"] = struct.unpack('!H',msg[43:45])[0] * 0.1

        # get Y axis angle : (msg[45]*256+msg[46])*0.1
        self.dic["Y axis angle"] = struct.unpack('!H',msg[45:47])[0] * 0.1

        # get Z axis angle : (msg[47]*256+msg[48])*0.1
        self.dic["Z axis angle"] = struct.unpack('!H',msg[47:49])[0] * 0.1

        # get work piece (id)
        self.dic["work piece"] = msg[49:99].decode("utf-8")

        self.shared["WholeSpotCount"] = spot_duration
        self.shared["CurrentEventId"] = self.dic["event index"]
        self.shared["LastFrameId"] = self.dic["frame id"]

        # compose acknowledgement message
        ba = bytearray([
            0x68,0x05, 0x00, 0x04, msg[12], msg[11], msg[14], msg[13],
            (0x68+0x05+0x00+0x04+msg[12]+msg[11]+msg[14]+msg[13])%256, 0x16
        ])
        self.dic["acknowledgement string"] = ba.hex()
        self.sendback = ba

        return self.dic


    def send_ack(self, cnn):
        cnn.send(self.sendback)

    def get_json_dic(self):
        dic = {}
        dic["CREATETIME"]       = 1234567.123   # ??
        dic["SPOTINDEX"]        = 1234567       # ??
        dic["SENSORINFO"]       = self.dic["sensor status"]
        dic["ID"]               = self.dic["event index"]
        dic["SPOTTIME"]         = self.dic["spot time"][:19]
        dic["TRIIGERTYPE"]      = self.dic["trigger type"][0]
        dic["DURATION"]         = int(self.dic["spot duration"])
        dic["INLETPRESSURE"]    = int(self.dic["inlet pressure"])
        dic["BACKPRESSURE"]     = int(self.dic["return pressure"])
        dic["WATERFLOW1"]       = float(self.dic["water flow1"])
        dic["WATERFLOW2"]       = float(self.dic["water flow1"])
        dic["WATERFLOW3"]       = float(self.dic["water flow1"])
        dic["TEMPERATURE1"]     = float(self.dic["temperature1"])
        dic["TEMPERATURE2"]     = float(self.dic["temperature2"])
        dic["TEMPERATURE3"]     = float(self.dic["temperature3"])
        dic["TEMPERATURE4"]     = float(self.dic["temperature4"])
        dic["TEMPERATURE5"]     = float(self.dic["temperature5"])
        dic["TEMPERATURE6"]     = float(self.dic["temperature6"])
        dic["TEMPERATURE7"]     = float(self.dic["temperature7"])
        dic["TEMPERATURE8"]     = float(self.dic["temperature8"])
        dic["XAXISANGLE"]       = float(self.dic["X axis angle"])
        dic["YAXISANGLE"]       = float(self.dic["Y axis angle"])
        dic["ZAXISANGLE"]       = float(self.dic["Z axis angle"])
        dic["SEQUENCEID"]       = self.dic["frame id"]
        dic["POWER"]            = 123.123   # ??
        dic["WORKPIECEID"]      = self.dic["work piece"]
        dic["COLLECTORIP"]      = "12.13.14.15" # ??

        return dic

    def test(self):
        from pprint import pprint
        pprint(self.dic, indent=4)
        with open('../output_json/frame0.txt', 'w') as out:
            pprint(self.dic, stream=out)

if __name__ == "__main__":
    from testdata import hexstring_list
    from common import shared
    frame0 = Frame0(shared)
    frame0.parse(bytes.fromhex(hexstring_list.data[0]))
    frame0.test()
    x = 1
