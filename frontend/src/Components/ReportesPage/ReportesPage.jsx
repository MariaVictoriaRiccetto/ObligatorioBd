import React, { useState } from "react";
import {
  reporteSalasMax,
  reporteTurnosMax,
  reportePromedioSala,
  reporteReservasFacultadCarrera,
  reporteAsistenciasProfAlumnos,
  reporteSancionesProfAlum,
  reporteReservasEfectivas,
  reporteMasInasistencias,
  reporteTopReservasActivas,
  reporteCantidadSalasPorEdificio,
} from "../API/api";
import "./ReportesPage.css";
import ReporteSalasMax from "../Reportes/ReportesSalasMax";
import { Link } from "react-router-dom";
export default function Reportes() {
  const [data, setData] = useState(null);
  const [msg, setMsg] = useState("");

  return(
   <div className="reportes-container">
    <h1>Reportes</h1>
   <Link to='/salasMaxReserva'>
    <button>Salas con más reservas</button>
    </Link>
    <Link to='/turnoMaxReserva'>
    <button>Turnos más demandados</button>
    </Link>
    <Link to='/promedioSalas'>
    <button>Promedio de participantes por sala</button>
    </Link>
    <Link to='/promedioFacultadCarrera'>
    <button>Reservas por facultad y carrera</button>
    </Link>
    <Link to='/asistenciasProfAlumnos'>
    <button>Asistencias por rol (profesores/alumnos)</button>
    </Link>
    </div>
  )

}
/*const handleReporte = async (fn) => {
  setMsg("Cargando...");
  try {
    const res = await fn();
    if (!res.ok) {
      setMsg(res.body?.error || "Error al obtener reporte");
      setData(null);
      return;
    }

    const resultados = res.body.data || [];
    setData(resultados);
    setMsg("");
  } catch (err) {
    setMsg("Error de conexión con el servidor");
    setData(null);
  }
};


  return (
    <div className="reportes-container">
      <h2>Reportes Administrativos</h2>
      <div className="botones-reportes">
        <button onClick={() => handleReporte(reporteSalasMax)}>Salas con más reservas</button>
        <button onClick={() => handleReporte(reporteTurnosMax)}>Turnos más usados</button>
        <button onClick={() => handleReporte(reportePromedioSala)}>Promedio reservas por sala</button>
        <button onClick={() => handleReporte(reporteReservasFacultadCarrera)}>Reservas por facultad/carrera</button>
        <button onClick={() => handleReporte(reporteAsistenciasProfAlumnos)}>Asistencias prof/alumnos</button>
        <button onClick={() => handleReporte(reporteSancionesProfAlum)}>Sanciones prof/alum</button>
        <button onClick={() => handleReporte(reporteReservasEfectivas)}>Reservas efectivas vs no</button>
        <button onClick={() => handleReporte(reporteMasInasistencias)}>Participantes con más inasistencias</button>
        <button onClick={() => handleReporte(reporteTopReservasActivas)}>Top reservas activas</button>
        <button onClick={() => handleReporte(reporteCantidadSalasPorEdificio)}>Cantidad de salas por edificio</button>
      </div>

      {msg && <p>{msg}</p>}

      {data && (
        <div className="tabla-reportes">
          {Array.isArray(data) && data.length > 0 && (
          <table>
            <thead>
              <tr>
                {Object.keys(data[0]).map((col, i) => (
                  <th key={i}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, i) => (
                <tr key={i}>
                  {Object.values(row).map((val, j) => (
                    <td key={j}>{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          )}
        </div>
      )}
    </div>
  );
}*/
