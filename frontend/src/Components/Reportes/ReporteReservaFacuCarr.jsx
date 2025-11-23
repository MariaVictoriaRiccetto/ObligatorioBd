import { useState, useEffect } from "react";
import { reporteReservasFacultadCarrera } from "../API/api";

export function ReporteReservasFacultadCarrera() {
  const [data, setData] = useState([]);

  useEffect(() => {
    reporteReservasFacultadCarrera().then((res) => {
      console.log("Respuesta reservas facultad/carrera:", res.body);
      setData(res.body["El promedio de la sala es  "] || []);
    });
  }, []);

  return (
    <div>
      <h2>Reservas por Facultad y Carrera</h2>
      {Array.isArray(data) && data.length > 0 ? (
        <ul>
          {data.map((item, index) => (
            <li key={index}>
              Facultad: {item[0]} — Carrera: {item[1]} → {item[2]} reservas
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay datos disponibles</p>
      )}
    </div>
  );
}
