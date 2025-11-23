import React, { useState } from "react";
import { eliminarParticipante } from "../API/api";
import "./estilos/EliminarParticipante.css";

export function EliminarParticipante() {
  const [ci, setCi] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await eliminarParticipante(ci);

    if (!res.ok) {
      setMsg(res.body?.error || "Error al eliminar participante");
      return;
    }

    setMsg(res.body.status || "Participante eliminado correctamente");

    // Reset del formulario
    setCi("");
  };

  return (
    <div className="divEP">
      <h2>Eliminar Participante</h2>
      <form onSubmit={handleSubmit} className="formEP">
        <input
          className="inputEP"
          placeholder="CI del participante"
          value={ci}
          onChange={(e) => setCi(e.target.value)}
          required
        />
        <button className="buttonEP" type="submit">
          Eliminar
        </button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
