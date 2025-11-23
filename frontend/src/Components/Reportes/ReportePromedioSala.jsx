import { useState, useEffect } from "react";
import { reportePromedioSala } from "../API/api";

export function ReportePromedioSala() {
  const [data, setData] = useState([]);

  useEffect(() => {
    reportePromedioSala().then((res) => {
      console.log("Respuesta PromedioSala:", res.body);
      setData(res.body["El promedio de la sala es  "] || []);
    });
  }, []);

  return (
    <div>
      <h2>Promedio de participantes por sala</h2>
      {Array.isArray(data) && data.length > 0 ? (
        <ul>
          {data.map((item, index) => (
            <li key={index}>
              Sala {item[0]} — Promedio: {item[1]}
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay datos disponibles</p>
      )}
    </div>
  );
}
