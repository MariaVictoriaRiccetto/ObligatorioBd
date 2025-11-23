import { useState } from "react";
import { generarSanciones } from "../API/api";

export function CrearSanciones() {
  const [msg, setMsg] = useState("");
  const [count, setCount] = useState(null);

  const handleGenerar = async () => {
    setMsg("Generando sanciones...");
    try {
      const res = await generarSanciones();
      if (!res.ok) {
        setMsg(res.body?.error || "Error al generar sanciones");
        setCount(null);
        return;
      }
      setMsg("Sanciones generadas correctamente");
      setCount(res.body.sanciones_creadas);
    } catch (err) {
      setMsg("Error de conexión con el servidor");
      setCount(null);
    }
  };

  return (
    <div>
      <h2>Generar sanciones</h2>
      <button onClick={handleGenerar}>Generar sanciones</button>
      {msg && <p>{msg}</p>}
      {count !== null && (
        <p>Se generaron {count} sanciones nuevas.</p>
      )}
    </div>
  );
}
