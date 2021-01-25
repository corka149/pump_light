from setuptools import setup

setup(
    name='pump_light',
    version='0.0.1',
    packages=['pump_light'],
    package_dir={'': 'src'},
    url='https://github.com/corka149/pump_light',
    license='',
    author='corka149',
    author_email='corka149@mailbox.org',
    description='IOT light for a pump',
    install_requires=[
        'pydantic',
        'PyYAML',
        'aiohttp'
    ]
)
