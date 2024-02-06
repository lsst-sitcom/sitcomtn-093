#%%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import datetime as dt
import numpy as np
import os
pd.options.mode.chained_assignment = None

#Store the csv chronograf data into a pandas dataframe
df_path = os.path.join(os.getcwd(), '2023-10-18-09-52 Chronograf Data_all.csv') #put here the csv path
df = pd.read_csv(df_path)

#Creating the plots subfolder if it doesn't exists.
if not os.path.exists(os.path.join(os.getcwd(), 'plots')):
     os.mkdir(os.path.join(os.getcwd(), 'plots'))

# %%
#Setting the start and stop time (from the 14-15-06-23-M2-rigid-body-position-stability-testing-log)
seq_times = {
    'X':['22:44:40',
         '22:54:45',
         '23:04:50',
         '23:14:55',
         '23:25:00',
         '23:35:05'],
     
    'DRX':['20:34:49',
           '20:41:49',
           '20:48:49',
           '20:55:49',
           '21:02:50',
           '21:09:50'],

    'Y':['17:10:58',
         '17:21:03',
         '17:31:08',
         '17:41:13',
         '17:51:18',
         '18:01:23'],
     
    'DRY':['21:14:57',
           '21:21:57',
           '21:28:57',
           '21:35:57',
           '21:42:57',
           '21:49:57'],

    'Z':['19:36:28',
         '19:46:33',
         '19:56:38',
         '20:06:43',
         '20:16:48',
         '20:26:53'],

    'DRZ':['21:53:35',
           '22:00:35',
           '22:07:35',
           '22:14:35',
           '22:21:35',
           '22:28:35']
}

days = ['14-06-23','15-06-23']

#Converting the time column elements into real datetime objects
df['time'] = pd.to_datetime(df['time'])
# %%

#Setting some threshold and variable for the plateau detection algorithm
min_time_interval = 20
off_threshold = 0.3
rot_threshold = 0.05


plats = dict() #Dictionary that will contain all the DOF sequences statictics

dof_fig, dof_axs = plt.subplots(nrows=2, ncols=3)
dof_fig.suptitle('DOF Sequences') 
dof_fig.set_figheight(6)
dof_fig.set_figwidth(12)

#FOR cycle through the DOF
c=0
for key, val in seq_times.items():

     #if key not in ['DRX']:
     #     c += 1
     #     continue
     
     #Initialize a dictionary for each DOF into store the statistic for each sequence.
     plats[key] = dict()

     #setting the corresponding unit
     if key in ['X', 'Y', 'Z']:
          threshold = off_threshold
          units = '$\\mu$m'
     else:
          threshold = rot_threshold
          units = 'arcsec'

     #Selecting the right day (X was taken the day before all the other DOF)
     if key == 'X': day=days[0]
     else: day=days[1]

     #Selecting the column to evaluate from the dataframe, it changes for every DOF.
     df_maincol = list(df.columns)[1:][c]

     #Cycling over the sequences of a DOF
     for i, seq in enumerate(list(val)[:-1]):
          
          #Here a slice of the dataframe is made, to isolate only the time interval of the sequence
          t1 = pd.to_datetime(day+'T'+seq+'-04:00') #start time of the i-sequence
          t2 = pd.to_datetime(day+'T'+val[i+1]+'-04:00') #start time of the i+1-sequence
          data = df[(df['time'] > t1) & (df['time'] < t2)] #slicing the dataframe and storing it in a new variable
          
          #Here the absolute time column is converted into a relative time column (in seconds)
          data.loc[:, ('time')] = data['time']-t1
          data.loc[:, ('time')] = data['time'].dt.total_seconds()

          #Here a new columns are added:
          #    -diff: Column that contains the difference between each point and the next one
          #    -#plateau: Column that contains the plateau number whose the point belongs (initialize with nans)
          data.loc[:, ('diff')] = np.ediff1d(data[df_maincol].values, to_end=[np.nan])
          data.loc[:, ('#plateau')] = np.nan

          #First part of the plateau detection algorithm.
          #Search for points that still below a certain threshold
          #and associates a progressive number for each plateau found
          plat_number = 0
          new_index = -1
          for index, row in data.iterrows():
               if index < new_index:
                    continue
               if abs(row['diff']) < threshold:
                    new_index = index
                    plat_number += 1
                    for iindex, irow in data.loc[new_index:].iterrows():
                         if abs(irow['diff']) < threshold:
                              data.loc[new_index:iindex, '#plateau'] = plat_number
                         else:
                              new_index = iindex
                              break
          
          #Second part of the detection algorithm
          #It discards all the plateau with a time interval below a certian min temporal threshold.
          #This should be filter out all the non real plateau.
          n = 1
          for el in data['#plateau'].dropna().unique():
               eval_df = data[data['#plateau'] == el]
               if eval_df.loc[eval_df.index[-1], 'time'] - eval_df.loc[eval_df.index[0], 'time'] <= min_time_interval:
                    data.loc[eval_df.index[0]:eval_df.index[-1], ('#plateau')] = np.nan
               else:
                    data.loc[eval_df.index[0]:eval_df.index[-1], '#plateau'] = n
                    n += 1

          #Here the statistic of all plateau in each sequence is stored in the plats[key] dictionary.
          ipad = 50
          fpad = 10
          plats_number = data['#plateau'].dropna().unique()
          plats[key].update({i: [(pl,
                             np.mean(data[df_maincol][data['#plateau'] == pl].values[ipad:-fpad]), #mean valuea of the plateau
                             abs(np.max(data[df_maincol][data['#plateau'] == pl].values[ipad:-fpad]) - 
                             np.min(data[df_maincol][data['#plateau'] == pl].values[ipad:-fpad])), #PtV
                             np.std(data[df_maincol][data['#plateau'] == pl].values[ipad:-fpad]), #STD dev
                             len(data[df_maincol][data['#plateau'] == pl].values[ipad:-fpad])) for pl in plats_number]}) #Number of the sample used.
          
          #PLOTTING PART OF THE SCRIPT
          #All the plots will be saved in the path working_dri/plots/
          #Plotting the subplot with a one sequence for each DOF.
          #if i == 1:
          if c <= 2:
               j = 0
               k = c
          else:
               j = 1
               k = c-3

          dof_axs[j,k].plot(data['time'].values,
                    data[df_maincol].values,
                    markersize=0,
                    alpha=0.6,
                    label=seq,
                    lw=2.5)
          dof_axs[j,k].set_title(key)
          dof_axs[j,k].grid(True)
          dof_axs[j,k].legend(fontsize='small')
          dof_axs[j,k].set_xlabel('TimeDelta [s]')
          dof_axs[j,k].set_ylabel(f'DOF units {units}')
          
          #Plot for each sequence with the plateau found.
          #These are for debugging purposes.
          plat_df = data.dropna()
          pfig = plt.figure()
          pax = pfig.add_subplot()
          pax.plot(plat_df['time'].values, plat_df[df_maincol].values,
                   marker='+',
                   markersize=5.0,
                   lw=0.0,
                   color = 'red',
                   alpha=0.6,
                   label='plat value'
                    )
          pax.plot(data['time'].values, data[df_maincol].values,
                   label='DOF value', 
                   color='green',
                   linewidth=2.0,
                   alpha=0.4)
          
          pax.set_xlabel('sec')
          pax.set_ylabel(units)
          pax.legend()
          pfig.suptitle(f'{key} Seq-{i+1}')
          pfig.tight_layout()
          pfig.savefig(os.path.join(os.getcwd(), 'plots', f'{key}_{i}_plats.png'), dpi=300)
          #plt.show()
          plt.close(pfig)

     #Plots with the STD and PtV for each plateau of each sequence of each DOF
     pv_fig = plt.figure(f'Repetability along {key} axis', figsize=(12,6))
     pv_fig.suptitle(f'Repetability along {key} axis')
     pv_ax = pv_fig.add_subplot()

     seq_array = list()
     for _, val in plats[key].items():
          seq_array.append(val)
     seq_array = np.array(seq_array)

     cseq = cm.rainbow(np.linspace(0, 1, len(seq_array)))

     pvpl_list = list([[pvpl for _, _, pvpl, _, _, in sq]for sq in seq_array])
     stpl_list = list([[stpl for _, _, _, stpl, _, in sq]for sq in seq_array])

     iseq = 0
     for pvseq, stseq in zip(pvpl_list, stpl_list):
          pv_ax.plot(np.arange(1,len(pvseq)+1), pvseq,
                     marker='d',
                     markersize=10,
                     lw=0,
                     alpha=0.7,
                     color=cseq[iseq],
                     label=f'RBM PtV, Seq.{iseq+1}')
          
          #pv_ax.plot(np.arange(1,len(stseq)+1), stseq,
          #           alpha=0.7,
          #           color=cseq[iseq],
          #           label=f'RBM STD, Seq.{iseq+1}')
          iseq += 1

     #Highlighting the requirement          
     if key in ['X', 'Y', 'Z']:
          pv_ax.axhspan(1.0, 1.0, 0, 1,
                     color='blue', alpha=1.0, lw=2.0, zorder=2)
          pv_ax.annotate('Requirement', (pv_ax.get_xlim()[0]*1.05, 1.01),
                         color='blue', fontsize='large', fontweight='bold')
     else:
          pv_ax.axhspan(0.108, 0.108, 0, 1,
                     color='blue', alpha=1.0, lw=2.0, zorder=2)
          pv_ax.annotate('Requirement', (pv_ax.get_xlim()[0]*1.05, 0.110),
                         color='blue', fontsize='large', fontweight='bold')

     #Setting some reasonable fixed limits for the linear and rotation DOF.
     #This should be help to compare the statictic between the same kind of DOF. 
     if key in ['X', 'Y', 'Z']:
          pv_ax.set_ylim(-0.1, 1.1)
     else:
          pv_ax.set_ylim(-0.02, 0.13)

     pv_ax.legend(ncol=len(seq_array), loc='upper right', fontsize='medium')
     pv_ax.set_xlabel('Commanded position', fontsize='large', fontweight='semibold')
     pv_ax.set_ylabel(f'Repetability PtV, {units}', fontsize='large', fontweight='semibold')
     pv_ax.tick_params(axis='both', labelsize=15)
     pv_ax.grid()

     pv_fig.tight_layout()
     pv_fig.savefig(os.path.join(os.getcwd(), 'plots', f'{key}_PV.png'), dpi=300)
     plt.close(pv_fig)
     c+=1

dof_fig.tight_layout(pad=0.6)
dof_fig.savefig(os.path.join(os.getcwd(), 'plots', f'DOF_seq.png'), dpi=300)
plt.close(dof_fig)

#%%
#WRITING OUTPUT PART

#Here a dictionary is initialized and filled with the statistic (mean and PtV) 
#of the same plateaus through all the sequences of a DOF.
rms_test = dict()
for key, val in plats.items():
     val_array = np.array([seq for _, seq in val.items()])

     stat = [(np.mean(val_array[:,c,1]),
            abs(np.max(val_array[:,c,1])-
            np.min(val_array[:,c,1])))for c in range(val_array.shape[1])]
     
     rms_test[key] = stat

#Here a txt files with the statistic are written. They are saved in the same directiory of the script
#    - stat.txt: contain mean and PtV of the same plateau through all the sequences.
#    - stat_single_seq.txt: contain mean, PtV, stddev and #sample of each plateau in each sequence. 
with (open(os.path.join(os.getcwd(), 'stat.txt'), 'w') as stat_file, 
      open(os.path.join(os.getcwd(), 'stat_single_seq.txt'), 'w') as stat_ss_file):
     for key, val in rms_test.items():
          stat_file.write(f'\n#{key}\n')
          stat_file.write('PLATEAU NUMBER\tPLATEAU MEAN\tPV\n')
          for i, row in enumerate(val):
               stat_file.write(f'\n{i+1}\t{row[0]}\t{row[1]}')
          stat_file.write('\n')
     
     for key, val in plats.items():
          stat_ss_file.write(f'\n\n#{key}')
          for seq_key, seq in val.items():
               stat_ss_file.write(f'\n\nSequence number:{seq_key}\n')
               stat_ss_file.write('PLATEAU NUMBER\tPLATEAU MEAN\tPV\tTDV_DEV\tSAMPLE')
               for row in seq:
                    for i, el in enumerate(row):
                         if i == 0:
                              stat_ss_file.write(f'\n{el}')
                         else:
                              stat_ss_file.write(f'\t{el}')