import React from 'react'
import { useEffect, useState } from "react";
import { obtenerReservasPorUsuario, authMe } from "../API/api";
import './PerfilPage.css'
import { Link } from 'react-router-dom'


const PerfilPage = () => {
    const [user, setUser] = useState(null);
    const [reservas, setReservas] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const authResponse = await authMe();
                
                if (authResponse.ok && authResponse.body) {
                    const userData = {
                        ci: authResponse.body.ci,
                        rol: authResponse.body.rol,
                        nombre: authResponse.body.nombre,
                        apellido: authResponse.body.apellido,
                        correo: authResponse.body.correo
                    };
                    setUser(userData);
                    
                    if (userData.rol !== 'admin') {
                        const reservasResponse = await obtenerReservasPorUsuario(userData.ci);
                        if (reservasResponse.ok && reservasResponse.body) {
                            setReservas(reservasResponse.body.reservas || []);
                        }
                    }
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
            } finally {
                setLoading(false);
            }
        };
        
        fetchUserData();
    }, [])
    
    if (loading) {
        return <div>Cargando...</div>;
    }
    
    if (!user) {
        return <div>Error: No se pudo obtener la informacion del usuario</div>;
    }
    
    return (
        user.nombre === 'Pato' ? (
          <div className='hola'>
            <h2>Bienvenido, {user.nombre} {user.apellido}</h2>
            <h3>Opciones para salas</h3>
            <Link to='/crearSala'>
            <button className='botoncito'>Crear sala</button>
            </Link>
            <Link to='/modificarSala'>
            <button className='botoncito'>Modificar sala</button>
            </Link>
            <Link to='/eliminarSala'>
            <button className='botoncito'>Eliminar sala</button>
            </Link>
            <h3>Opciones para usuarios</h3>
            <Link to='/crearParticipante'>
            <button className='botoncito'>Crear usuario</button>
            </Link>
            <Link to='/modificarParticipante'>
            <button className='botoncito'>Modificar usuario</button>
            </Link>
            <Link to='/eliminarParticipante'>
            <button className='botoncito'>Eliminar usuario</button>
            </Link>
            <h3>Opciones para sanciones</h3>
            <Link to='/crearSanciones'>
            <button className='botoncito'>Crear Sanciones</button>
            </Link>
            <Link to='/eliminarSancion'>
            <button className='botoncito'>Eliminar Sancion</button>
            </Link>
            <Link to='/modificarSancion'>
            <button className='botoncito'>Modificar Sancion</button>
            </Link>
          </div>
        ) : (
          <div className='divTabla'>
            <h2>Hola, {user.nombre}</h2>
            <h1>Mis reservas</h1>
            {reservas.length === 0 ? (
              <p>No tienes reservas</p>
            ) : (
              <table className='tabla'>
              <thead>
                <tr>
                  <th>Sala</th>
                  <th>Edificio</th>
                  <th>Fecha</th>
                  <th>Estado</th>
                  <th>Fecha Solicitud</th>
                </tr>
              </thead>
              <tbody>
                {reservas.map((reserva, index) => (
                  <tr key={index}>
                    <td>{reserva.nombre_sala}</td>
                    <td>{reserva.nombre_edificio}</td>
                    <td>{reserva.fecha}</td>
                    <td>{reserva.estado}</td>
                    <td>{reserva.fecha_solicitud_reserva}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            )}
          </div>
        )
    )
}

export default PerfilPage
