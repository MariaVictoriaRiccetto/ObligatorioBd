import { crearParticipante } from "../API/api";
import React, { useState } from "react";
import "./estilos/CrearParticipante.css";

export function CrearParticipante() {
  const [form, setForm] = useState({
    ci: "",
    nombre: "",
    apellido: "",
    email: "",
    contraseña:""
  });

  const [msg, setMsg] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await crearParticipante(form);

    if (!res.ok) {
      setMsg(res.body?.error || "Error al crear participante");
      return;
    }

    setMsg(res.body.status || "Participante creado correctamente");

    // Reset del formulario
    setForm({
      ci: "",
      nombre: "",
      apellido: "",
      email: "",
    });
  };

  return (
    <div className="divCP">
      <form onSubmit={handleSubmit} className="formParti">
        <h2>Crear Participante</h2>
        <input
          name="ci"
          placeholder="CI"
          value={form.ci}
          onChange={handleChange}
          required
        />
        <input
          name="nombre"
          placeholder="Nombre"
          value={form.nombre}
          onChange={handleChange}
          required
        />
        <input
          name="apellido"
          placeholder="Apellido"
          value={form.apellido}
          onChange={handleChange}
          required
        />
        <input
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <input
        name="contraseña"
        type="password"
        placeholder="Contraseña"
        value={form.contraseña}
        onChange={handleChange}
        required
        />
        <button type="submit">Crear</button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
