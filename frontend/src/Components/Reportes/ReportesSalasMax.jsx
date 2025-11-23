import React, { useEffect, useState } from "react";
import { reporteSalasMax } from "../API/api";

export default function ReporteSalasMax() {
  const [data, setData] = useState([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    const load = async () => {
      const res = await reporteSalasMax();
      if (!res.ok) {
        setErr(res.body.error || "No autorizado/otro error");
        return;
      }
      // res.body should have { estado: ..., data: [...] }
      const arr = res.body.data || res.body.Datos || [];
      setData(arr);
    };
    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Salas más reservadas</h2>
      {err && <p style={{ color: "red" }}>{err}</p>}
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead><tr><th>Sala</th><th>Cant. reservas</th></tr></thead>
        <tbody>
          {data.map((r, i) => (
            <tr key={i}>
              <td>{r[0]}</td>
              <td>{r[1]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
