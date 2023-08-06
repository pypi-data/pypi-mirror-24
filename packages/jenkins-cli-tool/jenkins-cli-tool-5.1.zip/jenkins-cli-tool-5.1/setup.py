from distutils.core import setup

setup(
    name='jenkins-cli-tool',
    version='5.1',
    packages=['cli', 'cli.startjob', 'cli.startandmonitor', 'tests', 'cli.queue', 'library'],
    url='https://git.ecd.axway.int/apigw-champions/jenkins-cli',
    license='MIT',
    author='chermet',
    author_email='chermet@axway.com',
    description='CLI tool for Jenkins',
    install_requires=[
       'click',
       'python-jenkins'
    ],
    entry_points={
        'console_scripts': [
            'jenkins_cli_tool = cli.cli:entry_point'
        ]
    }
)
