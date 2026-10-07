import os
from glob import glob

from setuptools import setup


package_name = 'fishbot_description'


setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            os.path.join('share', package_name),
            ['package.xml'],
        ),
        (
            os.path.join('share', package_name, 'urdf'),
            glob('urdf/*.urdf'),
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py'),
        ),
        (
            os.path.join('share', package_name, 'world'),
            glob('world/*.world'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shi',
    maintainer_email='shi@example.com',
    description='Robot models and launch files for the FishBot learning project.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)