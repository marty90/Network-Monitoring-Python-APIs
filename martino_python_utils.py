import re
import operator

bad_domains=set("co.uk co.jp co.hu co.il com.au co.ve .co.in com.ec com.pk co.th co.nz com.br com.sg com.sa \
com.do co.za com.hk com.mx com.ly com.ua com.eg com.pe com.tr co.kr com.ng com.pe com.pk co.th \
com.au com.ph com.my com.tw com.ec com.kw co.in co.id com.com com.vn com.bd com.ar \
com.co com.vn org.uk net.gr".split())

# Cut a domain after 2 levels
# e.g. www.google.it -> google.it
def get2LD(fqdn):
    if fqdn[-1] == ".":
        fqdn = fqdn[:-1]    
    names = fqdn.split(".")
    tln_array = names[-2:]
    tln = ""
    for s in tln_array:
        tln = tln + "." + s
    return tln[1:]

def getGood2LD(fqdn):
    if fqdn[-1] == ".":
        fqdn = fqdn[:-1]    
    names = fqdn.split(".")
    if ".".join(names[-2:]) in bad_domains:
        return get3LD(fqdn)
    tln_array = names[-2:]
    tln = ""
    for s in tln_array:
        tln = tln + "." + s
    return tln[1:]

# Cut a domain after 3 levels
# e.g. www.c3.google.it -> c3.google.it
def get3LD(fqdn):
    if fqdn[-1] == ".":
        fqdn = fqdn[:-1]
    names = fqdn.split(".")
    tln_array = names[-3:]
    tln = ""
    for s in tln_array:
        tln = tln + "." + s
    return tln[1:]

# Cut a domain after N levels
# e.g. (www.c3.google.it, 2) -> google.it
def getNLD(fqdn, n):
    if fqdn[-1] == ".":
        fqdn = fqdn[:-1]
    names = fqdn.split(".")
    tln_array = names[-n:]
    tln = ""
    for s in tln_array:
        tln = tln + "." + s
    return tln[1:]

# Create a 'bags' object, reading it from a file
def openBags(file_name):
    bags={}
    bags["domains"]={}
    bags["regexps"]=[]
    for row in open(file_name, "r"):
        if row[0] != '\t':
            core = row[:-1]
        elif (row[0] == '\t') and (row[1]!='#') and (row[0]!='#'):
            if row[:3] == "\tR:":
                name = row[3:-1].split("#")[0].strip()
                entry = (re.compile(name), core)
                bags["regexps"].append(entry)
            else:
                name = row[1:-1].split("#")[0].strip()
                bags["domains"][name] = core
    return bags

# Get the bag of a domain, or cut it after 2 levels if not found
# e.g. (mybags, fbcdn.net) -> facebook.com
def getBag(bags, name):
    name = name.lower()
    for entry in bags["regexps"]:
        if entry[0].match(name) is not None:
            return entry[1]    
    for n in range(2,6):
        if getNLD(name, n) in bags["domains"]:
            return(bags["domains"][getNLD(name, n)])
    return(get2LD(name))

# Strip digits, isolated characters from a domain
# e.g. client4.google.com -> clientD.google.com
def filter_name (name):
    
    # Strip cloudfront.net
    filtered_name = re.sub('[a-z0-9]+\.cloudfront.net', "X.cloudfront.net", name)
    filtered_name = re.sub('[a-z0-9]+\.profile\..*\.cloudfront.net', "X.cloudfront.net", filtered_name)
      
    # Strip googlevideo.com
    filtered_name = re.sub('---sn-.*\.googlevideo\.com',"---sn-X.googlevideo.com", filtered_name)
    filtered_name = re.sub('---sn-.*\.c\.pack\.google\.com',"---sn-X.c.pack.google.com", filtered_name)
    
    # Strip digits
    filtered_name = re.sub('\d+',"D", filtered_name)
    
    # Strip "C"
    filtered_name = re.sub('((?<=[-\._D])|^)[a-z](?=[-\._D])',"C", filtered_name)
    
    return filtered_name

# Create and write to file the cumulative distribution of the given samples. An array is also returned.
# e.g. [0,0,1,2,3] -> [(0, 0.4), (1, 0.6), (2, 0.8), (3, 1.0)]
def samples_to_cumul_to_file(samples, file_name):
    histo = {}
    
    for s in samples:
        if not s in histo:
            histo[s] = 0
        histo[s] += 1
        
    histo =  sorted(histo.items(), key = operator.itemgetter(0))
    cumul = []
    for t in histo:
        if t==histo[0]:
            entry = (t[0],t[1])
        else:
            entry = (t[0], t[1] + cumul[-1][1] )
        cumul.append(entry)
    maxx = cumul[-1][1]
    for i in range (0,len(cumul)):
        cumul[i] = (cumul[i][0], float(cumul[i][1])/maxx)
    # Save on file
    f = open(file_name, "w")
    for e in cumul:
        f.write(str(e[0]) + " " + str(e[1]) + "\n") 
    return cumul

# Extracts intersting fields from a line of the log_tcp_complete
def parseLogTcpLine (line):
    
    splitted = line.split()
    if len (splitted) < 130:
        return None
    
    c_ip = splitted[0]
    s_ip = splitted[14]
    c_bytes = splitted[6]
    s_bytes = splitted[20]
    bytes = int (splitted[6]) + int(splitted[20])
    fqdn = splitted[126]
    sni = splitted[115]
    if fqdn == "fqdn:127" :
        return False
    
    if sni == "-":
         name = fqdn
    else:
         name = sni
    parsed={}
    parsed["c_ip"]=c_ip
    parsed["s_ip"]=s_ip
    parsed["bytes"]=bytes
    parsed["c_bytes"]=c_bytes
    parsed["s_bytes"]=s_bytes
    parsed["fqdn"]=fqdn
    parsed["sni"]=sni
    parsed["name"]=c_ip
    return parsed

# Extracts intersting fields from a line of the passive DNS log
def parseLogDnsLine (line):
    splitted = line.split("||")
    parsed = {}
    if len (splitted) < 9:
        return None
    answer=splitted[6]
    query=splitted[4]
    typ=splitted[5]
    ttl=splitted[7]
    c_ip=splitted[1]
    time=float(splitted[0])
    parsed["answer"]=answer
    parsed["query"]=query
    parsed["type"]=typ
    parsed["ttl"]=ttl
    parsed["c_ip"]=c_ip
    parsed["time"]=time
    return parsed


