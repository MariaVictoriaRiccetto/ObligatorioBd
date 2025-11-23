import { useState, useEffect } from "react";
import { reporteAsistenciasProfAlumnos } from "../API/api";

export function ReporteAsistenciasRol() {
  const [data, setData] = useState([]);

  useEffect(() => {
    reporteAsistenciasProfAlumnos().then((res) => {
      console.log("Respuesta asistencias:", res.body);
      setData(res.body.data || []);
    });
  }, []);

  return (
    <div>
      <h2>Reservas y asistencias por rol</h2>
      {Array.isArray(data) && data.length > 0 ? (
        <ul>
          {data.map((item, index) => (
            <li key={index}>
              Rol: {item.rol} → Reservas: {item.total_reservas}, Asistencias: {item.total_asistencias}, Inasistencias: {item.total_inasistencias}
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay datos disponibles</p>
      )}
    </div>
  );
}
