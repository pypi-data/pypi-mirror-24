from setuptools import setup

setup(
    name='pydis',
    packages=['pydis'],
    version='0.3.2',
    description='Python wrappers for StrictRedis',
    author='masayang',
    author_email='masayang@msushi.com',
    url='https://github.com/masayang/py_redis',
    install_requires=['redis', 'python-dotenv'],
    zip_safe=False
)
