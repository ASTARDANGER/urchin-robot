from setuptools import find_packages, setup

package_name = 'my_robot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/my_robot_description']),
        ('share/my_robot_description', ['package.xml']),
        ('share/my_robot_description/urdf', ['urdf/robot.urdf']),
        ('share/my_robot_description/meshes', ['meshes/base.stl', 'meshes/part_1.stl']),
        ('share/my_robot_description/world', ['world/world.world']),
        ('share/my_robot_description/launch', ['launch/display.launch.py', 'launch/gazebo.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bjouvelot',
    maintainer_email='bjouvelot@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
