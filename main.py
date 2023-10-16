import threading # Klasse für alle Threading-Methoden
import time # Klasse für die Zeitmessung
class myThread (threading.Thread): # Klassendefinition mit geerbter Basisklasse Thread
    def __init__(self, threadID, name, delay_seconds): # Konstruktor mit weiteren Variablen
        threading.Thread.__init__(self) # Klasse myThread erbt alles von "Thread"
        self.threadID =threadID # Eigene Variablen der myThread-Klasse
        self.name=name
        self.delay=delay_seconds

    def run (self): # run-Methode ist die eigentliche Methode, welche im
        print ("Starting "+self.name) # Thread läuft.
        self.print_time(5) # Hier wird die Methode "print_time" 5 mal aufgerufen
        print ("Exiting "+self.name) # Nach Ablauf der 5 maligen Aufrufe ist die run-Methode
        # zu Ende.

    def print_time(self, counter): # print_time misst die Zeit und das Datum für den
        while counter: # bei jedem Aufruf auf. self.delay verzögert
            time.sleep(self.delay) # den print-Befehl.
            # Formatierte Printausgabe mit dem Threadnamen und der aktuellen Zeit
            print("%s: %s:" % (self.name, time.ctime(time.time())))
            counter -=1
            # Instanziierung der Threards

delay_thread1=1 # Eine Sekunde Verzögerung
delay_thread2=2 # Zwei Sekunden Verzögerung
thread1 = myThread(1, "Thread_schnell", delay_thread1) # ThreadID, Name, Verzögerungszeit für Thread1
thread2 = myThread(2, "Thread_langsam", delay_thread2) # ThreadID, Name, Verzögerungszeit für Thread2
# Start der Threads 1 und 2
thread1.start() # Threads sind abgearbeitet, sobald die run()-Methode beendet
thread2.start()

