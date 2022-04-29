import struct

class Frame2:
    def __init__(self,shared, averager):
        self.name = "voltage1"
        self.errs = []
        self.shared = shared
        self.dic = {}
        self.averager = averager

    def collect_shared(self, msg):
        event_id = struct.unpack('!H', msg[5:7])[0]
        if event_id != self.shared["CurrentEventId"]:
            err = f"the event index of current frame {event_id} is not equal to" 
            err += f" current event index: {self.shared['CurrentEventId']}"
            self.errs.append(err)
        # check last-frame-id, set it to shared
        last_frame_id = struct.unpack('!H', msg[7:9])[0]
        if last_frame_id != self.shared["LastFrameId"] + 1:
            err = f"the current frame {last_frame_id} is not next to last frame"
            self.errs.append(err)
        self.shared["LastFrameId"] = last_frame_id


    def parse(self, msg):
        self.collect_shared(msg)

        ba = bytearray([
            0x68, 0x05, 0x00, 0x04, msg[6], msg[5], msg[8], msg[7],
            (0x68+0x05+0x00+0x04+msg[6]+msg[5]+msg[8]+msg[7])%256, 0x16
        ])
        self.dic["acknowledgement string"] = ba.hex()
        self.sendback = ba

        self.dic["voltage1 samples"] = []
        self.dic["voltage1 count"] = struct.unpack('!H',msg[9:11])[0]
        for i in range(self.dic["voltage1 count"]):
            self.dic["voltage1 samples"].append(
                struct.unpack('!H', msg[13+i*2:15+i*2])[0])
        self.dic["average voltage1"] = \
            sum(self.dic["voltage1 samples"]) / self.dic["voltage1 count"]
        self.averager.add(self.name, self.dic["average voltage1"])

        return self.dic

    def send_ack(self, cnn):
        cnn.send(self.sendback)

    def get_json_dic(self):
        return {
            "AVERAGEVOLTAGE1": self.averager.get_av(self.name)
        }


    def test(self):
        from pprint import pprint
        pprint(self.dic, indent=4)
        with open('../output_json/frame2.txt', 'w') as out:
            pprint(self.dic, stream=out)
        
if __name__ == '__main__':
    from common import shared
    from testdata import hexstring_list
    frame2 = Frame2(shared)
    frame2.parse(bytes.fromhex(hexstring_list.data[2]))
    frame2.test()

    x = 1

