#######################
# Import libraries
import streamlit as st
import leafmap.foliumap as leafmap
import squarify
import matplotlib.pyplot as plt


volume = [350, 220, 170, 150, 50]
labels = ['Liquid\n volume: 350k', 'Savoury\n volume: 220k',
                'Sugar\n volume: 170k', 'Frozen\n volume: 150k',
                'Non-food\n volume: 50k']
color_list = ['#0f7216', '#b2790c', '#ffe9a3',
                    '#f9d4d4', '#d35158', '#ea3033']



plt.rc('font', size=14)
squarify.plot(sizes=volume, label=labels,
            color=color_list, alpha=0.7)
plt.axis('off')
st.pyplot()