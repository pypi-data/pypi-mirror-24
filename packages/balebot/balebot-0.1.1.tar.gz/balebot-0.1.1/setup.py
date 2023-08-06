import setuptools

setuptools.setup(name='balebot',
                 version='0.1.1',
                 description='python framework for Bale messenger Bot API ',
                 author='Ehsan Golshani',
                 author_email='ehsanroman74@gmail.com',
                 license='GNU',
                 install_requires=[
                     'aiohttp',
                     'asyncio',
                     'graypy',
                 ],
                 packages=['balebot'],
                 zip_safe=False)
