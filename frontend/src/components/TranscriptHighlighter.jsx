import React from 'react'

export default function TranscriptHighlighter(){
  // placeholder for word chips with click handlers
  const words = ['ಓದುದಿಲ್ಲ','ಉದಾಹರಣೆ','ಓದುವಿಕೆಯ']
  return (
    <div className="mt-4">
      <h4 className="font-medium">Transcript Preview</h4>
      <div className="mt-2 flex flex-wrap gap-2">
        {words.map((w,i)=> (
          <button key={i} className="chip" title="Click to suggest">{w}</button>
        ))}
      </div>
    </div>
  )
}
