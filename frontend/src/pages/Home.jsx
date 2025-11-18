import React from 'react'
import AudioRecorder from '../components/AudioRecorder'
import TranscriptHighlighter from '../components/TranscriptHighlighter'
import CorrectionPanel from '../components/CorrectionPanel'

export default function Home(){
  return (
    <div className="grid grid-cols-12 gap-6">
      <section className="col-span-4 p-4 border rounded-xl shadow-lg">
        <AudioRecorder />
        <TranscriptHighlighter />
      </section>
      <section className="col-span-8 p-4 border rounded-xl shadow-lg">
        <CorrectionPanel />
      </section>
      <section className="col-span-12 mt-6 p-4 border rounded-xl shadow-lg">
        <h2 className="font-semibold">Final Clean Text</h2>
        <div id="final-text" className="mt-2">(will appear here)</div>
      </section>
    </div>
  )
}
