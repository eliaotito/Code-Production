import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import sqlite3 as db
try:
    conn  = db.connect('train.db')
    cur = conn.cursor()
except:
    pass
cur.execute('''create table if not exists TrainInfor
(source text,
destionation text,
firstAC real,
secondAC real,
ThirdAC real,
sleeperAC real)''')
conn.commit()

cur.execute(''' create table if not exists PersonalInfo
(name text,
 contact int,
 nid text,
 address text,
 email text)''')
conn.commit()


cur.execute(''' create table if not exists Ticket(
coach text,
price real,
tickets int,
source text,
destination text,
total real
)''')

conn.commit()



##cur.execute(''' insert into  TrainInfor values('Mumbai','Delhi','1500','1400','1200','1300')''')
##cur.execute(''' insert into  TrainInfor values('Punjab','Gujarat','1600','1300','1100','1200')''')
##cur.execute(''' insert into  TrainInfor values('Delhi','Mumbai','1200','1100','1700','1900')''')
##cur.execute(''' insert into  TrainInfor values('Gujarat','Punjab','1300','1000','1500','1800')''')
##cur.execute(''' insert into  TrainInfor values('Mumbai','Gujarat','1200','1300','1400','1800')''')
##cur.execute(''' insert into  TrainInfor values('Gujarat','Mumbai','1200','1300','1400','1800')''')
##cur.execute(''' insert into  TrainInfor values('Delhi', 'Gujarat','1300','1400','1500','1800')''')
##cur.execute(''' insert into  TrainInfor values('Gujarat','Delhi','1300','1400','1500','1800')''')
##cur.execute(''' insert into  TrainInfor values('Mumbai','Punjab','1400','1300','1500','1800')''')
##cur.execute(''' insert into  TrainInfor values('Punjab','Mumbai','1400','1300','1500','1800')''')
##cur.execute(''' insert into  TrainInfor values('Delhi','Gujarat','1300','1400','1600','1800')''')
##cur.execute(''' insert into  TrainInfor values('Punjab','Delhi','1500','1600','1700','1800')''')
##cur.execute(''' insert into  TrainInfor values('Delhi','Punjab','1500','1600','1700','1800')''')
##cur.execute(''' insert into  TrainInfor values('Gujarat','Mumbai','1700','1800','1900','2800')''')
##cur.execute(''' insert into  TrainInfor values('Punjab','Gujarat','1900','2000','2100','2200')''')
##cur.execute(''' insert into  TrainInfor values('Gujarat','Punjab','1900','2000','2100','2200')''')
conn.commit()








class TrainResSystem:
    def __init__(self):
        #Initialize Database:
        cur.execute("select * from TrainInfor")
        trainInfo = cur.fetchall()
        source = set()
        destionation= set()
        for i in trainInfo:
            source.add(i[0])
            destionation.add(i[1])
        source = list(source)
        destionation= list(destionation)
        
        

        
        #Initialized Builder
        self.builder=Gtk.Builder() # Interface /Mediator for connecting UI and
        #Business Logic
        self.builder.add_from_file("TrainSystem.glade")
        self.builder.connect_signals(self) # To connect with our
        #Events Handlers Functions Buttons

        #Initialized Other Widgets:

        self.ticket_spin_button = self.builder.get_object("ticket_spin_button")
        self.source_combobox= self.builder.get_object("source_combobox")
        self.coach_combobox = self.builder.get_object("coach_combobox")
        self.Destination_Combobox= self.builder.get_object("Destination_Combobox")
        self.Full_Name_Entry = self.builder.get_object("Full_Name_Entry")
        self.Contact_Entry = self.builder.get_object("Contact_Entry")
        self.National_ID_Entry = self.builder.get_object("National_ID_Entry")
        self.residential_entry = self.builder.get_object("residential_entry")
        self.email_entry = self.builder.get_object("email_entry")

        #Initialize Ticket Dialog Widgets:
        self.ticket_box=self.builder.get_object('ticket_dialog')# My parent object ID
        self.coach_type= self.builder.get_object('coach_type')
        self.Price= self.builder.get_object('Price')
        self.tickets= self.builder.get_object('tickets')
        self.source_Station= self.builder.get_object('source_Station')
        self.destination_station= self.builder.get_object('destination_station')
        self.total_amount= self.builder.get_object('total_amount')
        
        #station = ['Mumbai','Delhi','Punjab','Gujarat']
        self.source_combobox.set_entry_text_column(0)
        self.Destination_Combobox.set_entry_text_column(0)

        coach = ['First Tier AC', 'Second Tier AC','Third Tie AC','Sleeper Class']
        self.coach_combobox.set_entry_text_column(0)
        
        for i in coach:
            self.coach_combobox.append_text(i)
            

        for i in source:
            self.source_combobox.append_text(i)
            

        for i in destionation:
            self.Destination_Combobox.append_text(i)    
    
        #Initialize Main Window
        self.win= self.builder.get_object("MainWin")# Grabbing the objects
        self.win.connect('destroy',Gtk.main_quit) # Once
        # we are going to press close button the applet window
        # will be closed / terminated
        self.win.show_all() # Used to show  the window
        # and all elements in the window


    def on_check(self,widget):
        pass
        #print(self.ticket_spin_button.get_value())

    def on_generate(self,widget):
       dialog=self.builder.get_object("ticket_dialog")
       
       no_tickets=int(self.ticket_spin_button.get_value())
       source=self.source_combobox.get_active_text()
       destionation=self.Destination_Combobox.get_active_text()
       coachType= self.coach_combobox.get_active_text()
       #print(self.coach_combobox.get_active())

       cur.execute("SELECT * From TrainInfor WHERE source =? and destionation=?",(source,destionation))
       #print(cur.fetchone())
       item = cur.fetchone()
       price = item[self.coach_combobox.get_active() + 2]
       totalPrice=no_tickets*price
     
       
       
       
       self.coach_type.set_text(coachType)
       self.Price.set_text(str(price))
       self.tickets.set_text(str(no_tickets))
       self.source_Station.set_text(source)
       self.destination_station.set_text(destionation)
       self.total_amount.set_text(str(totalPrice))
       
       
       dialog.run() # open your ticket dialog box
         
    def  on_clear(self,widget):
        self.Full_Name_Entry.set_text("")
        self.Contact_Entry.set_text("")
        self.National_ID_Entry.set_text("")
        self.residential_entry.set_text("")
        self.email_entry.set_text("")
        
        
        

    def  on_save(self,widget):
        ticket1= {'Coach':self.coach_type.get_text(),
                  'Price':self.Price.get_text(),
                  'Tickets':self.tickets.get_text(),
                  'Source Station':self.source_Station.get_text(),
                  'Destionation Station':self.destination_station.get_text(),
                  'Total Amount': self.total_amount.get_text()
            }
        with open('tickets.txt', 'a') as ticketsFile:
            for i in ticket1.items():
                ticketsFile.write(f'{i[0]}:{i[1]}\n')
       
        self.coach_type.get_text()
        self.Price.get_text()
        self.tickets.get_text()
        self.source_Station.get_text()
        self.destination_station.get_text()
        self.total_amount.get_text()

         

app= TrainResSystem() # Creating an object of class









Gtk.main()
conn.close()
