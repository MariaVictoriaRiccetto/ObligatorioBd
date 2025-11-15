create  database segunda;
USE segunda;


CREATE TABLE login(
    correo varchar(50) primary key ,
    contraseña varchar(50)
);

CREATE TABLE participante(
    ci int primary key ,
    nombre varchar (45) ,
    apellido varchar(45),
    email varchar(50)
);

CREATE TABLE facultad(
    id_facultad int primary key,
    nombre varchar(45)
);

CREATE TABLE edificio(
    id_edificio int primary key auto_increment,-- agregamos como primary key una id
    nombre_edificio varchar(45),
    direccion varchar(45),
    departamento varchar(45)

);

CREATE TABLE programa_academico(
    id_programa_academico int primary key auto_increment,-- agregamos como primary key una id
  nombre_programa VARCHAR(50),
  id_facultad INT,
  tipo VARCHAR(50),
  FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

CREATE TABLE participante_programa_academico(
  id_alumno_programa INT PRIMARY KEY,
  ci_participante INT,
    id_programa_academico int ,
  rol VARCHAR(15), -- estudiante o docente
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_programa_academico) REFERENCES programa_academico(id_programa_academico)-- usamos de referenica la nueva id de programa academico
);

CREATE TABLE sala(
    id_sala int primary key auto_increment,-- agregamos como primary key una id
  nombre_sala VARCHAR(50),
  id_edificio int(50),
  capacidad INT,
  tipo_sala VARCHAR(50),
  FOREIGN KEY (id_edificio) REFERENCES edificio(id_edificio)
);

CREATE TABLE turno(
  id_turno INT PRIMARY KEY,
  hora_inicio DATETIME,
  hora_fin DATETIME
);
-- pequeña confusion al poner datetime
ALTER TABLE turno
    MODIFY hora_inicio TIME,
    MODIFY hora_fin TIME;
-- ---------------------------------

CREATE TABLE reserva(
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    id_sala INT,
    fecha DATE,
    id_turno INT,
    estado VARCHAR(50),
    FOREIGN KEY (id_sala) REFERENCES sala(id_sala),
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);
CREATE TABLE sancion_participante(
    id_sancion INT PRIMARY KEY AUTO_INCREMENT,
    ci_participante INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);

CREATE TABLE reserva_participante(
    ci_participante INT,
    id_reserva INT,
    fecha_solicitud_reserva DATETIME,
    asistencia BOOLEAN,
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);


-- INSERTS


INSERT INTO facultad VALUES
(1,'Facultad de Ingeniería'),
(2,'Facultad de Ciencias Sociales'),
(3,'Facultad de Medicina'),
(4,'Facultad de Derecho'),
(5,'Facultad de Economía'),
(6,'Facultad de Arquitectura'),
(7,'Facultad de Psicología'),
(8,'Facultad de Artes'),
(9,'Facultad de Educación'),
(10,'Facultad de Ciencias');

INSERT INTO edificio(nombre_edificio, direccion, departamento) VALUES
('Sacré Cœur','Av. 8 de Octubre 2738', 'Montevideo'),
('San Jose', 'Av. 8 de Octubre 2733', 'Montevideo'),
('Semprun', 'Estero Bellaco 2771', 'Montevideo'),
('Mullin','Comandante Braga 2715', 'Montevideo'),
('San Ignacio', 'Cornelio Cantera 2733', 'Montevideo'),
('Athanasius', 'Gral. Urquiza 2871', 'Montevideo'),
('Madre Marta', 'Av. Garibaldi 2831', 'Montevideo'),
('Casa Xalambrí', 'Cornelio Cantera 2728', 'Montevideo');


INSERT INTO login VALUES
('natu@correo.ucu', 'soyNatu'),
('joaquin@correo.ucu', 'soyJoaquin'),
('vicky@correo.ucu', 'soyVicky'),
('nico@correo.ucu', 'soyNico'),
('bubu@correo.ucu', 'soyBubu'),
('guille@correo.ucu', 'soyGuille'),
('martu@correo.ucu', 'soyMartu'),
('pauli@correo.ucu', 'soyPauli'),
('poli@correo.ucu', 'soyPolipocket'),
('martin@correo.ucu', 'soyMartin'),
('juan@correo.ucu', 'soyJuan'),
('alfo@correo.ucu', 'soyAlfo'),
('franco@correo.ucu', 'soyFranco'),
('isa@correo.ucu', 'soyIsa'),
('fede@correo.ucu', 'soyFede');

INSERT INTO participante VALUES
(12345678, 'Natanael', 'Fernandez','natu@correo.ucu'),
(23456789, 'Joaquin', 'de Dios','joaquin@correo.ucu'),
(34567891, 'Victoria', 'Riccetto', 'vicky@correo.ucu'),
(45678912,'Nicolas', 'Wagner','nico@correo.ucu'),
(56789123,'Bruno', 'Ocampo', 'bubu@correo.ucu'),
(67891234, 'Guillermo', 'Gonzalez', 'guille@correo.ucu'),
(78912345, 'Martina', 'de Leon', 'martu@correo.ucu'),
(89123456, 'Paulina', 'Fernandez', 'pauli@correo.ucu'),
(91234567, 'Paula', 'Garro','poli@correo.ucu'),
(11223344, 'Martin', 'Sviridenko','martin@correo.ucu'),
(22334455,'Juan','Riccetto','juan@correo.ucu'),
(33445566, 'Alfonso', 'Gorga','alfo@correo.ucu'),
(44556677, 'Franco', 'Riccetto','franco@correo.ucu'),
(55667788, 'Isabela', 'Riccetto', 'isa@correo.ucu'),
(66778899,'Federico', 'Elgue','fede@correo.ucu');

INSERT INTO participante_programa_academico
(id_alumno_programa, ci_participante, id_programa_academico, rol)
VALUES
(1, 11223344, 1, 'estudiante'),
(2, 12345678, 2, 'estudiante'),
(3, 22334455, 3, 'estudiante'),
(4, 23456789, 4, 'estudiante'),
(5, 33445566, 5, 'estudiante'),
(6, 34567891, 6, 'estudiante'),
(7, 44556677, 7, 'estudiante'),
(8, 45678912, 8, 'estudiante'),
(9, 55667788, 9, 'estudiante'),
(10, 56789123, 10, 'estudiante'),
(11, 66778899, 3, 'estudiante'),
(12, 66778899, 9, 'estudiante'),
(13, 67891234, 1, 'estudiante'),
(14, 67891234, 5, 'estudiante'),
(15, 67891234, 10, 'estudiante'),
(16, 78912345, 4, 'estudiante'),
(17, 89123456, 6, 'estudiante'),
(18, 91234567, 7, 'estudiante');


INSERT INTO programa_academico(nombre_programa, id_facultad, tipo) VALUES
('Abogacia', 4, 'grado'),
('Agronomía', 1, 'grado'),
('Ingenieria en Informatica', 1, 'grado'),
('Artes Escenicas', 8, 'grado'),
('Fisioterapia', 3, 'grado'),
('Medicina', 3, 'grado'),
('Nutricion', 3, 'grado'),
('Business Analytics', 5, 'grado'),
('Economia', 5, 'grado'),
('Finanzas', 5, 'grado');


INSERT INTO sala(nombre_sala, id_edificio, capacidad, tipo_sala) VALUES
('sala 1', 1, 4, 'libre'),
('sala 2', 1, 3, 'libre'),
('sala 3', 1, 4, 'posgrado'),
('sala 4', 1, 2, 'docentes'),
('sala 5', 2, 4, 'libre'),
('sala 6', 2, 4, 'posgrado'),
('sala 7', 2, 2, 'posgrado'),
('sala 8', 2, 3, 'docentes'),
('sala 9', 3, 4, 'posgrado'),
('sala 10', 3, 3, 'posgrado'),
('sala 11', 3, 2, 'posgrado'),
('sala 12', 3, 4, 'posgrado'),
('sala 13', 4, 3, 'libre'),
('sala 14', 4, 2, 'libre'),
('sala 15', 4, 4, 'libre');


INSERT INTO turno VALUES
(1,'09:00:00','10:00:00'),
(2,'10:00:00','11:00:00'),
(3,'11:00:00','12:00:00'),
(4,'12:00:00','13:00:00'),
(5,'13:00:00','14:00:00'),
(6,'14:00:00','15:00:00'),
(7,'15:00:00','16:00:00'),
(8,'16:00:00','17:00:00'),
(9,'17:00:00','18:00:00'),
(10,'18:00:00','19:00:00');


INSERT INTO reserva(id_sala, fecha, id_turno, estado) VALUES
(1, '2025-10-05', 1, 'finalizada'),
(2, '2025-10-05', 2, 'finalizada'),
(3, '2025-10-05', 3, 'cancelada'),
(1, '2025-10-06', 4, 'cancelada'),
(12, '2025-10-06', 5, 'sin asistencia'),
(15, '2025-10-06', 6, 'activa'),
(6, '2025-10-07', 7, 'activa'),
(9, '2025-10-07', 8, 'cancelada'),
(13, '2025-10-07', 9, 'activa'),
(1, '2025-10-08', 10, 'activa'),
(4, '2025-10-08', 1, 'activa'),
(5, '2025-10-08', 1, 'cancelada'),
(8, '2025-10-09', 3, 'activa'),
(3, '2025-10-09', 4, 'activa'),
(7, '2025-10-09', 1, 'cancelada');

INSERT INTO reserva_participante VALUES
(12345678, 1, '2025-09-28 10:00:00', TRUE),
(23456789, 1, '2025-09-28 10:05:00', TRUE),

(34567891, 2, '2025-09-28 11:00:00', TRUE),
(45678912, 2, '2025-09-28 11:02:00', TRUE),

(56789123, 3, '2025-09-29 09:30:00', FALSE),
(67891234, 3, '2025-09-29 09:33:00', FALSE),

(78912345, 4, '2025-10-01 08:00:00', FALSE),

(89123456, 5, '2025-10-02 14:00:00', FALSE),
(91234567, 5, '2025-10-02 14:03:00', FALSE),

(11223344, 6, '2025-10-03 12:15:00', FALSE),
(22334455, 6, '2025-10-03 12:17:00', FALSE),

(33445566, 7, '2025-10-03 16:00:00', FALSE),
(44556677, 7, '2025-10-03 16:03:00', FALSE),

(55667788, 8, '2025-10-04 11:00:00', FALSE),

(66778899, 9, '2025-10-04 11:30:00', FALSE),
(12345678, 9, '2025-10-04 11:32:00', FALSE),

(23456789, 10, '2025-10-04 15:10:00', FALSE),

(34567891, 11, '2025-10-05 09:00:00', FALSE),
(45678912, 11, '2025-10-05 09:03:00', FALSE),

(56789123, 12, '2025-10-05 10:30:00', FALSE),

(67891234, 13, '2025-10-05 11:15:00', FALSE),
(78912345, 13, '2025-10-05 11:18:00', FALSE),

(89123456, 14, '2025-10-06 08:45:00', FALSE),

(91234567, 15, '2025-10-06 09:00:00', FALSE);

INSERT INTO sancion_participante(ci_participante, fecha_inicio, fecha_fin) VALUES
(89123456, '2025-10-06', '2025-12-06'),
(91234567, '2025-10-06', '2025-12-06');
-- insert participante academico
-- ver porque no anda el insert de reserva participante

-- CONSULTAS
-- veces reservadas cada sala
select s.nombre_sala, count(*) as cantidad_reservas
from reserva r
join sala s on r.id_sala = s.id_sala            -- FUNICONA NO TOCAR 
group by s.nombre_sala
order by cantidad_reservas desc;
-- devuelve la cantidad de veces que ser reservo un turno
/*
LISTO :arreglar los id de reservas para que aparezcan mas de una vez reservada cada sala
*/
select t.id_turno, count(*) as veces_reservado
from reserva r
join turno t on t.id_turno = r.id_turno -- FUNCIONA NO TOCAR
group by t.id_turno
order by veces_reservado desc
limit 1;

-- promedio de participantes por sala
-- avg es para hacer el promedio y roun ((),1) es para poner que devuelva solo un decimal despues de la coma
select s.nombre_sala, ROUND(avg(pr.cantidad_participante),1) as promedio_participantes
from sala s
join reserva r on r.id_sala=s.id_sala
left join (select id_reserva,count(ci_participante) as cantidad_participante                        -- FUNCIONA NO TOCAR
           from reserva_participante
           group by id_reserva)
pr on pr.id_reserva=r.id_reserva -- Unimos cada reserva con la cantidad de participantes que tiene (por id_reserva)
group by s.nombre_sala ;

-- reservas por facultad y carrera (programa_academico)
select f.nombre as facultad, p.nombre_programa as carrera, count(ppa.ci_participante) as cantidad_participantes
from facultad f
join programa_academico p on f.id_facultad = p.id_facultad                                             -- FUNCIONA NO TOCAR
left join participante_programa_academico ppa on p.id_programa_academico = ppa.id_programa_academico
group by f.nombre, p.nombre_programa
order by facultad,carrera;
