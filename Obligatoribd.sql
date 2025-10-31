USE ObligatorioBd;

-- ==========================
-- TABLAS BASE
-- ==========================
CREATE TABLE facultad(
  id_facultad INT PRIMARY KEY,
  nombre_facultad VARCHAR(50)
);

CREATE TABLE edificio(
  nombre_edificio VARCHAR(50) PRIMARY KEY,
  direccion VARCHAR(50),
  departamento VARCHAR(20)
);


CREATE TABLE programa_academico(
  nombre_programa VARCHAR(50) PRIMARY KEY,
  id_facultad INT,
  tipo VARCHAR(50),
  FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

CREATE TABLE participante_programa_academico(
  id_alumno_programa INT PRIMARY KEY,
  ci_participante INT,
  nombre_programa VARCHAR(50),
  rol VARCHAR(15), -- estudiante o docente
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (nombre_programa) REFERENCES programa_academico(nombre_programa)
);

CREATE TABLE sala(
  nombre_sala VARCHAR(50),
  edificio VARCHAR(50),
  capacidad INT,
  tipo_sala VARCHAR(50),
  PRIMARY KEY (nombre_sala, edificio),
  FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio)
);

CREATE TABLE turno(
  id_turno INT PRIMARY KEY,
  hora_inicio DATETIME,
  hora_fin DATETIME
);

CREATE TABLE reserva(
  id_reserva INT PRIMARY KEY,
  nombre_sala VARCHAR(50),
  edificio VARCHAR(50),
  fecha DATE,
  id_turno INT,
  estado VARCHAR(50),
  FOREIGN KEY (nombre_sala, edificio) REFERENCES sala(nombre_sala, edificio),
  FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);

-- ==========================
-- INSERTS
-- ==========================
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

INSERT INTO edificio VALUES
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

INSERT INTO programa_academico VALUES
('Abogacia', 4, 'grado'),
('Agronomía', 1, 'grado'),
('Ingenieria en Informatica', 1, 'grado'),
('Ingenieria Audiovisual', 1, 'grado'),
('Artes Escenicas', 8, 'grado'),
('Fisioterapia', 3, 'grado'),
('Medicina', 3, 'grado'),
('Nutricion', 3, 'grado'),
('Business Analytics', 5, 'grado'),
('Economia', 5, 'grado'),
('Finanzas', 5, 'grado');

INSERT INTO sala VALUES
('sala 1', 'Sacré Cœur', 4, 'libre'),
('sala 2', 'Sacré Cœur', 3, 'libre'),
('sala 3', 'Sacré Cœur', 4, 'posgrado'),
('sala 4', 'Sacré Cœur', 2, 'docentes'),
('sala 5', 'San Jose', 4, 'libre'),
('sala 6', 'San Jose', 4, 'posgrado'),
('sala 7', 'San Jose', 2, 'posgrado'),
('sala 8', 'San Jose', 3, 'docentes'),
('sala 9', 'Semprun', 4, 'posgrado'),
('sala 10', 'Semprun', 3, 'posgrado'),
('sala 11', 'Semprun', 2, 'posgrado'),
('sala 12', 'Semprun', 4, 'posgrado'),
('sala 13', 'Mullin', 3, 'libre'),
('sala 14', 'Mullin', 2, 'libre'),
('sala 15', 'Mullin', 4, 'libre');

INSERT INTO turno VALUES
(1,'2025-10-05 09:30:00', '2025-10-05 11:30:00'),
(2,'2025-10-05 09:40:00', '2025-10-05 11:00:00'),
(3,'2025-10-05 08:00:00', '2025-10-05 09:00:00'),
(4,'2025-10-06 09:30:00', '2025-10-06 11:30:00'),
(5,'2025-10-06 08:30:00', '2025-10-06 09:30:00'),
(6,'2025-10-06 10:00:00', '2025-10-06 12:00:00'),
(7,'2025-10-07 15:00:00', '2025-10-07 17:00:00'),
(8,'2025-10-07 10:15:00', '2025-10-07 11:00:00'),
(9,'2025-10-07 16:30:00', '2025-10-07 18:30:00'),
(10,'2025-10-08 08:30:00', '2025-10-08 10:30:00'),
(11,'2025-10-08 12:00:00', '2025-10-08 13:30:00'),
(12,'2025-10-08 08:00:00', '2025-10-08 10:00:00'),
(13,'2025-10-09 14:30:00', '2025-10-09 16:30:00'),
(14,'2025-10-09 13:00:00', '2025-10-09 14:00:00'),
(15,'2025-10-09 17:30:00', '2025-10-09 19:30:00');

INSERT INTO reserva VALUES
(1, 'sala 1','Sacré Cœur', '2025-10-05', 1, 'finalizada'),
(2, 'sala 2','Sacré Cœur', '2025-10-05', 2, 'finalizada'),
(3, 'sala 3','Sacré Cœur', '2025-10-05', 3, 'cancelada'),
(4, 'sala 1','Sacré Cœur', '2025-10-06', 4, 'cancelada'),
(5, 'sala 12','Semprun', '2025-10-06', 5, 'sin asistencia'),
(6, 'sala 15','Mullin', '2025-10-06', 6, 'activa'),
(7, 'sala 6','San Jose', '2025-10-07', 7, 'activa'),
(8, 'sala 9','Semprun', '2025-10-07', 8, 'cancelada'),
(9, 'sala 13','Mullin', '2025-10-07', 9, 'activa'),
(10, 'sala 1','Sacré Cœur', '2025-10-08', 10, 'activa'),
(11, 'sala 4','Sacré Cœur', '2025-10-08', 11, 'activa'),
(12, 'sala 5','San Jose', '2025-10-08', 12, 'cancelada'),
(13, 'sala 8','San Jose', '2025-10-09', 13, 'activa'),
(14, 'sala 3','Sacré Cœur', '2025-10-09', 14, 'activa'),
(15, 'sala 7','San Jose', '2025-10-09', 15, 'cancelada');
