from setuptools import setup, find_packages

setup(name='py_agent',
      version='0.0.1',
      entry_points = {
        'console_scripts': ['agent-test=py_agent.agent_test:main'],
    }
)