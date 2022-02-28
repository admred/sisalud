# SiSalud
Un sistema de turnos en linea 
para una tesis "Clinica de la Salud"

### 1  Como implementar (deploy) en ambiente Linux

git clone https://github.com/admred/sisalud.git

python3 -mvenv venv

source env.ini

source venv/bin/activate

pip3 install -r requeriments.txt

./recreate.sh

./run.sh


### 2 En navegador ingresar http://127.0.0.1:5000/

### 3 Logearse con "admin" y "1234" 

Todos los usuarios tienen la contraseña 1234.
Desde el "Listado" puede ver la cuenta de los usuarios
y logearse con ella para ver las opciones.
Segun el perfil van variando.

Este programa usa Flask 2.X , WTForms 2.X, SQLAlchemy, sqlite3 
bootstrap4

Este programa es una muestra o prueba, no asumo la responsabilidad
por los daños ocasionados.
