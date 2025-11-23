import { crearSala } from "../API/api";
import React, { useState } from "react";
import './estilos/CrearSala.css';

export default function CrearSala() {
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
    const res = await crearSala(form);
    if (!res.ok) {
      setMsg(res.body.error || "Error al crear sala");
      return;
    }
    setMsg(res.body.status); // 👈 muestra el mensaje del backend
    setForm({ nombre: "", id_edificio: "", capacidad: "", tipo: "" }); // reset form
  };

  return (
    <div className="input">
      <form onSubmit={handleSubmit} className="formSala">
        <h2>Crear Sala</h2>
        <input name="nombre" placeholder="Nombre" value={form.nombre} onChange={handleChange} />
        <input name="id_edificio" placeholder="ID Edificio" value={form.id_edificio} onChange={handleChange} />
        <input name="capacidad" placeholder="Capacidad" value={form.capacidad} onChange={handleChange} />
        <input name="tipo" placeholder="Tipo" value={form.tipo} onChange={handleChange} />
        <button className="crear" type="submit">Crear Sala</button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
