
import sys, os, json
import tkinter as tk
from tkinter import font

class main_menu:
    def __init__(self, root):
        self.menu = {
        }

    def show_menu(self):
        for key, value in self.menu.items():
            print(f'{key} - {value}')