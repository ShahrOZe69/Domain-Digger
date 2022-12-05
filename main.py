try:
    import gui
    import digger
    import os
    import time
except Exception as e:
    print(f'Error Importing!! {e}')

input('Press Enter to start!')

def remove_already_processed(ips):
    if os.path.exists('database.txt'):
        file_ips = open('database.txt').read().splitlines()
        for ip in ips:
            if ip not in file_ips:
                yield ip
            else:
                print(f'IP Already in Database..{ip}')
    else:
        yield from ips

def save_results(domains):
    # Sort the domains alphabetically
    domains = sorted(domains)
    domains =[i.replace('www.','') for i in domains]
    c = 'w'
    if os.path.isfile('results.txt'):
        c = input('Results file Already exists, Overwrite(Y) or Append(N)? ')
        if c.upper() =='Y':
            c = 'w'
        else: c = 'a'
    
    with open('results.txt',c,encoding='utf-8',errors='ignore') as file:
        file.write('\n'.join(domains)+'\n')


def reverse_lookup_ip(l):
    """Reverse lookup Each IP.
    Also saves the data of each IP to a JSON file 
    To prevent lookup of same IP twice
    """
    domains = []
    c=0
    total = len(l)
    start = time.time()
    database_file = open('database.txt','a+')
    for i in l:
        ip_results = []
        i = i.strip()
        c+=1
        print(f'Looking up IP {i} {c}/{total}')
        if not digger.check_ip_format(i):
            print(f'WARNING!! Wrong IP FORMAT {i}')
            continue

        print("Looking up on ViewDNS.com....")
        try:
            d = digger.reverse_lookup_ip_viewdns(i)
            ip_results+=[j['Domain'] for j in d]
            print(f'Results found: {len(d)}\n Domains Extracted: {len(ip_results)}')
        except Exception as e:
            print(f'Unknown Error in ViewDNS.info Lookup: {e}') 

        print('Looking up on IPWatson.com.......')
        try:        
            d=digger.reverse_lookup_ip_ipwatson(i)
            ip_results+=d
            print(f'Results found: {len(d)}\n Domains Extracted: {len(ip_results)}')
        except Exception as e:
            print(f'Unknown Error in IPWatson.com Lookup: {e}')  
            

        print('Looking up on IPAddress.com.......')
        try:        
            d=digger.reverse_lookup_ip_ipaddress(i)
            ip_results+=d
            print(f'Results found: {len(d)}\n Domains Extracted: {len(ip_results)}')
        except Exception as e:
            print(f'Unknown Error in IPAddress.com Lookup: {e}')
        
        
        domains+=ip_results
        print(f'Results found: {len(d)}\n Total Domains Extracted: {len(domains)}')

        # save the extracted ip results to database
        database_file.write(f'{i}\n')


    s = list(set(domains))

    print(f"""
    
    Process Finished:
    Total Domains:{len(s)}
    Total Time Taken:{(time.time()-start)/60} minutes
    """)
    database_file.close()
    return s


def get_domains_history(domains):
    x = []
    for domain in domains:
        print(f"Getting Domain history: {domain}")
        ips = digger.get_domain_history(domain)
        print(f"IPs Found: {len(ips)}")
        for i in ips:
            x.append(i['IP'])
    print(f'Total IPs Found: {len(x)}')
    return x



if __name__=='__main__':
    """
    Take input from user
    """

    # create empty database file if not exists
    if not os.path.exists('database.txt'):
        with open('database.txt','w') as f:
            pass

    print("Program Started................")
    input_data,type = gui.gui()
    if type=='IP List':
        ips = input_data
    
    if type == 'IP Range':
        ips = digger.ips(*input_data)      

    if type == 'Domain List':
        ips = get_domains_history(input_data)
    

    ips = list(remove_already_processed(ips))
    domains = reverse_lookup_ip(ips)
    print("SAVING RESULTS")            
    save_results(domains)
    input('Press Enter To Exit')

