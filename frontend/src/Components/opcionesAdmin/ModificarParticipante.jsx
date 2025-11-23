import React, { useState } from "react";
import { modificarParticipante } from "../API/api";
import "./estilos/ModificarParticipante.css";

export function ModificarParticipante() {
  const [ci, setCi] = useState("");
  const [form, setForm] = useState({
    nombre: "",
    apellido: "",
    email: "",
  });
  const [msg, setMsg] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await modificarParticipante(ci, form);

    if (!res.ok) {
      setMsg(res.body?.error || "Error al modificar participante");
      return;
    }

    setMsg(res.body.status || "Participante modificado correctamente");

    // Reset del formulario
    setCi("");
    setForm({
      nombre: "",
      apellido: "",
      email: "",
    });
  };

  return (
    <div>
      <h2>Modificar Participante</h2>
      <form onSubmit={handleSubmit} className="modificarForm">
        <p className="textoP">C.I.</p>
        <input
          placeholder="CI del participante"
          value={ci}
          onChange={(e) => setCi(e.target.value)}
          required
        />
        <p className="textoP">Nombre:</p>
        <input
          name="nombre"
          placeholder="Nuevo nombre"
          value={form.nombre}
          onChange={handleChange}
        />
        <p className="textoP">Apellido:</p>
        <input
          name="apellido"
          placeholder="Nuevo apellido"
          value={form.apellido}
          onChange={handleChange}
        />
        <p className="textoP">Email:</p>
        <input
          name="email"
          placeholder="Nuevo email"
          value={form.email}
          onChange={handleChange}
        />
        <button className="botonciti" type="submit">
          Modificar
        </button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
