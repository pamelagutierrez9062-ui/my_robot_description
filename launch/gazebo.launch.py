import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg_path = os.path.join(os.getcwd())
    xacro_file = os.path.join(pkg_path, 'urdf', 'robot.urdf.xacro')
    
    doc = xacro.process_file(xacro_file)
    robot_desc = doc.toxml()

    # Iniciar Gazebo Sim (mundo vacío)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # Publicar robot_description
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Nodo Spawner para meter el robot a Gazebo
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-string', robot_desc, '-name', 'my_robot'],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        rsp,
        spawn
    ])
