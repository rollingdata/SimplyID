# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 15:08:09 2018

@author: januszhou
"""

import os
import re
import csv
import sys
import requests
# from lxml.html import fromstring

from bs4 import BeautifulSoup


# simply try out fetching the webpage


http_proxy  = "http://web-proxy.tencent.com:8080"
https_proxy = "https://web-proxy.tencent.com:8080"


proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
            }



# hard code target address for now

# it will be a dict to look for different version of the area code
# make it to be a csv with 2 columns: version with time + download url



def trim_tags(string):
    trimmed_result = re.sub('<td class="xl70971">', '', string)
    trimmed_result = re.sub('</td>', '', trimmed_result)
    return(trimmed_result)




def main():
    # what are we expecting the input argv
    # i need a source url table, output directory

    # ???
    if len(sys.argv) != 3:
        print('Usage: %s [sources] [dir]' % sys.argv[0], file=sys.stderr)
        sys.exit(0)

    with open(sys.argv[1], 'r') as source_list:
        reader = csv.DictReader(source_list, delimiter=',')
        # make the list stroing tuples
        url_list = [
            (line['TimeVersion'], line['URL'])
            for line in reader
        ]
    
    for time_version, url in url_list:
        user_agent = {'User-agent': 'Mozilla/5.0'}
        req = requests.get(url, headers=user_agent, proxies=proxyDict)
        # req = requests.get(url, headers=user_agent)

        if req.status_code != 200:
            # if no success
            msg = 'ERROR: fetching MCA raw lookup failed: %s/%s %s' % (time_version, url, req.status_code)
            print(msg, file=sys.stderr)
            continue
        # unified all text with utf8 encoding
        # req.encoding('utf-8')
        
        # parsing the HTML
        html_doc = req.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        target_elements = soup.find_all('td', class_ = 'xl70971')
        # remove prefix and suffix
        
        for i in range(len(target_elements)):
            target_elements[i] = trim_tags(str(target_elements[i]))
            
        # drop empty stuff
        while '' in target_elements:
            target_elements.remove('')
    
        # odd: code 
        code = target_elements[::2]
        # even: area name
        area = target_elements[1::2]


        # manipulating the area names
        province_dict = {}
        city_dict = {}
        
        # it's a one-time job
        for (code_element, area_element) in zip(code, area):
            if re.match('^\d{2}[0]{4}$', code_element):
                province_dict[code_element[:2]] = area_element
            elif re.match('^\d{4}[0]{2}$', code_element):
                city_dict[code_element[:4]] = area_element
            
        for i in range(len(area)):
            if re.match('^\d{2}[0]{4}$', code[i]):
                pass
            elif re.match('^\d{4}[0]{2}$', code[i]):
                area[i] = province_dict[code[i][:2]] + area[i]
            else:
                try:
                    area[i] = province_dict[code[i][:2]] + city_dict[code[i][:4]] + area[i]
                except KeyError:
                    area[i] = province_dict[code[i][:2]] + area[i]
        
        # hard code, put everything under the folder named MCA
        dirname = os.path.join(sys.argv[2], 'MCA')
        output_filename = os.path.join(dirname, '%s.csv' % time_version)
        print('--> %s' % output_filename, file=sys.stderr)

        if not os.path.exists(dirname):
            os.makedirs(dirname)
            
        # write up the output file
        with open(output_filename, 'w', encoding='utf8', newline='') as output_file:
            print('time_version,code,area', file=output_file)
            writer = csv.writer(output_file)
            version = [time_version] * len(code)
            writer.writerows(zip(version, code, area))
            
        output_file.close()    
    
    
if __name__ == '__main__':
    main()