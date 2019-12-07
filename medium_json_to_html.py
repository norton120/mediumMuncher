from urllib.parse import unquote
from functools import reduce
import json
import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class Markup:
    name:str
    tag:str

@dataclass
class Container:
    name:str
    tag:str
    parent_tag:Optional[str]=None

@dataclass
class Tag:
    text:str
    index:int
    shifted:int=0

class MediumJsonToHtml:

    MARKUP=[
        "no Markup 0",
        Markup("bold","b"),
        Markup("italic","i"),
        Markup("hyperlink","a")
    ]



    CONTAINERS=[
        "No Container 0",
        Container("paragraph","p"),
        "No Container 2",
        Container("heading3","h3"),
        Container("figure caption for image", "figcaption"),
        "No Container 5",
        Container("block quote", "blockquote"),
        "No Container 7",
        "No Container 8",
        Container("bullet list","li","ul"),
        Container("numbered list","li","ol"),
        Container("figure caption for video","figcaption") 
    ]
   
    def convert_url(self,url):
        body=json.loads(requests.get(f"{url}?format=json").text[16:])
        paragraphs=body['payload']['value']['content']['bodyModel']['paragraphs']
        text=str()
        for i,p in enumerate(paragraphs):
            if p['type'] in (9,10,) and paragraphs[i-1]['type'] not in (9,10,):
                text+='<'+self.CONTAINERS[p['type']].parent_tag+'>'
            if p['type'] == 4:
                text+=f"<image src='https://miro.medium.com/max/3200/{p['metadata']['id']}' />"
            if p['type'] == 11:
                text+=f"<image src='{unquote(p['iframe']['thumbnailUrl'])}'/>"

            text+=self._wrap_paragraph(p,   
                            self._insert_tags(
                                self._shift_tags(
                                    self._build_unindexed_tags(p['markups'])
                                ),p['text'])
                            )
            if p['type'] in (9,10,) and paragraphs[i+1]['type'] not in (9,10,):
                text+='</'+self.CONTAINERS[p['type']].parent_tag+'>'
        ## wrap meta 
        payload=body['payload']['value']

        metas=[]
        for value in ('id','title','webCanonicalUrl','latestPublishedAt','creatorId',):
            metas.append(f"<meta name='{value}' content='{payload[value]}'/>")
        
        final=f"<!doctype html>\n<html><head><title>{payload['title']}</title>\n"
        final+= '\n'.join(metas)
        final+="</head>\n<body>\n"
        final+=text
        final+=f"\n</body>\n</html>"

        return final
            

    def _wrap_paragraph(self,paragraph,innerHTML):
        body=f"<{self.CONTAINERS[paragraph['type']].tag}>"+\
             innerHTML+\
             f"</{self.CONTAINERS[paragraph['type']].tag}>"
        return body

        


    def _shift_index(self,a,b):
        b.shifted = a.shifted + len(a.text)
        b.index += b.shifted

    def _is_nested(self,a,b):
        return (a['start'] >= b['start'] and a['end'] <= b['end'])
        

    def _build_unindexed_tags(self,markups):
        tags=[]   
        for a in markups:
            for b in markups:
                if a != b and (((a['start'],a['end'],) != (b['start'],b['end'],)) or (a['type'] > b['type'])):
                    #print(str(a)+'=>'+str(b))
                    if self._is_nested(a,b):
                        tags +=  [
                        Tag(f"<{self.MARKUP[b['type']].tag}>",b['start']),
                        Tag(f"<{self.MARKUP[a['type']].tag}>",a['start']),
                        Tag(f"</{self.MARKUP[a['type']].tag}>",a['end']),
                        Tag(f"</{self.MARKUP[b['type']].tag}>",b['end'])
                    ]
        return tags   

    def _shift_tags(self,tags):
        for i,t in enumerate(tags):
            if i+1 < len(tags):
                self._shift_index(t,tags[i+1])
        return tags

    def _insert_tags(self,tags,text):
        for tag in tags:
            text = self._insert_tag(tag,text)
        return text 

    def _insert_tag(self,tag,text):
        pre=text[:tag.index]
        post=text[tag.index:]
        return pre+tag.text+post   

   




        



