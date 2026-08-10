from tutorial_interfaces.srv import AddThreeInts

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import sys


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddThreeInts, 'add_three_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddThreeInts.Request()

    def send_request(self, a, b, c):
        self.req.a = a
        self.req.b = b
        self.req.c = c
        return self.cli.call_async(self.req)


def main(args=None):
    try:
        with rclpy.init(args=args):
            minimal_client = MinimalClientAsync()
            a = int(sys.argv[1])
            b = int(sys.argv[2])
            c = int(sys.argv[3])
            future = minimal_client.send_request(a,b,c)
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()
            minimal_client.get_logger().info(
                'Result of add_three_ints: for %d + %d + %d = %d' %
                (minimal_client.req.a, minimal_client.req.b, minimal_client.req.c, response.sum))
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
