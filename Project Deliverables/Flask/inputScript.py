from tldextract import extract
import ssl
import socket
from bs4 import BeautifulSoup
import urllib.request
import whois
import datetime
from socket import timeout



# 1) having ip
# 2) url length
# 3) shortening service
# 4) @ symbol
# 5) // redirect
# 6) prefix-suffix
# 7) sub domain
# 8) ssl final state
# 9) https in domain
# 10) request url
# 11) url of anchor
# 12) links in tags
# 13) submit to email
# 14) age of domain
# 15) dns record check


def checkIPAddress(url):
    l = url.split("/")
    # print(l)

    # 1.detecting ip addr
    try:
        if(l[2][:3].isalpha()):
            return 1
        else:
            return -1
    except:
        return -1


        

#Changing
def url_length(url):
    length=len(url)
    if(length<54):
        return 1
    elif(54<=length<=75):
        return 0
    else:
        return -1


def checkURL(url):
    # 3.detecting tinyurl and bit.ly
    if(("tinyurl" in url) or ("bit.ly" in url)):
        return -1
    else:
        return 1


def atTheRateChecker(url):
    # 4.detecting @ symbol
    if('@' in url):
        return -1
    else:
        return 1

def redirectURL(url):
    # 5.detecting // redirect

    l=url.split("//")
    
    if(len(l)>2):
        return -1
    else:
        return 1

#Changing
def prefix_suffix(url):
    # 6.detecting prefix-suffix
    l=url.split(".")
    print(l)
    if("-" in l[1]):
        return -1
    else:
        return 1



#Change
def subdomain(url):
    subDomain, domain, suffix = extract(url)
    if(subDomain.count('.')==1):
        return 1
    elif(subDomain.count('.')==2):
        return 0
    else:
        return -1


def detectingHTTP(url):
    # 8.detecting https
    l=url.split(".")
    print(l)
    if("https" in l[0]):
        return 1
    else:
        return -1

def detectingHTTPinDomain(url):
    # 9.detecting https in domain
    l=url.split("//")
    print(l)
    try:
        if("https" in l[1]):
            return -1

        else:
            return 1
    
    except:
        return 1
    
#  try:
#         response = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
#     except timeout:
#         logging.error('socket timed out - URL %s', url)


#10
#Changing
def request_url(url):
    try:    
        subDomain, domain, suffix = extract(url)
        websiteDomain = domain
        
        opener = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
        # print("CAME hjbdfx")
        soup = BeautifulSoup(opener, 'lxml')
        imgs = soup.findAll('img', src=True)
        total = len(imgs)
        # print("Came to 10")
        
        linked_to_same = 0
        avg =0
        for image in imgs:
            subDomain, domain, suffix = extract(image['src'])
            imageDomain = domain
            if(websiteDomain==imageDomain or imageDomain==''):
                linked_to_same = linked_to_same + 1
        vids = soup.findAll('video', src=True)
        total = total + len(vids)
        
        for video in vids:
            # print("LOOOP")

            subDomain, domain, suffix = extract(video['src'])
            vidDomain = domain
            if(websiteDomain==vidDomain or vidDomain==''):
                linked_to_same = linked_to_same + 1
        linked_outside = total-linked_to_same
        if(total!=0):
            avg = linked_outside/total
            
        if(avg<0.22):
            return 1
        elif(0.22<=avg<=0.61):
            return 0
        else:
            return -1
    except:
        return 0


#11
#Changing

def url_of_anchor(url):
    try:
        subDomain, domain, suffix = extract(url)
        websiteDomain = domain
        
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        anchors = soup.findAll('a', href=True)
        total = len(anchors)
        # print("Came to 11")
        linked_to_same = 0
        avg = 0
        for anchor in anchors:
            subDomain, domain, suffix = extract(anchor['href'])
            anchorDomain = domain
            if(websiteDomain==anchorDomain or anchorDomain==''):
                linked_to_same = linked_to_same + 1
        linked_outside = total-linked_to_same
        if(total!=0):
            avg = linked_outside/total
            
        if(avg<0.31):
            return 1
        elif(0.31<=avg<=0.67):
            return 0
        else:
            return -1
    except:
        return 0
    
#12
#Changing

def Links_in_tags(url):
    try:
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        
        no_of_meta =0
        no_of_link =0
        no_of_script =0
        anchors=0
        avg =0
        # print("Came to 12")
        for meta in soup.find_all('meta'):
            no_of_meta = no_of_meta+1
        for link in soup.find_all('link'):
            no_of_link = no_of_link +1
        for script in soup.find_all('script'):
            no_of_script = no_of_script+1
        for anchor in soup.find_all('a'):
            anchors = anchors+1
        total = no_of_meta + no_of_link + no_of_script+anchors
        tags = no_of_meta + no_of_link + no_of_script
        if(total!=0):
            avg = tags/total

        if(avg<0.17):
            return 1
        elif(0.17<=avg<=0.81):
            return 0
        else:
            return -1        
    except:        
        return 0

#13
#Changing
def email_submit(url):
    try:
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        # print("Came to 13")
        if(soup.find('mailto:')):
            return -1
        else:
            return 1 
    except:
        return 0


#14
#Changing
def ageOfDomain(url):
    try:
        w = whois.whois(url)
        start_date = w.creation_date
        current_date = datetime.datetime.now()
        age =(current_date-start_date[0]).days
        # print("Came to 14")
        if(age>=180):
            return 1
        else:
            return -1
    except Exception as e:
        print(e)
        return 0


def DNSRecord(url):
    l=url.split("/")
    try:
        info = whois.whois(l[2])
        # print("Came to 15")
        if(len(info.name_servers)>0):
            return 1
        else:
            return -1
    except:
        return -1
    


def main(url):

    
    check = [[
        checkIPAddress(url), url_length(url), checkURL(url), atTheRateChecker(url), redirectURL(url), prefix_suffix(url), subdomain(url), detectingHTTP(url), detectingHTTPinDomain(url),
        request_url(url), url_of_anchor(url) ,Links_in_tags(url), email_submit(url), ageOfDomain(url), DNSRecord(url)
    ]]
    
    
    return check



