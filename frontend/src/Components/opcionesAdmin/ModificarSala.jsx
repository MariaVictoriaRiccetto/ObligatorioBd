import React, { useState } from "react";
import { modificarSala } from "../API/api";
import "./estilos/ModificarSala.css";

export function ModificarSala() {
  const [idSala, setIdSala] = useState("");
  const [form, setForm] = useState({
    nombre: "",
    id_edificio: "",
    capacidad: "",
    tipo: "",
  });
  const [msg, setMsg] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await modificarSala(idSala, form);

    if (!res.ok) {
      setMsg(res.body?.error || "Error al modificar sala");
      return;
    }

    setMsg(res.body.status || "Sala modificada correctamente");

    // Reset form
    setIdSala("");
    setForm({
      nombre: "",
      id_edificio: "",
      capacidad: "",
      tipo: "",
    });
  };

  return (
    <div className="divMS">
      <h2>Modificar Sala</h2>
      <form onSubmit={handleSubmit} className="formMS">
        <input
          placeholder="ID Sala"
          value={idSala}
          onChange={(e) => setIdSala(e.target.value)}
          required
        />

        <input
          name="nombre"
          placeholder="Nuevo nombre"
          value={form.nombre}
          onChange={handleChange}
        />
        <input
          name="id_edificio"
          placeholder="Nuevo ID edificio"
          value={form.id_edificio}
          onChange={handleChange}
        />
        <input
          name="capacidad"
          placeholder="Nueva capacidad"
          value={form.capacidad}
          onChange={handleChange}
        />
        <input
          name="tipo"
          placeholder="Nuevo tipo"
          value={form.tipo}
          onChange={handleChange}
        />

        <button className="bbottonn" type="submit">
          Modificar
        </button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
