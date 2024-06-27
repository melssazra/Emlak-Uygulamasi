# -*- coding: utf-8 -*-
"""
Created on Sun May 26 05:15:39 2024

@author: mat76
"""

from PyQt5 import uic

with open("sifrearayuzuWidgets.py","w",encoding="utf-8") as fout:
    uic.compileUi("sifrearayuzu.ui",fout)