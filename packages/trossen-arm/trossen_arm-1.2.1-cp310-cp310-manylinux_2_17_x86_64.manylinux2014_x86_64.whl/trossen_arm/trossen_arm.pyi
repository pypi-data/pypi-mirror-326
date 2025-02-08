"""
Trossen Arm Python Bindings
"""
from __future__ import annotations
import pybind11_stubgen.typing_ext
import typing
__all__ = ['EndEffectorProperties', 'IPMethod', 'JointInput', 'JointInputPosition', 'JointInputTorque', 'JointInputVelocity', 'JointOutput', 'LinkProperties', 'Mode', 'Model', 'StandardEndEffector', 'TrossenArmDriver']
class EndEffectorProperties:
    finger_left: LinkProperties
    finger_right: LinkProperties
    offset_finger_left: float
    offset_finger_right: float
    palm: LinkProperties
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class IPMethod:
    """
    Members:
    
      manual
    
      dhcp
    """
    __members__: typing.ClassVar[dict[str, IPMethod]]  # value = {'manual': <IPMethod.manual: 0>, 'dhcp': <IPMethod.dhcp: 1>}
    dhcp: typing.ClassVar[IPMethod]  # value = <IPMethod.dhcp: 1>
    manual: typing.ClassVar[IPMethod]  # value = <IPMethod.manual: 0>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class JointInput:
    mode: Mode
    position: JointInputPosition
    torque: JointInputTorque
    velocity: JointInputVelocity
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class JointInputPosition:
    desired_position: float
    feedforward_acceleration: float
    feedforward_velocity: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class JointInputTorque:
    desired_torque: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class JointInputVelocity:
    desired_velocity: float
    feedforward_acceleration: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class JointOutput:
    external_torque: float
    position: float
    torque: float
    velocity: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class LinkProperties:
    inertia: typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(9)]
    mass: float
    origin_rpy: typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]
    origin_xyz: typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class Mode:
    """
    Members:
    
      idle
    
      position
    
      velocity
    
      torque
    """
    __members__: typing.ClassVar[dict[str, Mode]]  # value = {'idle': <Mode.idle: 0>, 'position': <Mode.position: 1>, 'velocity': <Mode.velocity: 2>, 'torque': <Mode.torque: 3>}
    idle: typing.ClassVar[Mode]  # value = <Mode.idle: 0>
    position: typing.ClassVar[Mode]  # value = <Mode.position: 1>
    torque: typing.ClassVar[Mode]  # value = <Mode.torque: 3>
    velocity: typing.ClassVar[Mode]  # value = <Mode.velocity: 2>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Model:
    """
    Members:
    
      wxai_v0
    """
    __members__: typing.ClassVar[dict[str, Model]]  # value = {'wxai_v0': <Model.wxai_v0: 0>}
    wxai_v0: typing.ClassVar[Model]  # value = <Model.wxai_v0: 0>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class StandardEndEffector:
    wxai_v0_base: typing.ClassVar[EndEffectorProperties]  # value = <trossen_arm.trossen_arm.EndEffectorProperties object>
    wxai_v0_follower: typing.ClassVar[EndEffectorProperties]  # value = <trossen_arm.trossen_arm.EndEffectorProperties object>
    wxai_v0_leader: typing.ClassVar[EndEffectorProperties]  # value = <trossen_arm.trossen_arm.EndEffectorProperties object>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class TrossenArmDriver:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def cleanup(self) -> None:
        """
                @brief Cleanup the driver
        """
    def configure(self, model: Model, end_effector: EndEffectorProperties, serv_ip: str, clear_error: bool) -> None:
        """
                @brief Configure the driver
        
                @param model Model of the robot
                @param end_effector End effector properties
                @param serv_ip IP address of the robot
                @param clear_error Whether to clear the error state of the robot
        """
    def get_dns(self) -> str:
        """
                @brief Get the DNS
        
                @return DNS address
        """
    def get_end_effector(self) -> EndEffectorProperties:
        """
                @brief Get the end effector mass properties
        
                @return The end effector mass property structure
        """
    def get_error_information(self) -> str:
        """
                @brief Get the error information of the robot
        
                @return Error information
        """
    def get_external_torques(self) -> list[float]:
        """
                @brief Get the external torques of the robot joints
        
                @return External torques of the robot joints in Newton meters
        """
    def get_factory_reset_flag(self) -> bool:
        """
                @brief Get the factory reset flag
        
                @return true if the configurations will be reset to factory defaults at the next startup
                @return false if the configurations will not be reset to factory defaults at the next startup
        """
    def get_gateway(self) -> str:
        """
                @brief Get the gateway
        
                @return Gateway address
        """
    def get_ip_method(self) -> IPMethod:
        """
                @brief Get the IP method
        
                @return IP method
        """
    def get_manual_ip(self) -> str:
        """
                @brief Get the manual IP
        
                @return Manual IP address
        """
    def get_modes(self) -> list[Mode]:
        """
                @brief Get the modes of the robot
        
                @return Modes of the robot, a vector of Mode
        """
    def get_num_joints(self) -> int:
        """
                @brief Get the number of joints
        
                @return Number of joints
        """
    def get_positions(self) -> list[float]:
        """
                @brief Get the positions of the robot joints
        
                @return Positions of the robot joints in radians
        """
    def get_robot_output(self) -> list[JointOutput]:
        """
                @brief Get the robot output
        
                @return Robot output
        """
    def get_subnet(self) -> str:
        """
                @brief Get the subnet
        
                @return Subnet address
        """
    def get_torque_correction(self) -> list[float]:
        """
                @brief Get the torque correction
        
                @return Torque correction
        """
    def get_torques(self) -> list[float]:
        """
                @brief Get the torques of the robot joints
        
                @return Torques of the robot joints in Newton meters
        """
    def get_velocities(self) -> list[float]:
        """
                @brief Get the velocities of the robot joints
        
                @return Velocities of the robot joints in radians per second
        """
    def move_arm_to(self, goal_time: float, goal_positions: list[float], goal_velocities: list[float] | None = None, goal_accelerations: list[float] | None = None) -> None:
        """
                @brief Move the arm joints to the desired positions
        
                @param goal_time Time to reach the goal positions in seconds
                @param goal_positions Desired positions in radians
                @param goal_velocities Optional: desired velocities in radians per second
                @param goal_accelerations Optional: desired accelerations in radians per second squared
        
                @details It does the following:
                  1. Check the size of the vectors
                  2. Check the goal time
                  3. Construct a vector of quintic Hermite interpolators
                  4. Construct vectors for the robot input
                  5. Get the robot output
                  6. Compute the coefficients for the interpolators
                  7. Set arm mode to position
                  8. Move the arm joints along the trajectory
        
                @note The gripper input will not change
        """
    def receive_robot_output(self) -> bool:
        """
                @brief Receive the robot output
        
                @return true if the robot output was received successfully
                @return false if the robot output was not received successfully
        """
    def request_robot_output(self) -> None:
        """
                @brief Request the robot output
        """
    def reset_error_state(self) -> None:
        """
                @brief Reset the error state of the robot
        """
    def set_arm_mode(self, mode: Mode = ...) -> None:
        """
                @brief Set the mode of the arm joints
        
                @param mode Mode for the arm joints
        """
    def set_arm_positions(self, positions: list[float], feedforward_velocities: list[float] | None = None, feedforward_accelerations: list[float] | None = None) -> None:
        """
                @brief Set the positions of the arm joints
        
                @param positions Desired positions in radians
                @param feedforward_velocities Optional: feedforward velocities in radians per second
                @param feedforward_accelerations Optional: feedforward accelerations in radians per second
                  squared
        """
    def set_arm_torques(self, torques: list[float]) -> None:
        """
                @brief Set the torques of the arm joints
        
                @param torques Desired torques in Newton meters
        """
    def set_arm_velocities(self, velocities: list[float], feedforward_accelerations: list[float] | None = None) -> None:
        """
                @brief Set the velocities of the arm joints
        
                @param velocities Desired velocities in radians per second
                @param feedforward_accelerations Optional: feedforward accelerations in radians per second
                  squared
        """
    def set_dns(self, dns: str = '8.8.8.8') -> None:
        """
                @brief Set the DNS
        
                @param dns DNS address
        """
    def set_end_effector(self, end_effector: EndEffectorProperties) -> None:
        """
                @brief Set the end effector mass properties
        
                @param end_effector The end effector mass property structure
        """
    def set_factory_reset_flag(self, flag: bool = True) -> None:
        """
                @brief Set the factory reset flag
        
                @param flag true if the configurations will be reset to factory defaults at the next startup
                @param flag false if the configurations will not be reset to factory defaults at the next startup
        """
    def set_gateway(self, gateway: str = '192.168.1.1') -> None:
        """
                @brief Set the gateway
        
                @param gateway Gateway address
        """
    def set_gripper_mode(self, mode: Mode = ...) -> None:
        """
                @brief Set the mode of the gripper joints
        
                @param mode Mode for the gripper joints
        """
    def set_gripper_position(self, position: float, feedforward_velocity: float | None = None, feedforward_acceleration: float | None = None) -> None:
        """
                @brief Set the position of the gripper
        
                @param position Desired position in meters
                @param feedforward_velocity Optional: feedforward velocity in meters per second
                @param feedforward_acceleration Optional: feedforward acceleration in meters per second
                  squared
        """
    def set_gripper_torque(self, torque: float) -> None:
        """
                @brief Set the torque of the gripper
        
                @param torque Desired torque in Newton meters
        """
    def set_gripper_velocity(self, velocity: float, feedforward_acceleration: float | None = None) -> None:
        """
                @brief Set the velocity of the gripper
        
                @param velocity Desired velocity in meters per second
                @param feedforward_acceleration Optional: feedforward acceleration in meters per second
                  squared
        """
    def set_ip_method(self, method: IPMethod = ...) -> None:
        """
                @brief Set the IP method
        
                @param method IP method
        """
    def set_manual_ip(self, manual_ip: str = '192.168.1.2') -> None:
        """
                @brief Set the manual IP
        
                @param manual_ip Manual IP address
        """
    def set_mode(self, mode: Mode = ...) -> None:
        """
                @brief Set all joints to the same mode
        
                @param mode Mode for all joints
        """
    def set_modes(self, modes: list[Mode]) -> None:
        """
                @brief Set the modes of the robot
        
                @param modes Modes of the robot, a vector of Mode
        """
    def set_positions(self, positions: list[float], feedforward_velocities: list[float] | None = None, feedforward_accelerations: list[float] | None = None) -> None:
        """
                @brief Set the positions of the robot joints
        
                @param positions Desired positions in radians
                @param feedforward_velocities Optional: feedforward velocities in radians per second
                @param feedforward_accelerations Optional: feedforward accelerations in radians per second
                  squared
        """
    def set_robot_input(self, robot_input: list[JointInput]) -> None:
        """
                @brief Set the robot input
        
                @param robot_input Robot input
        """
    def set_subnet(self, subnet: str = '255.255.255.0') -> None:
        """
                @brief Set the subnet
        
                @param subnet Subnet address
        """
    def set_torque_correction(self, torque_correction: list[float]) -> None:
        """
                @brief Set the torque correction
        
                @param torque_correction Torque correction
        """
    def set_torques(self, torques: list[float]) -> None:
        """
                @brief Set the torques of the robot joints
        
                @param torques Desired torques in Newton meters
        """
    def set_velocities(self, velocities: list[float], feedforward_accelerations: list[float] | None = None) -> None:
        """
                @brief Set the velocities of the robot joints
        
                @param velocities Desired velocities in radians per second
                @param feedforward_accelerations Optional: feedforward accelerations in radians per second
                  squared
        """
