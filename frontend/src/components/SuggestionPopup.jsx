import React from 'react'

export default function SuggestionPopup(){
  return (
    <div className="p-3 bg-white rounded-xl shadow-lg w-72">
      <div className="text-sm font-semibold">Heard: ವನೆ</div>
      <div className="mt-2">Suggestions: <span className="font-medium">ಮನೆ</span></div>
      <div className="mt-3 flex justify-end">
        <button className="btn-gradient px-3 py-1 rounded-xl">Apply</button>
      </div>
    </div>
  )
}
