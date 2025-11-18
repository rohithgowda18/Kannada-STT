import React from 'react'

export default function SuggestionPopup({ selected = { word: '', suggestions: [] }, onApply, onClose }){
  const { word, suggestions = [] } = selected || {}
  return (
    <div className="p-4 bg-white rounded-2xl shadow-xl w-80 z-50 border border-slate-200 animate-fade-in">
      <div className="flex justify-between items-center">
        <div className="text-sm font-semibold">System heard: <span className="font-medium">{word}</span></div>
        <button onClick={onClose} className="text-slate-400">✕</button>
      </div>
      <div className="mt-3 text-sm text-slate-600">Did you mean:</div>
      <div className="mt-2 grid gap-2">
        {suggestions.length ? suggestions.map((s,i)=> (
          <button key={i} onClick={() => onApply && onApply(s)} className="px-4 py-2 bg-blue-50 rounded-xl hover:bg-blue-100 text-left">{s}</button>
        )) : <div className="text-slate-500">No suggestions</div>}
      </div>
      <div className="mt-3 flex justify-end">
        <button onClick={() => onApply && onApply(suggestions[0])} className="btn-gradient px-3 py-1 rounded-2xl">Apply</button>
      </div>
    </div>
  )
}
