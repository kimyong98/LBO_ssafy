import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
from bluetooth import *

class BluetoothClientNode(Node):
    def __init__(self):
        super().__init__('bluetooth_client')
        self.sock = None
        self.buf_size = 1024

    def input_and_send(self):
        self.get_logger().info("Type something")
        while True:
            data = input()
            if len(data) == 0:
                break
            self.sock.send(data)
            self.sock.send("\n")

    def rx_and_echo(self):
        while True:
            data = self.sock.recv(self.buf_size)
            if data:
                self.get_logger().info(data.decode('utf-8'))

    def bluetooth_communication(self):
        # MAC address of ESP32
        addr = "08:D1:F9:D7:94:8A"
        service_matches = find_service(address=addr)

        if len(service_matches) == 0:
            self.get_logger().info("Couldn't find the SampleServer service =(")
            return

        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        port = 1  # Manually setting the port to 1
        self.get_logger().info("Connecting to \"%s\" on %s, port %s" % (name, host, port))

        # Create the client socket
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((host, port))

        self.get_logger().info("Connected")

        # Start threads for input and receiving
        input_thread = threading.Thread(target=self.input_and_send)
        rx_thread = threading.Thread(target=self.rx_and_echo)

        input_thread.start()
        rx_thread.start()

        input_thread.join()
        rx_thread.join()

        self.sock.close()
        self.get_logger().info("--- Bye ---")

def main(args=None):
    rclpy.init(args=args)
    bluetooth_client = BluetoothClientNode()
    bluetooth_client.bluetooth_communication()
    rclpy.spin(bluetooth_client)
    rclpy.shutdown()

if __name__ == '__main__':
    main()