from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re

print("Searching... please wait")
emails=[]

url="http://www.bbe.caltech.edu/people-public/all/all"
data=urlopen(url)
parse=BeautifulSoup(data).findAll('a')
b=[parse[k]['href'][7:] for k in range(len(parse)) if "@" in parse[k]['href']]
for k in b: emails.append(k)

links=[]
url="http://www.eas.caltech.edu/people"
data=urlopen(url)       
parse=BeautifulSoup(data).findAll('ul')[:2]
for k in parse:
    for j in k.findAll('li'):
        links.append("http://www.eas.caltech.edu"+j.a['href'])
for link in links:
    data=urlopen(link)
    parse=BeautifulSoup(data).findAll('div',attrs={'class':'contact-box'})
    try:
        val=re.split("Email: |<|>",str(parse[0].p))[3]+"@"+re.split("Email: |<|>",str(parse[0].p))[-3]
        if "gmail.com" in val or "caltech.edu" in val :
            emails.append(val)
    except: pass

url="http://www.pma.caltech.edu/people-public/professorial-faculty/all"
data=urlopen(url)
parse=BeautifulSoup(data).findAll('a')
b=[parse[k]['href'][7:] for k in range(len(parse)) if "@" in parse[k]['href']]
for k in b: emails.append(k)

url="http://www.hss.caltech.edu/people-public/Professorial%20Faculty/all"
data=urlopen(url)
parse=BeautifulSoup(data).findAll('a')
b=[parse[k]['href'][7:] for k in range(len(parse)) if "@" in parse[k]['href']]
for k in b: emails.append(k)

url="http://www.gps.caltech.edu/people-public/Professorial-Faculty/all"
data=urlopen(url)
parse=BeautifulSoup(data).findAll('a')
b=[parse[k]['href'][7:] for k in range(len(parse)) if "@" in parse[k]['href']]
for k in b: emails.append(k)

f=open('output.csv','w')
for k in emails :
    if k.count('@')>1:
        k='@'.join(k.split('@')[-2:])
	if k.startswith('Nora O') :
		k=k.split('(')[1].split(',')[0]
    f.write(k+'\n')
f.close()

print("Finished. Results saved to caltech_results.csv")

