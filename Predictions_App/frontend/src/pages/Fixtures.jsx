// src/pages/Fixtures.jsx
import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../utils/store'
import { API_URL } from '../api'

const TOURNAMENT_ID = 1

function Fixtures() {
  const { authToken } = useContext(AuthContext)
  const [fixtures, setFixtures] = useState([])
  const [predictions, setPredictions] = useState({})
  const [saved, setSaved] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch fixtures
    fetch(`${API_URL}/tournaments/${TOURNAMENT_ID}/fixtures`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then(res => res.json())
      .then(data => {
        setFixtures(data.results || [])
        setLoading(false)
      })

    // Fetch existing predictions and pre-fill
    fetch(`${API_URL}/predictions/me/${TOURNAMENT_ID}`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then(res => res.json())
      .then(data => {
        const predMap = {}
        const savedMap = {}
        ;(data.fixture_predictions || []).forEach(p => {
          predMap[p.fixture_id] = {
            score1: p.predicted_score_1,
            score2: p.predicted_score_2,
            pen1: p.predicted_pen_score_1 ?? '',
            pen2: p.predicted_pen_score_2 ?? ''
          }
          savedMap[p.fixture_id] = true
        })
        setPredictions(predMap)
        setSaved(savedMap)
      })
  }, [])

  function isLocked(fixtureTime) {
    return new Date(fixtureTime) < new Date()
  }

  function handleChange(fixtureId, field, value) {
    setPredictions(prev => ({
      ...prev,
      [fixtureId]: { ...prev[fixtureId], [field]: value }
    }))
  }

  function handleSave(fixtureId) {
    const p = predictions[fixtureId] || {}
    const body = {
      fixture_id: fixtureId,
      predicted_score_1: parseInt(p.score1),
      predicted_score_2: parseInt(p.score2),
      predicted_pen_score_1: p.pen1 !== '' ? parseInt(p.pen1) : null,
      predicted_pen_score_2: p.pen2 !== '' ? parseInt(p.pen2) : null
    }

    fetch(`${API_URL}/predictions/fixture`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`
      },
      body: JSON.stringify(body)
    })
      .then(res => res.json())
      .then(() => setSaved(prev => ({ ...prev, [fixtureId]: true })))
  }

  // Group fixtures by stage then group
  const grouped = fixtures.reduce((acc, f) => {
    const key = f.stage === 'Group' ? `Group ${f.group}` : f.stage
    if (!acc[key]) acc[key] = []
    acc[key].push(f)
    return acc
  }, {})

  if (loading) return <p className="loading">Loading fixtures...</p>

  return (
    <div className="page">
      <h1>📋 Match Predictions</h1>
      {Object.entries(grouped).map(([section, sectionFixtures]) => (
        <div key={section} className="fixture-section">
          <h2>{section}</h2>
          {sectionFixtures.map(fixture => {
            const locked = isLocked(fixture.fixture_time)
            const p = predictions[fixture.fixture_id] || {}
            const isDraw = p.score1 !== undefined && p.score2 !== undefined &&
              String(p.score1) === String(p.score2) && p.score1 !== ''
            const isSaved = saved[fixture.fixture_id]

            return (
              <div key={fixture.id} className={`fixture-card ${isSaved ? 'saved' : ''} ${locked ? 'locked' : ''}`}>
                <div className="fixture-teams">
                  <span className="team">{fixture.team_1}</span>
                  <div className="score-inputs">
                    <input
                      type="number"
                      min="0"
                      value={p.score1 ?? ''}
                      disabled={locked}
                      onChange={e => handleChange(fixture.id, 'score1', e.target.value)}
                    />
                    <span>-</span>
                    <input
                      type="number"
                      min="0"
                      value={p.score2 ?? ''}
                      disabled={locked}
                      onChange={e => handleChange(fixture.id, 'score2', e.target.value)}
                    />
                  </div>
                  <span className="team">{fixture.team_2}</span>
                </div>

                {isDraw && !locked && (
                  <div className="penalty-inputs">
                    <span>Penalties:</span>
                    <input
                      type="number"
                      min="0"
                      placeholder="PK"
                      value={p.pen1 ?? ''}
                      onChange={e => handleChange(fixture.id, 'pen1', e.target.value)}
                    />
                    <span>-</span>
                    <input
                      type="number"
                      min="0"
                      placeholder="PK"
                      value={p.pen2 ?? ''}
                      onChange={e => handleChange(fixture.id, 'pen2', e.target.value)}
                    />
                  </div>
                )}

                <div className="fixture-footer">
                  <span className="kickoff">{new Date(fixture.fixture_time).toLocaleString()}</span>
                  {locked
                    ? <span className="locked-label">🔒 Locked</span>
                    : <button onClick={() => handleSave(fixture.id)} className={isSaved ? 'btn-saved' : 'btn-save'}>
                        {isSaved ? '✓ Saved' : 'Save'}
                      </button>
                  }
                </div>
              </div>
            )
          })}
        </div>
      ))}
    </div>
  )
}

export default Fixtures
