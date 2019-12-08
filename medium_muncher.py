import xml.etree.ElementTree as ElementTree
from urllib.parse import unquote
from functools import reduce
import json
import requests
from dataclasses import dataclass
from typing import Optional,Union,List


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

class MediumMuncher:
    RECORDED_ATTRIBUTES=('id','title','webCanonicalUrl','latestPublishedAt','creatorId',)


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
   
    def munch_story(self,url:str,snippet:str=False,verbose:str=False)->Union[str,tuple]:
        ## make sure there's not already get params
        url=url.split("?")[0]
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

        ## meta 
        attributes=dict()
        for attribute in self.RECORDED_ATTRIBUTES:
            attributes[attribute]=payload=body['payload']['value'][attribute]
        
        final_html=text
        if not snippet:
            meta_tags=[]
            for key,value in attributes.items():
                meta_tags.append(f"<meta name='{key}' content='{value}'/>")
            
            final_html=f"<!doctype html>\n<html><head><title>{attributes['title']}</title>\n"
            final_html+= '\n'.join(meta_tags)
            final_html+="</head>\n<body>\n"
            final_html+=text
            final_html+=f"\n</body>\n</html>"

        if verbose:
            return final_html,attributes
        else:
            return final_html
            

    def munch_author_feed(self,author:str)->List[str]:
        tree = ElementTree.fromstring(requests.get(f'https://medium.com/feed/@{author}').text)
        channel=list(tree)[0]
        urls=list()
        for item in channel.findall('item'):
            raw_link_text=item.find('link').text
            link=raw_link_text.split('?')[0]
            urls.append(link)
        return urls      

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
        if len(markups) ==1:
            tags=[ 
                Tag(self._construct_tag_text(markups[0]),markups[0]['start']),
                Tag(f"</{self.MARKUP[markups[0]['type']].tag}>",markups[0]['end'])]
            return tags

        for a in markups:
            for b in markups:
                if a != b and (((a['start'],a['end'],) != (b['start'],b['end'],)) or (a['type'] > b['type'])):
                    if self._is_nested(a,b):
                        tags +=  [
                        Tag(self._construct_tag_text(b),b['start']),
                        Tag(self._construct_tag_text(a),a['start']),
                        Tag(f"</{self.MARKUP[a['type']].tag}>",a['end']),
                        Tag(f"</{self.MARKUP[b['type']].tag}>",b['end'])
                        ]
                    else:
                        open_tag=Tag(self._construct_tag_text(a),a['start'])
                        close_tag=Tag(f"</{self.MARKUP[a['type']].tag}>",a['end'])
                        if open_tag not in tags:
                            tags.append(open_tag)
                            tags.append(close_tag)
        return tags   

    def _construct_tag_text(self,markup:dict)->str:
        if markup['type'] == 3:
            return f"<{self.MARKUP[markup['type']].tag} href='{markup['href']}'>"
        else:
            return f"<{self.MARKUP[markup['type']].tag}>"

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

if __name__ == "__main__":
    m=MediumMuncher()
    print(

m.munch_story('https://towardsdatascience.com/is-your-company-too-dumb-to-be-data-driven-696932d597c3?')        

)
        



