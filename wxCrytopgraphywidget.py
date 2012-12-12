#!/usr/bin/env python
import os
import wx
import string
import affine
# import Permutation

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

    def set_to_shift(self):
        shift_txt = wx.StaticText(self.panel, label="Right shift by:", pos=(self.width/2-140, 50))
        
        shiftAmounts = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']
        key_button = wx.ComboBox(self.panel, -1, pos=(self.width/2 - 40, 50), size=(80, -1), choices=shiftAmounts, style=wx.CB_READONLY)

        self.widgetSizer.Add(key_button, 0, wx.ALL, 5)
        self.widgetSizer.Add(shift_txt, 0, wx.ALL, 5)

        # TODO Set button listners, last argument is method with input: def methodName(self,event):
        # self.encrypt_btn.Bind(wx.EVT_BUTTON, self.shiftEncrypt)
        # self.decrypt_btn.Bind(wx.EVT_BUTTON, self.shiftEncrypt)

        # self.encrypted.SetValue("Encrypted message")
        # self.decrypted.SetValue("Decrypted message")


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


        self.Bind(wx.EVT_BUTTON, self.encrypt_affine, self.encrypt_btn)#If not bound to button, will effect all buttons
        self.Bind(wx.EVT_BUTTON, self.decrypt_affine, self.decrypt_btn)
        # self.encrypt_btn.Bind(wx.EVT_BUTTON, self.encrypt_decrypt_affine(a, b, True))
        # self.decrypt_btn.Bind(wx.EVT_BUTTON, self.encrypt_decrypt_affine(a, b, False))


    def encrypt_affine(self, event):
        self.decrypted.SetValue("Yay!")
        # TODO CLEAN UP - REALLY SLOPPY
        a = int(self.a.GetValue())
        b = int(self.b.GetValue())
        msg = self.decrypted.GetValue().encode('ascii','ignore').upper()#TODO ignore /n and other non ascii chars


        # print a
        # print b
        # print msg

        encryption = affine.encode_affine(msg, a, b)

        # print encryption

        self.encrypted.SetValue(encryption)




    def decrypt_affine(self, event):

        a = int(self.a.GetValue()) 
        b = int(self.b.GetValue())
        msg = self.encrypted.GetValue().encode('ascii','ignore').upper()#TODO ignore /n and other non ascii chars

        decryption = affine.decode_affine(msg, a, b)

        # print decryption

        self.decrypted.SetValue(decryption)

    def set_to_substitution(self):
        # need a-z mapping, use dictionary
        self.dictionary = dict.fromkeys(string.ascii_uppercase, 0)#init each value to 0

        pos_x = 10
        pos_y = 50
        index = 0

        count_of_btns = 0

        remaining_values = list(string.ascii_uppercase)#map(chr, range(65, 91)) also works
        remaining_values.sort()
        # self.sub_combo_boxes = []

        # layout and crete alphabet
        for key in remaining_values:
            letter_label = wx.StaticText(self.panel,label=key+":", pos=(pos_x, pos_y))
            pos_x += 20
            letter_btn = wx.ComboBox(self.panel, -1, pos=(pos_x,pos_y), size=(50, -1),choices=remaining_values, style=wx.CB_READONLY, name=key)
            letter_btn.Bind(wx.EVT_COMBOBOX, self.on_letter_choice)

            # self.sub_combo_boxes.append(letter_btn)
            pos_x += 55
            index += 1
            count_of_btns += 2
            if index > len(self.dictionary)/3:
                pos_x =10
                pos_y += 20
                index = 0

            self.widgetSizer.Add(letter_label, 0, wx.ALL, 5)
            self.widgetSizer.Add(letter_btn, 0, wx.ALL, 5)





            # create label + input field
            # add to widgetsizer & numberOfBtns
            # if half way create new row (use 2 rows)

        # self.key.SetLabel("Substitution")
        # add validation method and display somehow

    def on_letter_choice(self, e):


        event_object = e.GetEventObject()
        value = event_object.GetValue()
        self.dictionary[event_object.GetName()] = value
        pprint(self.dictionary)

        # get index for later use
        # char_index = self.remaining_values.index(value.GetValue())
        # self.dictionary[value.GetName()] = value.GetValue();
        # TODO get previouse value, add it back to list

        # remove  global values selected
        # self.dictionary = dict.fromkeys(string.ascii_uppercase, 0)#init each value to 0
        # self.remaining_values.remove(value.GetValue())

        # update every other comboxbox
        # children = self.widgetSizer.GetChildren()
 
        # for child in children:
        #     widget = child.GetWindow()
            # if isinstance(widget, wx.ComboBox):d
                # for letter in dictionary.keys():
                #     if value.GetValue() == letter:
                #         dictionary[letter] += 1 
                #     if dictionary[letter] >0:
                #         value.SetValue(0)

                # widget.GetValue()
                # print widget.GetString(-1)
                # if widget != value:
                    # widget.Clear()
                    # for char in self.remaining_values:
                    #     widget.Append(char)

        # # remove selected letter from every other combo box
        # for combo_box in self.sub_combo_boxes:
        #     if combo_box != value:
        #             combo_box.Clear()
        #             for char in self.remaining_values:
        #                 combo_box.Append(char)



    def set_to_permutation(self):
        block_size = wx.StaticText(self.panel, label="Size of Blocks:", pos=(self.width/4 -40, 50))
        description = wx.StaticText(self.panel, label="Enter a size and enter positions of blocks separated by spaces that is the specified size.\n\t\t\t\t\t Example: 1 4 3 2 5 with size = 5", pos=(self.width/8, 75))

        cipher_txt = wx.StaticText(self.panel, label="Cipher:", pos=(self.width/2- 50, 50))
        block = wx.TextCtrl(self.panel, -1, '',pos=(self.width/3,50), size=(50, -1))
        cipher_input = wx.TextCtrl(self.panel, -1, '',pos=(self.width/2,50), size=(150, -1))

        self.widgetSizer.Add(block_size, 0, wx.ALL, 5)
        self.widgetSizer.Add(description, 0, wx.ALL, 5)
        self.widgetSizer.Add(cipher_txt, 0, wx.ALL, 5)
        self.widgetSizer.Add(block, 0, wx.ALL, 5)
        self.widgetSizer.Add(cipher_input, 0, wx.ALL, 5)
        #TODO parse for only letters and spaces 
        # self.key.SetLabel("Perumation")

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