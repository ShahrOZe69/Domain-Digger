import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re



def get_domain_history(domain):
    """
    Get domain IP history from viewDNS.info

    """
    try:
        res = requests.get(f'https://viewdns.info/iphistory/?domain={domain}',
                       headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
    except requests.exceptions.ConnectionError:
        return []
    except requests.exceptions.Timeout:
        return []
    except Exception as err:
        print(f'UNKNOWN ERROR IN GETTING DOMAIN HISTORY\nERROR: {err}')
        return []
    
    soup = BeautifulSoup(res.content, features='html.parser')
    table = soup.find('table', attrs={'border': 1})
    if table:
        data = []
        tr = table.find_all('tr')[1:]
        for x in tr:
            k = x.find_all('td')

            data.append({'IP':k[0].text,'Location':k[1].text,'Owner':k[2].text,'LastSeen':datetime.strptime(k[3].text,'%Y-%m-%d')})
        return data
    else:
        return []


def reverse_lookup_ip_viewdns(ip):
    """
    Get reverse lookup results from viewDNS.info

    """
    try:
        res = requests.get(f'https://viewdns.info/reverseip/?host={ip}&t=1',
                       headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
    except requests.exceptions.ConnectionError:
        return []
    except requests.exceptions.Timeout:
        return []
    except Exception as err:
        print(f'UNKNOWN ERROR IN GETTING DOMAIN HISTORY\nERROR: {err}')
        return []
    
    soup = BeautifulSoup(res.content, features='html.parser')
    table = soup.find('table', attrs={'border': 1})
    if table:
        data = []
        tr = table.find_all('tr')[1:]
        for x in tr:
            k = x.find_all('td')
            data.append({'Domain':k[0].text,'LastResolved':datetime.strptime(k[1].text,'%Y-%m-%d')})
        return data
    else:
        return []

def reverse_lookup_ip_ipwatson(ip):
    """
    Get reverse lookup results from Ipwatson.com

    """
    
    try:
        res = requests.get(f'https://www.ipwatson.com/engine/search.php?query={ip}',headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
    except requests.exceptions.ConnectionError:
        return []
    except requests.exceptions.Timeout:
        return []
    except Exception as err:
        print(f'UNKNOWN ERROR IN GETTING DOMAIN HISTORY\nERROR: {err}')
        return []

    j = res.json()
    return j.get('results',{}).get('domain',[])


def reverse_lookup_ip_ipaddress(ip):
    """Reverse lookup from ipaddress.com website"""
    try:
        res = requests.post('https://www.ipaddress.com/reverse-ip-lookup',data={'host':f'{ip}'},headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
    except requests.exceptions.ConnectionError:
        return []
    except requests.exceptions.Timeout:
        return []
    except Exception as err:
        print(f'UNKNOWN ERROR IN GETTING DOMAIN HISTORY\nERROR: {err}')
        return []
    
    soup = BeautifulSoup(res.content,features = 'html.parser')
    li = soup.find('ol')
    if not li:
        return []
    li = li.find_all('li')
    domains = [i.find('a').text for i in li]
    return domains
    

def ips(start, end):
    import socket, struct
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]+1
    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]


def check_ip_format(ip):
    return bool(re.search("""^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$""",ip))




if __name__=='__main__':
    # his = get_domain_history('twitter.codm')
    # print(his)
    # domains = []
    # rev = reverse_lookup_ip_viewdns('8.8.8.89')
    # print(rev)
    # domains.append(j['Domain'] for j in rev)
    # print(domains)
    print(reverse_lookup_ip_ipaddress('8.8.8.8'))
    # print(reverse_lookup_ip_ipwatson('8.8.8.8'))