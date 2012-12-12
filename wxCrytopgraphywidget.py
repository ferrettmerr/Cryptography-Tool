#!/usr/bin/env python
import os
import wx
import string
import re
from cryptography import *
from copy import copy
# TODO remove, used for testing to print dictionarys
from pprint import pprint

"""
TODO list

add exceptions for cryptography
Handle exceptiosn in gui

"""

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.width = 700
        self.height= 600
        wx.Frame.__init__(self, parent, title=title, size=(self.width,self.height))

        self.init_gui()
        self.init_menu()
        self.Show(True)
        self.combo_box.SetStringSelection('Shift')
        self.set_to_shift()

    def init_gui(self):
        self.panel = wx.Panel(self)

        # Static text
        self.encrypt_txt = wx.StaticText(self.panel, label="Encrypted text", pos=(500, 450))
        self.decrypt_txt = wx.StaticText(self.panel, label="Decrypted text", pos=(75, 450))

        # Textboxs, TODO set to max 500 character input
        self.decrypted = wx.TextCtrl(self.panel, -1, '',pos=(10,150),  size=(250, 300), style=wx.TE_MULTILINE)
        self.encrypted = wx.TextCtrl(self.panel, -1, '',pos=(self.width-260,150), size=(250, 300), style=wx.TE_MULTILINE)
           
        #self.CreateStatusBar() # A StatusBar in the bottom of the window
        self.widgetSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel.SetSizer(self.widgetSizer)

        # Creating the Combo box
        ciphers = ['Shift', 'Affine', 'Substitution', 'Permutation','Vigenere', 'One Time Pad', 'Hill' ]
        self.combo_box = wx.ComboBox(self.panel, -1, pos=(self.width/3, 10), size=(250, -1), choices=ciphers, style=wx.CB_READONLY)

        # Encrypt and Decrypt Buttons
        self.encrypt_btn = wx.Button(self.panel, 1, '>>', pos=(self.width/2 -25,175),size=(50, 100))
        self.decrypt_btn = wx.Button(self.panel, 2, '<<', pos=(self.width/2 -25,220),size=(50, 100))

        # Set events.
        self.Bind(wx.EVT_COMBOBOX, self.OnSelect, self.combo_box)#If not bound to button, will effect all buttons
        self.Bind(wx.EVT_BUTTON, self.encrypt_pressed, self.encrypt_btn)
        self.Bind(wx.EVT_BUTTON, self.decrypt_pressed, self.decrypt_btn)

    def init_menu(self):
        filemenu= wx.Menu()
        menuBar = wx.MenuBar()

        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program.")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A Cryptographic learning tool built by Lawrence Brewer and Walter Seme.", "Cryptographic Learning Tool", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnSelect(self, event):     
        self.widgetSizer.DeleteWindows()

        # Dynamic TextControls do clean properly because of focus, this is a hack, VIGENERE NOT CLEANING UP PROPERLY
        self.decrypted.SetFocus()
        self.encrypted.SetFocus()
        self.decrypted.SetFocus()


        # Reset encrypted text field only, incase same message wants to be used for different encryptions
        # self.encrypted.SetValue("")
        input_object = event.GetEventObject()
        cipher = input_object.GetValue()
        # cipher = self.combo_box.GetValue() #another way to do this, might want to clean up later

        # No switch statement in python, use dictionary with functions
        # But that didn't work because every function would be called
        if cipher == "Shift":
            self.set_to_shift()
        elif cipher == "Affine":
            self.set_to_affine()
        elif cipher == "Substitution":
            self.set_to_substitution()
        elif cipher == "Permutation":
            self.set_to_permutation()
        elif cipher == "Vigenere":
            self.set_to_vigenere()
        elif cipher == "One Time Pad":
            self.setToOneTimePad()
        elif cipher == "Hill":
            self.set_to_hill()

    def encrypt_pressed(self, event):
        cipher = self.combo_box.GetValue()

        plain_text = self.decrypted.GetValue().encode('ascii','ignore').upper().replace(' ', '')

        pattern = re.compile(r'\s+')
        plain_text = re.sub(pattern, '', plain_text)

        if cipher == "Shift":
            cipher_text = shift(plain_text, int(self.shift_combo.GetValue()))
            self.encrypted.SetValue(cipher_text)
        
        elif cipher == "Affine":
            a = int(self.a.GetValue())
            b = int(self.b.GetValue())

            encrypted_text = affine(plain_text, a, b)
            self.encrypted.SetValue(encrypted_text)
        
        elif cipher == "Substitution":
            cipher = copy(self.dictionary)
            for k,v in cipher.iteritems():
                v = v.GetValue();
            
            encrypted_text = substitution(plain_text, cipher)
            self.encrypted.SetValue(encrypted_text)
        elif cipher == "Permutation":
            cipher_text = [int(x) for x in self.cipher_text.GetValue().split(' ')]

            encrypted_text = permutation(plain_text, cipher_text)
            self.encrypted.SetValue(encrypted_text)

        elif cipher == "Vigenere":
            self.set_to_vigenere()

        elif cipher == "One Time Pad":
            self.setToOneTimePad()
        elif cipher == "Hill":
            self.set_to_hill()

    def decrypt_pressed(self, event):
        cipher = self.combo_box.GetValue()

        encrypted_text = self.encrypted.GetValue().encode('ascii','ignore').upper()
        
        pattern = re.compile(r'\s+')
        encrypted_text = re.sub(pattern, '', encrypted_text)

        if cipher == "Shift":
            plain_text = shift(encrypted_text, int(self.shift_combo.GetValue()), True)
            self.decrypted.SetValue(plain_text)
        
        elif cipher == "Affine":
            a = int(self.a.GetValue())
            b = int(self.b.GetValue())

            plain_text = affine(encrypted_text, a, b, True)
            self.decrypted.SetValue(plain_text)
        
        elif cipher == "Substitution":
            cipher_dict = dict()
            for k in dictionary.iterkeys():
                cipher_dict[k] = dictionary[k].GetValue()
            for key, value in dict.items(cipher_dict):
                self.encrypted.SetValue(self.encrypted.GetValue + key + ", " + value + "\r\n")
            # plain_text = substitution(encrypted_text, cipher_dict, True)
            # self.decrypted.SetValue(plain_text)

        elif cipher == "Permutation":
            cipher_text = [int(x) for x in self.cipher_text.GetValue().split(' ')]

            decrypted_text = permutation(encrypted_text, cipher_text, True)
            self.decrypted.SetValue(decrypted_text)
        elif cipher == "Vigenere":
            self.set_to_vigenere()

        elif cipher == "One Time Pad":
            self.setToOneTimePad()

        elif cipher == "Hill":
            self.set_to_hill()

    def set_to_shift(self):
        shift_txt = wx.StaticText(self.panel, label="Right shift by:", pos=(self.width/2-140, 50))
        
        shiftAmounts = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']
        self.shift_combo = wx.ComboBox(self.panel, -1, pos=(self.width/2 - 40, 50), size=(80, -1), choices=shiftAmounts, style=wx.CB_READONLY)

        self.widgetSizer.Add(self.shift_combo, 0, wx.ALL, 5)
        self.widgetSizer.Add(shift_txt, 0, wx.ALL, 5)

    def set_to_affine(self):
        a_txt = wx.StaticText(self.panel, label="A:", pos=(self.width/2 - 100, 52))
        b_txt = wx.StaticText(self.panel, label="B:", pos=(self.width/2, 52))

        # store a and b arguements
        aValues = ['1','3','5','7','9','11','15','17','19','21','23','25']
        bValues = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']

        self.a = wx.ComboBox(self.panel, -1, pos=(self.width/2 - 86, 50), size=(75, -1), choices=aValues, style=wx.CB_READONLY)
        self.b = wx.ComboBox(self.panel, -1, pos=(self.width/2 + 14, 50), size=(75, -1), choices=bValues, style=wx.CB_READONLY)

        self.widgetSizer.Add(self.a, 0, wx.ALL, 5)
        self.widgetSizer.Add(self.b, 0, wx.ALL, 5)
        self.widgetSizer.Add(a_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(b_txt, 0, wx.ALL, 5)

    def set_to_substitution(self):
        # need a-z mapping, use dictionary
        pos_x = 10
        pos_y = 50

        self.dictionary = dict()
        remaining_values = list(string.ascii_uppercase)#map(chr, range(65, 91)) also works
        remaining_values.sort()
        remaining_values = [' '] + remaining_values

        # layout and crete alphabet
        for key in remaining_values:
            if key == ' ':
                continue
            letter_label = wx.StaticText(self.panel,label=key+":", pos=(pos_x, pos_y))
            pos_x += 20 
            letter_btn = wx.ComboBox(self.panel, -1, pos=(pos_x,pos_y), size=(50, -1),choices=remaining_values, style=wx.CB_READONLY, name=key)
            letter_btn.Bind(wx.EVT_COMBOBOX, self.on_letter_choice)

            pos_x += 55
            if pos_x > 650:
                pos_x = 10
                pos_y += 20
                        
            self.widgetSizer.Add(letter_label, 0, wx.ALL, 5)
            self.widgetSizer.Add(letter_btn, 0, wx.ALL, 5)

    def on_letter_choice(self, e):

        event_object = e.GetEventObject()
        value = event_object.GetValue()
        if (value in self.dictionary):
            self.dictionary[value].SetStringSelection(' ')
        
        self.dictionary[value] = event_object



    def set_to_permutation(self):
        description = wx.StaticText(self.panel, label="Enter positions of blocks separated by spaces that is the specified size.\n\t\t\t\t\t Example: 1 4 3 2 5", pos=(self.width/8, 75))

        cipher_txt = wx.StaticText(self.panel, label="Cipher:", pos=(self.width/2 - 125, 50))
        self.cipher_text = wx.TextCtrl(self.panel, -1, '',pos=(self.width/2 - 150/2,50), size=(150, -1))

        self.widgetSizer.Add(description, 0, wx.ALL, 5)
        self.widgetSizer.Add(cipher_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(self.cipher_text, 0, wx.ALL, 5)

    def set_to_vigenere(self):
        keyword_txt = wx.StaticText(self.panel, label="Keyword:", pos=(self.width/3 -65, 50))
        keyword_description = wx.StaticText(self.panel, label="Pick a keyword that is between 3-6 letters.", pos=(self.width/3 - 10, 75))
        keyword = wx.TextCtrl(self.panel, -1, '',pos=(self.width/3,50), size=(250, -1))#TODO parse for only ascii chars

        self.widgetSizer.Add(keyword_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(keyword_description, 0, wx.ALL, 5)
        self.widgetSizer.Add(keyword, 0, wx.ALL, 5)
     

    def setToOneTimePad(self):        
        key_phase_txt = wx.StaticText(self.panel, label="Key phase:", pos=(self.width/3 -70, 50))
        description_txt = wx.StaticText(self.panel, label="The key phase has to be just as long as the decrypted message or longer.", pos=(self.width/6, 75))
        keyphase = wx.TextCtrl(self.panel, -1, '',pos=(self.width/3,50), size=(250, -1))#TODO parse for only ascii chars and limit messsage

        self.widgetSizer.Add(key_phase_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(description_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(keyphase, 0, wx.ALL, 5)

    def set_to_hill(self):
        matrix_txt = wx.StaticText(self.panel, label="Matrix:", pos=(self.width/3 -50, 50))
        description_txt = wx.StaticText(self.panel, label="Enter a matrix that is in the format {[5, 9],[11, 8]} with values modulos of 25.", pos=(self.width/6, 75))
        matrix = wx.TextCtrl(self.panel, -1, '',pos=(self.width/3,50), size=(250, -1))#TODO parse for only ascii chars

        self.widgetSizer.Add(matrix_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(description_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(matrix, 0, wx.ALL, 5)
        # self.key.SetLabel("Hill")



app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()