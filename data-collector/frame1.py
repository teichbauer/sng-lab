import struct

class Frame1:
    def __init__(self,shared, averager):
        self.name = "current"
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

        self.dic["current sampling rate"] = struct.unpack('!H', msg[11:13])[0]
        self.dic["current count"] = struct.unpack('!H', msg[9:11])[0]
        ba = bytearray([
            0x68, 0x05, 0x00, 0x04, msg[6], msg[5], msg[8], msg[7],
            (0x68+0x05+0x00+0x04+msg[6]+msg[5]+msg[8]+msg[7])%256, 0x16
        ])
        self.dic["acknowledgement string"] = ba.hex()
        self.sendback = ba

        self.dic["current samples"] = []
        for i in range(self.dic["current count"]):
            self.dic["current samples"].append(
                struct.unpack('!H', msg[13+i*2:15+i*2])[0])
        self.dic["average current"] = \
            sum(self.dic["current samples"]) / self.dic["current count"]
        self.averager.add(self.name, self.dic["average current"])
        
        return self.dic

    def send_ack(self, cnn):
        cnn.send(self.sendback)

    def get_json_dic(self):
        return {
            "AVERAGECURRENT": self.averager.get_av(self.name)
        }

    def test(self):
        from pprint import pprint
        pprint(self.dic, indent=4)
        with open('../output_json/frame1.txt', 'w') as out:
            pprint(self.dic, stream=out)

if __name__ == '__main__':
    from common import shared
    from testdata import hexstring_list
    frame1 = Frame1(shared)
    frame1.parse(bytes.fromhex(hexstring_list.data[1]))
    frame1.test()

    x = 1
    



