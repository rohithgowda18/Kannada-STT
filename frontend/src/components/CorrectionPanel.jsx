import React from 'react'

export default function CorrectionPanel({ corrections = [] }){
  return (
    <div>
      <h3 className="font-medium">Correction Workspace</h3>
      <div className="mt-4">
        {corrections.length === 0 && <div className="text-slate-500">No corrections yet.</div>}
        {corrections.map((c, i) => (
          <div key={i} className="bg-white shadow-lg p-4 rounded-2xl mb-3 border-l-4 border-blue-500">
            <div className="text-sm">Position: {c.position}</div>
            <div className="font-medium">Replace with: {c.replacement}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
