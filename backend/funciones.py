from bd import get_connection

def esta_sancionado(ci):
    conn=get_connection()
    cursor=conn.cursor()

    query=("Select * from sancion_participante "
           "WHERE ci_participante=%s  AND CURDATE() BETWEEN fecha_inicio AND fecha_fin")

    cursor.execute(query, (ci,))
    resultado=cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado is not None:
        return True

    return False;

def sala_existe(id_sala):
    conn=get_connection()
    cursor=conn.cursor()

    query=("SELECT 1 from sala "
          "WHERE id_sala=%s "
           "Limit 1;")

    cursor.execute(query,(id_sala,))
    resultado=cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado is None:
        return False

    return True


def turnos_validos(id_turnos):
    conn = get_connection()
    cursor = conn.cursor()

    for turno in id_turnos:
        cursor.execute("SELECT 1 FROM turno WHERE id_turno = %s", (turno,))
        resultado = cursor.fetchone()

        if resultado is None:
            cursor.close()
            conn.close()
            return False

    cursor.close()
    conn.close()
    return True


def validar_capacidad(id_sala, participantes):
    conn=get_connection()
    cursor=conn.cursor()

    query1 = ("SELECT capacidad FROM sala "
              "WHERE id_sala = %s")

    cursor.execute(query1,(id_sala,))
    fila=cursor.fetchone()

    cursor.close()
    conn.close()

    if fila is None:
        return False

    capacidad=fila[0]

    return len(participantes)<=capacidad

def validar_horario(id_sala,fecha,id_turnos):

    conn=get_connection()
    cursor=conn.cursor()

    query =(" SELECT 1 FROM reserva "
            "Where id_sala=%s"
            "and fecha= %s"
            "and id_turno= %s"
            "and estado='activa'"
           " Limit 1;"
)
    cursor.execute(query, (id_sala, fecha, id_turno))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado is None

def validar_tipo_sala(participantes, id_sala ):

    conn=get_connection()
    cursor=conn.cursor()

    query=("SELECT tipo_sala FROM sala "
           "where id_sala=%s")
    cursor.execute(query,(id_sala,))
    tipo_sala=cursor.fetchone()[0]
    if tipo_sala=="libre":
        return True

    query=("Select rol from participante_programa_academico "
           "where ci_participante=%s")

    for ci in participantes:
        cursor.execute(query,(ci,))
        roles=cursor.fetchall()

        if not roles:
            return false

        if tipo_sala=="posgrado":
            if not any(r[0] in ("posgrado", "docentes") for r in roles):
                return False
        if tipo_sala== "docente":
            if not any(r[0] in ( "docente") for r in roles):
                return False

        cursor.close()
        conn.close()
        return True

def validar_limite_diario(ci,fecha, id_turnos):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(" Select rol from participante_programa_academico "
                       "where ci_participante=%s",(ci,))
    roles=[r[0] for r in cursor.fetchall()]

    if "docente" in roles or "posgrado" in roles:
        cursor.close()
        conn.close()
        return True

    cursor.execute("SELECT count(*) from reserva r "
                       "Join reserva_participante rp on r.id_reserva =rp.id_reserva "
                       "where rp.ci_participante=%s"
                       "and r.fecha=%s "
                       "and r.estado='activa'",(ci,fecha) )

    reservas_previas=cursor.fetchone()[0]

    turnos_nuevos=len(id_turnos)
    if reservas_previas+turnos_nuevos>2:
        cursor.close()
        conn.close()
        return False
    cursor.close()
    conn.close()
    return True

def validar_limite_semanal(ci, fecha):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT rol FROM participante_programa_academico "
            "WHERE ci_participante = %s",
            (ci,)
        )
        roles = [r[0] for r in cursor.fetchall()]

        if "docente" in roles or "posgrado" in roles:
            cursor.close()
            conn.close()
            return True

        cursor.execute(
            "SELECT COUNT(*) "
            "FROM reserva r "
            "JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva "
            "WHERE rp.ci_participante = %s "
            "AND YEARWEEK(r.fecha, 1) = YEARWEEK(%s, 1) "
            "AND r.estado = 'activa'",
            (ci, fecha)
        )

        reservas_semana = cursor.fetchone()[0]

        if reservas_semana >= 3:
            cursor.close()
            conn.close()
            return False

        cursor.close()
        conn.close()
        return True

def hay_solapamiento(id_sala, fecha, id_turnos):
    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join(["%s"] * len(id_turnos))

    query = (
        "SELECT COUNT(*) "
        "FROM reserva "
        "WHERE id_sala = %s "
        "AND fecha = %s "
        "AND estado = 'activa' "
        f"AND id_turno IN ({placeholders})"
    )

    params = [id_sala, fecha] + id_turnos
    cursor.execute(query, params)

    res = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    if res > 0:
        return True

    return False













