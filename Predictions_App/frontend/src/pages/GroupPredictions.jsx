// src/pages/GroupPredictions.jsx
import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../utils/store'
import { API_URL } from '../api'

const TOURNAMENT_ID = 1
const GROUPS = ['A','B','C','D','E','F','G','H','I','J','K','L']
const TOURNAMENT_START = new Date('2026-06-11T19:00:00Z')

function GroupPredictions() {
  const { authToken } = useContext(AuthContext)
  const [fixtures, setFixtures] = useState([])
  const [groupPreds, setGroupPreds] = useState({})
  const [saved, setSaved] = useState({})
  const [loading, setLoading] = useState(true)
  const isLocked = new Date() > TOURNAMENT_START

  useEffect(() => {
    fetch(`${API_URL}/tournaments/${TOURNAMENT_ID}/fixtures`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then(res => res.json())
      .then(data => {
        setFixtures(data.results || [])
        setLoading(false)
      })

    fetch(`${API_URL}/predictions/me/${TOURNAMENT_ID}`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then(res => res.json())
      .then(data => {
        const predMap = {}
        const savedMap = {}
        ;(data.group_predictions || []).forEach(p => {
          // API returns group_id, first_place, second_place, third_place
          predMap[p.group_id] = {
            first: p.first_place,
            second: p.second_place,
            third: p.third_place
          }
          savedMap[p.group_id] = true
        })
        setGroupPreds(predMap)
        setSaved(savedMap)
      })
  }, [])

  function getTeamsForGroup(group) {
    const groupFixtures = fixtures.filter(f => f.group === group && f.stage === 'Group')
    const teams = new Set()
    groupFixtures.forEach(f => {
      teams.add(f.team_1)
      teams.add(f.team_2)
    })
    return Array.from(teams)
  }

  function handleChange(group, place, value) {
    setGroupPreds(prev => ({
      ...prev,
      [group]: { ...prev[group], [place]: value }
    }))
    setSaved(prev => ({ ...prev, [group]: false }))
  }

  function handleSave(group) {
    const p = groupPreds[group] || {}
    fetch(`${API_URL}/predictions/group`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`
      },
      body: JSON.stringify({
        tournament_id: TOURNAMENT_ID,
        group,
        first: p.first,
        second: p.second,
        third: p.third
      })
    })
      .then(res => res.json())
      .then(() => setSaved(prev => ({ ...prev, [group]: true })))
  }

  if (loading) return <p className="loading">Loading groups...</p>

  return (
    <div className="page">
      <h1>🗂 Group Predictions</h1>
      <p className="subtitle">Predict the top 3 teams in each group. 4th place is derived automatically.</p>
      {isLocked && (
        <p style={{ color: '#888', fontSize: '0.85rem', marginBottom: '16px' }}>
          🔒 Group predictions are locked — tournament has started.
        </p>
      )}
      <div className="groups-grid">
        {GROUPS.map(group => {
          const teams = getTeamsForGroup(group)
          const p = groupPreds[group] || {}
          const isSaved = saved[group]

          return (
            <div key={group} className={`group-card ${isSaved ? 'saved' : ''} ${isLocked ? 'locked' : ''}`}>
              <h3>Group {group}</h3>
              {['first', 'second', 'third'].map((place, i) => (
                <div key={place} className="group-select-row">
                  <label>{i + 1}{i === 0 ? 'st' : i === 1 ? 'nd' : 'rd'}</label>
                  <select
                    value={p[place] || ''}
                    disabled={isLocked}
                    onChange={e => handleChange(group, place, e.target.value)}
                  >
                    <option value="">Select team</option>
                    {teams.map(team => (
                      <option key={team} value={team}>{team}</option>
                    ))}
                  </select>
                </div>
              ))}
              {!isLocked && (
                <button
                  onClick={() => handleSave(group)}
                  className={isSaved ? 'btn-saved' : 'btn-save'}
                >
                  {isSaved ? '✓ Saved' : 'Save'}
                </button>
              )}
              {isLocked && isSaved && (
                <p style={{ color: '#4caf50', fontSize: '0.78rem', marginTop: '8px' }}>✓ Saved</p>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default GroupPredictions