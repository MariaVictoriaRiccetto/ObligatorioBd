
import './App.css'
import HomePage from './Components/HomePage/HomePage'
import { useState } from 'react'
import ReservaPage from './Components/ReservaPage/ReservaPage'
import LoginSignup from './Components/Login/LoginSignup'

function App() {
  const [user, setUser] = useState([])
  return (
    <>
    { user.length === 0 ? <LoginSignup setUser={setUser}></LoginSignup>:
    <HomePage user={user} setUser={setUser}></HomePage>
    }
  
   </>
  )
}

export default App
