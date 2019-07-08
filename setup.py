from setuptools import setup

setup(
    name='pretext',
    version='0.1',
    py_modules=['pretext'],
    install_requires=[
        'Click',
        'lxml',
        'PyYAML',
        'appdirs',
        # 'os',
    ],
    entry_points='''
        [console_scripts]
        pretext=pretext:cli
    ''',
)
