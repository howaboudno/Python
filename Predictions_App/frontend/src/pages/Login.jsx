// src/pages/Login.jsx
import { useState, useContext } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { AuthContext } from '../utils/store'
import { API_URL } from '../api'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { setAuthToken } = useContext(AuthContext)
  const navigate = useNavigate()

  function handleLogin() {
    setError('')
    fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
      .then(res => res.json())
      .then(data => {
        if (data.access_token) {
          setAuthToken(data.access_token)
          navigate('/')
        } else {
          setError(data.message || 'Login failed')
        }
      })
  }

  return (
    <div className="auth-page">
      <h1>Log in</h1>
      {error && <p className="error">{error}</p>}
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Log in</button>
      <p className="link">No account? <Link to="/register">Register</Link></p>
    </div>
  )
}

export default Login
