from ftplib import FTP
import datetime
from datetime import date, timedelta
import os as os
import shutil as shutil

ftp = FTP('wp12373544.server-he.de')
ftp.login('ftp12373544-data', '!JaTzVAKMslTkGT6')
ftp.cwd('Messnetz')
filelist=ftp.nlst()


date_e =  datetime.datetime.now()
date_b = date_e -  datetime.timedelta(days = 1)

for fle in filelist:
    
    try:
        shutil.rmtree('Data/' + fle) 
    except:
        print("Folder doesn't exists")
    os.mkdir('Data/' + fle)

    try: 
        ftp.cwd(fle)
#        print(ftp.nlst())
        for sfle in ftp.nlst():
            try:
                ftime = datetime.datetime.strptime(sfle[:10],'%Y-%m-%d')
                if ftime >= date_b and ftime <= date_e:
                    print(sfle)
                    #filename = '2018-04-01-OPC-001.dat'
#                    try:
#                        with open('Data/'  + fle + '/' + sfle, 'wb') as local_file:
#                            ftp.retrbinary('RETR ' + sfle, local_file.write)
#                    except Exception as e:
#                        print(e)
#                        pass
                    handle = open('Data/'  + fle + '/' + sfle , 'wb')
                    ftp.retrbinary('RETR ' + sfle, handle.write)
                    #print(sfle)
#                    handle.close()
            except Exception as e:
                print(e)
        ftp.cwd('../')
    except Exception as e:
        print(e)
    
#ftp.cwd('OPC-001') 
#filelist=ftp.nlst()
#print(filelist)




#filename = '2018-04-01-OPC-001.dat'
#handle = open(filename, 'wb')
#ftp.retrbinary('RETR ' + filename, handle.write)
