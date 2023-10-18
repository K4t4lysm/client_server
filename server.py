from socket import * # Package für Sockets
import threading # Package für Threads, Timer, Events
import os # Package für Subprocess-Kommandos (Bash-Skripte)
import time # Package für die Messung von Systemzeiten
# Server hat die IP 192.168.119 im Demoaufbau
class MyServer: # Klasse für den Socket-Server
    echo_port=50007 # Port-Nummer des Servers (frei wählbar)
    bufsize=1024 # Max. Empfangs-/Sendebuffer
    def __init__(self): # Konstruktor der Klasse
        self.data_recv=None # Speicher für empfangene Nachricht
        self.data_send=None # Speicher für gesendete Nachrichten
        self.socket_connection=socket(AF_INET, SOCK_STREAM) # Einen IpV4-TCP/IP-Socket erzeugen
        self.socket_connection.bind(('', self.echo_port)) # Assoziiere den Socket mit einer Standard IP-Nummer
        self.socket_connection.listen(1) # Auf einen(!) Verbindungspartner (Client) warten
        print("Server gestartet") # Wenn ein Client erkannt wurde erfolgt die
        print("Namen des Hosts: ", gethostname()) # Nachricht, dass der Server mit eigener Host ID
        print("IP des Hosts: ", gethostbyname(gethostname())) # gestartet ist.
        # Hier wartet der Server, bis er einen Client akzeptiert hat. Server und Client sind nun eine Verbindung eingegangen.
        # Im Objekt self.conn sind alle Informationen über die angeschlossenen Clients enthalten!
        self.conn, (self.remotehost, self.remoteport)=self.socket_connection.accept()
        print("Verbunden mit %s %s"% (self.remotehost,self.remoteport)) # Ausgabe, mit welchem Client die Verbindung aufgenommen
        # wurde.
        self.thread_recv=threading.Thread(target=self.worker_recv) # Instanziiere einen Empfangsthread
        self.thread_send=threading.Thread(target=self.worker_send) # Instanziiere einen Sendethread
        self.laufzeit=30 # Laufzeit der Verbindung (zu Demonstrationszwecken)
        self.exit=False # Flag zum Beenden der Threads
        self.thread_recv.start() # Starten des Receive-Threads
        self.thread_send.start() # Starten des Send-Threads

    def worker_recv(self):  # Workerfunktion zum Auslesen der Socket-Nachricht
            while self.exit == False:  # Solange Exit-Flag False ist, wird ausgelesen.
                self.data_recv = self.conn.recv(self.bufsize)  # Auslesen des Empfangsbuffers
                if self.data_recv != None:  # Prüfe, ob Nachricht enthalten ist
                    print("Server empfängt Nachricht %s" % (self.data_recv))  # Ausgabe der Nachricht auf der Console

    def worker_send(self):  # Workerfunktion zum Senden einer
            while self.exit == False:  # Socketnachricht

                # Lese die aktuelle CPU-Temperatur des Raspberry PIs aus durch einen Subprocess-Call
                # Python nutzt hierbei die Möglichkeit, Kommandozeilen an das Betriebssystem zu senden
                self.data_send = os.popen('vcgencmd measure_clock arm').readline()
                # Zusammenbau des Strings, der über die Socketverbindung an den Client gesendet werden soll.
                self.data_send = "Server " + str(self.data_send) + " Noch: " + str(self.laufzeit) + " Sekunden"
                self.conn.send(self.data_send.encode())  # Die Nachricht wird vom Server versandt
                self.laufzeit -= 1  # Dekrementiere Laufzeitzähler um 1
                time.sleep(1)  # Warte 1 Sekunde bis zum nächsten Senden

    def stopp_connection(self):  # Methode zum Beenden der Threads und der

            # Socketverbindung
            self.exit = True  # Setze Exit-Flag auf True
            self.thread_recv.join()  # Beende Threads (warten ab bis beide
            self.thread_send.join()  # abgearbeitet sind.
            self.socket_connection.close()  # Schließe die Socketverbindung


server = MyServer()  # Instanziiere Server-Objekt
while server.laufzeit >= 0:  # Prüfe ob Laufzeitzähler >=0 ist
    None  # Alles bleibt aktiv
server.stopp_connection()