// src/pages/Fixtures.jsx
import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../utils/store'
import { API_URL } from '../api'

const TOURNAMENT_ID = 1

<<<<<<< HEAD
=======
const STAGE_ORDER = ['Group', 'R32', 'R16', 'QF', 'SF', 'F']
>>>>>>> 679a57fbc604d293f458ef683d70d0f5d4c8738f
const STAGE_LABELS = { R32: 'Round of 32', R16: 'Round of 16', QF: 'Quarter-finals', SF: 'Semi-finals', F: 'Final' }

function NumInput({ value, onChange, disabled, placeholder }) {
  return (
    <input
      type="text"
      inputMode="numeric"
      pattern="[0-9]*"
      value={value}
      disabled={disabled}
      placeholder={placeholder ?? '0'}
      onChange={e => onChange(e.target.value.replace(/[^0-9]/g, ''))}
    />
  )
}

function Fixtures() {
  const { authToken } = useContext(AuthContext)
  const [fixtures, setFixtures] = useState([])
  const [predictions, setPredictions] = useState({})
  const [saved, setSaved] = useState({})
  const [loading, setLoading] = useState(true)
  const [showGroups, setShowGroups] = useState(true)
<<<<<<< HEAD
  const [saving, setSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState(null) // 'success' | 'error' | null
=======
>>>>>>> 679a57fbc604d293f458ef683d70d0f5d4c8738f

  useEffect(() => {
    fetch(`${API_URL}/tournaments/${TOURNAMENT_ID}/fixtures`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then(res => res.json())
      .then(data => {
        const all = data.results || []
        setFixtures(all)
<<<<<<< HEAD
        const hasStartedKO = all.some(f => f.stage !== 'Group' && new Date(f.fixture_time + 'Z') < new Date())
        if (hasStartedKO) setShowGroups(false)
=======

        // Auto-hide groups if any KO fixture has started
        const hasStartedKO = all.some(f => f.stage !== 'Group' && new Date(f.fixture_time + 'Z') < new Date())
        if (hasStartedKO) setShowGroups(false)

>>>>>>> 679a57fbc604d293f458ef683d70d0f5d4c8738f
        setLoading(false)
      })

    fetch(`${API_URL}/predictions/me/${TOURNAMENT_ID}`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then(res => res.json())
      .then(data => {
        const predMap = {}
        const savedMap = {}
        ;(data.fixture_predictions || []).forEach(p => {
          predMap[p.fixture_id] = {
            score1: String(p.predicted_score_1 ?? ''),
            score2: String(p.predicted_score_2 ?? ''),
            pen1: p.predicted_pen_score_1 != null ? String(p.predicted_pen_score_1) : '',
            pen2: p.predicted_pen_score_2 != null ? String(p.predicted_pen_score_2) : ''
          }
          savedMap[p.fixture_id] = true
        })
        setPredictions(predMap)
        setSaved(savedMap)
      })
  }, [])

  function isLocked(fixtureTime) {
    const kickoff = new Date(fixtureTime + 'Z')
    return new Date() > new Date(kickoff.getTime() + 60 * 1000)
  }

  function formatKickoff(fixtureTime) {
    return new Date(fixtureTime + 'Z').toLocaleString('nl-NL', {
      timeZone: 'Europe/Amsterdam',
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  function handleChange(fixtureId, field, value) {
    setPredictions(prev => ({
      ...prev,
      [fixtureId]: { ...prev[fixtureId], [field]: value }
    }))
    setSaved(prev => ({ ...prev, [fixtureId]: false }))
  }

  function handleSave(fixtureId) {
    const p = predictions[fixtureId] || {}
    fetch(`${API_URL}/predictions/fixture`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
      body: JSON.stringify({
        fixture_id: fixtureId,
        predicted_score_1: parseInt(p.score1),
        predicted_score_2: parseInt(p.score2),
        predicted_pen_score_1: p.pen1 !== '' ? parseInt(p.pen1) : null,
        predicted_pen_score_2: p.pen2 !== '' ? parseInt(p.pen2) : null
      })
    })
      .then(res => res.json())
      .then(() => setSaved(prev => ({ ...prev, [fixtureId]: true })))
      .catch(err => console.error('Error saving prediction:', err))
  }

<<<<<<< HEAD
  async function handleSaveAll() {
    // Collect all unlocked fixtures that have both scores filled in
    const toSave = fixtures.filter(f => {
      if (isLocked(f.fixture_time)) return false
      const p = predictions[f.id] || {}
      return p.score1 !== '' && p.score1 !== undefined && p.score2 !== '' && p.score2 !== undefined
    })

    if (toSave.length === 0) return

    setSaving(true)
    setSaveStatus(null)

    try {
      await Promise.all(toSave.map(f => {
        const p = predictions[f.id] || {}
        return fetch(`${API_URL}/predictions/fixture`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
          body: JSON.stringify({
            fixture_id: f.id,
            predicted_score_1: parseInt(p.score1),
            predicted_score_2: parseInt(p.score2),
            predicted_pen_score_1: p.pen1 !== '' ? parseInt(p.pen1) : null,
            predicted_pen_score_2: p.pen2 !== '' ? parseInt(p.pen2) : null
          })
        })
      }))

      const newSaved = {}
      toSave.forEach(f => { newSaved[f.id] = true })
      setSaved(prev => ({ ...prev, ...newSaved }))
      setSaveStatus('success')
    } catch (err) {
      console.error('Error saving all predictions:', err)
      setSaveStatus('error')
    } finally {
      setSaving(false)
      setTimeout(() => setSaveStatus(null), 3000)
    }
  }

  const hasKOFixtures = fixtures.some(f => f.stage !== 'Group')

  const unsavedCount = fixtures.filter(f => {
    if (isLocked(f.fixture_time)) return false
    const p = predictions[f.id] || {}
    return !saved[f.id] && p.score1 !== '' && p.score1 !== undefined && p.score2 !== '' && p.score2 !== undefined
  }).length

=======
  const hasKOFixtures = fixtures.some(f => f.stage !== 'Group')

  // Sort chronologically, filter groups if hidden
>>>>>>> 679a57fbc604d293f458ef683d70d0f5d4c8738f
  const sorted = [...fixtures]
    .filter(f => showGroups || f.stage !== 'Group')
    .sort((a, b) => new Date(a.fixture_time) - new Date(b.fixture_time))

<<<<<<< HEAD
=======
  // Split into sections with dividers: Group stage as one block, then each KO stage
>>>>>>> 679a57fbc604d293f458ef683d70d0f5d4c8738f
  const sections = []
  let currentStage = null
  sorted.forEach(f => {
    const sectionKey = f.stage === 'Group' ? 'Group' : f.stage
    if (sectionKey !== currentStage) {
      currentStage = sectionKey
      sections.push({ key: sectionKey, fixtures: [] })
    }
    sections[sections.length - 1].fixtures.push(f)
  })

  if (loading) return <p className="loading">Loading fixtures...</p>

  return (
    <div className="page">
      <h1>📋 Match Predictions</h1>

<<<<<<< HEAD
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '10px' }}>
        {hasKOFixtures ? (
=======
      {hasKOFixtures && (
        <div style={{ marginBottom: '16px' }}>
>>>>>>> 679a57fbc604d293f458ef683d70d0f5d4c8738f
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.85rem', color: '#888' }}>
            <input
              type="checkbox"
              checked={showGroups}
              onChange={e => setShowGroups(e.target.checked)}
              style={{ width: 'auto', margin: 0 }}
            />
            Show group stage matches
          </label>
<<<<<<< HEAD
        ) : <div />}

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {saveStatus === 'success' && (
            <span style={{ fontSize: '0.82rem', color: 'var(--green)' }}>✓ All saved</span>
          )}
          {saveStatus === 'error' && (
            <span style={{ fontSize: '0.82rem', color: '#f44336' }}>Error saving</span>
          )}
          <button
            onClick={handleSaveAll}
            disabled={saving || unsavedCount === 0}
            className="btn-save"
            style={{ padding: '6px 16px', fontSize: '0.85rem' }}
          >
            {saving ? 'Saving...' : unsavedCount > 0 ? `Save all (${unsavedCount})` : '✓ All saved'}
          </button>
        </div>
      </div>

      {sections.map((section, idx) => (
        <div key={section.key} className="fixture-section">
          <div style={{
            display: 'flex', alignItems: 'center', gap: '10px',
            margin: idx === 0 ? '0 0 12px' : '16px 0 12px',
            color: section.key === 'Group' ? 'var(--accent-light)' : '#ffb74d'
          }}>
            <div style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
            <span style={{ fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              {section.key === 'Group' ? 'Group Stage' : STAGE_LABELS[section.key] || section.key}
            </span>
            <div style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
          </div>
=======
        </div>
      )}

      {sections.map((section, idx) => (
        <div key={section.key} className="fixture-section">
          {/* Divider between sections */}
          {idx > 0 && (
            <div style={{
              display: 'flex', alignItems: 'center', gap: '10px',
              margin: '16px 0 12px', color: section.key === 'Group' ? 'var(--accent-light)' : '#ffb74d'
            }}>
              <div style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
              <span style={{ fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {section.key === 'Group' ? 'Group Stage' : STAGE_LABELS[section.key] || section.key}
              </span>
              <div style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
            </div>
          )}
          {idx === 0 && (
            <div style={{
              display: 'flex', alignItems: 'center', gap: '10px',
              margin: '0 0 12px', color: section.key === 'Group' ? 'var(--accent-light)' : '#ffb74d'
            }}>
              <div style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
              <span style={{ fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {section.key === 'Group' ? 'Group Stage' : STAGE_LABELS[section.key] || section.key}
              </span>
              <div style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
            </div>
          )}
>>>>>>> 679a57fbc604d293f458ef683d70d0f5d4c8738f

          {section.fixtures.map(fixture => {
            const fid = fixture.id
            const locked = isLocked(fixture.fixture_time)
            const isKO = fixture.stage !== 'Group'
            const p = predictions[fid] || {}
            const isDraw = isKO && p.score1 !== '' && p.score2 !== '' && p.score1 === p.score2
            const isSaved = saved[fid]

            return (
              <div key={fid} className={`fixture-card ${isSaved ? 'saved' : ''} ${locked ? 'locked' : ''}`}>
                <div className="fixture-teams">
                  <span className="team">{fixture.team_1}</span>
                  <div className="score-inputs">
                    <NumInput
                      value={p.score1 ?? ''}
                      disabled={locked}
                      onChange={val => handleChange(fid, 'score1', val)}
                    />
                    <span>-</span>
                    <NumInput
                      value={p.score2 ?? ''}
                      disabled={locked}
                      onChange={val => handleChange(fid, 'score2', val)}
                    />
                  </div>
                  <span className="team">{fixture.team_2}</span>
                </div>

                {isDraw && !locked && (
                  <div className="penalty-inputs">
                    <span>Penalties:</span>
                    <NumInput value={p.pen1 ?? ''} placeholder="PK" onChange={val => handleChange(fid, 'pen1', val)} />
                    <span>-</span>
                    <NumInput value={p.pen2 ?? ''} placeholder="PK" onChange={val => handleChange(fid, 'pen2', val)} />
                  </div>
                )}

                <div className="fixture-footer">
                  <span className="kickoff">
                    {isKO && <span style={{ color: '#ffb74d', marginRight: '6px', fontSize: '0.75rem', fontWeight: 600 }}>{fixture.stage}</span>}
                    {!isKO && <span style={{ color: 'var(--accent-light)', marginRight: '6px', fontSize: '0.75rem' }}>Gr. {fixture.group}</span>}
                    {formatKickoff(fixture.fixture_time)}
                  </span>
                  {locked
                    ? <span className="locked-label">🔒 Locked</span>
                    : <button onClick={() => handleSave(fid)} className={isSaved ? 'btn-saved' : 'btn-save'}>
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