from apixwaves.list_files_l2_cwwic_between_dates import list_l2_swim_between_dates
from datetime import timedelta,datetime
import netCDF4
import logging
import numpy as np
import os
def get_filepathl2cwwic_from_date(dt,delta_seconds_threshold=2):
    """

    :param dt: datetime
    :return:
    """

    sta = dt-timedelta(hours=2)
    sto = dt+timedelta(hours=2)
    lists = sorted(list_l2_swim_between_dates(sta,sto))
    alldates = None
    res = None
    idx = None

    for ff in lists:
        logging.info('ff = %s',ff)
        nc = netCDF4.Dataset(ff)
        vartime = nc.variables['time_spec_l2']
        nr_units = vartime.units
        nr_units = nr_units.replace('s+us','seconds')
        timeseeknum = netCDF4.date2num(dt,nr_units)
        # nr_fac = 0.001
        nr_fac = 1e-6
        time_coarse = vartime[:,:,0].ravel()
        time_microsec = vartime[:,:,1].ravel()
        numerical_values = time_coarse + (time_microsec) * nr_fac
        #logging.debug('num = %s',numerical_values)
        nc.close()

        if timeseeknum in numerical_values or (abs(numerical_values-timeseeknum)<delta_seconds_threshold).any():
            res = ff
            if timeseeknum not in numerical_values:
                idx = np.where(abs(numerical_values-timeseeknum)<delta_seconds_threshold)
            else:
                logging.debug('exact match!')
            break
    if res is None:
        logging.info('no matching file with file date...')
    else:
        if idx is not None:
            logging.debug('closest date found = %s',netCDF4.num2date(numerical_values[idx],nr_units))
    return res

def get_filepathl2cwwic_from_date_interval(dt):
    """

    :param dt:
    :return:
    """

    sta = dt-timedelta(hours=2)
    sto = dt+timedelta(hours=2)
    lists = sorted(list_l2_swim_between_dates(sta,sto))
    alldates = None
    res = None
    idx = None

    for ff in lists:
        startdt = datetime.strptime(os.path.basename(ff).split('_')[9],'%Y%m%dT%H%M%S')
        stopdt = datetime.strptime(os.path.basename(ff).split('_')[10].replace('.nc',''),'%Y%m%dT%H%M%S')
        logging.debug('%s %s',startdt,stopdt)
        if dt>=startdt and dt<=stopdt:
            res = ff
            break
    if res is None:
        logging.info('no matching file with file date...')
    return res


if __name__ =='__main__':

    import argparse
    parser = argparse.ArgumentParser(description='my title')
    parser.add_argument('--verbose', action='store_true',default=False)
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)-5s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
    else:
        logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)-5s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
    dt = datetime(2020,2,12,6,26,58,90761)
    res = get_filepathl2cwwic_from_date(dt)
    res2 = get_filepathl2cwwic_from_date_interval(dt)
    print(res)
    print('res2',res2)
