import React, { useState } from 'react'

export default function AudioRecorder({ onTranscribe }){
  const [file, setFile] = useState(null)
  const [filename, setFilename] = useState('')

  const handleChange = (e) => {
    const f = e.target.files?.[0]
    if (f) { setFile(f); setFilename(f.name) }
  }

  return (
    <div>
      <h3 className="font-medium">Audio Input</h3>
      <div className="mt-2">
        <label className="block border-2 border-dashed border-slate-300 rounded-2xl p-6 text-center bg-white shadow-md hover:border-blue-400 transition">
          <input type="file" accept="audio/*" onChange={handleChange} className="hidden" />
          <div className="text-sm text-slate-500">Drag & drop or click to select audio</div>
          <div className="text-sm text-slate-700 mt-2">{filename || 'No file selected'}</div>
        </label>
        <div className="mt-3 flex gap-2">
          <button
            className="btn-gradient px-4 py-2 rounded-2xl"
            onClick={() => file && onTranscribe && onTranscribe(file)}
            disabled={!file}
          >
            Transcribe
          </button>
        </div>
      </div>
    </div>
  )
}
