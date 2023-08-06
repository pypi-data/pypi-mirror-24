from setuptools import setup

setup(
    name='poker-program-demo',
    version='0.1.0',
    description='play poker; my first python project to learn',
    url='https://bitbucket.org/codyc54321/poker_program_demo',
    author='Cody Childers',
    author_email='cchilder@mail.usf.edu',
    license='MIT',
    packages=['holdem'],
    install_requires=[],
    zip_safe=False,
    entry_points={
        'console_scripts': ['play-poker=holdem.holdem_game:run_poker_game']
    }
)
