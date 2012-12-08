#!/usr/bin/env python
import os
import wx
import string

# TODO remove, used for testing to print dictionarys
from pprint import pprint


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,500))

        self.initStaticGUI()
        self.initMenu()
        self.Show(True)


    def initStaticGUI(self):
        self.panel = wx.Panel(self)

        # Static text
        self.encrypt_txt = wx.StaticText(self.panel, label="Encrypted text", pos=(330, 75))
        self.decrypt_txt = wx.StaticText(self.panel, label="Decrypted text", pos=(50, 75))

        # Textboxs
        self.decrypted = wx.TextCtrl(self.panel, -1, '',pos=(10,100), size=(200, 150), style=wx.TE_MULTILINE)
        self.encrypted = wx.TextCtrl(self.panel, -1, '',pos=(290,100), size=(200, 150), style=wx.TE_MULTILINE)
        self.key = wx.StaticText(self.panel, label="", pos=(100, 300), size=(200, 150))
           
        #self.CreateStatusBar() # A StatusBar in the bottom of the window
        self.widgetSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.number_of_buttons = 0
        self.panel.SetSizer(self.widgetSizer)

        # Creating the Combo box
        ciphers = ['Shift', 'Affine', 'Substitution', 'Permutation','Vigenere', 'One Time Pad', 'Hill' ]
        self.combo_box = wx.ComboBox(self.panel, -1, pos=(100, 10), size=(250, -1), choices=ciphers, style=wx.CB_READONLY)

        # Encrypt and Decrypt Buttons
        self.encrypt_btn = wx.Button(self.panel, 1, '>>', pos=(225,125),size=(50, 100))
        self.decrypt_btn = wx.Button(self.panel, 1, '<<', pos=(225,170),size=(50, 100))
   
        # self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)

        # Set events.
        self.Bind(wx.EVT_COMBOBOX, self.OnSelect, self.combo_box)#If not bound to button, will effect all buttons

    def initMenu(self):
        filemenu= wx.Menu()
        menuBar = wx.MenuBar()

        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program.")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)


    def removeDynamicGUI(self):
        # TODO clean up method, sloppy
        isGUICleared = True
        while isGUICleared:
            if self.widgetSizer.GetChildren():#Make for loop, didn't work when I did it
                self.widgetSizer.Hide(self.number_of_buttons-1)
                self.widgetSizer.Remove(self.number_of_buttons-1)
                self.number_of_buttons -= 1
            else:
                isGUICleared =  False

            

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A Cryptographic learning tool built by Lawrence Brewer and Walter Seme.", "Cryptographic Learning Tool", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnSelect(self, event):      
        self.removeDynamicGUI();
        # Reset encrypted text field only, incase same message wants to be used for different encryptions
        self.encrypted.SetValue("")

        cipher = self.combo_box.GetValue()
        # No switch statement in python, use dictionary with functions
        # But that didn't work because every function would be called
        if cipher == "Shift":
            self.setToShift()
        elif cipher == "Affine":
            self.setToAffine()
        elif cipher == "Substitution":
            self.setToSubstitution()
        elif cipher == "Permutation":
            self.setToPermutation()
        elif cipher == "Vigenere":
            self.setToVigenere()
        elif cipher == "One Time Pad":
            self.setToOneTimePad()
        elif cipher == "Hill":
            self.setToHill()


    def setToShift(self):
        # self.key.SetLabel("Shift by:")
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

    def setToAffine(self):
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


    def setToSubstitution(self):
        # need a-z mapping, use dictionary
        dictionary = dict.fromkeys(string.ascii_uppercase, 0)#init each value to 0

        # for value in dictionary:
            # create label + input field
            # add to widgetsizer & numberOfBtns
            # if half way create new row (use 2 rows)
        pprint(dictionary)
        self.key.SetLabel("Substitution")
        # add validation method and display somehow

    def setToPermutation(self):
        self.key.SetLabel("Perumation")

    def setToVigenere(self):
        self.key.SetLabel("Vigenere")

    def setToOneTimePad(self):
        self.key.SetLabel("One Time pad")

    def setToHill(self):
        self.key.SetLabel("Hill")

    def setToRSA(self):
        self.key.SetLabel("RSA")


app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()