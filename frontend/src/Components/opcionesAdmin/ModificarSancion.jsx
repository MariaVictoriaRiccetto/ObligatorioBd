import { useState } from "react";
import { modificarSancion } from "../API/api";

export function ModificarSancion() {
  const [ci, setCi] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("Modificando sanción...");
    try {
      const res = await modificarSancion(ci, {
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
      });

      if (!res.ok) {
        setMsg(res.body?.error || "Error al modificar sanción");
        return;
      }

      setMsg(res.body.estado || "Operación realizada");
      setCi("");
      setFechaInicio("");
      setFechaFin("");
    } catch (err) {
      setMsg("Error de conexión con el servidor");
    }
  };

  return (
    <div>
      <h2>Modificar sanción</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="CI del participante"
          value={ci}
          onChange={(e) => setCi(e.target.value)}
          required
        />
        <input
          type="date"
          placeholder="Nueva fecha inicio"
          value={fechaInicio}
          onChange={(e) => setFechaInicio(e.target.value)}
          required
        />
        <input
          type="date"
          placeholder="Nueva fecha fin"
          value={fechaFin}
          onChange={(e) => setFechaFin(e.target.value)}
          required
        />
        <button type="submit">Modificar</button>
      </form>
      {msg && <p>{msg}</p>}
    </div>
  );
}
