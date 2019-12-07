## Medium JSON to HTML

Medium makes content readily available for machine consumption through the `format=json` param, however the json response is not exactly plug-and-play for redisplaying it has HTML. Enter this package. 

### Installation
via pip with 

```
pip3 install medium-json-html

```

### Usage

The package is really simple and only has one accessor method, `convert_url()`. To use: 

````
from medium_json_to_html import MediumJsonToHtml

html = MediumJsonToHtml().convert_url('https://medium.com/some-author/some-amazing-article-039525')

print(html) ## prints plain html version of article

### Meta tags
I added some useful meta values in the head tag, could add more or less as needed from the mass of data that comes back with the request. 
