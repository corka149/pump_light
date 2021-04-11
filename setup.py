from setuptools import setup

setup(
    name='pump_light',
    version='1.0.2',
    packages=['pump_light'],
    package_dir={'': 'src'},
    include_package_data=True,  # IMPORTANT for configs in combination with MANIFEST.in
    url='https://github.com/corka149/pump_light',
    license='',
    author='corka149',
    author_email='corka149@mailbox.org',
    description='IOT light for a pump',
    install_requires=[
        'pydantic',
        'PyYAML',
        'aiohttp',
        'gpiozero',
        'RPi.GPIO'
    ]
)
