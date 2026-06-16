// src/pages/Profile.jsx
import { useState, useContext } from 'react'
import { AuthContext } from '../utils/store'
import { API_URL } from '../api'

function Profile() {
  const { authToken } = useContext(AuthContext)
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [message, setMessage] = useState(null)
  const [isError, setIsError] = useState(false)

  function handleSubmit() {
    setMessage(null)

    if (newPassword !== confirmPassword) {
      setMessage('New passwords do not match')
      setIsError(true)
      return
    }

    if (newPassword.length < 6) {
      setMessage('New password must be at least 6 characters')
      setIsError(true)
      return
    }

    fetch(`${API_URL}/auth/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`
      },
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.message === 'Password changed successfully') {
          setMessage('Password changed successfully')
          setIsError(false)
          setCurrentPassword('')
          setNewPassword('')
          setConfirmPassword('')
        } else {
          setMessage(data.detail || 'Something went wrong')
          setIsError(true)
        }
      })
  }

  return (
    <div className="page">
      <h1>⚙ Profile</h1>
      <p className="subtitle">Change your password below.</p>
      <div className="bonus-card">
        {message && (
          <p style={{
            color: isError ? '#f44336' : '#4caf50',
            fontSize: '0.85rem',
            marginBottom: '12px'
          }}>
            {message}
          </p>
        )}
        <div className="bonus-row">
          <label>Current password</label>
          <input
            type="password"
            value={currentPassword}
            onChange={e => setCurrentPassword(e.target.value)}
            placeholder="Enter current password"
          />
        </div>
        <div className="bonus-row">
          <label>New password</label>
          <input
            type="password"
            value={newPassword}
            onChange={e => setNewPassword(e.target.value)}
            placeholder="Enter new password"
          />
        </div>
        <div className="bonus-row">
          <label>Confirm new password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={e => setConfirmPassword(e.target.value)}
            placeholder="Repeat new password"
          />
        </div>
        <button onClick={handleSubmit} className="btn-save">
          Change password
        </button>
      </div>
    </div>
  )
}

export default Profile