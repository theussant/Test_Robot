import launch
from launch_ros.actions import Node

def generate_launch_description():

    bl_teleop_pkg_share = FindPackageShare('baylittle_teleop').find('baylittle_teleop')

    joy_type = LaunchConfiguration('joy_type', default="generic")
    joystick_config = [TextSubstitution(text=os.path.join(bl_teleop_pkg_share, 'config', '')),
                        joy_type, TextSubstitution(text='_joystick.yaml')]

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='both',
        parameters=[{
        'deadzone': 0.05,
        'autorepeat_rate': 1.0,
        'sticky_buttons': False,
        'coalesce_interval_ms': 1
        }]
    )

    joy_teleop = Node(
        package='baylittle_teleop',
        executable='joy_teleop',
        name='joy_teleop_node',
        parameters=[joystick_config]
    )

    return launch.LaunchDescription([
        DeclareLaunchArgument(name='joy_type', default_value='generic',
                            description='Set the joystick type (generic, x360 or ps4)'),
        joy_node,
        TimerAction(period=3.0, actions=[joy_teleop])
    ])