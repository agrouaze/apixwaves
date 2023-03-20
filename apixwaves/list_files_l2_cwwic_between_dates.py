import logging
import glob
import os
from dateutil import rrule
import datetime
from apixwaves.conf import DIR_L2
#import netCDF4
import xarray as xr
def list_l2_swim_between_dates(sta,sto,raffine_on_time=False):
    """
    :args:
        sta (datetime): acquisition date
        sto (datetime): 
    :returns:
        avail_prod (list): contains full path
    """
    logging.info('DIR_L2 = %s',DIR_L2)
    avail_prod = []
    raffined_list = []
    suffix = '*.nc'
    
    logging.debug('%s to %s',sta,sto)
#     if sta==sto:
#         sto += datetime.timedelta(days=1)
    for dd in rrule.rrule(rrule.DAILY,dtstart=sta,until=sto):
        pattern = os.path.join(DIR_L2,dd.strftime('%Y'),dd.strftime('%j'),suffix)
        logging.debug('pat = %s',pattern)
        list_tmp = sorted(glob.glob(pattern))
        if raffine_on_time:
            logging.debug('raffine with time')
            for ff in list_tmp:
                logging.debug('test : %s',ff)
                #nc = netCDF4.Dataset(ff)
                ds = xr.open_dataset(ff)
                #stadata = nc.getncattr('time_coverage_start')
                #stodata = nc.getncattr('time_coverage_end')
                stadata = ds.time_coverage_start
                stodata = ds.time_coverage_end
                stadatadt = datetime.datetime.strptime(stadata,'%Y-%m-%dT%H:%M:%SZ')
                stodatadt = datetime.datetime.strptime(stodata,'%Y-%m-%dT%H:%M:%SZ')
                #nc.close()
                logging.debug('stadatadt : %s stodatadt: %s ',stadatadt,stodatadt)
                if ((stadatadt>=sta) & (stadatadt<=sto)) | ((stodatadt>=sta) & (stodatadt<=sto)) | ((sta>=stadatadt) & (sto<=stodatadt)):
                    raffined_list.append(ff)
            list_tmp = raffined_list
        avail_prod += list_tmp
        logging.debug('dd= %s length = %s + %s',dd,len(avail_prod),len(list_tmp))
    logging.debug('final %s files found',len(avail_prod))
    return avail_prod
    
if __name__ =='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='list SWIM L2 CWWIC')
    parser.add_argument('--verbose', action='store_true',default=False)
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)-5s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
    else:
        logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)-5s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
    sta = datetime.datetime(2018,12,20)
#     sto = datetime.datetime(2018,12,20)
    sta = datetime.datetime(2019,3,2)
    sto = datetime.datetime(2019,3,3)
#     version_base = 'v0.2'
#     version_proc = '0.2.1'
#     version_proc = None
    res = list_l2_swim_between_dates(sta,sto)
#     print(res)
    print('nb %s'%(len(res)))