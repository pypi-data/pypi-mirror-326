#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:34:59 2025
Custom plotter function which copies styles used by Shawn Pavey in Prism. Many
inputs are customizable, but defaults work well. This script contains two
functions: custom_plotter (full plotting + formating) and prism_reskin (only
reformats given figures).
@author: paveyboys
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from .base_plotter import BasePlotter
from .utils import match_rgba_to_color


class BarPlotter(BasePlotter):
    def __init__(self, input_dict,**kwargs):
        super().__init__(input_dict,**kwargs)
        
    def just_plot(self,**kwargs):
        self.DF[self.xlab] = self.DF[self.xlab].astype(str)

        kwargs,DF,markers,palette,dodge,ax,capsize,linewidth,width = super().kwarg_conflict_resolver(
            kwargs, ['DF','markers','palette','dodge','ax','capsize','linewidth','width'])

        defaults_list = [self.colors[0:len(self.unique)], self.def_line_w, self.box_width]

        palette, linewidth, width = super().var_existence_check(
            [palette, linewidth, width],
            ['palette', 'linewidth', 'width'],
            defaults_list, kwargs=kwargs)

        sns.barplot(
            x=self.xlab, y=self.ylab, data=DF,
            hue =self.zlab,
            palette=palette,
            linewidth=linewidth,width=width,
            dodge = dodge,ax=ax, err_kws={'color': 'k','linewidth': self.def_line_w}, capsize=capsize,
            **kwargs)
        dark_palette = []
        while len(self.unique) > len(self.hatches):
            self.hatches.extend(self.hatches)

        for bar in self.ax.patches:
            hue_group = bar.get_label()
            match_rgba_to_color(bar.get_facecolor(), self.colors)
            current_face_color =  match_rgba_to_color(bar.get_facecolor(), self.colors)#rgba_to_named_color(bar.get_facecolor())
            bar.set_hatch(self.hatches[self.colors.index(current_face_color)])
            bar.set_edgecolor('black')
            hatch_pattern = self.hatches[self.colors.index(current_face_color)]
            hatch_density = 1
            bar.set_hatch(f"{hatch_pattern * hatch_density}")
            bar.set_linewidth(self.def_line_w)

        for i in range(len(self.DF[self.zlab].unique())):
            dark_palette.append('k')
        for i, category in enumerate(self.DF[self.zlab].unique()):
            df_copy = self.DF.copy()
            df_copy.loc[df_copy[self.zlab] != category, self.ylab] = np.nan
            try:
                sns.stripplot(
                    data=df_copy, x=self.xlab, y=self.ylab,hue=self.zlab,
                    dodge = self.dodge,palette=dark_palette,
                    marker=self.marker_dict[category],ax=self.ax)
            except KeyError:
                pass
        plt.xlabel(" ")

    def plot(self, save=True,**kwargs):
        super().plot(save=save)
        return self.fig, self.ax
    
    def pre_format(self):
        super().pre_format()
        return self.fig, self.ax
    
    def post_format(self):
        super().post_format()
        return self.fig, self.ax

    def save(self):
        super().save()
        return self.fig, self.ax

    def show(self):
        super().show()
        return self.fig, self.ax


            
    
