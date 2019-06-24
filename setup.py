from setuptools import setup

setup(
    name='pretext',
    version='0.1',
    py_modules=['pretext'],
    install_requires=[
        'Click',
        'lxml',
        # 'os',
    ],
    entry_points='''
        [console_scripts]
        pretext=pretext:cli
    ''',
)