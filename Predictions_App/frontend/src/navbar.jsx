// src/navbar.jsx
import { useContext } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { AuthContext } from './utils/store'

function Navbar() {
  const { authToken, setAuthToken } = useContext(AuthContext)
  const navigate = useNavigate()

  function handleLogout() {
    setAuthToken(null)
    navigate('/login')
  }

  if (!authToken) return null

  return (
    <nav className="navbar">
      <span className="navbar-brand">⚽ Predictor</span>
      <div className="navbar-links">
        <Link to="/">Scoreboard</Link>
        <Link to="/predictions">Predictions</Link>
        <Link to="/groups">Groups</Link>
        <Link to="/bonus">Champion & Top Scorer</Link>
        <button onClick={handleLogout} className="logout-btn">Log out</button>
      </div>
    </nav>
  )
}

export default Navbar
