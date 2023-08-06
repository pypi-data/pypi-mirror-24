from setuptools import setup

setup( name='geminipython',
       version='0.3.0',
       description='Async API wrapper for the Gemini cryptocurrency exchange',
       url='https://gitlab.com/aaron235/gemini-python.git',
       author='Aaron Adler',
       author_email='qwertyman159@gmail.com',
       license='MIT',
       packages=[ 'geminipython' ],
       install_requires=[
           'aiohttp',
       ],
       zip_safe=False )
