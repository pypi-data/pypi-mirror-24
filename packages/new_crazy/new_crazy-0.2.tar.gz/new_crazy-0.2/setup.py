import setuptools

setuptools.setup(name='new_crazy',
                 version='0.2',
                 description='The new_crazy in the world',
                 author='EhsanGolshani',
                 url="https://github.com/ehsangolshani/new_crazy",
                 author_email='ehsanroman74@gmail.com',
                 license='MIT',
                 install_requires=[
                     'aiohttp',
                     'asyncio',
                 ],
                 packages=['new_crazy'],
                 zip_safe=False)
