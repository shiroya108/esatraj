from connection import Connection
import struct
import numpy as np
import quaternion

connection = Connection(type="COM", port="COM5", baud=9600)
connection.connect()
connection.send(b'esatraj_start')

connected = False
start = False
cur_p = np.array([0,0,0], dtype=float)
cur_q = quaternion.from_float_array([1,0,0,0])

while True:
    try:
        data_raw = connection.read(29)
        # print(data_raw)
        # if data_raw == b'esatraj_started':
        #     print('started')
        # else:
        # print(len(data_raw))
        data = struct.unpack('>sfffffff',data_raw)
        # print(data)

        if data[0] == b'c':
            print('connected')
            connected = True

        if not connected:
            continue

        if data[0] == b's':
            print('start') 
            cur_p = np.array([0,0,0], dtype=float)
            cur_q = quaternion.from_float_array([1,0,0,0])
            start = True
        elif data[0] == b'e':
            print('end')
            start = False 
        elif data[0] == b'r':
            print('reset') 
            break

        
        if not start:
            continue

        if data[0] == b'y' and len(data) >= 8:
            delta_p = np.array([data[1],data[2],data[3]])
            delta_q = np.array([data[4],data[5],data[6],data[7]])
            

            temp_dis = np.matmul(quaternion.as_rotation_matrix(cur_q), delta_p.T).T
            cur_p = cur_p + temp_dis
            cur_q = cur_q * quaternion.from_float_array(delta_q).normalized()
            print(cur_p,cur_q)

        # data_raw = self.serial.readline()
        #data = data_raw.decode()
        # print(data_raw)      


    except KeyboardInterrupt:
        connection.disconnect()
        break  
    except Exception as e:
        print(e)
        continue