from setuptools import setup 
import os
from medium_muncher.__init__ import __version__

args=dict()
with open("README.md","r",encoding='utf-8') as f:
    args["long_description"] = f.read()
args['long_description_content_type']='text/markdown'
args["install_requires"]=["requests==2.22.0"]
args["url"]="https://github.com/norton120/mediumMuncher"
args["home_page"]="https://github.com/norton120/mediumMuncher"
args["packages"]=["medium_muncher"]
args["name"] = "mediumMuncher"
args["version"]=__version__
args["summary"]="Converts medium stories and author feeds into plain HTML."
args["keywords"]="Medium"
args["author"]="Ethan Knox"
args["author-email"]="ethan.m.knox@gmail.com"
args["license"]="MIT"
python_requires=">=3.7"

setup(**args)
