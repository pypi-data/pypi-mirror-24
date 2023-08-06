from distutils.core import setup

setup(
    name='pydis',
    packages=['pydis'],
    version='0.2.1',
    description='Python wrappers for StrictRedis',
    author='masayang',
    author_email='masayang@msushi.com',
    url='https://github.com/masayang/py_redis',
    install_requires=['redis', 'python_dotenv'],
    zip_safe=False
)
