'''
Created on Feb 3, 2014
This code converts from the klm like hierarchical csv format used by junar open data platform 
to a flat csv format. 
The script reads in a junar csv and emits a standard csv, paths given by fnamein and fnameout
Code tested with Sacramento Cites locations-of-city-trees.csv and PARKI-SPACE.csv
@author: jay venti
Created for codw4sac a Code 4 America brigade
'''
#fnamein  = "D:\Storage\Project and Reasch\Work Consulting\Code Sacramento\sac city apis\PARKI-SPACE.csv"
#fnameout = "D:\Storage\Project and Reasch\Work Consulting\Code Sacramento\sac city apis\gen-PARKI-SPACE.csv"
fnamein  = "D:\Storage\Project and Reasch\Work Consulting\Code Sacramento\sac city apis\80137-locations-of-city-trees.csv"
fnameout = "D:\Storage\Project and Reasch\Work Consulting\Code Sacramento\sac city apis\gen-locations-of-city-trees.csv"

from time import gmtime, strftime
#from pprint import pprint

def htmlstr2rowheaderstr(htmlstring):
    from bs4 import BeautifulSoup  # @UnresolvedImport
    soup = BeautifulSoup(htmlstring)    #MAKE THE SOUP OBJECT
    delm ='"'   #CREATE A DLM VAR, VALUE = DOUBLE QUOTATION MARK
    key = ''    #CREATE A VAR NAMED KEY, INIT AS STR
    i =0        #CREATE COUNTER VAR NAMED I, SET TO ZERO
    for tables in soup.find_all('table'):
        i +=1
        if i > 1000 : break     #JUST IN CASE, IF >1000 TABLES, STOP.. SOMETHING MAY BE WRONG
        rowstr = '';            #CREATE ROWSTR VAR, INIT AS EMPTY STRING
        # if first row has data, then process this table 
        for trow in tables.find_all('tr'): # get each table row
            tds = trow.find_all('td')
            if len(tds) == 2 : # then first row has a key vale pair
                key = tds[0].text

                # print key + " = " + val
                # fillin column entries
                rowstr = rowstr + delm + key.encode('utf-8') + delm  +','
            # if first or any other html row has other than 2 elements
            else : break  
        # last key val pair 
    # last html table
    rowstr = rowstr.rstrip(',') #REMOVE THE LAST COMMA SINCE IT IS A ONE OFF
    return rowstr               #RETURN THE RESULTING STRING OF HEADERS

def htmlstr2rowdatastr(htmlstring):
    from bs4 import BeautifulSoup  # @UnresolvedImport
    soup = BeautifulSoup(htmlstring)
    delm ='"'
    val = ''
    i =0
    for tables in soup.find_all('table'):
        i +=1
        if i > 1000 : break
        rowstr = '';
        # if first row has data, then process this table 
        for trow in tables.find_all('tr'): # get each table row
            tds = trow.find_all('td')
            if len(tds) == 2 : # then first row has a key vale pair
                
                val = tds[1].text
                if val == '<Null>': val = 'NULL'
                # print key + " = " + val
                # fillin column entries
                rowstr = rowstr + delm + val.encode('utf-8')+delm  + ','
            # if first or any other html row has other than 2 elements
            else : break  
        # last key val pair 
    # last html table
    rowstr = rowstr.rstrip(',')
    return rowstr

def sumtagfrq(row,tgfrq):
    for key in row:
        if key not in tgfrq:
            tgfrq[key.encode('utf-8')] = 0
        tgfrq[key.encode('utf-8')] += 1
    return tgfrq

import csv
delm ='"'
csvfile = open(fnamein, "rb")
reader = csv.reader(csvfile)
print strftime("%b %d %Y %H:%M:%S", gmtime()), 'reader'
print
csvout = open(fnameout, "w")
rownum = 0
csvheadstr = ''
csvdatastr = ''
firsthit = True
for row in reader: 
    if rownum == 0:
        header = row
        # Save header row but omits the hierarchical element 'Description' from csvheadstr output string
        for e in row: 
            if e != 'Description':
                csvheadstr = csvheadstr + delm + e + delm + ','
    else:
        colnum = 0
        csvdatastr = ''
        for col in row:
            #print '%-8s: %s' % (header[colnum], col)
            if header[colnum]=='Description': # processes a hierarchical element stored within the html code
                if firsthit == True: # the first time record the rest of the csvheadstr header string
                    csvheadstr = csvheadstr + htmlstr2rowheaderstr(col)
                    #print  csvheadstr
                    csvout.write(csvheadstr+'\n')
                    firsthit = False
                csvdatastr = csvdatastr + htmlstr2rowdatastr(col)
                #print  csvdatastr
                csvout.write(csvdatastr+'\n')
            else: # processes the non-hierarchical non-html elements
                csvdatastr = csvdatastr + delm+col.encode('utf-8')+delm + ','
            colnum += 1
    if rownum % 1000 == 0 : #to test on a limited run set 0 t0 999 and uncommon to the break below
        print 'rownum =',rownum
        print strftime("%b %d %Y %H:%M:%S", gmtime()), 'write'
        #break     
    rownum += 1
  
csvfile.close()
csvout.close()
