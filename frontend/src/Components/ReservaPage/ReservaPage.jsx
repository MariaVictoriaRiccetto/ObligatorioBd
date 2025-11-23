import React, { useState, useEffect, useContext } from "react";
import { crearReserva} from "../API/api";
import { AuthContext } from "../context/AuthContext";

export default function CrearReserva() {

  const { user, fetchUser } = useContext(AuthContext);
  const [form, setForm] = useState({
    ci: "",
    id_sala: "",
    fecha: "",
    id_turnos: "",
    participantes: "",
  });
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (user) {
      setForm((prev) => ({ ...prev, ci: user.ci }));
    } else {
      fetchUser(); // por si el usuario aún no está cargado
    }
  }, [user, fetchUser]);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      ci: Number(form.ci),
      id_sala: Number(form.id_sala),
      fecha: form.fecha,
      id_turnos: form.id_turnos.split(",").map((t) => Number(t.trim())),
      participantes: form.participantes.split(",").map((c) => Number(c.trim())),
    };
    const res = await crearReserva(payload);
    if (!res.ok) {
      setMsg(res.body.error || "Error al crear reserva");
      return;
    }
    setMsg("Reserva creada: " + JSON.stringify(res.body));
    setForm({
      ci: user?.ci || "",
      id_sala: "",
      fecha: "",
      id_turnos: "",
      participantes: "",
    });
  };

  if (!user) return <div>Cargando...</div>;

  return (
    <div>
      <h2>Crear reserva</h2>
      <form onSubmit={handleSubmit}>
        <input name="ci" value={form.ci} readOnly />
        <input name="id_sala" placeholder='Id sala' value={form.id_sala} onChange={handleChange} required />
        <input name="fecha" placeholder='fecha YYYY-MM-DD' value={form.fecha} onChange={handleChange} required />
        <input name="id_turnos" placeholder="Turnos e.g. 1,2" value={form.id_turnos} onChange={handleChange} required />
        <input name="participantes" placeholder="CI participantes (separar con comas)"value={form.participantes} onChange={handleChange} required />
        <button type="submit">Reservar</button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
