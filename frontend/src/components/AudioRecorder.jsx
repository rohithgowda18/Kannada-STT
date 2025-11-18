import React from 'react'

export default function AudioRecorder(){
  return (
    <div>
      <h3 className="font-medium">Audio Input</h3>
      <div className="mt-2">
        <input type="file" accept="audio/*" />
      </div>
    </div>
  )
}
