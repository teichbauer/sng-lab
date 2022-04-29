import struct
from datetime import datetime

sample_dict = {
    # time-stamp: "2021-11-06T14:38:20.669602"  varchar(30)         0 >[0:30]
    "info1": "what's going on?",                # varchar(30)       1 >[30:60]
    "int-value1": 243,                          # 4                 2 >[60:64]
    "info2": "nothing is going. That's all",    # varchar(30)       3 >[64:94]
    "float-value1": 23.456,                     # 4                 4 >[94:98]
    "int-value2": 1243,                         # 4                 5 >[98:102]
    "info3": "This is the best of all things",  # varchar(30)       6 >[102:132]
    "float-value2": 123.456,                    # 4                 7 >[132:136]
    "int-value3": 2430,                         # 4                 8 >[136:140]
    "info4": "nothing is going. That's all." * 2, # varchar(60)     9 >[140:200]
    "double-value1": 23.4560098,                # 8                10 >[200:208]
    "int-value4": 987654321,                    # 4                11 >[208:212]
    "info5": "That's all",                      # varchar(20)      12 >[212:232]
    "double-value2": 230997.456                 # 8                13 >[232:240]
    #-------------------------------------------total: 14 fields ------
    #                              total size:    240 byte long
}
keytuple_list = [
# -- data-type, 'key-name,    (starting,ending)  # position (total:14)
    ('utf-8',   'time-stamp',   (0,30)),         # 0
    ('utf-8',   'info1',        (30, 60)),       # 1
    ('int',     'int-value1',   (60, 64)),       # 2
    ('utf-8',   'info2',        (64, 94)),       # 3
    ('float',   'float-value1', (94, 98)),       # 4
    ('int',     'int-value2',   (98, 102)),      # 5
    ('utf-8',   'info3',        (102, 132)),     # 6
    ('float',   'float-value2', (132, 136)),     # 7
    ('int',     'int-value3',   (136, 140)),     # 8
    ('utf-8',   'info4',        (140, 200)),     # 9
    ('double',  'double-value1',(200, 208)),     # 10
    ('int',     'int-value4',   (208, 212)),     # 11
    ('utf-8',   'info5',        (212, 232)),     # 12
    ('double',  'double-value2',(232, 240))      # 13
]  

def make_bytes():
    sample_dict["time-stamp"] = datetime.now().isoformat()

    byte_array = bytearray(240) # reserve 240 byte-long data-space
    # -0---------  time-stamp: 30 varchar --------------------
    # add time-stamp for 30 chars
    # string-msg: right-padded to be 30 char-long
    msg = sample_dict['time-stamp'].ljust(30)  # info left-justified
    # encode it to 30 bytes
    byte_array[0:30] = msg.encode('utf-8')

    # -1---------  info1: 30 varchar --------------------
    msg = sample_dict["info1"].ljust(30)
    byte_array[30:60] = msg.encode('utf-8')

    # -2---------  int-value1: 4 bytes long --------------------
    byte_array[60:64] = sample_dict["int-value1"].to_bytes(4,'little')

    # -3---------  info2: 30 varchar --------------------
    msg = sample_dict["info2"].ljust(30)
    byte_array[64:94] = msg.encode('utf-8')

    # -4---------  float-value1: 4 bytes long --------------------
    byte_array[94:98] = struct.pack('f',sample_dict["float-value1"])

    # -5---------  int-value2: 4 bytes long --------------------
    byte_array[98:102] = sample_dict["int-value2"].to_bytes(4, 'little')

    # -6---------  info3: 30 varchar --------------------
    msg = sample_dict["info3"].ljust(30)
    byte_array[102:132] = msg.encode('utf-8')

    # -7---------  float-value2: 4 bytes long --------------------
    byte_array[132:136] = struct.pack('f',sample_dict["float-value2"])

    # -8---------  int-value3: 4 bytes long --------------------
    byte_array[136:140] = sample_dict["int-value3"].to_bytes(4, 'little')

    # -9---------  info4: 60 varchar --------------------
    msg = sample_dict["info4"].ljust(60)
    byte_array[140:200] = msg.encode('utf-8')

    # -10---------  double-value1: 8 bytes long --------------------
    byte_array[200:208] = struct.pack('d', sample_dict["double-value1"])

    # -11---------  int-value4: 4 bytes long --------------------
    byte_array[208:212] = sample_dict["int-value4"].to_bytes(4,'little')

    # -12---------  info5: 60 varchar --------------------
    msg = sample_dict["info5"].ljust(20)
    byte_array[212:232] = msg.encode('utf-8')

    # -13---------  double-value2: 8 bytes long --------------------
    byte_array[232:240] = struct.pack('d', sample_dict["double-value2"])

    return byte_array

def decode_bytes(bytes):
    dic = {}
    for tup in keytuple_list:
        p0 = tup[2][0]
        p1 = tup[2][1]

        if tup[0] == 'utf-8':
            dic[tup[1]] = bytes[p0:p1].decode('utf-8')
        elif tup[0] == 'int':
            dic[tup[1]] = int.from_bytes(bytes[p0:p1],'little')
        elif tup[0] == 'float':
            fvalues = struct.unpack('f', bytes[p0:p1])  
            # fvalues is a tuple(<value>,) with only 1 value in it
            dic[tup[1]] = fvalues[0]
        elif tup[0] == 'double':
            dvalues = struct.unpack('d', bytes[p0:p1])
            # dvalues is a tuple(<value>,) with only 1 value in it
            dic[tup[1]] = dvalues[0]
        else:
            raise Exception("wrong type!")
    return dic

