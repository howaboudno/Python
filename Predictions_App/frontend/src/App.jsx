// src/App.jsx
import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Scoreboard from './pages/Scoreboard'
import Fixtures from './pages/Fixtures'
import GroupPredictions from './pages/GroupPredictions'
import BonusPredictions from './pages/BonusPredictions'
import ProtectedRoute from './utils/ProtectedRoute'
import Navbar from './navbar'
import Profile from './pages/Profile'

function App() {
  return (
    <>
      <Navbar />
      <div className="main-content">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/profile" element={<Profile />} />
            <Route path="/" element={<Scoreboard />} />
            <Route path="/predictions" element={<Fixtures />} />
            <Route path="/groups" element={<GroupPredictions />} />
            <Route path="/bonus" element={<BonusPredictions />} />
          </Route>
        </Routes>
      </div>
    </>
  )
}

export default App
