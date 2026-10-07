import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class EKFExperiment(Node):

    def __init__(self):
        super().__init__('ekf_experiment_controller')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

    def publish_velocity(self, linear_x, angular_z, duration):
        msg = Twist()

        msg.linear.x = linear_x
        msg.angular.z = angular_z

        rate = 10.0
        dt = 1.0 / rate

        steps = int(duration * rate)

        for _ in range(steps):
            self.publisher.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(dt)

    def stop_robot(self, duration):
        self.publish_velocity(
            linear_x=0.0,
            angular_z=0.0,
            duration=duration
        )


def main():

    rclpy.init()

    node = EKFExperiment()

    print("")
    print("===================================")
    print("EKF experiment started")
    print("===================================")

    # --------------------------------------------------------
    # Phase 1: stationary
    # --------------------------------------------------------

    print("Phase 1: Stationary - 4 s")

    node.stop_robot(4.0)

    # --------------------------------------------------------
    # Phase 2: straight motion
    # --------------------------------------------------------

    print("Phase 2: Straight motion - 3 s")

    node.publish_velocity(
        linear_x=0.05,
        angular_z=0.0,
        duration=3.0
    )

    # --------------------------------------------------------
    # Phase 3: stationary
    # --------------------------------------------------------

    print("Phase 3: Stop - 4 s")

    node.stop_robot(4.0)

    # --------------------------------------------------------
    # Phase 4: rotation
    # --------------------------------------------------------

    print("Phase 4: Rotation - 3 s")

    node.publish_velocity(
        linear_x=0.0,
        angular_z=0.25,
        duration=3.0
    )

    # --------------------------------------------------------
    # Phase 5: stationary
    # --------------------------------------------------------

    print("Phase 5: Stop - 4 s")

    node.stop_robot(4.0)

    # --------------------------------------------------------
    # Phase 6: curved motion
    # --------------------------------------------------------

    print("Phase 6: Curved motion - 3 s")

    node.publish_velocity(
        linear_x=0.05,
        angular_z=0.20,
        duration=3.0
    )

    # --------------------------------------------------------
    # Phase 7: final stop
    # --------------------------------------------------------

    print("Phase 7: Final stop - 4 s")

    node.stop_robot(4.0)

    # Extra safety stop
    print("Sending final zero velocity commands...")

    node.stop_robot(2.0)

    print("")
    print("===================================")
    print("Experiment finished.")
    print("Robot should now be stopped.")
    print("===================================")

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()

