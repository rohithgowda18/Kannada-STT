import React from 'react'

export default function TranscriptHighlighter({ transcript = '', suggestionsMap = {}, onWordClick }){
  const words = transcript ? transcript.split(/\s+/) : []

  return (
    <div className="mt-4">
      <h4 className="font-medium">Transcript Preview</h4>
      <div className="mt-2 flex flex-wrap gap-2">
        {words.map((w,i)=> {
          const hasSuggestion = suggestionsMap[i] && suggestionsMap[i].length > 0
          const cls = `inline-block px-2 py-1 rounded-lg cursor-pointer ${hasSuggestion ? 'bg-yellow-100 shadow' : 'bg-white'}`
          return (
            <button key={i} className={cls} onClick={() => onWordClick && onWordClick(w, i)}>
              {w}
            </button>
          )
        })}
      </div>
    </div>
  )
}
