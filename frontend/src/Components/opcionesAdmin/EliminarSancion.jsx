import { useState } from "react";
import { eliminarSancion } from "../API/api";

export function EliminarSancion() {
  const [ci, setCi] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("Eliminando sanción...");
    try {
      const res = await eliminarSancion(ci);
      if (!res.ok) {
        setMsg(res.body?.error || "Error al eliminar sanción");
        return;
      }
      setMsg(res.body.Estado || "Operación realizada");
      setCi(""); // limpiar campo
    } catch (err) {
      setMsg("Error de conexión con el servidor");
    }
  };

  return (
    <div>
      <h2>Eliminar sanción</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="CI del participante"
          value={ci}
          onChange={(e) => setCi(e.target.value)}
          required
        />
        <button type="submit">Eliminar</button>
      </form>
      {msg && <p>{msg}</p>}
    </div>
  );
}
