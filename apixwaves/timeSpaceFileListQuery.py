#!/usr/bin/env python
"""
code from fpaul to retrieve the file list of a given spatio-temporal selection in datavore
history:
    march2018: agrouaze fix issue
usage:
    sentinel1_getfilelist_s1_WV_datavore.py --bbox='158,-30,185,0' --satellite S1A -d='20140701010101,20170106112608' --debug > /tmp/toto.txt
  
"""
import os
import sys
import json
import requests
import argparse
import logging
from datetime import datetime
import collections
import get_full_path_from_measurement
#sys.path.append('/home1/datahome/satwave/sources_en_exploitation2/cfosat-calval-exe/')
sys.path.append('/home1/datahome/agrouaze/git/cfosat-calval-exe/')
from get_file_l2cwwic_from_date import get_filepathl2cwwic_from_date,get_filepathl2cwwic_from_date_interval
logging.basicConfig()
logging.getLogger().setLevel(logging.WARNING)
log = logging.getLogger('getlisting_sentinel')
log.setLevel(logging.INFO)
    
# sys.path.insert(0, '/home/losafe/users/fpaul/_Tests/PyQt')
#sys.path.insert(0,'/home/satwave/sources_en_exploitation/mpc-sentinel/mpc-sentinel/mpcsentinellibs/indexation_in_hbase')
#import hbaserequests as hbr

def cmdlineparser():
    parser = argparse.ArgumentParser(description='Get TIFF listing for sentinel-1 based on datavore index')
    parser.add_argument('--bbox', '-b',
          default=None, help='latmin,lonmin,latmax,lonmax(eg 30,-30,-30,10)',
          required=True)
    parser.add_argument('--date-interval', '-d', 
          default=None, help='YYYYMMDDHHMMSS,YYYYMMDDHHMMSS (eg 20140101010101,20170106112608)',
          required=True)
    parser.add_argument('--satellite', '-s',
          default='S1A', help='S1A or S1B or CFO')
    parser.add_argument('--debug',
          action='store_true', default=False,
          help='Debug logs')

    return parser.parse_args()

def main():
    args = cmdlineparser()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    log.debug('Arg bbox : %s'%(args.bbox))
    log.debug('Arg date_interval : %s'%(args.date_interval))
    log.debug('Arg satellite : %s'%(args.satellite))
    
    #coord = '-24.960937667638063,29.688052749856798,-20.742187667638063,32.694865977875075'
    #dateinterval = '20140101010101,20170106112608'
    coord = args.bbox
    dateinterval = args.date_interval
    
    # PAS BON url = 'http://datavore.ifremer.fr/#/s1quicklook?r=-30.761718917638063,30.44867367928756,-28.476562667638063,32.54681317351514&dt=20140101010101,20170106112608'
    #url = 'http://br156-136.ifremer.fr:8000/datavore/public/all%3C/sss/-24.960937667638063,29.688052749856798,-20.742187667638063,32.694865977875075/20140101010101,20170106112608/filelist/?dl=0&inv=null&filters={%22ww3_hs_cutoff%22:{%22min%22:null,%22max%22:null},%22ecmwf_windspeed%22:{%22min%22:null,%22max%22:null},%22oswIncidenceAngle%22:{%22min%22:null,%22max%22:null}}'
    if False:
        url = 'http://br156-136.ifremer.fr:8000/datavore/public/all%3C/sss/'
        url += '%s/%s/'%(coord, dateinterval)
        url += 'filelist/?dl=0&inv=null&filters={%22ww3_hs_cutoff%22:{%22min%22:null,%22max%22:null},%22ecmwf_windspeed%22:{%22min%22:null,%22max%22:null},%22oswIncidenceAngle%22:{%22min%22:null,%22max%22:null}}&limit=null'
    else:
        #url = 'http://br156-136.ifremer.fr:8000/datavore/public/S1A%3C,S1B,CFO%3C/sss/-180,-90,180,90/20140101010101,20200306120106/sentinel1AndCFOSatData/?filters=ROUGHNESSINDEXED|=|True$IMAGINARYINDEXED|=|True$REALINDEXED|=|True$FULLINDEXED|=|True$SENSOR|Contains|S1A*WV_MODE|Equal|wv1$SENSOR|Contains|S1A*WV_MODE|Equal|wv2$SENSOR|Contains|S1B*WV_MODE|Equal|wv1$SENSOR|Contains|S1B*WV_MODE|Equal|wv2$&cfoFilters='
        #url = 'http://br156-136.ifremer.fr:8000/datavore/public/%s</sss/'%args.satellite
        url = 'https://xwaves-services.ifremer.fr/datavore/exp/datavore/public/S1A%3C,S1B/sss/'
        #url += '%s/%s/'%(coord, dateinterval)
        url += '%s/%s/true/false/sentinel1AndCFOSatData/'%(coord, dateinterval)
        #url += 'filelist/?dl=0&inv=null&filters=null&limit=null'
        if False:
            complement_sensor = "$SENSOR|Contains|%s*WV_MODE|Equal|wv1$SENSOR|Contains|%s*WV_MODE|Equal|wv2$"%(args.satellite,args.satellite )
            url += 'sentinel1AndCFOSatData/?filters=ROUGHNESSINDEXED|=|True$IMAGINARYINDEXED|=|True$REALINDEXED|=|True$FULLINDEXED|=|True'+complement_sensor+'&cfoFilters=&limit=500'
        logging.debug('url = %s',url)
    searchresult0 = json.loads(requests.get(url).content)
    searchresult = json.loads(searchresult0['S1CFO'])
    print('searchresult',type(searchresult))
    # ci = hbr.CersatIndexClient()
    cnt = collections.defaultdict(int)
    cfolist = []
    logging.debug('type content paylaod : %s',type(searchresult))
    for i in searchresult:
        logging.debug('i = %s length = %s',i,len(i))
        #fileid, startdate, coords, satellite,polygon,latcenter,loncenter = i
        if args.satellite=='CFO':
            startdate,stopdate,empty,satellite,polygon,lat,lon,wv,classif,hstot,uuidtiff,uuidocn,classlabel_classscore,stamp = i
            dt = datetime.strptime(startdate,'%Y%m%d%H%M%S%f')
            # fullpath = get_filepathl2cwwic_from_date(dt,delta_seconds_threshold = 2)
            fullpath = get_filepathl2cwwic_from_date_interval(dt)
            if fullpath not in cfolist:
                go_echo = True
            else:
                go_echo = False
            if fullpath is not None and fullpath not in cfolist:
                cfolist.append(fullpath)

        else:
            go_echo = True

            startdate,stopdate,empty,satellite,polygon,lat,lon,wv,classif,hstot,tiffsubpath,ocnsubpath,classlabel_classscore,stamp = i
            #startdate, stopdate, empty, satellite, polygon, lat, lon, wv, classif, hstot, uuidtiff, uuidocn, classlabel_classscore, stamp = i
            logging.debug('sat = %s',satellite)
            if satellite==args.satellite:
                safebase,measu_base = ocnsubpath.split('/')
                fullpath = get_full_path_from_measurement.get_full_path_with_safe_and_measu(safebase,measu_base)
        if fullpath is not None and go_echo:
            print(fullpath)
#         if satellite != args.satellite:
#             continue
#         rowkey = '%sWV.v3#DT#%s#%s'%(satellite,startdate,fileid)
#         log.debug( rowkey )
# #         print "content",ci.table_collectionfiles.row(rowkey).keys()
#         if 'cf:fpath' in ci.table_collectionfiles.row(rowkey).keys():
#             filepath_indexed = ci.table_collectionfiles.row(rowkey)['cf:fpath']
#             if os.path.exists(filepath_indexed):
#                 print( filepath_indexed)
#                 cnt['found'] += 1
#             else:
#                 replaced = filepath_indexed.replace('/home/cercache','/home/datawork-cersat-public/cache')
#                 if os.path.exists(replaced):
#                     print(replaced)
#                     cnt['found'] += 1
#                 else:
#                     cnt['not_found'] += 1
#                     print('not found example',filepath_indexed)
#         else:
#             cnt['no_fpath'] += 1
#             print("strf satellite != args.satellite:
#             continue
#         rowkey = '%sWV.v3#DT#%s#%s'%(satellite,startdate,fileid)
#         log.debug( rowkey )
# #         print "content",ci.table_collectionfiles.row(rowkey).keys()
#         if 'cf:fpath' in ci.table_collectionfiles.row(rowkey).keys():
#             filepath_indexed = ci.table_collectionfiles.row(rowkey)['cf:fpath']
#             if os.path.exists(filepath_indexed):
#                 print( filepath_indexed)
#                 cnt['found'] += 1
#             else:
#                 replaced = filepath_indexed.replace('/home/cercache','/home/datawork-cersat-public/cache')
#                 if os.path.exists(replaced):
#                     print(replaced)
#                     cnt['found'] += 1
#                 else:
#                     cnt['not_found'] += 1
#                     print('not found example',filepath_indexed)
#         else:
#             cnt['no_fpath'] += 1
#             print("strange entry in index",fileid)

    log.info('Number of results : %s'%(cnt))
    

if __name__ == '__main__':
    main()
