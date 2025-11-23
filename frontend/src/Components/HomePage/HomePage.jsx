import { Link } from 'react-router-dom'
import './HomePage.css'

function HomePage() {

  return (
    <>
    <div className='mainC'>
    <div className='homePage'>
      <h1>Bienvenido a la plataforma de reservas!</h1>
    </div>
    <div className='botones'>
      <Link to='/reserva'>
      <button className='botn'>Reservar sala</button>
      </Link>
      <Link to='/perfil'>
      <button className='botn'>Mi perfil</button>
      </Link>
      <Link to='/reportes'>
      <button className='botn'>Consultas</button>
      </Link>

    </div>
    </div>
    </>
  )
}

export default HomePage
