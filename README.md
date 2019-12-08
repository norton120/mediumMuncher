## Medium Muncher

Medium makes content readily available for machine consumption through the `format=json` param, and content feeds via the `feeds` path, however the XML and JSON responses are not exactly plug-and-play for redisplaying content. Enter this package. 

### Installation
via pip with 

```
pip3 install mediummuncher

```

### Usage

Getting a story as stand-alone HTML (with head and body tags)

```
from mediummuncher import MediumMuncher

muncher = MediumMuncher()
full_html=muncher.munch_story('https://medium.com/some-author/some-amazing-article-039525')
#returns "<!doctype html><head>... "
```
Getting a story as an html snippet (no head or body)

```
html_snippet=muncher.munch_story('https://medium.com/some-author/some-amazing-article-039525',snippet=True)
#returns "<p>article text!..."
```

Using the `verbose` flag returns a tuple with the html and a dictionary of interesting article attributes such as title, published date etc. 

```
html_snippet=muncher.munch_story('https://medium.com/some-author/some-amazing-article-039525',snippet=True, verbose=True)
#returns tuple ("<p>article text!...", {"title":"this amazing article"...,)
```

Getting all the story urls for a given author

```
stories=muncher.munch_author_feed('some-author')
#returns tuple ("https://medium.com/some-author/amazing-article-one-12902990",..,) 
```

Putting it all together to extract all stories for a given author

```
stories=list()
for url in muncher.munch_author_feed('ethan.m.knox'):
    stories.append(muncher.munch_story( url,
                                        snippet=True,
                                        verbose=True))
print(list)

```

## Contributing
Please feel free to fork and PR! Can always use another helping hand.
