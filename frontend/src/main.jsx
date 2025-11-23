import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from "./Components/context/AuthContext";
import HomePage from './Components/HomePage/HomePage.jsx'
import ReservaPage from './Components/ReservaPage/ReservaPage.jsx'
import {createBrowserRouter, RouterProvider} from 'react-router-dom'
import PerfilPage from './Components/PerfilPage/PerfilPage.jsx'
import { CrearParticipante } from './Components/opcionesAdmin/CrearParticipante.jsx'
import CrearSala from './Components/opcionesAdmin/CrearSala.jsx'
import { EliminarSala } from './Components/opcionesAdmin/EliminarSala.jsx'
import { EliminarParticipante } from './Components/opcionesAdmin/EliminarParticipante.jsx'
import { ModificarSala } from './Components/opcionesAdmin/ModificarSala.jsx'
import { ModificarParticipante } from './Components/opcionesAdmin/ModificarParticipante.jsx'
import ReporteSalasMax from './Components/Reportes/ReportesSalasMax.jsx'
import { ReporteTurnosMax } from './Components/Reportes/ReporteTurnoMax.jsx'
import { ReportePromedioSala } from './Components/Reportes/ReportePromedioSala.jsx'
import { ReporteReservasFacultadCarrera } from './Components/Reportes/ReporteReservaFacuCarr.jsx'
import Reportes from './Components/ReportesPage/ReportesPage.jsx';
import { ReporteAsistenciasRol } from './Components/Reportes/ReporteReservasAsistenciaRol.jsx';
import { CrearSanciones } from './Components/opcionesAdmin/CrearSanciones.jsx';
import { EliminarSancion } from './Components/opcionesAdmin/EliminarSancion.jsx';
import { ModificarSancion } from './Components/opcionesAdmin/ModificarSancion.jsx';

const router = createBrowserRouter([
  {path:'/', element:<App />},
  {path:'/home', element: <HomePage />},
  {path:'/reserva', element:<ReservaPage /> },
  {path:'/perfil', element: <PerfilPage/>},
  {path:'/crearParticipante', element: <CrearParticipante/>},
  {path:'/crearSala', element: <CrearSala/>},
  {path:'/eliminarSala', element: <EliminarSala/>},
  {path:'/eliminarParticipante', element: <EliminarParticipante/>},
  {path:'/modificarSala', element: <ModificarSala/>},
  {path:'/modificarParticipante', element: <ModificarParticipante/>},
  {path: '/salasMaxReserva', element: <ReporteSalasMax/>},
  {path: '/turnoMaxReserva', element: <ReporteTurnosMax/>},
  {path: '/promedioSalas', element: <ReportePromedioSala/>},
  {path: '/promedioFacultadCarrera', element: <ReporteReservasFacultadCarrera/>},
  {path:'/reportes', element:<Reportes />},
  {path:'/asistenciasProfAlumnos', element:<ReporteAsistenciasRol/>},
  {path:'/crearSanciones', element:<CrearSanciones/>},
  {path:'/eliminarSancion', element:<EliminarSancion/>},
  {path:'/modificarSancion', element:<ModificarSancion/>},
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
  <AuthProvider>
  <RouterProvider router={router} />
 </AuthProvider>
  </StrictMode>,
)
