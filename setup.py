from setuptools import setup

long_description = '''
hr-little-api is the Python API for controlling Hanson Robotics consumer robots:
you can make your robot speak, walk and animate!

Read the documentation here: https://github.com/hansonrobotics/hr-little-api

hr-little-api is compatible with Python 3.6 and above and is distributed with 
the Apache 2.0 License.
'''

setup(
    name='hr_little_api',
    version='19.10.1',
    description='The Python API for controlling Hanson Robotics consumer robots',
    long_description=long_description,
    license='Apache License Version 2.0',
    author='Hanson Robotics Limited',
    author_email='info@hansonrobotics.com',
    url='https://github.com/hansonrobotics/hr-little-api',
    packages=['hr_little_api', 'hr_little_api_examples'],
    download_url='https://github.com/hansonrobotics/hr-little-api/v19.10.1.tar.gz',
    keywords=['robotics', 'einstein', 'sophia', 'robot', 'AI'],
    install_requires=['logbook>=1.5.2'],
    test_suite="tests",
    entry_points={
        'console_scripts': [
            'hr_little_api_action_callbacks = hr_little_api_examples.action_callbacks:main',
            'hr_little_api_actions = hr_little_api_examples.actions:main',
            'hr_little_api_custom_animations = hr_little_api_examples.custom_animations:main',
            'hr_little_api_functional_api = hr_little_api_examples.functional_api:main',
            'hr_little_api_functional_api_callbacks = hr_little_api_examples.functional_api_callbacks:main',
            'hr_little_api_sensors = hr_little_api_examples.sensors:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
