from serial import Serial
import bluetooth

class Connection():
    type = 0
    address=""
    port = ""

    def __init__(self, type="COM", address="", port="", baud=9600):
        self.type = type
        self.adddress = address
        self.port = port
        self.baud = baud

    def connect(self):
        if self.type == "COM": # use serial
            self.serial = Serial(self.port, self.baud)
        elif self.type == "MAC":  # use bluez
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((self.adddress, int(self.port)))

    
    def send(self,bytes):
        if self.type == "COM": # use serial
            self.serial.write(bytes)
        elif self.type == "MAC":  # use bluez
            self.socket.send(bytes)

    def read(self,size=1024):
        if self.type == "COM": # use serial
            bytes = self.serial.read(size)
            # bytes = self.serial.readline()
            return bytes
        elif self.type == "MAC":  # use bluez
            bytes = self.socket.recv(size)
            return bytes
        
    def disconnect(self):
        if self.type == "COM": # use serial
            self.serial.close()
        elif self.type == "MAC":  # use bluez
            self.socket.close()