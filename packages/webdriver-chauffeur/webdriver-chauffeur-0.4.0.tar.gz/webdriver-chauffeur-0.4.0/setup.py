from setuptools import setup

setup(
    name='webdriver-chauffeur',
    version='0.4.0',
    description='A helpful wrapper around the formerly annoying stuff of using Selenium Webdriver',
    url='https://github.com/codyc4321/webdriver_chauffeur',
    author='Cody Childers',
    author_email='cchilder@mail.usf.edu',
    license='MIT',
    packages=['webdriver_chauffeur'],
    install_requires=[
        'bs4',
        'selenium'
    ],
    zip_safe=False,
)
