![Przykładowy wykres Grafana](grafana-dcn-macs.png)

## Co to robi?
Pobiera ilość wszystkich MAC ze swichy DCN S5750E-16X-SI. Następnie zapisuje je do bazy InfluxDB. Otrzymane wyniki można zwizualizować za pomocą grafany.

## Jak uruchomić?
* cp config.py.default config.py
* uzupełnić parametry w pliku config.py

## InfluxDB przydatne polecenia
* curl -G 'http://localhost:8086/query?db=macs' --data-urlencode 'q=SELECT * FROM "macs"'
* curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE macs"
* curl -i -XPOST http://localhost:8086/query --data-urlencode "q=DRP DATABASE macs"
