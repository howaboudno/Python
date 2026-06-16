// src/pages/Scoreboard.jsx
import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../utils/store'
import { API_URL } from '../api'

const TOURNAMENT_ID = 1

function Scoreboard() {
  const { authToken } = useContext(AuthContext)
  const [scoreboard, setScoreboard] = useState([])
  const [expanded, setExpanded] = useState(null)
  const [loading, setLoading] = useState(true)

  function fetchScoreboard() {
    fetch(`${API_URL}/tournaments/${TOURNAMENT_ID}/scoreboard`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then(res => res.json())
      .then(data => {
        setScoreboard(data.results || [])
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchScoreboard()
    const interval = setInterval(fetchScoreboard, 30000)
    return () => clearInterval(interval)
  }, [])

  function toggleRow(userId) {
    setExpanded(expanded === userId ? null : userId)
  }

  if (loading) return <p className="loading">Loading scoreboard...</p>

  return (
    <div className="page">
      <h1>🏆 Scoreboard</h1>
      <table className="scoreboard-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Player</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {scoreboard.map((entry, index) => (
            <>
              <tr
                key={entry.user_id}
                className={`scoreboard-row ${index === 0 ? 'gold' : index === 1 ? 'silver' : index === 2 ? 'bronze' : ''}`}
                onClick={() => toggleRow(entry.user_id)}
                style={{ cursor: 'pointer' }}
              >
                <td>{index + 1}</td>
                <td>{entry.username}</td>
                <td><strong>{entry.total}</strong></td>
              </tr>
              {expanded === entry.user_id && (
                <tr key={`${entry.user_id}-detail`} className="breakdown-row">
                  <td colSpan={3}>
                    <div className="breakdown">
                      <span>Match points: <strong>{entry.fixture_points}</strong></span>
                      <span>Group ranking points: <strong>{entry.ranking_points}</strong></span>
                      <span>Bonus points: <strong>{entry.bonus_points}</strong></span>
                    </div>
                  </td>
                </tr>
              )}
            </>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Scoreboard
