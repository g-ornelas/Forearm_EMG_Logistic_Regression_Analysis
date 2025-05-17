## This python file contains all of the plotting functions used in the jupyter notebook. 

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay
import numpy as np

def plot_time_series_needle(nDQ_data, nDC_data, n_time): 
    fig, axs = plt.subplots(1,2, figsize=(15,3), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.2, wspace= .2) 
    axs[0].plot(n_time, nDQ_data, color='green')
    axs[0].set_title('Needle at DQ')
    axs[0].set_xlabel('Time $(s)$')

    axs[1].plot(n_time, nDC_data, color='orange')
    axs[1].set_title('Needle at DC')
    axs[1].set_xlabel('Time $(s)$')
    fig.text(0.04, 0.5, 'Amplitude', va='center', rotation='vertical',fontsize=18)
    
def plot_time_series_surface(s_data, s_time): 
    fig, axs = plt.subplots(2,4, figsize=(20,10), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.2, wspace= .2) #this is to establish how much space you want inb
    axs = axs.ravel()
    for i in range(8):
        d = s_data[i,:]
        axs[i].plot(s_time, d) 
        axs[i].set_title('Channel %s' %(i+1), fontsize=12)
    fig.suptitle('Surface Electrodes', fontsize=18)
    fig.text(0.5, 0.04, 'Time $(s)$', ha='center',fontsize=18)
    fig.text(0.04, 0.5, 'Voltage $( \u03bc V)$', va='center', rotation='vertical',fontsize=20)

    
def plot_time_series_surface2(s_data, s_time): 
    fig, axs = plt.subplots(2,4, figsize=(20,10), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.2, wspace= .2) #this is to establish how much space you want inb
    #axs = axs.ravel()
    for i,ax in zip(range(8), axs.flat):
        d = s_data[i,:]
        ax.plot(s_time, d) 
        ax.set_title('Channel %s' %(i+1), fontsize=12)
    fig.suptitle('Surface Electrodes', fontsize=18)
    fig.text(0.5, 0.04, 'Time $(s)$', ha='center',fontsize=18)
    fig.text(0.04, 0.5, 'Voltage $( \u03bc V)$', va='center', rotation='vertical',fontsize=20)
    

def plot_2_comparisons(time, data1_og, data1_new, data2_og, data2_new, title1, title2): 
    fig, axs = plt.subplots(1,2, figsize = (15,5), facecolor ='w', edgecolor='k')
    axs[0].plot(time, data1_og, label='before')
    axs[0].plot(time, data1_new, label='after')
    axs[0].set_ylabel('Amplitude ($\mu V$)', fontsize=14)
    axs[0].set_xlabel('Time (s)', fontsize = 14)
    axs[0].set_title(title1, fontsize = 14)
    axs[0].legend(loc="upper right")
    
    axs[1].plot(time, data2_og, label='before')
    axs[1].plot(time, data2_new, label='after')
    axs[1].set_ylabel('Amplitude ($\mu V$)', fontsize=14)
    axs[1].set_xlabel('Time (s)', fontsize = 14)
    axs[1].legend(loc="upper right")
    

def plot_all_binary(n_data1, n_data2, downsample, s_data, color_arr, label_arr): 
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(n_data1[0:-1:downsample],'k', label='nDQ')
    plt.plot(n_data2[0:-1:downsample]+2,'C7', label='nDC')
    for i in range(8): 
        plt.plot(s_data[i]+((i*2)+4), color_arr[i], label = label_arr[i])
    plt.title('Needle vs Surface Channels', fontsize=20)
    plt.ylabel('Amplitude Waveform', fontsize=18)
    plt.xlabel('Time (s)', fontsize=18)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], title='Line', loc='upper right')
    
    
def plot_feature_importance_ROC(n_data1,fig_title): 
    # Plotting feature importance
    fig,axs = plt.subplots(1,2, figsize=(15, 5), facecolor ='w', edgecolor='k')
    fig.subplots_adjust(hspace=1, wspace= .2)
    n_data1['model_coefficients'].sort_values().plot(kind='barh', color='skyblue', ax=axs[0])
    axs[0].set_title("Feature Importance (Logistic Regression Coefficients)")
    axs[0].set_xlabel("Coefficient Value")
    axs[0].grid(True)

    # Plot ROC curve
    RocCurveDisplay.from_estimator(n_data1['model'], n_data1['x_test'], n_data1['y_test'], ax=axs[1])
    axs[1].set_title("ROC Curve for Logistic Regression Model")
    axs[1].grid(True)
    fig.suptitle(fig_title, fontsize=14)
    
# Generating the Heat map 
def generate_heat_map(data_to_plot, labels): 
    fig, axs = plt.subplots(1,2, figsize=(15,5))
    cmap = matplotlib.cm.YlOrRd
    cbar_ax = fig.add_axes([.92, .25, .02, .5])
    xCh= np.arange(1,5)
    yCh= np.arange(1,3)

    for i, data in enumerate(data_to_plot): 
        im0 =axs[i].imshow(data_to_plot[data]['model_coef'].reshape(2,4), cmap=cmap, interpolation = 'none', vmin = -3, vmax = 5, origin = "lower")
        axs[i].set_title(data_to_plot[data]['plot_title'], fontsize = 18)
        axs[i].set_xticks(np.arange(0, 4, 1), minor=False)
        axs[i].set_yticks(np.arange(0, 2, 1), minor=False)
        axs[i].grid(which='minor', color='w', linestyle='-', linewidth=2)
        axs[i].set_xticklabels(xCh, fontsize = 16);
        axs[i].set_yticklabels(yCh, fontsize = 16);
        axs[i].text(0.2, 1.2,'nDC')
        axs[i].text(1.5, 0.2,'nDQ')
        hold = [] 
        for n in range(4): 
            hold.append([data_to_plot[data]['model_coef'][n],data_to_plot[data]['model_coef'][n+4]])
    
        for k in range(4): 
            for j in range(2): 
                text = axs[i].text(k,j, labels[k][j], ha="center", va="center", color="k")
                text = axs[i].text(k,j-0.2, hold[k][j], ha="center", va="center", color="k")

    cbar = fig.colorbar(im0,cax=cbar_ax)
    cbar.ax.tick_params(labelsize=14)