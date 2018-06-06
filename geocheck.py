import csv, time
import socket, struct

F_COUNTRIES = 'geolite2/GeoLite2-Country-Locations-en.csv'
F_IPV4 = 'geolite2/GeoLite2-Country-Blocks-IPv4.csv'

ipv4_keys = [
    "network",
    "geoname_id",
    "registered_country_geoname_id",
    "represented_country_geoname_id",
    "is_anonymous_proxy",
    "is_satellite_provider"
]

country_keys = [
    "geoname_id",
    "locale_code",
    "continent_code",
    "continent_name",
    "country_iso_code",
    "country_name",
    "is_in_european_union"
]

eu_countries = (
        'EU', 'AD', 'AL', 'AT', 'BA', 'BE', 'BG', 'BY', 
        'CH', 'CS', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 
        'FO', 'FR', 'FX', 'GB', 'GI', 'GR', 'HR', 'HU', 
        'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MC', 
        'MD', 'MK', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 
        'SE', 'SI', 'SJ', 'SK', 'SM', 'UA', 'VA'
)

countries = {}
with open(F_COUNTRIES) as f:
    reader = csv.reader(f)        
    for row in reader:
        countries[row[0]] = row

ipv4s = []
with open(F_IPV4) as f:
    reader = csv.reader(f)
    for row in reader:
        ipv4s.append (row)

def addressInNetwork(ip, net):
   ipaddr = int(''.join([ '%02x' % int(x) for x in ip.split('.') ]), 16)
   netstr, bits = net.split('/')
   netaddr = int(''.join([ '%02x' % int(x) for x in netstr.split('.') ]), 16)
   mask = (0xffffffff << (32 - int(bits))) & 0xffffffff
   return (ipaddr & mask) == (netaddr & mask)

def get_info(ip):
    for ipv4 in ipv4s:
        if addressInNetwork(ip, ipv4[0]):
            print ipv4
            ret = dict(zip(ipv4_keys, ipv4))
            ret['registered_country'] = dict(zip(
                country_keys,
                countries[ret['registered_country_geoname_id']]
            ))
            ret['country'] = dict(zip(
                country_keys,
                countries[ret['geoname_id']]
            ))     

            return ret       


