from ftplib import FTP
import sys
import datetime
from datetime import date, timedelta
import os as os
import shutil as shutil
import calendar
# sys.path.append('/home/hdr/PycharmProjects/meteo_parser/venv/lib/python3.5/site-packages')
# print(sys.path)
ftp = FTP('wp12373544.server-he.de')
ftp.login('ftp12373544-data', '!JaTzVAKMslTkGT6')
ftp.cwd('Messnetz')
filelist=ftp.nlst()


date_e =  datetime.datetime.now()
print(date_e)
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
                modify_t_utc = datetime.datetime.strptime(ftp.voidcmd('MDTM %s'%sfle)[4:].strip(),'%Y%m%d%H%M%S')


                timestamp = calendar.timegm(modify_t_utc.timetuple())
                modify_t_local = datetime.datetime.fromtimestamp(timestamp)
                # assert modify_t_utc.resolution >= timedelta(microseconds=1)
                # modify_t_local = modify_t_local.replace(microsecond=modify_t_utc.microsecond)
                modify_t_local = modify_t_local.replace(hour=0,minute=0,second=0)




                if modify_t_local>=date_b and modify_t_local<=date_e:
                    print(modify_t_local)
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
