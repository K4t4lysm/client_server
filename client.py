from socket import * # Package für Sockets
import threading # Package für Threads, Timer, Events
import os # Package für Subprocess-Komando (Bash-Skripte)
import time # Package für die Messung von Systemzeiten
class MyClient: # Klasse für den SocketClient
    server_port=50007 # Port-Nummer des Servers (frei wählbar)
    bufsize=1024 # Max. Empfangs-/Sendebuffer
    host = "192.168.2.119" # Host-ID des Servers
    def __init__(self): # Konstruktor der Klasse
        self.data_recv=None # Speicher für empfangene Nachricht
        self.data_send=None # Speicher für gesendete Nachrichten
        self.socket_connection=socket(AF_INET, SOCK_STREAM) # Einen IpV4-TCP/IP-Socket erzeugen
        self.thread_recv=threading.Thread(target=self.worker_recv) # Instanziiere einen Empfangsthread
        self.thread_send=threading.Thread(target=self.worker_send) # Instanziiere einen Sendethread
        self.laufzeit=30 # Laufzeit der Verbindung
        self.socket_connection.connect((self.host,self.server_port)) # Verbindung zum Server aufbauen
        print("Verbunden mit dem Server %s: " %(self.host))
        self.exit=False # Flag zum Beenden der Threads
        self.thread_recv.start() # Starten des Receive-Threads
        self.thread_send.start() # Starten des Send-Threads

    def worker_recv(self):  # Workerfunktion zum Auslesen der
        while self.exit == False:  # Socket-Nachricht
            self.data_recv = self.socket_connection.recv(self.bufsize)  # Auslesen des Empfangsbuffers

        if self.data_recv != None:  # Prüfe, ob Nachricht enthalten ist
            print("Client empfängt Nachricht %s" % (self.data_recv))  # Ausgabe der Nachricht

    def worker_send(self):  # Workerfunktion zum Senden einer
        while self.exit == False:  # Socketnachricht

            # Lese die aktuelle CPU-Temperatur des Raspberry PIs aus
            self.data_send = os.popen('vcgencmd measure_temp').readline()  # Subprocess einer Kommondozeile unter Python
            self.data_send = "Client " + str(self.data_send) + " Noch: " + str(self.laufzeit) + " Sekunden"
            self.socket_connection.send(self.data_send.encode())
            self.laufzeit -= 1  # Dekrementiere Laufzeit um 1
            time.sleep(1)  # Warte 1 Sekunde

    def stopp_connection(self):  # Methode zum Beenden der Threads und der

        # Socketverbindung
        self.exit = True  # Setze Exit-Flag auf True
        self.thread_recv.join()  # Beende Threads (warten ab bis beide
        self.thread_send.join()  # abgearbeitet sind.
        self.socket_connection.close()  # Schließe die Socketverbindung



client = MyClient()  # Instanziiere Client-Objekt
while client.laufzeit >= 0:  # Prüfe ob Laufzeit >=0 ist
    print(MyClient().laufzeit)
    None  # Alles bleibt aktiv
client.stopp_connection()  # Leite Beendigung der Threads und der
# Socketverbindung ein