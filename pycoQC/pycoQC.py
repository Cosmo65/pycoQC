# -*- coding: utf-8 -*-

"""       
  ___              ___   ___ 
 | _ \_  _ __ ___ / _ \ / __|
 |  _/ || / _/ _ \ (_) | (__ 
 |_|  \_, \__\___/\__\_\\___|
      |__/      
                                __   __     ___ 
 /\  _| _. _ _   |   _ _  _ _    _) /  \ /|   / 
/--\(_|| |(-| )  |__(-(_)(-|    /__ \__/  |  /  
                      _/                        
"""

# Standard library imports
from sys import exit as sysexit
from collections import OrderedDict

# Third party imports
try:
    import numpy as np
    import pylab as pl
    import pandas as pd
    import seaborn as sns
    get_ipython()
    from IPython.core.display import display
    
except (NameError, ImportError) as E:
    print (E)
    print ("A third party package is missing. Please verify your dependencies")
    sysexit()

##~~~~~~~ MAIN CLASS ~~~~~~~#
class pycoQC():

    #~~~~~~~FUNDAMENTAL METHODS~~~~~~~#    
    def __init__ (self, seq_summary_file, runid=None, verbose=False):
        """
        Parse Albacore sequencing_summary.txt file and cleanup the data
        * seq_summary_file
            Path to the sequencing_summary.txt generated by Albacore
        * runid
            If you want a specific runid to be analysed. Usually there are 2 runids per minion experiment, the mux run and the sequencing
            run. By default it will analyse the runid with the most reads, ie the sequencing run. [Default None]
        * verbose
            print additional informations. [Default False]
        """
        self.verbose=verbose
        
        # import in a dataframe
        self.seq_summary_file = seq_summary_file
        self.df = pd.read_csv(seq_summary_file, sep ="\t")
        self.df.dropna(inplace=True)
        
        # Verify the presence of the columns required for pycoQC
        for colname in ['run_id', 'channel', 'start_time', 'duration', 'num_events','sequence_length_template', 'mean_qscore_template']:
            assert colname in self.df.columns, "Column {} not found in the provided sequence_summary file".format(colname)
        
        # Find or verify runid
        runid_counts = self.df['run_id'].value_counts(sort=True)
                
        if not runid:
            if self.verbose:
                print ("Runid found in the datasets")
                runid_counts.name = "Count"
                runid_df = pd.DataFrame(runid_counts)
                runid_df.columns.name = "Run_ID"
                display(runid_df)
                print ("Selecting Run_ID {}".format(runid_counts.index[0]))
                
            self.runid = runid_counts.index[0]
            self.total_reads = runid_counts.loc[self.runid]
            
        else:
            self.runid = runid
            self.total_reads = runid_counts.loc[self.runid]
        
        # Extract the runid data from the overall dataframe
        self.df = self.df[(self.df["run_id"] == self.runid)]
        self.df = self.df.reset_index(drop=True)
        self.df.set_index("read_id", inplace=True)
        #self.df.drop(['filename', 'run_id'], axis=1, inplace=True)
        
        if self.verbose:
            print ("Dataframe head")
            display (self.df.head())
    
    def __str__(self):
        """readable description of the object"""
        msg = "{} instance\n".format(self.__class__.__name__)
        msg+= "\tParameters list\n"
        
        # list all values in object dict in alphabetical order
        for k,v in OrderedDict(sorted(self.__dict__.items(), key=lambda t: t[0])).items():
            if k != "df":
                msg+="\t{}\t{}\n".format(k, v)
        return (msg)

    #~~~~~~~PUBLIC METHODS~~~~~~~#
    
    def overview (self):
        """
        Generate a quick overview of the data (tables + plots)
        """
        df = pd.DataFrame(columns=["Count"])
        df.loc["Reads", "Count"] = len(self.df)
        df.loc["Bases", "Count"] = self.df["sequence_length_template"].sum()
        df.loc["Events", "Count"] = self.df["num_events_template"].sum()
        df.loc["Active Channels", "Count"] = self.df["channel"].nunique()
        df.loc["Run Duration (h)", "Count"] = ((self.df["start_time"]+self.df["duration"]).max() - self.df["start_time"].min())/3600
        display(df)

        df = self.df[['mean_qscore_template', 'sequence_length_template']].describe(percentiles=[0.1,0.25,0.5, 0.75, 0.90])
        df.rename(columns={'mean_qscore_template': 'Quality score distribution', 'sequence_length_template': 'Read length distribution'},
            inplace=True)
        display(df)

        fig, (ax1, ax2) = pl.subplots(1, 2, figsize=(12, 6))
        g1 = sns.violinplot(data=self.df['mean_qscore_template'], color="orangered", alpha=0.5, bw=.2, linewidth=1,
            inner="quartile", ax=ax1)
        t = ax1.set_title("Quality score distribution")
        g2 = sns.violinplot(data=self.df['sequence_length_template'], color="orangered", alpha=0.5, bw=.2, cut=1, linewidth=1,
            inner="quartile", ax=ax2)
        t= ax2.set_title("Read length distribution")
        
    def trim_read_len (self, min_len=None, max_len=None):
        """
        Remove reads longer or shorter than the indicated limits from all downstream analysis
        * min_len
            Minimal length of the reads to retain
        * max_len
            Maximal length of the reads to retain
        """
        if min_len:
            self.df = self.df[(self.df['sequence_length_template'] >= min_len)]
            print ("{} short reads were removed".format(self.total_reads-len(self.df)))
            self.total_reads = len(self.df)
            
        if max_len:
            self.df = self.df[(self.df['sequence_length_template'] <= max_len)]
            print ("{} long reads were removed".format(self.total_reads-len(self.df)))
            self.total_reads = len(self.df)
    
    def trim_read_qual (self, min_qual=None, max_qual=None):
        """
        Remove reads under or above indicated limits from all downstream analysis
        * min_len
            Minimal quality of the reads to retain
        * max_len
            Maximal quality of the reads to retain
        """
        if min_qual:
            self.df = self.df[(self.df['mean_qscore_template'] >= min_qual)]
            print ("{} low quality reads were removed".format(self.total_reads-len(self.df)))
            self.total_reads = len(self.df)
            
        if max_qual:
            self.df = self.df[(self.df['mean_qscore_template'] <= max_qual)]
            print ("{} high quality reads were removed".format(self.total_reads-len(self.df)))
            self.total_reads = len(self.df)
    
    def channels_activity (self, level="reads", figsize=[24,12], cmap="OrRd", alpha=1, robust=True, annot=True, fmt="d", cbar=False,
        **kwargs):
        """
        Plot the activity of channels at read, base or event level. Based on Seaborn heatmap function. The layout does not represent the
        physical layout of the flowcell, and   
        * level
            Aggregate channel output results by "reads", "bases" or "events". [Default "reads"]
        * figsize 
            Size of ploting area [Default [24,12]]
        * cmap
            Matplotlib colormap code to color the space [Default "OrRd"]
        * alpha
            Opacity of the area from 0 to 1 [Default 1]
        * robust
            if True the colormap range is computed with robust quantiles instead of the extreme values [Default True]
        * annot
            If True, write the data value in each cell. [Default True]
        * fmt
            String formatting code to use when adding annotations (see matplotlib documentation) [Default "d"]
        * cbar
            Whether to draw a colorbar scale on the right of the graph [Default False]
        => Return
            A matplotlib.axes object for further user customisation (http://matplotlib.org/api/axes_api.html)
        """
        
        # Compute the count per channel
        if level == "reads":
            s = self.df['channel'].value_counts(sort=False)
            title = "Reads per channels"
        if level == "bases":
            s = self.df.groupby("channel").aggregate(np.sum)["sequence_length_template"]
            title = "Bases per channels"
        if level == "events":
            s = self.df.groupby("channel").aggregate(np.sum)["num_events"]
            title = "Events per channels"
            
        # Fill the missing values
        for i in range(1, 512):
            if i not in s.index:
                s.loc[i] = 0

        # Sort by index value 
        s.sort_index(inplace=True)

        # Reshape the series to a 2D frame similar to the Nanopore flowcell grid 
        a = s.values.reshape(16,32)

        # Plot a heatmap like grapd
        fig, ax = pl.subplots(figsize=figsize)
        ax = sns.heatmap(a, ax=ax, annot=annot, fmt=fmt, linewidths=2, cbar=cbar, cmap=cmap, alpha=alpha, robust=robust)
                    
        # Tweak the plot
        t = ax.set_title (title)
        t = ax.set_xticklabels("")
        t = ax.set_yticklabels("")
        
        for text in ax.texts:
            text.set_size(8)
        
        return ax
    
    def mean_qual_distribution (self, figsize=[30,7], hist=True, kde=True, kde_color="black", hist_color="orangered", kde_alpha=0.5,
        hist_alpha=0.5, win_size=0.1, xmin=None, xmax=None, ymin=None, ymax=None, **kwargs):
        """
        * figsize
            Size of ploting area [Default [30,7]]
        * hist
            If True plot an histogram of distribution [Default True]
        * kde
            If True plot a univariate kernel density estimate [Default True]
        * kde_color / hist_color
            Color map or color codes to use for the 3 plots [Default "black" "orangered"]
        * kde_alpha / hist_alpha
            Opacity of the area from 0 to 1 for the 3 plots [Default 0.5 0.5]
        * win_size
            Size of the bins in quality score ranging from 0 to 40 for the histogram [Default 0.1]
        * xmin, xmax, ymin, ymax
            Lower and upper limits on x/y axis [Default None]
        => Return
            A matplotlib.axes object for further user customisation (http://matplotlib.org/api/axes_api.html)
        """
                
        # Extract length limits
        if not xmax or xmax<=0 or xmax>40:
            xmax = max(self.df['mean_qscore_template'])
        if not xmin or xmin<0 or xmin>=40:
            xmin = 0
        if xmax-xmin < win_size:
            win_size = xmax-xmin
        
        # Plot
        fig, ax = pl.subplots(figsize=figsize)
        # Plot the kde graph
        if kde:
            sns.kdeplot(self.df["mean_qscore_template"], ax=ax, color=kde_color, alpha=kde_alpha, shade=not hist, gridsize=500,
                legend=False)
        # Plot a frequency histogram 
        if hist:
            ax = self.df['mean_qscore_template'].plot.hist(
                bins=np.arange(xmin, xmax, win_size), ax=ax, normed=True, color=hist_color, alpha=hist_alpha, histtype='stepfilled')
        
        # Tweak the plot       
        t = ax.set_title ("Mean quality distribution per read")
        t = ax.set_xlabel("Mean PHRED quality Score")
        t = ax.set_ylabel("Read Frequency")
        
        if not ymin:
            ymin = 0
        if not ymax:
            ymax = ax.get_ylim()[1]
        
        t = ax.set_xlim([xmin, xmax])
        t = ax.set_ylim([ymin, ymax])
        
        return ax
        
    def reads_len_distribution (self, figsize=[30,7], hist=True, kde=True, kde_color="black", hist_color="orangered", kde_alpha=0.5,
        hist_alpha=0.5, win_size=250, xmin=None, xmax=None, ymin=None, ymax=None, **kwargs):
            
        """
        Plot the distribution of read length in base pairs
        * figsize
            Size of ploting area [Default [30,7]]
        * hist
            If True plot an histogram of distribution [Default True]
        * kde
            If True plot a univariate kernel density estimate [Default True]
        * kde_color / hist_color
            Color map or color codes to use for the 3 plots [Default "black" "orangered"]
        * kde_alpha / hist_alpha
            Opacity of the area from 0 to 1 for the 3 plots [Default 0.5 0.5]
        * win_size
            Size of the bins in base pairs for the histogram [Default 250]
        * xmin, xmax, ymin, ymax
            Lower and upper limits on x/y axis [Default None]
        => Return
            A matplotlib.axes object for further user customisation (http://matplotlib.org/api/axes_api.html)
        """
        # Extract length limits
        if not xmax:
            xmax = max(self.df['sequence_length_template'])
        if not xmin:
            xmin = 0
        if xmax-xmin < win_size:
            win_size = xmax-xmin
        
        # Plot
        fig, ax = pl.subplots(figsize=figsize)
        # Plot the kde graph
            
        if kde:
            sns.kdeplot(self.df["sequence_length_template"], ax=ax, color=kde_color, alpha=kde_alpha, shade=not hist, gridsize=500,
                legend=False)
        # Plot a frequency histogram 
        if hist:
            ax = self.df['sequence_length_template'].plot.hist(
                bins=np.arange(xmin, xmax, win_size), ax=ax, normed=True, color=hist_color, alpha=hist_alpha, histtype='stepfilled')
        
        # Tweak the plot       
        t = ax.set_title ("Distribution of reads length")
        t = ax.set_xlabel("Length in bp")
        t = ax.set_ylabel("Read Frequency")
                
        if not ymin:
            ymin = 0
        if not ymax:
            ymax = ax.get_ylim()[1]
            
        t = ax.set_xlim([xmin, xmax])
        t = ax.set_ylim([ymin, ymax])
        
        return ax

    def output_over_time (self, level="reads", figsize=[30,7], color="orangered", alpha=0.5, win_size=0.25, cumulative=False, **kwargs):
        """
        Plot the output over the time of the experiment at read, base or event level
        * level
            Aggregate channel output results by "reads", "bases" or "events" [Default "reads"]
        * figsize
            Size of ploting area [Default [30,7]
        * color
            Color of the plot. Valid matplotlib color code [Default "orangered"]
        * alpha
            Opacity of the area from 0 to 1 [Default 0.5]
        * win_size
            Size of the bins in hours [Default 0.25]
        * cumulative
            cumulative histogram [Default False]
        => Return
            A matplotlib.axes object for further user customisation (http://matplotlib.org/api/axes_api.html)
        """
        
        df = self.df[["num_events", "sequence_length_template"]].copy()
        df["end_time"] = (self.df["start_time"]+self.df["duration"])/3600

        # Compute the mean, min and max for each win_size interval
        df2 = pd.DataFrame(columns=["reads", "bases", "events"])
        for t in np.arange(0, max(df["end_time"]), win_size):
            if cumulative:
                sdf = df[(df["end_time"] < t+win_size)]
            else:
                sdf = df[(df["end_time"] >= t) & (df["end_time"] < t+win_size)]
            df2.loc[t] =[len(sdf), sdf["sequence_length_template"].sum(), sdf["num_events"].sum()]

        # Plot the graph
        fig, ax = pl.subplots(figsize=figsize)
        df2[level].plot.area(ax=ax, color=color, alpha=alpha)

        # Tweak the plot
        t = ax.set_title ("Total {} over time".format(level))
        t = ax.set_xlabel("Experiment time (h)")
        t = ax.set_ylabel("{} count".format(level))
        t = ax.set_xlim (0, max(df2.index))
        t = ax.set_ylim (0, ax.get_ylim()[1])
        
        return ax
    
    def quality_over_time (self, figsize=[30,7], color="orangered", alpha=0.25, win_size=0.25, **kwargs):
        """
        Plot the evolution of the mean read quality over the time of the experiment at read, base or event level
        * figsize
            Size of ploting area [Default [30,7]
        * color
            Color of the plot. Valid matplotlib color code [Default "orangered"]
        * alpha
            Opacity of the area from 0 to 1 [Default 0.25]
        * win_size
            Size of the bins in hours [Default 0.25]
        => Return
            A matplotlib.axes object for further user customisation (http://matplotlib.org/api/axes_api.html)
        """
        
        # Slice the main dataframe
        df = self.df[["mean_qscore_template"]].copy()
        df["end_time"] = (self.df["start_time"]+self.df["duration"])/3600
        
        # Compute the mean, min and max for each win_size interval
        df2 = pd.DataFrame(columns=["mean", "min", "max", "q1", "q3"])
        for t in np.arange(0, max(df["end_time"]), win_size):
            sdf = df["mean_qscore_template"][(df["end_time"] >= t) & (df["end_time"] < t+win_size)]
            df2.loc[t] =[sdf.median(), sdf.min(), sdf.max(), sdf.quantile(0.25), sdf.quantile(0.75)]

        # Plot the graph
        fig, ax = pl.subplots(figsize=figsize)
        ax.fill_between(df2.index, df2["min"], df2["max"], color=color, alpha=alpha)
        ax.fill_between(df2.index, df2["q1"], df2["q3"], color=color, alpha=alpha)
        ax.plot(df2["mean"], color=color)
        
        # Tweak the plot
        t = ax.set_title ("Mean read quality over time (Median, Q1-Q3, Min-Max)")
        t = ax.set_xlabel("Experiment time (h)")
        t = ax.set_ylabel("Mean read PHRED quality")
        t = ax.set_xlim (0, max(df2.index))
        t = ax.set_ylim (0, ax.get_ylim()[1])
        
        return ax
        
    def reads_len_quality (self, figsize=12, kde=True, scatter=True, margin_plot=True, kde_cmap="copper", scatter_color="orangered",
        margin_plot_color="orangered", kde_alpha=1, scatter_alpha=0.01, margin_plot_alpha=0.5, kde_levels=10, kde_shade=False, xmin=None,
        xmax=None, ymin=None, ymax=None, **kwargs):
        """
        Draw a bivariate plot of read length vs mean read quality with marginal univariate plots.
        The bivariate kde can takes time to calculate depending on the number of datapoints 
        * figsize
            Size of square ploting area [Default 12]
        * kde
            If True plot a bivariate kernel density estimate [Default True]
        * scatter
            If True plot a scatter plot  [Default true]
        * margin_plot
            If True plot marginal univariate distributions [Default True]
        * kde_cmap / scatter_color / margin_plot_color
            Color map or color codes to use for the 3 plots [Default "copper", "orangered", "orangered"]
        * kde_alpha / scatter_alpha / margin_plot_alpha
            Opacity of the area from 0 to 1 for the 3 plots [Default 1, 0.01, 0.5]
        * kde_levels
            Number of levels for the central density plot [Default 10]
        * kde_shade
            If True the density curves will be filled [Default False]
        * xmin, xmax, ymin, ymax
            Lower and upper limits on x/y axis [Default None]
        => Return
            A seaborn JointGrid object with the plot on it. (http://seaborn.pydata.org/generated/seaborn.JointGrid.html)
        """
        
        # Plot the graph
        g = sns.JointGrid("sequence_length_template", "mean_qscore_template", data=self.df, space=0.1, size=figsize)
        if kde:
            if kde_shade:
                g = g.plot_joint(sns.kdeplot, cmap=kde_cmap, alpha=kde_alpha, shade=True, shade_lowest=False, n_levels=kde_levels,)
            else:
                g = g.plot_joint(sns.kdeplot, cmap=kde_cmap, alpha=kde_alpha, shade=False, shade_lowest=False, n_levels=kde_levels, linewidths=1)
        if scatter:
            g = g.plot_joint(pl.scatter, color=scatter_color, alpha=scatter_alpha)
        if margin_plot:
            g = g.plot_marginals(sns.kdeplot, shade=True, color=margin_plot_color, alpha=margin_plot_alpha)
        
        # Tweak the plot
        t = g.ax_marg_x.set_title ("Mean read quality per sequence length")
        t = g.ax_joint.set_xlabel("Sequence length (bp)")
        t = g.ax_joint.set_ylabel("Mean read quality (PHRED)")

        if not xmin:
            xmin = g.ax_joint.get_xlim()[0]
        if not xmax:
            xmax = g.ax_joint.get_xlim()[1]
        if not ymin:
            ymin = g.ax_joint.get_ylim()[0]
        if not ymax:
            ymax = g.ax_joint.get_ylim()[1]
            
        t = g.ax_joint.set_xlim([xmin, xmax])
        t = g.ax_joint.set_ylim([ymin, ymax])
        
        return g
