#!/usr/bin/env python
import os
import wx
import string

# TODO remove, used for testing to print dictionarys
from pprint import pprint


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.width = 700
        self.height= 600
        wx.Frame.__init__(self, parent, title=title, size=(self.width,self.height))

        self.init_gui()
        self.init_menu()
        self.Show(True)


    def init_gui(self):
        self.panel = wx.Panel(self)

        # Static text
        self.encrypt_txt = wx.StaticText(self.panel, label="Encrypted text", pos=(400, 450))
        self.decrypt_txt = wx.StaticText(self.panel, label="Decrypted text", pos=(75, 450))

        # Textboxs
        self.decrypted = wx.TextCtrl(self.panel, -1, '',pos=(10,150),  size=(250, 300), style=wx.TE_MULTILINE)
        self.encrypted = wx.TextCtrl(self.panel, -1, '',pos=(340,150), size=(250, 300), style=wx.TE_MULTILINE)
        self.key = wx.StaticText(self.panel, label="", pos=(100, 550), size=(200, 300))
           
        #self.CreateStatusBar() # A StatusBar in the bottom of the window
        self.widgetSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.number_of_buttons = 0
        self.panel.SetSizer(self.widgetSizer)

        # Creating the Combo box
        ciphers = ['Shift', 'Affine', 'Substitution', 'Permutation','Vigenere', 'One Time Pad', 'Hill' ]
        self.combo_box = wx.ComboBox(self.panel, -1, pos=(self.width/3, 10), size=(250, -1), choices=ciphers, style=wx.CB_READONLY)

        # Encrypt and Decrypt Buttons
        self.encrypt_btn = wx.Button(self.panel, 1, '>>', pos=(275,175),size=(50, 100))
        self.decrypt_btn = wx.Button(self.panel, 1, '<<', pos=(275,220),size=(50, 100))
   
        # self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)

        # Set events.
        self.Bind(wx.EVT_COMBOBOX, self.OnSelect, self.combo_box)#If not bound to button, will effect all buttons

    def init_menu(self):
        filemenu= wx.Menu()
        menuBar = wx.MenuBar()

        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
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

        # Reset encrypted text field only, incase same message wants to be used for different encryptions
        self.encrypted.SetValue("")

        cipher = self.combo_box.GetValue()
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


    def set_to_shift(self):
        shift_txt = wx.StaticText(self.panel, label="Shift by:", pos=(100, 50))
        
        shiftAmounts = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']
        new_button = wx.ComboBox(self.panel, -1, pos=(155, 50), size=(75, -1), choices=shiftAmounts, style=wx.CB_READONLY)

        self.widgetSizer.Add(new_button, 0, wx.ALL, 5)
        self.widgetSizer.Add(shift_txt, 0, wx.ALL, 5)
        self.number_of_buttons += 2

        # TODO Set button listners, last argument is method with input: def methodName(self,event):
        # self.encrypt_btn.Bind(wx.EVT_BUTTON, self.shiftEncrypt)
        # self.decrypt_btn.Bind(wx.EVT_BUTTON, self.shiftEncrypt)

        # self.encrypted.SetValue("Encrypted message")
        # self.decrypted.SetValue("Decrypted message")

    def set_to_affine(self):
        a_txt = wx.StaticText(self.panel, label="A:", pos=(135, 52))
        b_txt = wx.StaticText(self.panel, label="B:", pos=(235, 52))

        # store a and b arguements
        aValues = ['1','3','5','7','9','11','15','17','19','21','23','25']
        bValues = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']

        a = wx.ComboBox(self.panel, -1, pos=(152, 50), size=(75, -1), choices=aValues, style=wx.CB_READONLY)
        b = wx.ComboBox(self.panel, -1, pos=(250, 50), size=(75, -1), choices=bValues, style=wx.CB_READONLY)

        self.widgetSizer.Add(a, 0, wx.ALL, 5)
        self.widgetSizer.Add(b, 0, wx.ALL, 5)
        self.widgetSizer.Add(a_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(b_txt, 0, wx.ALL, 5)
        self.number_of_buttons += 4


    def set_to_substitution(self):
        # need a-z mapping, use dictionary
        dictionary = dict.fromkeys(string.ascii_uppercase, 0)#init each value to 0

        pos_x = 10
        pos_y = 50
        index = 0

        count_of_btns = 0

        remaining_values = dictionary.keys()

        
        for key in dictionary.keys():
            letter_label = wx.StaticText(self.panel,label=key+":", pos=(pos_x, pos_y))
            pos_x += 20
            letter_btn = wx.ComboBox(self.panel, -1, pos=(pos_x,pos_y), size=(50, -1),choices=dictionary.keys(), style=wx.CB_READONLY)
            letter_btn.Bind(wx.EVT_COMBOBOX, self.on_letter_choice)
            pos_x += 55
            index += 1
            count_of_btns += 2
            if index > len(dictionary)/3:
                pos_x =10
                pos_y += 20
                index = 0

            self.widgetSizer.Add(letter_label, 0, wx.ALL, 5)
            self.widgetSizer.Add(letter_btn, 0, wx.ALL, 5)





            # create label + input field
            # add to widgetsizer & numberOfBtns
            # if half way create new row (use 2 rows)
        pprint(dictionary)
        # self.key.SetLabel("Substitution")
        # add validation method and display somehow

    def on_letter_choice(self, e):
        remaining_values = array.fromstring(string.ascii_uppercase)

    def set_to_permutation(self):
        self.key.SetLabel("Perumation")

    def set_to_vigenere(self):
        keyword_txt = wx.StaticText(self.panel, label="keyword:", pos=(self.width/3 -65, 50))
        keyword = wx.TextCtrl(self.panel, -1, '',pos=(self.width/3,50), size=(250, -1))#TODO parse for only ascii string

        self.widgetSizer.Add(keyword_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(keyword, 0, wx.ALL, 5)
     

    def setToOneTimePad(self):
        self.key.SetLabel("One Time pad")

    def set_to_hill(self):
        self.key.SetLabel("Hill")



app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()