// src/pages/BonusPredictions.jsx
import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../utils/store'
import { API_URL } from '../api'

const TOURNAMENT_ID = 1

function BonusPredictions() {
  const { authToken } = useContext(AuthContext)
  const [champion, setChampion] = useState('')
  const [topScorer, setTopScorer] = useState('')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    fetch(`${API_URL}/predictions/me/${TOURNAMENT_ID}`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then(res => res.json())
      .then(data => {
        if (data.bonus_prediction) {
          setChampion(data.bonus_prediction.predicted_winner || '')
          setTopScorer(data.bonus_prediction.predicted_top_scorer || '')
          setSaved(true)
        }
      })
  }, [])

  function handleSave() {
    fetch(`${API_URL}/predictions/bonus`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`
      },
      body: JSON.stringify({
        tournament_id: TOURNAMENT_ID,
        predicted_winner: champion,
        predicted_top_scorer: topScorer
      })
    })
      .then(res => res.json())
      .then(() => setSaved(true))
  }

  return (
    <div className="page">
      <h1>⭐ Champion & Top Scorer</h1>
      <p className="subtitle">These predictions are worth 50 points each.</p>
      <div className="bonus-card">
        <div className="bonus-row">
          <label>Tournament Champion</label>
          <input
            type="text"
            value={champion}
            onChange={e => { setChampion(e.target.value); setSaved(false) }}
            placeholder="e.g. Netherlands"
          />
        </div>
        <div className="bonus-row">
          <label>Top Scorer</label>
          <input
            type="text"
            value={topScorer}
            onChange={e => { setTopScorer(e.target.value); setSaved(false) }}
            placeholder="e.g. Kylian Mbappé"
          />
        </div>
        <button
          onClick={handleSave}
          className={saved ? 'btn-saved' : 'btn-save'}
        >
          {saved ? '✓ Saved' : 'Save predictions'}
        </button>
      </div>
    </div>
  )
}

export default BonusPredictions
