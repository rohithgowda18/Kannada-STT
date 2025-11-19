import React, { useState } from 'react'
import AudioRecorder from '../components/AudioRecorder'
import TranscriptHighlighter from '../components/TranscriptHighlighter'
import CorrectionPanel from '../components/CorrectionPanel'
import FinalTextCard from '../components/FinalTextCard'
import SuggestionPopup from '../components/SuggestionPopup'
import { transcribeFile, detectText, applyCorrections } from '../api'

export default function Home(){
  const [loading, setLoading] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [segments, setSegments] = useState([])
  const [suggestionsMap, setSuggestionsMap] = useState({})
  const [selectedWord, setSelectedWord] = useState(null)
  const [corrections, setCorrections] = useState([])
  const [finalText, setFinalText] = useState('')

  const handleTranscribe = async (file) => {
    setLoading(true)
    try {
      const data = await transcribeFile(file)
      setTranscript(data.text || '')
      setSegments(data.segments || [])
      setFinalText(data.text || '')
      // call detect
      const det = await detectText(data.text || '')
      const map = {}
      ;(det.confusables || []).forEach(item => { map[item.position] = item.suggestions })
      ;(det.dialect_suggestions || []).forEach(item => { map[item.position] = (map[item.position] || []).concat(item.to) })
      setSuggestionsMap(map)
    } catch (e) {
      console.error(e)
      alert('Transcription failed')
    }
    setLoading(false)
  }

  const handleWordClick = (word, position) => {
    const suggestions = suggestionsMap[position] || []
    setSelectedWord({ word, position, suggestions })
  }

  const handleApply = async (replacement) => {
    const newCorrections = [...corrections, { position: selectedWord.position, replacement, original: selectedWord.word, alternatives: selectedWord.suggestions || [], detected_letter: selectedWord.word }]
    setCorrections(newCorrections)
    // call backend to apply
    try {
      const res = await applyCorrections(transcript, newCorrections)
      setFinalText(res.final || finalText)
      // optionally show link to saved CSV log
      if (res.log_path) console.log('Saved log:', res.log_path)
    } catch (e) {
      console.error(e)
    }
    setSelectedWord(null)
  }

  return (
    <div className="grid grid-cols-12 gap-6">
      <section className="col-span-4 p-4 border rounded-2xl shadow-lg bg-white">
        <AudioRecorder onTranscribe={handleTranscribe} />
        <TranscriptHighlighter transcript={transcript} suggestionsMap={suggestionsMap} onWordClick={handleWordClick} />
      </section>
      <section className="col-span-8 p-4 border rounded-2xl shadow-lg bg-white">
        <CorrectionPanel corrections={corrections} />
      </section>
      <section className="col-span-12 mt-6 p-4 border rounded-2xl shadow-lg bg-white">
        <h2 className="font-semibold">Final Clean Text</h2>
        <FinalTextCard text={finalText} before={transcript} />
      </section>
      {selectedWord && (
        <div className="fixed bottom-8 right-8">
          <SuggestionPopup selected={selectedWord} onApply={handleApply} onClose={() => setSelectedWord(null)} />
        </div>
      )}
    </div>
  )
}
