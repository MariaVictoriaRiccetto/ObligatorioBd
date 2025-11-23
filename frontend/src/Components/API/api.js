const API_URL = "http://127.0.0.1:5000";

// Helper: token storage
export const saveToken = (token) => localStorage.setItem("token", token);
export const getToken = () => localStorage.getItem("token");
export const removeToken = () => localStorage.removeItem("token");

// Helper: build headers with Authorization if token exists
const buildHeaders = (extra = {}) => {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...extra,
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  return headers;
};

// small helper to parse json and attach http status if needed
async function parseRes(res) {
  let json = {};
  try {
    json = await res.json();
  } catch (e) {
    console.warn('No JSON in response:', e);
  }
  return { status: res.status, ok: res.ok, body: json };
}

/* -------------------------
   AUTH
   ------------------------- */

// POST /auth/login
export const loginApi = async (email, password) => {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: buildHeaders({ "Content-Type": "application/json" }),
    body: JSON.stringify({ correo: email, password }),
  });
  return parseRes(res);
};

// GET /auth/me  (requires token)
export const authMe = async () => {
  const res = await fetch(`${API_URL}/auth/me`, {
    method: "GET",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

/* -------------------------
   PARTICIPANTES
   ------------------------- */

// GET /participantes  (admin_required)
export const getParticipantes = async () => {
  const res = await fetch(`${API_URL}/participantes`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// POST /participantes/crear  (open)
export const crearParticipante = async (data) => {
  try {
    console.log('Enviando a:', `${API_URL}/participantes/crear`);
    console.log('Datos:', data);
    const res = await fetch(`${API_URL}/participantes/crear`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    console.log('Response status:', res.status);
    const parsed = await parseRes(res);
    console.log('Response body:', parsed.body);
    return parsed;
  } catch (err) {
    console.error('Network error in crearParticipante:', err);
    throw new Error('No se pudo conectar al servidor. ¿Está running en http://127.0.0.1:5000?');
  }
};

// DELETE /participantes/delete/:ci (admin)
export const eliminarParticipante = async (ci) => {
  const res = await fetch(`${API_URL}/participantes/delete/${ci}`, {
    method: "DELETE",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// PUT /participantes/modificar/:ci (admin)
export const modificarParticipante = async (ci, data) => {
  const res = await fetch(`${API_URL}/participantes/modificar/${ci}`, {
    method: "PUT",
    headers: buildHeaders(),
    body: JSON.stringify(data),
  });
  return parseRes(res);
};

/* -------------------------
   SALAS
   ------------------------- */

// POST /sala/crear (admin)
export const crearSala = async (data) => {
  const res = await fetch(`${API_URL}/sala/crear`, {
    method: "POST",
    headers: buildHeaders(),
    body: JSON.stringify(data),
  });
  return parseRes(res);
};

// GET /salas/obtenerAdmin (admin)
export const obtenerSalasAdmin = async () => {
  const res = await fetch(`${API_URL}/salas/obtenerAdmin`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// GET /salas/obtenerTodos (logged user)
export const obtenerSalasUsuario = async () => {
  const res = await fetch(`${API_URL}/salas/obtenerTodos`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// DELETE /sala/delete/:id_sala (admin)
export const eliminarSala = async (id_sala) => {
  const res = await fetch(`${API_URL}/sala/delete/${id_sala}`, {
    method: "DELETE",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// PUT /sala/modificar/:id_sala (admin)
export const modificarSala = async (id_sala, data) => {
  const res = await fetch(`${API_URL}/sala/modificar/${id_sala}`, {
    method: "PUT",
    headers: buildHeaders(),
    body: JSON.stringify(data),
  });
  return parseRes(res);
};

/* -------------------------
   RESERVAS
   ------------------------- */

// GET /reservas/obtener (admin)
export const obtenerReservas = async () => {
  const res = await fetch(`${API_URL}/reservas/obtener`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// GET /reservas/obtener/usuario/:ci_participante (logged user)
export const obtenerReservasPorUsuario = async (ci) => {
  const res = await fetch(`${API_URL}/reservas/obtener/usuario/${ci}`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// GET /reservas/obtener/activas (admin)
export const obtenerReservasActivas = async () => {
  const res = await fetch(`${API_URL}/reservas/obtener/activas`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// GET /reservas/obtener/inactivas (admin)
export const obtenerReservasInactivas = async () => {
  const res = await fetch(`${API_URL}/reservas/obtener/inactivas`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// POST /reservas/crear (logged user)
export const crearReserva = async (data) => {
  const res = await fetch(`${API_URL}/reservas/crear`, {
    method: "POST",
    headers: buildHeaders(),
    body: JSON.stringify(data),
  });
  return parseRes(res);
};

// PUT /reservas/eliminar/:id_reserva  (changed to PUT, logged user)
export const eliminarReserva = async (id_reserva) => {
  const res = await fetch(`${API_URL}/reservas/eliminar/${id_reserva}`, {
    method: "PUT",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// PUT /reservas/modificar/:id_reserva (logged user)
export const modificarReserva = async (id_reserva, data) => {
  const res = await fetch(`${API_URL}/reservas/modificar/${id_reserva}`, {
    method: "PUT",
    headers: buildHeaders(),
    body: JSON.stringify(data),
  });
  return parseRes(res);
};

// PUT /reservas/asistencia/:id_reserva (admin)
export const marcarAsistencia = async (id_reserva) => {
  const res = await fetch(`${API_URL}/reservas/asistencia/${id_reserva}`, {
    method: "PUT",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// PUT /reservas/finalizar_automatico (admin)
export const finalizarReservasAutomatico = async () => {
  const res = await fetch(`${API_URL}/reservas/finalizar_automatico`, {
    method: "PUT",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

/* -------------------------
   SANCIONES
   ------------------------- */

// POST /sanciones/generar (admin)
export const generarSanciones = async () => {
  const res = await fetch(`${API_URL}/sanciones/generar`, {
    method: "POST",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// POST /sanciones/crear/:ci (admin)
export const sancionarManual = async (ci) => {
  const res = await fetch(`${API_URL}/sanciones/crear/${ci}`, {
    method: "POST",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// DELETE /sanciones/eliminar/:ci (admin)
export const eliminarSancion = async (ci) => {
  const res = await fetch(`${API_URL}/sanciones/eliminar/${ci}`, {
    method: "DELETE",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// GET /sanciones/:ci (admin)
export const listarSanciones = async (ci) => {
  const res = await fetch(`${API_URL}/sanciones/${ci}`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// DELETE /sanciones/limpiar (admin)
export const limpiarSancionesVencidas = async () => {
  const res = await fetch(`${API_URL}/sanciones/limpiar`, {
    method: "DELETE",
    headers: buildHeaders(),
  });
  return parseRes(res);
};

// PUT /sanciones/modificar/:ci (admin)
export const modificarSancion = async (ci, data) => {
  const res = await fetch(`${API_URL}/sanciones/modificar/${ci}`, {
    method: "PUT",
    headers: buildHeaders(),
    body: JSON.stringify(data),
  });
  return parseRes(res);
};

// GET /sanciones/obtener (admin)
export const obtenerTodasSanciones = async () => {
  const res = await fetch(`${API_URL}/sanciones/obtener`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

/* -------------------------
   REPORTES (la mayoría ADMIN)
   ------------------------- */

export const reporteSalasMax = async () => {
  const res = await fetch(`${API_URL}/reportes/salasMaxReserva`, {
    headers: buildHeaders(),
  });
  const parsed = await parseRes(res);

  console.log("Respuesta reporteSalasMax:", parsed);

  return parsed;
};


export const reporteTurnosMax = async () => {
  const res = await fetch(`${API_URL}/reportes/turnosMax`, {
    headers: buildHeaders(),
  });
  console.log("Respuesta reporteTurnosMax:", res.body);
  return parseRes(res);
};

export const reportePromedioSala = async () => {
  const res = await fetch(`${API_URL}/reportes/sala/promedio`, {
    headers: buildHeaders(),
  });
  console.log("Respuesta reportePromedioSala:", res.body);

  return parseRes(res);
};

export const reporteReservasFacultadCarrera = async () => {
  const res = await fetch(`${API_URL}/reportes/reservas/facultad-carrera`, {
    headers: buildHeaders(),
  });
  console.log("Respuesta reporteReservasFacultadCarrera:", res.body);
  return parseRes(res);
};

export const reporteAsistenciasProfAlumnos = async () => {
  const res = await fetch(`${API_URL}/reportes/reservas/asistencias-prof-alumnos`, {
    headers: buildHeaders(),
  });
  console.log("reporteAsistenciasProfAlumnos:", res.body);
  return parseRes(res);
};

export const reporteSancionesProfAlum = async () => {
  const res = await fetch(`${API_URL}/reportes/sanciones/prof-alum`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

export const reporteReservasEfectivas = async () => {
  const res = await fetch(`${API_URL}/reportes/reservas/efectivasNo`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

export const reporteMasInasistencias = async () => {
  const res = await fetch(`${API_URL}/reportes/participante/masInasistencia`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

export const reporteTopReservasActivas = async () => {
  const res = await fetch(`${API_URL}/reportes/participante/reservaActiva`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};

export const reporteCantidadSalasPorEdificio = async () => {
  const res = await fetch(`${API_URL}/reportes/sala/cantidadXEdificio`, {
    headers: buildHeaders(),
  });
  return parseRes(res);
};
