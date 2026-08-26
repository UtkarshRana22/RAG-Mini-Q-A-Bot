import json

file_1=open("data/01-getting-started.md",'r',encoding='utf-8')
file_2=open("data/02-pricing-and-plans.md",'r',encoding='utf-8')
file_3=open("data/03-troubleshooting.md",'r',encoding='utf-8')
chunk1=file_1.read().split("##")
chunk2=file_2.read().split("##")
chunk3=file_3.read().split("##")
str=''

dict_={}
list_=[]
for c in chunk1:
     
     parts=c.split("\n\n")
     dict_={"filename":"01-getting-started.md","section":parts[0].strip(),"text":"\n\n".join(parts[1:]).strip()}
     if dict_["text"]:
          list_.append(dict_)
for c in chunk2:
     parts=c.split("\n\n")
     dict_={"filename":"02-pricing-and-plans.md","section":parts[0].strip(),"text":"\n\n".join(parts[1:]).strip()}
     if dict_["text"]:
          list_.append(dict_)
for c in chunk3:
     parts=c.split("\n\n")
     dict_={"filename":"03-troubleshooting.md","section":parts[0].strip(),"text":"\n\n".join(parts[1:]).strip()}
     if dict_["text"]:
          list_.append(dict_)


with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(list_, f, indent=2)