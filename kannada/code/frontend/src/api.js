import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function transcribeFile(file) {
  const fd = new FormData()
  fd.append('file', file)
  const res = await axios.post(`${API_BASE}/transcribe`, fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

export async function detectText(transcript) {
  const res = await axios.post(`${API_BASE}/detect`, { transcript })
  return res.data
}

export async function applyCorrections(transcript, corrections) {
  const res = await axios.post(`${API_BASE}/apply`, { transcript, corrections })
  return res.data
}
