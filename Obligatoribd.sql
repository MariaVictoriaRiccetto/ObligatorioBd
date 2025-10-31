create table login(correo varchar(20) primary key, contrasenia varchar(100));
create table participante(ci integer primary key , nombre varchar(50),apellido varchar(50),email varchar(20),
                          foreign key (email) references login(correo));
create table programa_academico(nombre_programa varchar(50) primary key ,id_facultad integer,tipo varchar(50),
                                foreign key (id_facultad) references facultad(id_facultad));
create table participante_programa_academico( id_alumno_programa integer primary key, ci_participante integer, nombre_programa varchar(50), rol varchar(15),
                            foreign key (ci_participante) references participante(ci)); #estudiante o docente
create table facultad(id_facultad integer primary key, nombre_facultad varchar(50));
create table sala(nombre_sala varchar(50),edificio varchar(50),capacidad integer,tipo_sala  varchar(50) ); #docente, libre o postgrado hay que hacer una pk combinada entre nombre_sala y edificio
create table edificio(nombre_edificio varchar(50) primary key ,direccion varchar(50), departamento varchar(20));
create table turno(id_turno integer primary key,hora_inicio datetime, hora_fin datetime);
create table reserva(id_reserva integer primary key, nombre_sala varchar(50),edificio varchar(50),fecha date,id_turno integer,estado varchar(50),
                        foreign key (id_turno) references turno (id_turno));# estados pueden ser activa,cancelada, sin asistencia o finalizada

/*
 ------------------------------------------------------------------------
                                Inserts
 ------------------------------------------------------------------------
 */

INSERT INTO facultad(id_facultad, nombre_facultad) VALUES(1,'Facultad de Ingeniería'),(2,'Facultad de Ciencias Sociales'),(3,'Facultad de Medicina'),
                                                       (4,'Facultad de Derecho'),(5,'Facultad de Economía'),(6,'Facultad de Arquitectura'),
                                                       (7,'Facultad de Psicología'),(8,'Facultad de Artes'),(9,'Facultad de Educación'),
                                                       (10,'Facultad de Ciencias');

INSERT INTO login(correo, contrasenia) VALUES ('natu@correo.ucu', 'soyNatu'),('joaquin@correo.ucu', 'soyJoaquin'), ('vicky@correo.ucu', 'soyVicky'),
                                              ('nico@correo.ucu', 'soyNico'), ('bubu@correo.ucu', 'soyBubu'), ('guille@correo.ucu', 'soyGuille'),
                                              ('martu@correo.ucu', 'soyMartu'), ('pauli@correo.ucu', 'soyPauli'), ('poli@correo.ucu', 'soyPolipocket'),
                                              ('martin@correo.ucu', 'soyMartin'), ('juan@correo.ucu', 'soyJuan'), ('alfo@correo.ucu', 'soyAlfo'),
                                              ('franco@correo.ucu', 'soyFranco'), ('isa@correo.ucu', 'soyIsa'), ('fede@correo.ucu', 'soyFede');

INSERT INTO participante(ci, nombre, apellido, email) VALUES (12345678, 'Natanael', 'Fernandez','natu@correo.ucu' ),(23456789, 'Joaquin', 'de Dios','joaquin@correo.ucu' ), (34567891, 'Victoria', 'Riccetto', 'vicky@correo.ucu'),
                                                             (45678912,'Nicolas', 'Wagner','nico@correo.ucu'),(56789123,'Bruno', 'Ocampo', 'bubu@correo.ucu'),(67891234, 'Guillermo', 'Gonzalez', 'guille@correo.ucu'),
                                                             (78912345, 'Martina', 'de Leon', 'martu@correo.ucu'),(89123456, 'Paulina', 'Fernandez', 'pauli@correo.ucu'),(912345678, 'Paula', 'Garro','poli@correo.ucu' ),
                                                             (11223344, 'Martin', 'Sviridenko','martin@correo.ucu'),(22334455,'Juan','Riccetto','juan@correo.ucu'),(33445566, 'Alfonso', 'Gorga','alfo@correo.ucu'),
                                                             (44556677, 'Franco', 'Riccetto','franco@correo.ucu'),(55667788, 'Isabela', 'Riccetto', 'isa@correo.ucu'),(66778899,'Federico', 'Elgue','fede@correo.ucu' );

INSERT INTO programa_academico(nombre_programa, id_facultad, tipo) VALUES ('Abogacia', 4, 'grado'),('Agronomía', 1, 'grado'),('Ingenieria en Informatica', 1, 'grado'),
                                                                          ('Ingenieria Audiovisual', 1, 'grado'),('Artes Escenicas', 8, 'grado'),('Fisioterapia', 3, 'grado'),
                                                                          ('Medicina', 3, 'grado'),('Nutricion', 3, 'grado'),('Business Analytics', 5, 'grado'),
                                                                          ('Economia', 5, 'grado'),('Finanzas', 5, 'grado'),('Abogacia', 4, 'grado');

INSERT INTO sala(nombre_sala, edificio, capacidad, tipo_sala) VALUES ('sala 1', 'Sacré Cœur', 4, 'libre'),
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

INSERT INTO edificio(nombre_edificio, direccion, departamento) VALUES ('Sacré Cœur','Av. 8 de Octubre 2738', 'Montevideo'),
                                                                      ('San Jose', 'Av. 8 de Octubre 2733', 'Montevideo'),
                                                                      ('Semprun', 'Estero Bellaco 2771', 'Montevideo'),
                                                                      ('Mullin','Comandante Braga 2715', 'Montevideo'),
                                                                      ('San Ignacio', 'Cornelio Cantera 2733', 'Montevideo'),
                                                                      ('Athanasius', 'Gral. Urquiza 2871', 'Montevideo'),
                                                                      ('Madre Marta', 'Av. Garibaldi 2831', 'Montevideo'),
                                                                      ('Casa Xalambrí', 'Cornelio Cantera 2728', 'Montevideo');

INSERT INTO turno(id_turno, hora_inicio, hora_fin) VALUES (01,'2025-10-05 09:30:00', '2025-10-05 11:30:00'),(02,'2025-10-05 09:40:00', '2025-10-05 11:00:00'),(03,'2025-10-05 08:00:00', '2025-10-05 09:00:00'),
                                                          (04,'2025-10-06 09:30:00', '2025-10-06 11:30:00'),(05,'2025-10-06 08:30:00', '2025-10-06 09:30:00'),(06,'2025-10-06 10:00:00', '2025-10-06 12:00:00'),
                                                          (07,'2025-10-07 15:00:00', '2025-10-07 17:00:00'),(08,'2025-10-07 10:15:00', '2025-10-07 11:00:00'),(09,'2025-10-07 16:30:00', '2025-10-07 18:30:00'),
                                                          (10,'2025-10-08 08:30:00', '2025-10-08 10:30:00'),(11,'2025-10-08 12:00:00', '2025-10-08 13:30:00'),(12,'2025-10-08 08:00:00', '2025-10-08 10:00:00'),
                                                          (13,'2025-10-09 14:30:00', '2025-10-09 16:30:00'),(14,'2025-10-09 13:00:00', '2025-10-09 14:00:00'),(15,'2025-10-09 17:30:00', '2025-10-05 19:30:00');

INSERT INTO reserva(id_reserva, nombre_sala, edificio, fecha, id_turno, estado) VALUES (01, 'sala 1','Sacré Cœur', '2025-10-05', 01, 'finalizada'),(02, 'sala 2','Sacré Cœur', '2025-10-05', 02, 'finalizada'),(03, 'sala 3','Sacré Cœur', '2025-10-05', 03, 'cancelada'),
                                                                                       (04, 'sala 1','Sacré Cœur', '2025-10-06', 04, 'cancelada'),(05, 'sala 12','Semprun', '2025-10-06', 05, 'sin asistencia'),(06, 'sala 15','Mullin', '2025-10-06', 06, 'activa'),
                                                                                       (07, 'sala 6','San Jose', '2025-10-07', 07, 'activa'),(08, 'sala 9','Semprun', '2025-10-07', 08, 'cancelada'),(09, 'sala 13','Mullin', '2025-10-07', 09, 'activa'),
                                                                                       (10, 'sala 1','Sacré Cœur', '2025-10-08', 10, 'activa'),(11, 'sala 4','Sacré Cœur', '2025-10-08', 11, 'activa'),(12, 'sala 5','San Jose', '2025-10-08', 12, 'cancelada'),
                                                                                       (13, 'sala 8','San Jose', '2025-10-09', 13, 'activa'),(14, 'sala 3','Sacré Cœur', '2025-10-09', 14, 'activa'),(15, 'sala 7','San Jose', '2025-10-09', 15, 'cancelada');






