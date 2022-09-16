#!/usr/bin/python
# -*- coding: utf-8 -*-
# phonebook.py

import wx, wx.html
import os.path

#Το κείμενο html για το παράθυρο βοήθειας
helpText = u""" <h2>Προσθήκη επαφής</h2>
<p>Press add button and fill in details, all values must be filled</p>
<h2>Επεξεργασία-ενημέρωση επαφής</h2>
<p>Select Contact, press edit button and fill in details, all values must be filled</p>
<h2>Διαγραφή Επαφής</h2>
<p>Select Contact and press delete button</p>
<h2>Αναζήτηση επαφής</h2>
<p>Από το menu επιλέγουμε αναζήτηση κατά όνομα ή τηλέφωνο. Αν βρεθει η επαφή θα εμφανιστει στην τρέχουσα επαφή</p>"""

class MainFrame (wx.Frame):
    
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(500, 550))

        self.contactsList = [] #Λίστα με τα στοιχεια των επαφών
        self.InitGUI()
        self.GetContactsFromFile() #Διαβάζει τη λίστα επαφών από αρχείο

    #Αρχικοποιεί το GUI
    def InitGUI(self):

        #Δημιουργία μενού
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenuItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')

        editMenu=wx.Menu()
        addMenuItem = editMenu.Append(21, '&Add a person')
        editMenuItem = editMenu.Append(22, '&Edit a person')
        deleteMenuItem = editMenu.Append(23, '&Delete a person')
        menubar.Append(editMenu, '&Edit')

        searchMenu=wx.Menu()
        searchByNameMenuItem = searchMenu.Append(31, '&Search by name')
        searchByPhoneMenuItem = searchMenu.Append(32, '&Search by phone')
        menubar.Append(searchMenu, '&Search')
        
        helpMenu = wx.Menu()
        helpMenuItem = helpMenu.Append(wx.ID_HELP, 'Help', 'Help for this application')
        aboutMenuItem = helpMenu.Append(wx.ID_ABOUT, 'About', 'About this application')
        menubar.Append(helpMenu, '&Help')
   
        self.SetMenuBar(menubar)

        #Bind menu events
        self.Bind(wx.EVT_MENU, self.OnQuit, fileMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAdd, addMenuItem)
        self.Bind(wx.EVT_MENU, self.OnEdit, editMenuItem)
        self.Bind(wx.EVT_MENU, self.OnDelete, deleteMenuItem)
        self.Bind(wx.EVT_MENU, self.OnSearchByName, searchByNameMenuItem)
        self.Bind(wx.EVT_MENU, self.OnSearchByPhone, searchByPhoneMenuItem)
        self.Bind(wx.EVT_MENU, self.OnHelp, helpMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutMenuItem)

        #Bind system close button
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        #Contact Details GUI, το GUI για την τρέχουσα επαφή
        panel = wx.Panel(self, -1)
        headingText = wx.StaticText(panel, -1, label=u"Πληροφορίες Επαφής", pos=(5, 5)) #u μπροστά από κάθε utf string
        headingText.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        wx.StaticText(panel, label=u"Όνοματεπώνυμο", pos=(5, 50))
        wx.StaticText(panel, label=u"Τηλέφωνο", pos=(5, 80))
        wx.StaticText(panel, label="Email", pos=(5, 110))
        self.contactName = wx.TextCtrl(panel, pos=(120, 50), size=(200, 25))
        self.contactName.SetEditable(False)
        self.contactPhone = wx.TextCtrl(panel, pos=(120, 80), size=(200, 25))
        self.contactPhone.SetEditable(False)
        self.contactEmail = wx.TextCtrl(panel, pos=(120, 110), size=(200, 25))
        self.contactEmail.SetEditable(False)

        #Buttons
        addButton = wx.Button(panel, label='Add', pos=(50, 150))
        addButton.Bind(wx.EVT_BUTTON, self.OnAdd)
        editButton = wx.Button(panel, label='Edit', pos=(150, 150))
        editButton.Bind(wx.EVT_BUTTON, self.OnEdit)
        deleteButton = wx.Button(panel, label='Delete', pos=(250, 150))
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDelete)
                
        #Contacts List Control, το control που εμφανίζει τη λίστα επαφών
        self.contactsListCtrl = wx.ListCtrl(panel, pos=(50, 200), size=(400, 200), style=wx.LC_REPORT)
        self.contactsListCtrl.InsertColumn(0,u"Όνοματεπώνυμο")
        self.contactsListCtrl.InsertColumn(1,u"Τηλέφωνο")
        self.contactsListCtrl.InsertColumn(2,"Email")
        self.contactsListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

    #Φορτώνει τις επαφές από αρχειο στην λίστα contactsList  , αν δεν υπάρχει το δημιουργεί
    def GetContactsFromFile(self):
        #check if file phonebook.txt exist
        if os.path.isfile("phonebook.txt"):
            print 'File already exists, reading contacts'
            fo = open("phonebook.txt", "r")
            for line in fo:
                line = unicode(line, 'utf-8')       #διαβάζω την γραμμή ως utf
                self.contactsList.append(line.strip().split(','))
        else:
            #create file phonebook.txt
            print 'Creating file phonebook.txt'
            fo = open("phonebook.txt", "w")
        fo.close()

    #Γράφει τις επαφές σε αρχείο, αυτό γίνεται στο τέλος του προγράμματος
    def WriteContactsToFile(self):
        print 'writing contacts to file'
        fw = open("phonebook.txt", "w")
        for contact in self.contactsList:
            name, phone, email = contact
            line = name + ',' + phone + ',' + email
            fw.write("%s\n" % line.encode('utf-8'))     #encode σε utf πριν την εγγραφή στο αρχείο
        fw.close()

    #Εγγράφει την λίστα επαφών contactsList στο control contactsListCtrl ώστε να εμφανιστούν στο παράθυρο
    #Αυτό γίνεται στην αρχή του προγράμματος και μετά απο κάθε add, edit και delete    
    def PopulateList(self):
        self.contactsList.sort()
        self.contactsListCtrl.DeleteAllItems()
        for i in range(len(self.contactsList)) :
            name,phone,email = self.contactsList[i]
            self.contactsListCtrl.InsertStringItem(i, name)
            self.contactsListCtrl.SetStringItem(i, 1, phone)
            self.contactsListCtrl.SetStringItem(i, 2, email)
        self.contactsListCtrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.contactsListCtrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.currentSelection = 0

    #Όταν επιλέγει μια επαφή απο τη λίστα εμφανίζει στο παράθυρο τις λεπτομέρεις επαφής
    def OnItemSelected(self, event):
        self.currentSelection = event.m_itemIndex
        name, phone, email = self.contactsList[self.currentSelection]
        self.contactName.SetValue(name)
        self.contactPhone.SetValue(phone)
        self.contactEmail.SetValue(email)
        #print "Selected", self.currentSelection

    #Προσθήκη επαφής
    def OnAdd(self, event):
        dlg = AddEditDialog(self, -1, 'Add Contact')
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            self.contactsList.append ([dlg.contactName.GetValue(), dlg.contactPhone.GetValue(), dlg.contactEmail.GetValue()])
            self.PopulateList()
        dlg.Destroy()

    #Επεγεργασία-ενημέρωση επαφής
    def OnEdit(self, event):
        if self.contactsList: #Check if list not empty
            dlg = AddEditDialog(self, -1, 'Edit Contact')
            name, phone, email = self.contactsList[self.currentSelection]
            dlg.contactName.SetValue(name)
            dlg.contactPhone.SetValue(phone)
            dlg.contactEmail.SetValue(email)
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                self.contactsList[self.currentSelection]= [dlg.contactName.GetValue(), dlg.contactPhone.GetValue(), dlg.contactEmail.GetValue()]
                self.PopulateList()
        
    #Διαγραφή επαφής
    def OnDelete(self, event):
        if self.contactsList: #Check if list not empty
            dlg = wx.MessageDialog(self, u"Είστε σίγουρος ότι θέλετε να διαγράψετε την επαφή","Confirm Delete", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                del self.contactsList[self.currentSelection]
                self.contactsListCtrl.Select(0)
                self.PopulateList()

    #Κλείσιμο εφαρμογής
    def OnQuit(self, event):
        self.WriteContactsToFile()
        #self.Close()
        self.Destroy()


    #Αναζητά επαφή, prompt το κείμενο του παραθύρου, title o τιτλος του παραθύρου
    #index = 0 αναζητά όνομα, #index = 1 αναζητά τηλέφωνο
    #Δεν λαμβανει υποψιν μικρά-κεφαλαία. Σταματά στην πρώτη επαφή που βρίσκει
    def SearchContact(self, prompt, title, index):
        dlg = wx.TextEntryDialog(None, prompt, title)
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            searchTerm = dlg.GetValue()
            found = False
            for i in range(len(self.contactsList)):
                if self.contactsList[i][index].lower() == searchTerm.lower():
                    found = True
                    self.contactsListCtrl.Select(self.currentSelection, 0) #deselect curent item
                    self.contactsListCtrl.Select(i) #select found item
                    break
            if found:
                message = u"Βρέθηκε επαφή"
            else:
                message = u"ΔΕΝ βρέθηκε επαφή με τα στοιχεία που δώσατε"
            wx.MessageBox(message, 'Info', wx.OK | wx.ICON_INFORMATION)
        
    #Αναζήτηση κατά όνομα
    def OnSearchByName(self, event):
        self.SearchContact('Enter a contact name to search', 'Search by Name', 0)

    #Αναζήτηση κατά τηλέφωνο
    def OnSearchByPhone(self, event):
        self.SearchContact('Enter a contact phone to search', 'Search by Phone', 1)

    #Εμφανίζει το παράθυρο βοήθειας
    def OnHelp(self, event):
        dlg = HelpBox()
        dlg.ShowModal()
        dlg.Destroy()

    #Εμφανίζει παράθυρο πληροφοριών
    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.SetName('Phone Book')
        info.SetVersion('1.0')
        info.SetDescription(u"Εφαρμογή τηλεφωνικού κσαταλόγου")
        info.SetCopyright('(C) Unicersity of ....')
        #info.SetWebSite('http://www.zetcode.com')
        info.AddDeveloper(u'Ονοματεπώνυμο developer')
        wx.AboutBox(info)
        
#Κλάση με παράθυρο διαλόγου για προσθήκη ή επεξεργασία επαφής
class AddEditDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(350,250))
        #Ετικέτες και πεδία
        panel = wx.Panel(self, -1)
        headingText = wx.StaticText(panel, -1, label=title, pos=(5, 5))
        headingText.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        wx.StaticText(panel, label=u"Όνοματεπώνυμο", pos=(5, 50))
        wx.StaticText(panel, label=u"Τηλέφωνο", pos=(5, 80))
        wx.StaticText(panel, label="Email", pos=(5, 110))
        self.contactName = wx.TextCtrl(panel, pos=(120, 50), size=(200, 25))
        self.contactPhone = wx.TextCtrl(panel, pos=(120, 80), size=(200, 25))
        self.contactEmail = wx.TextCtrl(panel, pos=(120, 110), size=(200, 25))
        #Buttons
        okButton = wx.Button(panel, wx.ID_OK, label='OK', pos=(120, 150))
        cancelButton = wx.Button(panel, label='Cancel', pos=(220, 150))
        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnClose)

    #Button OK, ελέγχει αν συμπληρώθηκαν όλα τα πεδία και επιστρέφει κώδικα ID_OK
    def OnOK(self, e):
        if (self.contactName.GetValue() and  self.contactPhone.GetValue() and  self.contactEmail.GetValue()):
            self.Destroy()
            self.SetReturnCode(wx.ID_OK)
        else:
            wx.MessageBox(u'Παρακαλώ συμπληρώστε όλα τα πεδία', 'Info', wx.OK | wx.ICON_INFORMATION)

    #Κλεινει το παράθυρο
    def OnClose(self, e):
        self.Destroy()

#κλάση για html κείμενο
class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
        
#παράθυρο βοήθειας με html κείμενο
class HelpBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "Help for app")
        hwin = HtmlWindow(self, -1, size=(200,200))
        hwin.SetPage(helpText)
        self.SetFocus()
        
class PhoneBookApp (wx.App):
    def OnInit (self):
        frame = MainFrame(None, 'Phone Book')
        frame.Show(True)
        frame.PopulateList()
        frame.contactsListCtrl.Select(0)
        self.SetTopWindow(frame)
        
        return True

app = PhoneBookApp(0)
app.MainLoop()
