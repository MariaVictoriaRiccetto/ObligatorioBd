import React, { useState } from "react";
import { eliminarSala } from "../API/api";
import "./estilos/EliminarSala.css";

export function EliminarSala() {
  const [idSala, setIdSala] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await eliminarSala(idSala);

    if (!res.ok) {
      setMsg(res.body?.error || "Error al eliminar sala");
      return;
    }

    setMsg(res.body.status || "Sala eliminada correctamente");

    // Reset del formulario
    setIdSala("");
  };

  return (
    <div className="divES">
      <h2>Eliminar Sala</h2>
      <form onSubmit={handleSubmit} className="formES">
        <input
          placeholder="ID Sala"
          value={idSala}
          onChange={(e) => setIdSala(e.target.value)}
          required
        />
        <button type="submit">Eliminar</button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
