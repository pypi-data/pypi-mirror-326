'''
    Rosetta version 3-alpha (3a) 
    Pedotransfer functions by Schaap et al., 2001 and Zhang and Schaap, 2016.
    Copyright (C) 2016  Marcel G. Schaap

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    Marcel G. Schaap can be contacted at:
    mschaap@cals.arizona.edu

'''

#running this script:

# python Rpredic.py -h                                              # provides help
# python Rpredict.py --predict                                      # gets predictions with summary results  (MySQL DB implied)
# python Rpredict.py --predict  --sqlite=./sqlite/Rosetta.sqlite     # gets predictions with summary results  (sqlite, no MySQL)
# python Rpredict.py --predict  --raw                               # gets raw predictions (MySQL DB implied)

###########################################################################################################################################
#### Inputs to change based on the required Module & paths at your local PC

import csv
# Change the following number to the model you like to run
chosen_model = 5
# Change the following to the folder path of that has the Rosetta python files at your local pc
# folder_path_python_files = ROSETTA3_DIR # r'C:\MSU\Rosetta 3 and ros file'
# Change the following to the full file path of your input file at your local pc, it can be xls, xlsx, or space separated txt file
# Change the following to the output folder, parent directory has to be already existing
# output_folder = STEP_A_OUT_DIR_2# r'C:\MSU\Rosetta 3 and ros file\output/'
tortuosity = 0.50000
max_root_depth = 45 
effective_root_depth = 30
roots_layer = 1 # The layer number that has the majority of the roots
''' For the created ros file the tortuosity is set to a constant user specified value (originally 0.5)
. Also for each soil layer, the matching point at saturation K0 is set equal to the saturated hydraulic conductivity
. These assumptions were used based on DRAINMOD manual'''
create_ros_file = 1 # enter 1 if you want to create the ros files and 0 otherwise
###########################################################################################################################################
#tested on python 3.8.5
import os  
import numpy as N
import argparse
import pandas as pd
import datetime as dt
import time as T
from contextlib import closing
from cigsatbuf_utils.rosetta3.ANN_Module import PTF_MODEL
from cigsatbuf_utils.rosetta3.DB_Module import DB


parser = argparse.ArgumentParser(description='Rosetta 3 pedotransfer function interface example.')
parser.add_argument('--host', default='localhost', help='MySQl host')
parser.add_argument('--user', default='root', help='MySQl username')  # you want to change the username
parser.add_argument('--db', default='Rosetta', help='MySQl database')
parser.add_argument('--predict', action='store_true', help='get data and predict')
parser.add_argument('--check', action='store_true', help='check prediction (for development only)')
parser.add_argument('--raw', action='store_true', help='get raw data')
parser.add_argument('--sqlite', default='', help='sqlite path (ignores MySQL options)')  #using this option will ignore the mysql options.
parser.add_argument('-i', '--input', action='store', help='input from file ')
parser.add_argument('-o','--output', action='store', help='store predicted data')



def run(input_txt_file_path, output_folder, rosetta_dir):

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    if os.path.splitext(input_txt_file_path)[-1] in ['.xls', '.xlsx']:
        all_data = pd.read_excel(input_txt_file_path)

    elif os.path.splitext(input_txt_file_path)[-1] == '.csv':
        all_data = pd.read_csv(input_txt_file_path, header=0).dropna(how='all', axis=1)

    elif os.path.splitext(input_txt_file_path)[-1] == '.txt':
        all_data = pd.read_csv(input_txt_file_path, sep=" ", header=None).dropna(how='all', axis=1)

    all_data.columns = ['sand', 'silt', 'clay', 'bd', 'fc', 'pwp', 'mukey', 'cokey', 'layer', 'muname', 'ksat_r',
                        'resdept_r', 'wsatiated_r']
    all_data[['fc', 'pwp']] = all_data[['fc', 'pwp']] / 100.0
    data_in = all_data.drop(['mukey', 'cokey', 'layer'], axis=1).to_numpy().transpose()
    data_in = data_in[0:chosen_model + 1, ]

    # sqlite_file_path = r'{}/Rosetta.sqlite'.format(ROSETTA3_DIR)
    sqlite_file_path = r'{}/Rosetta.sqlite'.format(rosetta_dir)

    args = argparse.Namespace(check=False, db='Rosetta', host='localhost', input=input_txt_file_path,
                              output='output file path',
                              predict=True, raw=False, sqlite=sqlite_file_path, user='root')

    if args.predict:
        # host, user and db_name need to be named or None, even when using sqlite.
        # the block below could be integrated in other code.
        with DB(host=args.host, user=args.user, db_name=args.db, sqlite_path=args.sqlite) as db:

            print("Getting models from database")
            T0=T.time()

            #IMPORTANT LINE!!!
            ptf_model=PTF_MODEL(chosen_model, db)
            #if predicting multiple times, keep the ptf_model object around, otherwise you'll be hitting the DB a lot.

            print("Getting models from database, done (%s s)" % (T.time()-T0))

            data = data_in
            print (data)
            #IMPORTANT: note transpose if a model has 3 input variables and predictions need
            # to be made for N samples, the data array must have the shape (3,N)
            # NOT N,3.
            # this is due to a Matlab convention how input and output are dimensionalized
            # (and contrary to intuition!)

            T0 = T.time()
            print("Processing")
            # Development - may be needed for detecting numerical errors
            #N.seterr(over='raise') # debug or new model

            if not args.raw:
                # At UA we've been playing with levi-distributions to characterize the shape of the estimated distributions
                # This is NOT ready for general use (and it may never be because the estimation of levi distributions is somewhat unstable)
                # Below we print means (which is what most people want), stdv (uncertainty),
                # as well as skewness and kurtosis (which may NOT be reliable)
                # the covariance is also printed as a 3D matrix
                # shape of mean,stdev,skew,kurt: (nout,nsamp)
                # shape of cov: (nout,nout,nsamp)

                # Added by J - create a dic of map unit name unique to each combination of mukey-cokey
                muname_dic = dict()
                muname_df = all_data[['mukey', 'cokey', 'muname']]
                for k,c, m in zip(muname_df['mukey'], muname_df['cokey'], muname_df['muname']):
                    idm = str(k) + '_' + str(c)
                    muname_dic[idm] = m

                #IMPORTANT LINE!!!
                values_column = ['sand','silt','clay','bd','fc','pwp', 'ksat_r', 'resdept_r', 'wsatiated_r']
                multi_df = all_data.pivot_table(index=['mukey', 'cokey', 'layer'], values=values_column)
                mukeys_list = multi_df.index.get_level_values(0).unique()
                # munames_list = multi_df.index.get_level_values(1).unique()
                # multi_df = multi_df.droplevel(level=1, axis=0)
                cur_used_columns = []
                for acol in values_column:
                    if acol in multi_df.columns:
                        cur_used_columns.append(acol)
                # for mukey, muname in zip(mukeys_list, munames_list):
                for mukey in mukeys_list:
                    cokeys_list = multi_df.loc[mukey].index.get_level_values(0).unique()
                    for acokey in cokeys_list:
                        cur_df = multi_df.loc[mukey].loc[acokey][cur_used_columns]
                        layers = multi_df.loc[mukey].loc[acokey].index.get_level_values(0)
                        num_of_layers = len(layers)
                        data = cur_df.to_numpy().transpose()
                        data = data[0:chosen_model+1,]
                        print("current data is \n {}".format(data))
                        res_dict = ptf_model.predict(data,sum_data=True)
                        # with sum_data=False you get the raw output WITHOUT Summary statistics
                        # res_dict['sum_res_mean'] output log10 of VG-alpha,VG-n, and Ks

                        print("Processing done (%s s)" % (T.time()-T0))
                        vgm_name=res_dict['var_names']
                        print(vgm_name)
                        vgm_mean=res_dict['sum_res_mean']
                        vgm_new=N.stack((vgm_mean[0],vgm_mean[1],10**vgm_mean[2],10**vgm_mean[3],10**vgm_mean[4]))
                        vgm_new=vgm_new.transpose()
                        print(vgm_new)

                        # vgm_new = vgm_new.round(5)
                        vgm_new_df = pd.DataFrame(vgm_new)
                        vgm_new_df['layers'] = layers
                        vgm_new_df=vgm_new_df[['layers',0,1,2,3,4]]
                        vgm_new_df = vgm_new_df.sort_values(by=['layers'])
                        vgm_new_df[5] = vgm_new_df[4]
                        vgm_new_df[6] = tortuosity

                        # output estimation
                        cur_output_folder = r'{}/{}_{}/'.format(output_folder, mukey, acokey)
                        if not os.path.exists(cur_output_folder):
                            os.mkdir(cur_output_folder)
                        cur_output_file_path = r'{}/{}_{}.txt'.format(cur_output_folder, mukey, acokey)
                        N.savetxt(cur_output_file_path, vgm_new_df[['layers',0,1,2,3,4]].to_numpy(), delimiter=',',fmt='%3i %.5f %.5f %.5f %.5f %.5f')

                        if create_ros_file:
                            # cur_output_ros_path = r'{}/{}_{}_setpB.ros'.format(cur_output_folder, mukey, acokey)
                            cur_output_ros_path = r'{}/{}_{}.ros'.format(cur_output_folder, mukey, acokey)
                            outfile = open(cur_output_ros_path, 'wt')
                            # outfile.write('{} layers - mukey: {} - Component : {} - Rosetta3 Module {}\n'.format(num_of_layers, mukey, acokey, chosen_model)
                            muname = muname_dic[str(mukey) + '_' + str(acokey)]
                            outfile.write('{} layers - Mukey: {} - Cokey: {} - {}\n'.format(num_of_layers, mukey, acokey, muname))
                            outfile.write('0{} 1\n'.format(num_of_layers))
                            outfile.close()

                            with open(cur_output_ros_path, 'a') as fobj:
                                N.savetxt(fobj, vgm_new_df[['layers', 0, 1, 2, 3, 4, 5, 6]].to_numpy(),
                                          delimiter=',', fmt='%-3i     %10.5f     %10.5f     %10.5f     %10.5f     %10.5f     %10.5f     %10.5f', )
                                fobj.write('{}, {}, {}'.format(max_root_depth, effective_root_depth, roots_layer))


                            # vgm_new_df.to_csv(cur_output_ros_path, header=None, index=None, sep=' ', mode='a',  )
                            # outfile = open(cur_output_ros_path, 'a')
                            # outfile.write('{}, {}, {}'.format(max_root_depth, effective_root_depth, roots_layer))
                            # outfile.close()

            else:
                # we requested raw input.  You'll need to process these yourself.

                res_dict = ptf_model.predict(data,sum_data=False)
                #shape: (nboot,nout,nsamp)
                #Warning: old rosetta (models 102..105) can ONLY provide retention parameters (not Ks)
                #New models (2..5) provide retention+ks
                #This is because the retention and ks models are synchronized in the new models wheras they were calibrated on different datasets in the old model
                # nboot is 1000, output is log10 of VG-alpha,VG-n, and Ks
                #print(res_dict['res'][0])
                #print(N.shape(res_dict['res'][0]))

