import { useState, useEffect } from "react";
import { reporteTurnosMax } from "../API/api";

export function ReporteTurnosMax() {
  const [data, setData] = useState([]);

  useEffect(() => {
    reporteTurnosMax().then((res) => {
      console.log("Respuesta TurnosMax:", res.body); // 👀 para verificar
      setData(res.body.data || []); // 👈 aquí está el array
    });
  }, []);

  return (
    <div>
      <h2>Turnos más demandados</h2>
      <ul>
        {Array.isArray(data) &&
          data.map((item, index) => (
            <li key={index}>
              Turno: {item[0]} — Reservado {item[1]} veces
            </li>
          ))}
      </ul>
    </div>
  );
}
