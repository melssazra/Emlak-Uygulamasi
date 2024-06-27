# -*- coding: utf-8 -*-
"""
Created on Sun May 26 05:15:39 2024

@author: mat76
"""

from PyQt5 import uic

with open("hakkindaWidgets.py","w",encoding="utf-8") as fout:
    uic.compileUi("hakkinda.ui",fout)