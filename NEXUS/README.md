# Co robi skrypt nexus-control-plane-arp-and-macs.py ?
Odczytuje ze switcha informacje o:
* ilości wszystkich MAC
* ilości wszystkich MAC typu multicast
* control-plane arp Out
* control-plane arp Drop
* control-plane arp pps

# Co robi skrypt nexus-environment.py ?
Odczytuje jaki jest pobór mocy, napięcie oraz natężenie prądu.

# Github:
https://github.com/kyob/

# InfluxDB przydatne polecenia
curl -G 'http://localhost:8086/query?db=macs' --data-urlencode 'q=SELECT * FROM "moja_baza"'
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE moja_baza"
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=DRP DATABASE moja_baza"

