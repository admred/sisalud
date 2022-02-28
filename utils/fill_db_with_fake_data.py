#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3
from faker import *
from random import randint,choice
from datetime import *

N_ADMIN=1
N_DOCTOR=10
N_PATIENT=100
N_RECEPTIONIST=3

PASSWORD = 'pbkdf2:sha256:260000$l6l8pNEMnz3MSqCg$b0c10fb38d95252d4e92b63a822d8b220c874d68fb47e0f90099a645a69cef91' # 1234

DB_URI = 'file:///home/user/TESIS_FINAL/v3/webapp/database.db?synchronous=off&journal=off&cache=shared&nolock=1'

social_secure=(
    (100106,'OBRA SOCIAL PARA EL PERSONAL DE LA INDUSTRIA ACEITERA DESMOTADORA Y AFINES','OSIAD'),
    (100205,'OBRA SOCIAL DE ACTORES','OSA'),
    (100304,'OBRA SOCIAL DE TECNICOS DE VUELO DE LINEAS AEREAS','OSTVLA'),
    (100403,'OBRA SOCIAL DEL PERSONAL SUPERIOR Y PROFESIONAL DE EMPRESAS AEROCOMERCIALES','OSPEA'),
    (100502,'OBRA SOCIAL DEL PERSONAL AERONAUTICO','OSPA'),
    (100601,'OBRA SOCIAL DEL PERSONAL DE AERONAVEGACION DE ENTES PRIVADOS','OSPADEP'),
    (100700,'OBRA SOCIAL DEL PERSONAL TECNICO AERONAUTICO','OSPTA'),
    (100809,'OBRA SOCIAL DE AERONAVEGANTES','OSA'),
    (100908,'OBRA SOCIAL EMPLEADOS DE AGENCIAS DE INFORMES','OSEADI'),
    (101000,'OBRA SOCIAL DEL PERSONAL DE AGUAS GASEOSAS Y AFINES','OSPAGA'),
    (101109,'OBRA SOCIAL DE ALFAJOREROS REPOSTEROS  PIZZEROS Y HELADEROS','OSARPYH'),
    (101208,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DE LA ALIMENTACION','OSPIA'),
    (101604,'OBRA SOCIAL DEL PERSONAL DEL AUTOMOVIL  CLUB ARGENTINO','OSPACA'),
    (101802,'OBRA SOCIAL DEL PERSONAL DEL AZUCAR DEL INGENIO LA ESPERANZA','OSPA'),
    (101901,'OBRA SOCIAL DEL PERSONAL DEL AZUCAR DEL INGENIO LEDESMA','OSPAIL'),
    (102300,'OBRA SOCIAL DEL PERSONAL DEL AZUCAR DEL INGENIO SAN MARTIN','OSPA'),
    (102706,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA AZUCARERA','OSPIA'),
    (103006,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA BOTONERA','OSPIB'),
    (103105,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL CALZADO','OSPICAL'),
    (103402,'OBRA SOCIAL DEL PERSONAL DE CARGA Y DESCARGA','OSPCYD'),
    (103600,'OBRA SOCIAL DEL PERSONAL AUXILIAR DE CASAS PARTICULARES','OSPACP'),
    (103709,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL CAUCHO','OSPIC'),
    (103808,'OBRA SOCIAL DEL PERSONAL DEL CAUCHO','OSPECA'),
    (103907,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL CAUCHO DE SANTA FE','OSPIC SANTA FE'),
    (104009,'OBRA SOCIAL DEL PERSONAL DE CEMENTERIOS DE LA REPUBLICA ARGENTINA.','OSPCRA'),
    (104108,'OBRA SOCIAL DE CERAMISTAS','OSCE'),
    (104207,'OBRA SOCIAL DEL PERSONAL DE LA CERAMICA SANITARIOS  PORCELANA DE MESA Y AFINES','OSPCSPMYA'),
    (104306,'OBRA SOCIAL DEL PERSONAL DE LA ACTIVIDAD CERVECERA Y AFINES','OSPACA'),
    (104405,'OBRA SOCIAL DEL PERSONAL CINEMATOGRAFICO DE MAR DEL PLATA','OSPERCIN'),
    (104504,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA CINEMATOGRAFICA','OSPIC'),
    (104603,'OBRA SOCIAL DE OPERADORES CINEMATOGRAFICOS','OSOC'),
    (104801,'OBRA SOCIAL DE COLOCADORES DE AZULEJOS MOSAICOS  GRANITEROS  LUSTRADORES Y PORCELANEROS','OSCAMGLYP'),
    (105002,'OBRA SOCIAL DE CONDUCTORES NAVALES','OSCONARA'),
    (105309,'OBRA SOCIAL DEL PERSONAL ADMINISTRATIVO Y TECNICO DE LA CONSTRUCCION Y AFINES','OSPATCA'),
    (105408,'OBRA SOCIAL DEL PERSONAL DE LA CONSTRUCCION','OSPECON'),
    (105507,'OBRA SOCIAL DE LOS CORTADORES DE LA INDUMENTARIA','OSUCI'),
    (105606,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL CUERO Y AFINES','OSPICA'),
    (105705,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL CHACINADO Y AFINES','OSPICHA'),
    (105804,'OBRA SOCIAL DE CHOFERES DE CAMIONES','OSCHOCA'),
    (106005,'OBRA SOCIAL DEL PERSONAL DE ENTIDADES DEPORTIVAS Y CIVILES','OSPEDYC'),
    (106104,'OBRA SOCIAL DE EMPLEADOS DE DESPACHANTES DE ADUANA','OSEDA'),
    (106203,'OBRA SOCIAL DEL PERSONAL DE DISTRIBUIDORAS CINEMATOGRAFICAS DE LA R.A.','OSPEDICI'),
    (106302,'OBRA SOCIAL DE DOCENTES PARTICULARES','OSDOP'),
    (106401,'OBRA SOCIAL DEL PERSONAL DE EDIFICIOS DE RENTA Y HORIZONTAL DE LA REPUBLICA ARGENTINA','OSPERYHRA'),
    (106500,'OBRA SOCIAL DEL PERSONAL DE EDIFICIOS DE RENTA Y HORIZONTAL DE LA CIUDAD AUTONOMA DE BUENOS AIRES  Y GRAN BUENOS AIRES','OSPERYH'),
    (106609,'OBRA SOCIAL ELECTRICISTAS NAVALES','OSEN'),
    (106807,'OBRA SOCIAL DEL PERSONAL DE LA ENSEÑANZA PRIVADA','OSPEP'),
    (106906,'OBRA SOCIAL DEL PERSONAL DE ESCRIBANIAS DE LA PROVINCIA DE BUENOS AIRES','OSPEPBA'),
    (107008,'OBRA SOCIAL DEL PERSONAL DE ESCRIBANOS','OSPE'),
    (107107,'OBRA SOCIAL DEL PERSONAL DEL ESPECTACULO PUBLICO','OSPEP'),
    (107206,'OBRA SOCIAL DEL PERSONAL DE ESTACIONES DE SERVICIO GARAGES  PLAYAS DE ESTACIONAMIENTO Y LAVADEROS AUTOMATICOS','OSPESGYPE'),
    (107404,'OBRA SOCIAL DEL PERSONAL DE FARMACIA','OSPF'),
    (107800,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL FIBROCEMENTO','OSPIF'),
    (107909,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA FIDEERA','OSPIF'),
    (108001,'OBRA SOCIAL  PARA EL PERSONAL DE LA INDUSTRIA FORESTAL DE SANTIAGO DEL ESTERO','OSPIFSE'),
    (108100,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL FOSFORO ENCENDIDO Y AFINES','OSPIF'),
    (108209,'OBRA SOCIAL DE FOTOGRAFOS','OSFOT'),
    (108407,'OBRA SOCIAL DEL PERSONAL DE LA ACTIVIDAD FRUTICOLA','OSPAF'),
    (108506,'OBRA SOCIAL DEL PERSONAL DE MANIPULEO EMPAQUE Y EXPEDICION DE FRUTA FRESCA Y HORTALIZAS DE CUYO','OSFYHC'),
    (108605,'OBRA SOCIAL DE FUTBOLISTAS','FAA'),
    (108704,'OBRA SOCIAL DE TECNICOS DE FUTBOL','OSTECF'),
    (108803,'OBRA SOCIAL  DE LA UNION  DE TRABAJADORES  DEL TURISMO HOTELEROS Y GASTRONOMICOS DE LA REPUBLICA  ARGENTINA','OSUTHGRA'),
    (109004,'OBRA SOCIAL DEL PERSONAL GRAFICO','OSPG'),
    (109301,'OBRA SOCIAL DEL PERSONAL DE CONSIGNATARIOS DEL MERCADO NACIONAL DE HACIENDA DE LINIERS','OSPEMER'),
    (109400,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL HIELO Y MERCADOS PARTICULARES','OSPIHMP)','COLOMBRES 1573   (SINDICATO'),
    (109509,'OBRA SOCIAL DEL PERSONAL DE LOS HIPODROMOS DE BUENOS AIRES Y SAN ISIDRO','OSPHGBAYSI'),
    (109707,'OBRA SOCIAL DEL PERSONAL DE IMPRENTA DIARIOS Y AFINES','OSPIDA'),
    (110008,'OBRA SOCIAL DEL PERSONAL DE JABONEROS','OSPEJ'),
    (110107,'OBRA SOCIAL DE JARDINEROS PARQUISTAS  VIVERISTAS Y FLORICULTORES DE LA REPUBLICA ARGENTINA','OSJPVYF'),
    (110305,'OBRA SOCIAL DEL PERSONAL LADRILLERO','OSPL'),
    (110404,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA LADRILLERA A MAQUINA','OSPILM'),
    (110503,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA LECHERA','OSPIL'),
    (110602,'OBRA SOCIAL DE LOCUTORES','OSDEL'),
    (110701,'OBRA SOCIAL DE LA FEDERACION ARGENTINA DE TRABAJADORES DE LUZ Y FUERZA','OSFATLYF'),
    (110800,'OBRA SOCIAL DE LOS TRABAJADORES DE LAS EMPRESAS DE ELECTRICIDAD','OSTEE'),
    (110909,'OBRA SOCIAL DEL PERSONAL DE LUZ Y FUERZA DE CORDOBA','OSLYF'),
    (111001,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA MADERERA','OSPIM'),
    (111209,'OBRA SOCIAL DEL PERSONAL DE MAESTRANZA','OSPM'),
    (111407,'OBRA SOCIAL DE CAPITANES DE ULTRAMAR Y OFICIALES DE LA MARINA MERCANTE','OSCOMM'),
    (111506,'OBRA SOCIAL DE CAPITANES BAQUEANOS FLUVIALES DE LA MARINA MERCANTE','OSCAPBAQFLU'),
    (111605,'OBRA SOCIAL DE EMPLEADOS DE LA MARINA MERCANTE','OSEMM'),
    (111704,'OBRA SOCIAL DE ENCARGADOS APUNTADORES MARITIMOS','OSEAM'),
    (111803,'OBRA SOCIAL DEL PERSONAL MARITIMO','OSPM'),
    (111902,'OBRA SOCIAL DEL SINDICATO DE MECANICOS Y AFINES DEL TRANSPORTE AUTOMOTOR','OSMATA'),
    (112004,'OBRA SOCIAL DEL PERSONAL SUPERIOR MERCEDES BENZ ARGENTINA','OSPS MERCEDES'),
    (112103,'OBRA SOCIAL DE LA UNION OBRERA METALURGICA DE LA REPUBLICA ARGENTINA','OSUOMRA'),
    (112202,'OBRA SOCIAL DE LOS  SUPERVISORES DE LA INDUSTRIA METALMECANICA DE LA REPUBLICA ARGENTINA','OSSIMRA'),
    (112301,'OBRA SOCIAL DEL PERSONAL DE  MICROS Y OMNIBUS DE MENDOZA','OSPEMOM'),
    (112400,'OBRA SOCIAL DE LA ACTIVIDAD MINERA','O.S.A.M.'),
    (112509,'OBRA SOCIAL MODELOS ARGENTINOS','OSMA'),
    (112608,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA MOLINERA','OSPIM'),
    (112707,'OBRA SOCIAL DEL PERSONAL MOSAISTA','OSPM'),
    (112806,'OBRA SOCIAL DE MUSICOS','OSDEM'),
    (113205,'OBRA SOCIAL DE JEFES Y OFICIALES NAVALES DE RADIOCOMUNICACIONES','OSJONR'),
    (113304,'OBRA SOCIAL DE JEFES Y OFICIALES MAQUINISTAS NAVALES','OSJOMN'),
    (113403,'OBRA SOCIAL DEL PERSONAL NAVAL','OSPENA'),
    (113601,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL NEUMATICO','OSPIN'),
    (113700,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA NAVAL','OSPIN'),
    (113908,'OBRA SOCIAL DEL PERSONAL DE PANADERIAS','OSPEP'),
    (114000,'OBRA SOCIAL DE PANADEROS PASTELEROS Y FACTUREROS DE ENTRE RIOS','OSSPYFER'),
    (114109,'OBRA SOCIAL DEL PERSONAL DEL PAPEL CARTON Y QUIMICOS','OSPPCYQ'),
    (114208,'OBRA SOCIAL DE LA INDUSTRIA DE PASTAS ALIMENTICIAS','OSIPA'),
    (114307,'OBRA SOCIAL TRABAJADORES  PASTELEROS CONFITEROS  PIZZEROS   HELADEROS Y ALFAJOREROS DE LA REPUBLICA ARGENTINA','OSTPCHPYARA'),
    (114703,'OBRA SOCIAL DEL PERSONAL DE PELUQUERIAS ESTETICAS Y AFINES','OSPPEA'),
    (114901,'OBRA SOCIAL DE OFICIALES PELUQUEROS Y PEINADORES DE ROSARIO','OSOFPP DE ROSARIO'),
    (115003,'OBRA SOCIAL DEL PERSONAL DE LA ACTIVIDAD PERFUMISTA','OSPAP'),
    (115102,'OBRA SOCIAL DE TRABAJADORES DE PRENSA DE BUENOS AIRES','OSTPBA'),
    (115201,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL PESCADO DE MAR DEL PLATA','OSPIP'),
    (115300,'OBRA SOCIAL DE PETROLEROS','OSPE'),
    (115409,'OBRA SOCIAL DEL PETROLEO Y GAS PRIVADO','OSPEGAP'),
    (115508,'OBRA SOCIAL DE PETROLEROS DE CORDOBA','O.S.PE.COR'),
    (115607,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA PETROQUIMICA','OSPIP'),
    (115706,'OBRA SOCIAL PARA PILOTOS DE LINEAS AEREAS COMERCIALES Y REGULARES','OSPLA'),
    (115805,'OBRA SOCIAL DEL PERSONAL DE FABRICAS DE PINTURA','UPFPARA'),
    (116006,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL PLASTICO','OSPIP'),
    (116105,'OBRA SOCIAL DE CAPATACES  ESTIBADORES PORTUARIOS','OSCEP'),
    (116204,'OBRA SOCIAL DE PORTUARIOS ARGENTINOS','OSPA'),
    (117207,'OBRA SOCIAL DEL PERSONAL DE PRENSA DE LA REPUBLICA ARGENTINA','OSPPRA'),
    (117702,'OBRA SOCIAL DEL PERSONAL DE PRENSA DE MAR DEL PLATA','OSPREN'),
    (118002,'OBRA SOCIAL DE EMPLEADOS DE PRENSA DE CORDOBA','OSEPC'),
    (118200,'OBRA SOCIAL DE AGENTES DE PROPAGANDA MEDICA DE LA REPUBLICA ARGENTINA','OSAPM'),
    (118309,'OBRA SOCIAL DE AGENTES DE PROPAGANDA MEDICA DE CORDOBA','OSAPMCBA)','AVDA OLMOS 485 PISO 2 (ESQUINA STAGO DEL ESTERO'),
    (118408,'OBRA SOCIAL DE AGENTES DE PROPAGANDA MEDICA DE ENTRE RIOS','OSAPMER'),
    (118606,'OBRA SOCIAL DEL PERSONAL DE LA PUBLICIDAD','OSPP'),
    (118705,'OBRA SOCIAL DEL PERSONAL DE INDUSTRIAS QUIMICAS Y PETROQUIMICAS','OSPIQYP'),
    (118804,'OBRA SOCIAL DE RECIBIDORES DE GRANOS Y ANEXOS','OSRGA'),
    (119203,'OBRA SOCIAL DE RELOJEROS Y JOYEROS','OSRJA'),
    (119302,'OBRA SOCIAL DEL PERSONAL RURAL Y ESTIBADORES DE LA REPUBLICA ARGENTINA','OSPRERA'),
    (119500,'OBRA SOCIAL DEL PERSONAL DE LA SANIDAD ARGENTINA','OSPSA'),
    (119609,'OBRA SOCIAL DEL PERSONAL DE INSTALACIONES SANITARIAS','OSPIS'),
    (119708,'OBRA SOCIAL DEL PERSONAL DE SEGURIDAD COMERCIAL INDUSTRIAL E INVESTIGACIONES PRIVADAS','OSPSIP'),
    (120306,'OBRA SOCIAL DEL PERSONAL DE SUPERVISION DE LA EMPRESA SUBTERRANEOS DE BUENOS AIRES','OSPSESBA'),
    (120405,'OBRA SOCIAL DEL PERSONAL DE DIRECCION DE LA EMPRESA SUBTERRANEOS DE BUENOS AIRES','OSPDESBA'),
    (120504,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA  DEL TABACO','OSPIT'),
    (120603,'OBRA SOCIAL DE EMPLEADOS DEL TABACO DE LA REPUBLICA ARGENTINA','OSETRA'),
    (120702,'OBRA SOCIAL DEL PERSONAL DE LAS TELECOMUNICACIONES DE LA REPUBLICA ARGENTINA','OSTEL'),
    (120801,'OBRA SOCIAL DE TRABAJADORES DE LAS COMUNICACIONES','OSTRAC'),
    (120900,'OBRA SOCIAL DEL PERSONAL DE TELEVISION','OSPTV'),
    (121002,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA TEXTIL','OSPIT'),
    (121101,'OBRA SOCIAL DE EMPLEADOS TEXTILES Y AFINES','OSETYA'),
    (121309,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL TRACTOR','OSPIT'),
    (121507,'OBRA SOCIAL DE LA INDUSTRIA DEL TRANSPORTE  AUTOMOTOR DE CORDOBA','OSITAC'),
    (121705,'OBRA SOCIAL DEL PERSONAL DE LA ACTIVIDAD DEL TURF','OSPAT'),
    (121804,'OBRA SOCIAL CONDUCTORES DE TAXIS DE CORDOBA','OSTC'),
    (122005,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL VESTIDO','OSPIV'),
    (122104,'OBRA SOCIAL DE VIAJANTES VENDEDORES DE LA REPUBLICA ARGENTINA. (ANDAR)','OSVVRA'),
    (122302,'OBRA SOCIAL DEL PERSONAL DE LA ACTIVIDAD VIAL','OSPA-VIAL'),
    (122401,'OBRA SOCIAL DE  EMPLEADOS DE LA INDUSTRIA DEL VIDRIO','OSEIV'),
    (122500,'OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA DEL VIDRIO','OSPIV'),
    (122609,'OBRA SOCIAL DEL PERSONAL DE LA ACTIVIDAD VITIVINICOLA','OSPAV'),
    (122807,'OBRA SOCIAL DEL PERSONAL DE VIGILANCIA Y SEGURIDAD COMERCIAL INDUSTRIAL E INVESTIGACIONES PRIVADAS DE CORDOBA','OSPEVIC'),
    (122906,'OBRA SOCIAL DEL PERSONAL DE ESTACIONES DE SERVICIO GARAGES PLAYAS Y LAVADEROS AUTOMATICOS DE LA PROVINCIA DE SANTA FE','OSPESGA'),
    (123008,'OBRA SOCIAL PARA EL PERSONAL DE ESTACIONES DE SERVICIO GARAGES  PLAYAS DE ESTACIONAMIENTO  LAVADEROS AUTOMATICOS Y GOMERIAS DE LA REPUBLICA ARGENTINA','OSPES'),
    (123107,'OBRA SOCIAL TALLERISTAS A DOMICILIO','OSTAD'),
    (123305,'OBRA SOCIAL DEL PERSONAL DE SOCIEDADES DE AUTORES Y AFINES','OSPESA)','MONTEVIDEO 453  (DOMICILIO PROVISORIO'),
    (123404,'OBRA SOCIAL DEL PERSONAL DE PRENSA DE ROSARIO','OSPRO'),
    (123503,'OBRA SOCIAL DEL PERSONAL DE PRENSA DE TUCUMAN','OSPRENTUC'),
    (123602,'OBRA SOCIAL DE TRABAJADORES DE PERKINS ARGENTINA S.A.I.C','OSTP'),
    (123701,'OBRA SOCIAL DE PEONES DE TAXIS DE LA CAPITAL FEDERAL','OSPETAX'),
    (123909,'OBRA SOCIAL DE VENDEDORES AMBULANTES DE LA REPUBLICA ARGENTINA','OSVARA'),
    (124001,'OBRA SOCIAL DE BOXEADORES AGREMIADOS DE LA REPUBLICA ARGENTINA','OSBARA'),
    (124506,'OBRA SOCIAL DE TRABAJADORES DE LA INDUSTRIA DEL GAS','OSTIG'),
    (125103,'OBRA SOCIAL DE LOS PROFESIONALES UNIVERSITARIOS DEL AGUA Y LA ENERGIA ELECTRICA','OSPUAYE'),
    (125301,'OBRA SOCIAL FEDERAL DE LA FEDERACION NACIONAL DE TRABAJADORES DE OBRAS SANITARIAS','OSFFENTOS'),
    (125509,'OBRA SOCIAL DE LA FEDERACION ARGENTINA DEL TRABAJADOR  DE LAS UNIVERSIDADES NACIONALES','OSFATUN'),
    (125707,'OBRA SOCIAL UNION PERSONAL DE LA UNION DEL  PERSONAL CIVIL DE LA NACION','OSPCN'),
    (125905,'OBRA SOCIAL DE ARBITROS DEPORTIVOS DE LA REPUBLICA ARGENTINA','OSADRA'),
    (126106,'OBRA SOCIAL PARA LOS TRABAJADORES DE LA EDUCACION PRIVADA','OSTEP'),
    (126205,'OBRA SOCIAL DE LOS EMPLEADOS DE COMERCIO Y ACTIVIDADES CIVILES','OSECAC'),
    (126304,'OBRA SOCIAL SERVICIOS SOCIALES BANCARIOS','OSBA'),
    (126502,'OBRA SOCIAL DE LA CONFEDERACION DE OBREROS Y EMPLEADOS MUNICIPALES  ARGENTINA ( OSCOEMA )','OSCOEMA'),
    (126601,'OBRA SOCIAL DEL PERSONAL DE INDUSTRIAS  QUIMICAS Y PETROQUIMICAS DE ZARATE CAMPANA','OPZC'),
    (126809,'OBRA SOCIAL DE CONDUCTORES DE REMISES Y AUTOS AL INSTANTE Y AFINES','OSCRAIA'),
    (126908,'OBRA SOCIAL DE LOS MEDICOS DE LA CIUDAD DE BUENOS AIRES','OSMEDICA'),
    (127000,'OBRA SOCIAL DE TRABAJADORES DE ESTACIONES DE SERVICIO','OSTES'),
    (127109,'OBRA SOCIAL DEL PERSONAL DE TELECOMUNICACIONES SINDICATO BUENOS AIRES','OSPETELCO'),
    (127208,'OBRA SOCIAL DE MANDOS MEDIOS DE TELECOMUNICACIONES EN LA REPUBLICA ARGENTINA Y MERCOSUR','OSMMEDT'),
    (127406,'OBRA SOCIAL DE OBREROS Y EMPLEADOS TINTOREROS SOMBREREROS Y LAVADEROS DE LA REPUBLICA ARGENTINA','OSOETSYLARA'),
    (127505,'OBRA SOCIAL DE  LAS ASOCIACIONES DE EMPLEADOS DE FARMACIA','OSADEF'),
    (127604,'OBRA SOCIAL PARA EL PERSONAL DE OBRAS Y SERVICIOS SANITARIOS','OSOSS'),
    (127703,'OBRA SOCIAL PERSONAL ESTACIONES DE SERVICIO GARAGES PLAYAS Y LAVADEROS DE LA PROVINCIA DEL CHACO','OSPESCHA'),
    (127802,'OBRA SOCIAL DE LUZ Y FUERZA DE LA PATAGONIA','OSLYF PATAGONIA'),
    (127901,'OBRA SOCIAL DE PETROLEROS PRIVADOS','OS.PE.PRI'),
    (128102,'OBRA SOCIAL DE LA UNION DE TRABAJADORES DEL INSTITUTO NACIONAL DE SERVICIOS SOCIALES PARA JUBILADOS Y PENSIONADOS DE LA REPUBLICA ARGENTINA','OSUTI'),
    (128201,'OBRA SOCIAL DEL SINDICATO UNICO DE RECOLECTORES DE RESIDUOS Y BARRIDO DE CORDOBA','O.S.S.U.R.R.B.A.C'),
    (128300,'OBRA SOCIAL PEONES DE TAXIS DE ROSARIO','O.S.PE.TAX.R'),
    (128409,'OBRA SOCIAL DEL SINDICATO OBREROS Y EMPLEADOS DE EMPRESAS DE LIMPIEZA','OSSOELSAC'),
    (128508,'OBRA SOCIAL DE FARMACEUTICOS Y BIOQUIMICOS','OSFYB'),
    (128706,'OBRA SOCIAL DEL PERSONAL DE DRAGADO Y BALIZAMIENTO','OSPEDYB'),
    (128805,'OBRA SOCIAL DEL PERSONAL ADUANERO DE LA REPUBLICA ARGENTINA','OSPAD'),
    (128904,'OBRA SOCIAL DE LOS TRABAJADORES ARGENTINOS DE CENTROS DE CONTACTOS','O.S.T.A.C.C'),
    (129006,'OBRA SOCIAL DE LA ASOCIACION DEL PERSONAL SUPERIOR DE LA EMPRESA PROVINCIAL DE ENERGIA DE CORDOBA','O.S.A.P.S.E'),
    (None,'Swix Medical',None),
    (134999,'Medi Fe',None),
    )


specialities=(
    ('Medicina general','Es especialidad médica que proporciona atenión sanitaria general.'),
    ('Dermatología','Es la especialidad médica que estudia de la estrutura y función de la piel, las enfermedades que la afectan, su diagnóstio, prevenión y tratamiento.'),
    ('Ginecología','Es una especialidad que se dedica al estudio y tratamiento de diversos problemas y enfermedades del aparato genital.'),
    ('Obstetricia','La especialidad médica que estudia  embarazo y el parto.'),
    ('Oftalmología','Es la especialidad média que estudia las enfermedades del ojo como su tratamiento.'),
    ('Pediatría','La pediatría es la especialidad que estudia al niño y sus enfermedades, desde el nacimiento hasta la adolesenia.'),
    ('Psiquiatría','Es la especialidad de la medicina que se ocupa del estudio, el diagnóstio, el tratamiento y la prevenión de las enfermedades mentales.'),
    ('Urología','Es la especialidad médio que se ocupa del estudio, diagnóstio y tratamiento de las patologías que afetan al aparato urinario, glándulas suprarrenales y retroperitoneo de hombres y mujeres y el aparato reprodutor.'),
    ('Traumatologia','Es la ciencia que estudia la estructura osea y sus enfermedades.'),
    ('Cardiologia','Es la ciencia que estudia las enfermedades relacionados corazon y sistema circulatorio.'),
    )

def insert_social_secure():
    con=sqlite3.connect(DB_URI,uri=True)
    cur=con.cursor()
    cur.execute('DELETE FROM socialsecure;')
    for c in social_secure:
        cur.execute('INSERT INTO socialsecure (rnos,short,name,address,phone,email) VALUES (?,?,?,?,?,?);',(
                c[0],
                c[2],
                c[1],
                "Calle %d"%randint(1,2300),
                "%d"%(randint(10000,1000000000),),
                "email_%d@example.com"%(randint(1,1000000000),),
                ))
    con.commit()
    con.close()

def insert_speciality():
    db=sqlite3.connect(DB_URI,uri=True)
    cur=db.cursor()
    cur.execute('DELETE FROM speciality;')
    cur.executemany('INSERT INTO speciality (name,description) VALUES (?,?);',specialities)
    db.commit()
    db.close()


def create_user(_type,count,cur):
    profile_id={"admin":1,"doctor":2,"patient":3,"receptionist":4,"anonymous":5}[_type]
    faker=Faker(lang='es',use_weighting=False)
    for i in range(count):
        email=faker.email()
        username=email.split('@')[0]
        try:
            cur.execute('INSERT INTO user  (dni,username,password,firstname,secondname,lastname,phone,address,email,profile_id,_type) VALUES (?,?,?,?,?,?,?,?,?,?,?)',(
                randint(10000000,40000000),
                username,
                PASSWORD,
                faker.first_name(),
                faker.first_name(),
                faker.last_name(),
                randint(1000000,9999999),
                faker.address(),
                email,
                profile_id,
                _type
            ))
        except Exception:
            email=faker.email()
            username=email.split('@')[0]
            cur.execute('INSERT INTO user  (dni,username,password,firstname,secondname,lastname,phone,address,email,profile_id,_type) VALUES (?,?,?,?,?,?,?,?,?,?,?)',(
                randint(10000000,40000000),
                username,
                PASSWORD,
                faker.first_name(),
                faker.first_name(),
                faker.last_name(),
                randint(1000000,9999999),
                faker.address(),
                email,
                profile_id,
                _type
            ))

def create_doctor(count,cur):
    matricula=None
    id=None

    cur.execute('SELECT count() FROM speciality;')
    n_esp=cur.fetchone()[0]
    assert n_esp != None and n_esp >0

    create_user("doctor",count,cur)
    cur.execute('SELECT id FROM user WHERE profile_id=2;')
    for row in cur.fetchall():
        matricula=randint(10000,99999)
        speciality_id=randint(1,n_esp)
        cur.execute('INSERT INTO doctor  (id,license_,speciality_id) VALUES (?,?,?)',(
            row[0],
            randint(1000000,9999999),
            speciality_id,
        ))

def create_patient(count,cur):
    cobertura_id=None

    cur.execute('SELECT count() FROM socialsecure;')
    n_cob=cur.fetchone()[0]
    assert n_cob != None and n_cob >0

    create_user("patient",count,cur)
    cur.execute('SELECT id FROM user WHERE profile_id=3;')
    for row in cur.fetchall():
        cobertura_id = randint(1,n_cob)
        cur.execute('INSERT INTO patient (id,socialsecure_id) VALUES (?,?)',(row[0],cobertura_id))

def create_receptionist(count,cur):
    create_user("receptionist",count,cur)

def create_admin(count,cur):

    cur.execute('INSERT INTO user (username, password, dni, firstname, secondname, lastname,profile_id,_type) VALUES ("admin", "%s",0,"Admin","Admin","Admin",1,"admin")'%(PASSWORD,))
    for i in range(1,count):
        cur.execute('INSERT INTO user (dni,username,password,firstname,secondname,lastname,profile_id,_type) VALUES (%d,"admin%d","%s","Admin%d","Admin%d","Admin%d",1,"admin");'%(i,i,PASSWORD,i,i,i));

def insert_all_users():
    con=sqlite3.connect(DB_URI,uri=True)
    assert con != None

    cur=con.cursor()
    cur.execute('DELETE FROM user;')
    cur.execute('DELETE FROM doctor;')
    cur.execute('DELETE FROM patient;')

    create_admin(N_ADMIN,cur)
    create_receptionist(N_RECEPTIONIST,cur)
    create_doctor(N_DOCTOR,cur)
    create_patient(N_PATIENT,cur)

    con.commit()
    con.close()

def insert_appointment():
    con=sqlite3.connect(DB_URI,uri=True)
    assert con != None
    cur=con.cursor()

    cur.execute('DELETE FROM appointment;')

    q=cur.execute('SELECT id FROM doctor;')
    assert q != []

    doctors_ids=[ x[0] for x in q ]
    today=datetime.today()
    start_date=today+timedelta(days=-60)
    start_hour=8
    start_date=datetime(start_date.year,start_date.month,start_date.day,start_hour)
    diff=today+timedelta(days=30)-start_date
    days=diff.days

    for day in range(1,days):
        when=start_date+timedelta(days=day)
        for _id in doctors_ids:
            duration=choice([2,4,6,8])
            cur.execute('INSERT INTO appointment ("when",duration,is_canceled,doctor_id) VALUES (?,?,?,?)',(when.strftime("%F %T"),duration,False,_id))

    con.commit()
    con.close()

def insert_turn():
    con=sqlite3.connect(DB_URI,uri=True)
    assert con != None
    cur=con.cursor()

    cur.execute('DELETE FROM turn;')
    q=cur.execute('SELECT id FROM doctor;')
    assert q != []
    doctors_ids=[ x[0] for x in q ]


    q=cur.execute('SELECT id FROM patient;')
    assert q != []
    patients_ids=[ x[0] for x in q ]

    q=cur.execute('SELECT id,"when",duration,doctor_id  FROM appointment;')
    assert q != []
    appointments=[ x for x in  q ]


    tomorrow=datetime.now()+timedelta(days=1)
    i = 0
    for s in appointments:
        when=datetime.strptime(s[1],"%Y-%m-%d %H:%M:%S")
        doctor_id=s[3]
        _stop=when+timedelta(hours=s[2])
        while when <= _stop:
            duration=choice([15,15,15,15,15,15,15,15,15,15,15,15,15,30,30,30,30,60])
            if when < tomorrow :
                is_available= False
                is_missed = ( True if randint(1,10) == 1 else False )
                patient_id = patients_ids[i % N_PATIENT]
            else:
                is_missed = False
                is_available=True
                patient_id = None

            cur.execute('INSERT INTO turn ("when",duration,is_available,is_missed,is_canceled,doctor_id,patient_id) VALUES (?,?,?,?,?,?,?)',(
                when.strftime("%F %T"),
                duration,
                is_available,
                is_missed,
                False,
                doctor_id,
                patient_id,
            ))
            i+=1
            when=when + timedelta(minutes=duration)

    con.commit()
    con.close()


def test_created():
    con=sqlite3.connect(DB_URI,uri=True)
    assert con != None

    cur=con.cursor()
    cur.execute('SELECT count() FROM speciality;')
    n=cur.fetchone()[0]
    assert n == len(specialities)

    cur.execute('SELECT count() FROM socialsecure;')
    n=cur.fetchone()[0]
    assert n == len(social_secure)

    cur.execute('SELECT count() FROM doctor;')
    n=cur.fetchone()[0]
    assert n == N_DOCTOR

    cur.execute('SELECT count() FROM patient;')
    n=cur.fetchone()[0]
    if n != N_PATIENT:
        print("n : ",n)
        print("N_PATIENT : ",N_PATIENT)

    assert n == N_PATIENT
    cur.execute('SELECT count() FROM user WHERE profile_id=4;')
    n=cur.fetchone()[0]
    assert n == N_RECEPTIONIST

    cur.execute('SELECT count() FROM user WHERE profile_id=1;')
    n=cur.fetchone()[0]
    assert n == N_ADMIN

    cur.execute('SELECT count() FROM turn;')
    n=cur.fetchone()[0]
    assert n !=0

    cur.execute('SELECT count() FROM appointment;')
    n=cur.fetchone()[0]
    assert n !=0

    con.close()


def main():
    insert_speciality()
    insert_social_secure()
    insert_all_users()
    insert_appointment()
    insert_turn()
    test_created()
    print ('OK Test passed' )

if __name__ == '__main__':
    main()
