import React from 'react'

export default function FinalTextCard({text}){
  return (
    <div className="p-4 rounded-xl shadow-lg bg-white">
      <div className="font-medium">Final Text</div>
      <pre className="mt-2 whitespace-pre-wrap">{text}</pre>
      <div className="mt-3 flex gap-2">
        <button className="btn-gradient px-3 py-1 rounded-xl">Download</button>
        <button className="px-3 py-1 rounded-xl border">Copy</button>
      </div>
    </div>
  )
}
