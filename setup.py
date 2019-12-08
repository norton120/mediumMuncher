from setuptools import setup, find_packages
import os

args=dict()
with open('./README.md', 'r') as f:
    args['long_description'] = f.read()


reqs = []
with open("requirements.txt") as file:
    for line in file:
        # remove linebreak which is the last character of the string
        currentReq = line[:-1]
        reqs.append(currentReq)

args['install_requires']=reqs
#args['classifiers']=["License :: OSI Approved :: MIT License",
#        "Programming Language :: Python :: 3.7",],
args['description-content-type']='text/markdown'
args['packages']=find_packages()
args['name'] = "mediumToHTML"
args['version']='0.0.01'
args['summary']='converts Medium articles to simple HTML'
args['keywords']='Medium'
args['author']='Ethan Knox'
args['author-email']='ethan.m.knox@gmail.com'

setup(**args)
