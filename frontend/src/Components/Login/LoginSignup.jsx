import React, { useState} from 'react'
import './Login.css'
import { loginApi, saveToken, crearParticipante } from "../API/api";
import { useNavigate } from 'react-router-dom'


//NO ANDA EL LOGIN
const LoginSignup = () => {
    const [action, setAction] = useState("Login")
    const [mensaje, setMensaje] = useState("")

    const navigate = useNavigate()
    
    const [formData, setFormData] = useState({ 
      ci: "",
      nombre: "",
      apellido: "",
      email: "",
      contraseña: "" 
    });
    const [loginEmail, setLoginEmail] = useState("");
    const [loginPass, setLoginPass] = useState("");

    const handleChange = (e) => {
      setFormData({ 
        ...formData,
        [e.target.name]: e.target.value 
      })
    }
    /*---SIGN UP--- */
    const handleSignUp = async (e) => {
    e.preventDefault();
    const { ci, nombre, apellido, email, contraseña } = formData;
      // NO enviar si algún campo está vacío
    if (!nombre || !ci || !contraseña || !apellido || !email) {
      setMensaje("Todos los campos son obligatorios")
      return
    }
    
    try {
      const payload = { ...formData, email: formData.email.trim().toLowerCase() };
      const res = await crearParticipante(payload);
      if(!res.ok){
        setMensaje(res.body?.error || "Error en el registro");
        return;
      }
      setMensaje("Registro exitoso.");
      setFormData({ ci: "", nombre: "", apellido: "", email: "", contraseña: "" });
      navigate('/home');
    } catch (err) {
      setMensaje(err.message || "Error de conexión con el servidor");
      console.error('Error en handleSignUp:', err);
    }
  }
/*---LOGIN---*/
  const handleLogin = async (e) => {
    e.preventDefault();

    if (!loginEmail || !loginPass) {
      setMensaje("Email y contraseña son obligatorios")
      return
    }
    const correo = loginEmail.trim().toLowerCase();
    const res = await loginApi(correo, loginPass);
    
    if(!res.ok){
      setMensaje(res.body?.error || "Error en el login");
      return;
    }

    saveToken(res.body.token);
    setMensaje("Login exitoso. Rol:" + res.body.rol);
    navigate('/home');
    }
  
  return (
    <div className='container'>
        <div className='header'>
            <div className='text'>{action}</div>
        </div>

      <div className='inputs'>
         
        {action==="Login"?<div></div>:       
         <>
         <div className='input'>
            <input 
            type="text"
            name="nombre"
            placeholder='Nombre'
            value={formData.nombre}
            onChange={handleChange}
            />
        </div>
        <div className='input'>
            <input
            type="text"
            name="apellido" 
            placeholder='Apellido'
            value={formData.apellido}
            onChange={handleChange}
            />
        </div>
        <div  className='input' >
            <input
            type="text"
            name='ci'
            placeholder='C.I'
            value={formData.ci}
            onChange={handleChange} />
        </div>
        </>
        }

        <div className='input'>
            <input
            type="email"
            name="email"
            placeholder='Email' 
            value={action==="Login"?loginEmail:formData.email}
            onChange={(e) => {
              if (action === "Login") {
                setLoginEmail(e.target.value);
              } else {
                setFormData({ ...formData, email: e.target.value });
              }
            }}
            />
        </div>
        <div className='input'>
            <input
            type="password"
            name="contraseña"
            placeholder='Contraseña'
            value={action==="Login"?loginPass:formData.contraseña}
            onChange={(e) => {
              if (action === "Login") {
                setLoginPass(e.target.value);
              } else {
                setFormData({ ...formData, contraseña: e.target.value });
              }
            }}
            />
        </div>
      </div>

      {action == 'Login' ?
      <div className='submit-container' >
         <button className="submit" onClick={handleLogin}>Login </button>
      </div> :
        <div className='submit-container' >
         <button className="submit" onClick={handleSignUp}>Sign Up</button>
      </div>
      }
      <div className='submit-container'>
        <button className={action==="Login"?"submit gray":"submit"} onClick={() => {setAction("Sign Up")}}>Sign Up</button>
        <button className={action==="Sign Up"?"submit gray":"submit"} onClick={() => {setAction("Login")}}>Login</button>
      </div>
      <p>{mensaje}</p>
    </div>
  )

}
export default LoginSignup
