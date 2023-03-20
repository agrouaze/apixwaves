import os

PROJECT_DIR_DATARMOR = '/home/datawork-cersat-public/cache/project/mpc-sentinel1/'
PROJECT_DIR_DATARMOR_ALT = '/home/datawork-cersat-public/project/mpc-sentinel1/'
datarmor_archive_esa_ifremer = os.path.join(PROJECT_DIR_DATARMOR_ALT,"data","esa")
data_dir_s1a = os.path.join(PROJECT_DIR_DATARMOR,'data','esa','sentinel-1a')
data_dir_s1b = os.path.join(PROJECT_DIR_DATARMOR,'data','esa','sentinel-1b')
dir_data = {'S1A':data_dir_s1a,
            'S1B':data_dir_s1b}
sats_acro = {'S1A':'sentinel-1a'
             ,'S1B':'sentinel-1b'}
DIR_L2 = "/home/datawork-cersat-public/provider/cnes/satellite/l2/cfosat/swim/swi_l2____/op06/6.1.0/"