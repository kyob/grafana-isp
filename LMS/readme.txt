# Co robi skrypt lms-klienci.py ?
Pobiera z bazy LMS aktualną ilość klientów usuniętych, aktywnych oraz wszystkich klientów. Następnie zapisuje je do bazy InfluxDB. Otrzymane dane można zwizualizować za pomocą grafany.

# Co robi skrypt lms-taryfy.py ?
Pobiera z bazy LMS wszystkie aktywyne taryfy i zlicza ilu klientów używa tych taryf. Następnie zapisuje je do bazy InfluxDB. Otrzymane dane można zwizualizować za pomocą grafany.

# Github:
https://github.com/kyob/

# InfluxDB przydatne polecenia
curl -G 'http://localhost:8086/query?db=macs' --data-urlencode 'q=SELECT * FROM "lms_klienci"'
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE lms_klienci"
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=DRP DATABASE lms_klienci"

