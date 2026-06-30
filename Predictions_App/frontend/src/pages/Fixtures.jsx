// src/pages/Fixtures.jsx
import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../utils/store'
import { API_URL } from '../api'

const TOURNAMENT_ID = 1
const STAGE_LABELS = { R32: 'Round of 32', R16: 'Round of 16', QF: 'Quarter-finals', SF: 'Semi-finals', F: 'Final' }
const STAGE_ORDER = ['R32', 'R16', 'QF', 'SF', 'F']
const parseScore = v => v === '' || v === undefined ? 0 : parseInt(v)

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
  const [activeTab, setActiveTab] = useState('group')
  const [saving, setSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState(null)
  const [openTooltipId, setOpenTooltipId] = useState(null)
  const [othersCache, setOthersCache] = useState({})
  const [othersLoading, setOthersLoading] = useState(null)

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
      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'
    })
  }

  function handleChange(fixtureId, field, value) {
    setPredictions(prev => ({ ...prev, [fixtureId]: { ...prev[fixtureId], [field]: value } }))
    setSaved(prev => ({ ...prev, [fixtureId]: false }))
  }

  function handleSave(fixtureId) {
    const p = predictions[fixtureId] || {}
    fetch(`${API_URL}/predictions/fixture`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
      body: JSON.stringify({
        fixture_id: fixtureId,
        predicted_score_1: parseScore(p.score1),
        predicted_score_2: parseScore(p.score2),
        predicted_pen_score_1: p.pen1 !== '' ? parseScore(p.pen1) : null,
        predicted_pen_score_2: p.pen2 !== '' ? parseScore(p.pen2) : null
      })
    })
      .then(res => res.json())
      .then(() => setSaved(prev => ({ ...prev, [fixtureId]: true })))
      .catch(err => console.error('Error saving prediction:', err))
  }

  async function handleSaveAll(fixtureList) {
    const toSave = fixtureList.filter(f => !isLocked(f.fixture_time))
    if (toSave.length === 0) return
    setSaving(true)
    setSaveStatus(null)
    try {
      await Promise.all(toSave.map(f => {
        const p = predictions[f.id] || {}
        const parseScore = v => v === '' || v === undefined ? 0 : parseInt(v)
        return fetch(`${API_URL}/predictions/fixture`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
          body: JSON.stringify({
            fixture_id: f.id,
            predicted_score_1: parseScore(p.score1),
            predicted_score_2: parseScore(p.score2),
            predicted_pen_score_1: p.pen1 !== '' ? parseScore(p.pen1) : null,
            predicted_pen_score_2: p.pen2 !== '' ? parseScore(p.pen2) : null
          })
        })
      }))
      const newSaved = {}
      toSave.forEach(f => { newSaved[f.id] = true })
      setSaved(prev => ({ ...prev, ...newSaved }))
      setSaveStatus('success')
    } catch (err) {
      setSaveStatus('error')
    } finally {
      setSaving(false)
      setTimeout(() => setSaveStatus(null), 3000)
    }
  }

  function toggleTooltip(fixtureId) {
    if (openTooltipId === fixtureId) { setOpenTooltipId(null); return }
    setOpenTooltipId(fixtureId)
    if (!othersCache[fixtureId]) {
      setOthersLoading(fixtureId)
      fetch(`${API_URL}/tournaments/${TOURNAMENT_ID}/fixtures/${fixtureId}/all-predictions`, {
        headers: { Authorization: `Bearer ${authToken}` }
      })
        .then(res => res.json())
        .then(data => setOthersCache(prev => ({ ...prev, [fixtureId]: data.results || [] })))
        .catch(err => console.error('Error loading other predictions:', err))
        .finally(() => setOthersLoading(null))
    }
  }

  // ── Shared fixture card renderer (used in both tabs) ──
  function renderFixtureCard(fixture, opts = {}) {
    const fid = fixture.id
    const locked = isLocked(fixture.fixture_time)
    const isKO = fixture.stage !== 'Group'
    const p = predictions[fid] || {}
    const s1 = p.score1 === '' || p.score1 === undefined ? '0' : p.score1
    const s2 = p.score2 === '' || p.score2 === undefined ? '0' : p.score2
    const isDraw = isKO && s1 === s2
    const isSaved = saved[fid]
    const tooltipOpen = openTooltipId === fid
    const othersData = othersCache[fid]
    const isOthersLoading = othersLoading === fid

    return (
      <div key={fid} className={`fixture-card ${isSaved ? 'saved' : ''} ${locked ? 'locked' : ''}`} style={{ position: 'relative', ...(opts.style || {}) }}>
        <div className="fixture-teams">
          <span className="team">{fixture.team_1 || 'TBD'}</span>
          <div className="score-inputs">
            <NumInput value={p.score1 ?? ''} disabled={locked} onChange={val => handleChange(fid, 'score1', val)} />
            <span>-</span>
            <NumInput value={p.score2 ?? ''} disabled={locked} onChange={val => handleChange(fid, 'score2', val)} />
          </div>
          <span className="team">{fixture.team_2 || 'TBD'}</span>
          <button
            onClick={() => toggleTooltip(fid)}
            title="See everyone's predictions"
            style={{ background: 'none', border: 'none', color: tooltipOpen ? 'var(--accent-light)' : 'var(--text-muted)', cursor: 'pointer', fontSize: '0.95rem', padding: '2px 4px', lineHeight: 1 }}
          >👥</button>
        </div>

        {tooltipOpen && (
          <div style={{ marginTop: '6px', padding: '8px 10px', background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: '6px', fontSize: '0.8rem' }}>
            {isOthersLoading && <span style={{ color: 'var(--text-muted)' }}>Loading...</span>}
            {!isOthersLoading && othersData && othersData.length === 0 && <span style={{ color: 'var(--text-muted)' }}>No predictions yet</span>}
            {!isOthersLoading && othersData && othersData.length > 0 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                {othersData.slice().sort((a, b) => a.username.localeCompare(b.username)).map(pred => (
                  <div key={pred.username} style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text)' }}>
                    <span style={{ color: 'var(--text-muted)' }}>{pred.username}</span>
                    <span>
                      {pred.predicted_score_1}-{pred.predicted_score_2}
                      {pred.predicted_pen_score_1 != null && (
                        <span style={{ color: 'var(--text-muted)' }}> (pen {pred.predicted_pen_score_1}-{pred.predicted_pen_score_2})</span>
                      )}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

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
  }

  // ── Group stage tab ──
  function renderGroupTab() {
    const groupFixtures = [...fixtures]
      .filter(f => f.stage === 'Group')
      .sort((a, b) => new Date(a.fixture_time) - new Date(b.fixture_time))

    const unsavedCount = groupFixtures.filter(f => !isLocked(f.fixture_time) && !saved[f.id]).length

    return (
      <>
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '12px', gap: '10px', alignItems: 'center' }}>
          {saveStatus === 'success' && <span style={{ fontSize: '0.82rem', color: 'var(--green)' }}>✓ All saved</span>}
          {saveStatus === 'error' && <span style={{ fontSize: '0.82rem', color: '#f44336' }}>Error saving</span>}
          <button
            onClick={() => handleSaveAll(groupFixtures)}
            disabled={saving || unsavedCount === 0}
            className="btn-save"
            style={{ padding: '6px 16px', fontSize: '0.85rem' }}
          >
            {saving ? 'Saving...' : unsavedCount > 0 ? `Save all (${unsavedCount})` : '✓ All saved'}
          </button>
        </div>
        <div className="fixture-section">
          {groupFixtures.map(f => renderFixtureCard(f))}
        </div>
      </>
    )
  }

  // ── Compact bracket card (used only in bracket tab) ──
  function renderBracketCard(fixture) {
    const fid = fixture.id
    const locked = isLocked(fixture.fixture_time)
    const p = predictions[fid] || {}
    const s1 = p.score1 === '' || p.score1 === undefined ? '0' : p.score1
    const s2 = p.score2 === '' || p.score2 === undefined ? '0' : p.score2
    const isDraw = s1 === s2
    const isSaved = saved[fid]

    return (
      <div style={{
        background: 'var(--surface)',
        border: `1px solid ${isSaved ? 'var(--green)' : 'var(--border)'}`,
        borderRadius: '6px',
        padding: '8px 10px',
        width: '180px',
        opacity: locked ? 0.6 : 1,
        fontSize: '0.8rem'
      }}>
        {/* Team row 1 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
          <span style={{ flex: 1, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {fixture.team_1 || 'TBD'}
          </span>
          <div style={{ width: '32px', flexShrink: 0 }}><NumInput value={p.score1 ?? ''} disabled={locked} onChange={val => handleChange(fid, 'score1', val)} /></div>
        </div>
        {/* Team row 2 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
          <span style={{ flex: 1, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {fixture.team_2 || 'TBD'}
          </span>
          <div style={{ width: '32px', flexShrink: 0 }}><NumInput value={p.score2 ?? ''} disabled={locked} onChange={val => handleChange(fid, 'score2', val)} /></div>
        </div>
        {/* Penalties row */}
        {isDraw && !locked && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
            <span>Pen:</span>
            <NumInput value={p.pen1 ?? ''} placeholder="PK" onChange={val => handleChange(fid, 'pen1', val)} />
            <span>-</span>
            <NumInput value={p.pen2 ?? ''} placeholder="PK" onChange={val => handleChange(fid, 'pen2', val)} />
          </div>
        )}
        {/* Footer */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>{formatKickoff(fixture.fixture_time)}</span>
          {locked
            ? <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>🔒</span>
            : <button onClick={() => handleSave(fid)} className={isSaved ? 'btn-saved' : 'btn-save'} style={{ padding: '2px 8px', fontSize: '0.72rem' }}>
                {isSaved ? '✓' : 'Save'}
              </button>
          }
        </div>
      </div>
    )
  }

  // ── KO bracket tab ──
  function renderBracketTab() {
    const koFixtures = fixtures.filter(f => f.stage !== 'Group')
    if (koFixtures.length === 0) {
      return <p style={{ color: 'var(--text-muted)', marginTop: '24px', textAlign: 'center' }}>No knockout fixtures available yet.</p>
    }

    const stagesPresent = STAGE_ORDER.filter(s => koFixtures.some(f => f.stage === s))
    const entryStageIdx = STAGE_ORDER.indexOf(stagesPresent[0])
    const stages = STAGE_ORDER.slice(entryStageIdx)

    const byStage = {}
    stages.forEach(s => {
      byStage[s] = koFixtures
        .filter(f => f.stage === s)
        .sort((a, b) => {
          const numA = parseInt(String(a.fixture_number).replace(/\D/g, '')) || 0
          const numB = parseInt(String(b.fixture_number).replace(/\D/g, '')) || 0
          return numA - numB
        })
    })

    const unsavedKO = koFixtures.filter(f => !isLocked(f.fixture_time) && !saved[f.id]).length
    const CARD_H = 90 // compact card height in px
    const COL_W = 180

    return (
      <>
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '12px', gap: '10px', alignItems: 'center' }}>
          {saveStatus === 'success' && <span style={{ fontSize: '0.82rem', color: 'var(--green)' }}>✓ All saved</span>}
          {saveStatus === 'error' && <span style={{ fontSize: '0.82rem', color: '#f44336' }}>Error saving</span>}
          <button
            onClick={() => handleSaveAll(koFixtures)}
            disabled={saving || unsavedKO === 0}
            className="btn-save"
            style={{ padding: '6px 16px', fontSize: '0.85rem' }}
          >
            {saving ? 'Saving...' : unsavedKO > 0 ? `Save all (${unsavedKO})` : '✓ All saved'}
          </button>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start', minWidth: 'max-content', paddingBottom: '16px' }}>
            {stages.map((stage, stageIdx) => {
              const stageFixtures = byStage[stage] || []
              const totalSlots = Math.pow(2, stages.length - 1 - stageIdx)
              const slots = Array.from({ length: totalSlots }, (_, i) => stageFixtures[i] || null)
              const pairSize = Math.pow(2, stageIdx)

              return (
                <div key={stage} style={{ display: 'flex', flexDirection: 'column', width: COL_W + 'px' }}>
                  <div style={{
                    fontSize: '0.68rem', fontWeight: 600, textTransform: 'uppercase',
                    letterSpacing: '0.06em', color: '#ffb74d',
                    textAlign: 'center', marginBottom: '8px', paddingBottom: '4px',
                    borderBottom: '1px solid var(--border)'
                  }}>
                    {STAGE_LABELS[stage] || stage}
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column' }}>
                    {slots.map((fixture, slotIdx) => {
                      const topMargin = slotIdx === 0
                        ? (pairSize - 1) * (CARD_H / 2)
                        : pairSize * CARD_H - CARD_H

                      return (
                        <div key={slotIdx} style={{ marginTop: topMargin + 'px' }}>
                          {fixture
                            ? renderBracketCard(fixture)
                            : (
                              <div style={{
                                background: 'var(--surface2)', border: '1px dashed var(--border)',
                                borderRadius: '6px', height: CARD_H + 'px', width: COL_W + 'px',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                color: 'var(--text-muted)', fontSize: '0.78rem'
                              }}>TBD</div>
                            )
                          }
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </>
    )
  }

  const hasKO = fixtures.some(f => f.stage !== 'Group')

  if (loading) return <p className="loading">Loading fixtures...</p>

  return (
    <div className="page">
      <h1>📋 Match Predictions</h1>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        <button
          onClick={() => setActiveTab('group')}
          style={{
            padding: '7px 18px', fontSize: '0.85rem', borderRadius: '6px', border: 'none', cursor: 'pointer',
            background: activeTab === 'group' ? 'var(--accent)' : 'var(--surface)',
            color: activeTab === 'group' ? '#fff' : 'var(--text-muted)',
            outline: activeTab === 'group' ? 'none' : '1px solid var(--border)'
          }}
        >
          Group Stage
        </button>
        {hasKO && (
          <button
            onClick={() => setActiveTab('bracket')}
            style={{
              padding: '7px 18px', fontSize: '0.85rem', borderRadius: '6px', border: 'none', cursor: 'pointer',
              background: activeTab === 'bracket' ? '#ffb74d' : 'var(--surface)',
              color: activeTab === 'bracket' ? '#000' : 'var(--text-muted)',
              outline: activeTab === 'bracket' ? 'none' : '1px solid var(--border)'
            }}
          >
            Knockout Bracket
          </button>
        )}
      </div>

      {activeTab === 'group' && renderGroupTab()}
      {activeTab === 'bracket' && renderBracketTab()}
    </div>
  )
}

export default Fixtures