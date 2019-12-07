from urllib.parse import unquote
from functools import reduce
import json
import requests
from dataclasses import dataclass
from typing import Optional



TEST={'name': 'b62a', 'type': 6, 'text': 'CPO: “Well, Mr.Cleese (the CFO) didn’t show to the board meeting last week, but we did find a newt in his office. So naturally we assumed a witch turned him into a newt. We voted to find and remove all witches in the company immediately, and be data-driven about it. So we figure, witches burn and so does wood, right? And of course wood floats, and ducks also float. So if the data says we have any employees that weigh as much as a duck, they are witches!”\nYou: (facepalms)', 'markups': [{'type': 1, 'start': 0, 'end': 4}, {'type': 1, 'start': 459, 'end': 463}, {'type': 2, 'start': 0, 'end': 4}, {'type': 2, 'start': 459, 'end': 463}]}

@dataclass
class Markup:
    name:str
    tag:str

MARKUP=[
    "no Markup 0",
    Markup("bold","b"),
    Markup("italic","i"),
    Markup("hyperlink","a")
]

@dataclass
class Container:
    name:str
    tag:str
    parent_tag:Optional[str]=None

CONTAINERS=[
    "No Container 0",
    Container("paragraph","p"),
    "No Container 2",
    Container("heading3","h3"),
    Container("figure caption", "figcaption"),
    "No Container 5",
    Container("block quote", "blockquote"),
    "No Container 7",
    "No Container 8",
    Container("bullet list","li","ul"),
    Container("numbered list","li","ol"),
    Container("figure caption","figcaption") ## 11 is for video, 4 for images?
]
   
def fetch_json(url):
    body=json.loads(requests.get(f"{url}?format=json").text[16:])
    paragraphs=body['payload']['value']['content']['bodyModel']['paragraphs']
    text=str()
    for i,p in enumerate(paragraphs):
        if p['type'] in (9,10,) and paragraphs[i-1]['type'] not in (9,10,):
            text+='<'+CONTAINERS[p['type']].parent_tag+'>'
        if p['type'] == 4:
            text+=f"<image src='https://miro.medium.com/max/3200/{p['metadata']['id']}' />"
        if p['type'] == 11:
            text+=f"<image src='{unquote(p['iframe']['thumbnailUrl'])}'/>"

        text+=wrap_paragraph(p,   
                        insert_tags(
                            shift_tags(
                                build_unindexed_tags(p['markups'])
                            ),p['text'])
                        )
        if p['type'] in (9,10,) and paragraphs[i+1]['type'] not in (9,10,):
            text+='</'+CONTAINERS[p['type']].parent_tag+'>'
    print(text)
        

def wrap_paragraph(paragraph,innerHTML):
    body=f"<{CONTAINERS[paragraph['type']].tag}>"+\
         innerHTML+\
         f"</{CONTAINERS[paragraph['type']].tag}>"
    return body

    
@dataclass
class Tag:
    text:str
    index:int
    shifted:int=0

def shift_index(a,b):
    b.shifted = a.shifted + len(a.text)
    b.index += b.shifted

def is_nested(a,b):
    return (a['start'] >= b['start'] and a['end'] <= b['end'])
    

def build_unindexed_tags(markups):
    tags=[]   
    for a in markups:
        for b in markups:
            if a != b and (((a['start'],a['end'],) != (b['start'],b['end'],)) or (a['type'] > b['type'])):
                #print(str(a)+'=>'+str(b))
                if is_nested(a,b):

                    


                    tags +=  [
                    Tag(f"<{MARKUP[b['type']].tag}>",b['start']),
                    Tag(f"<{MARKUP[a['type']].tag}>",a['start']),




                    Tag(f"</{MARKUP[a['type']].tag}>",a['end']),
                    Tag(f"</{MARKUP[b['type']].tag}>",b['end'])
                ]
    return tags   

def shift_tags(tags):
    for i,t in enumerate(tags):
        if i+1 < len(tags):
            shift_index(t,tags[i+1])
    return tags

def insert_tags(tags,text):
    for tag in tags:
        text = insert_tag(tag,text)
    return text 

def insert_tag(tag,text):
    pre=text[:tag.index]
    post=text[tag.index:]
    return pre+tag.text+post   

   
if __name__ == "__main__":
    fetch_json('https://towardsdatascience.com/is-your-company-too-dumb-to-be-data-driven-696932d597c3')


        



