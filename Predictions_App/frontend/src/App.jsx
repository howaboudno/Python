import { Routes, Route } from 'react-router-dom'

function App() {
  return(
    <Routes>
      <Route path= "/" element={<div>Dashboard</div>} />
      <Route path= "/login" element={<div>Login</div>} />
      <Route path= "/register" element={<div>Register</div>} />
    </Routes>
  )
}

export default App