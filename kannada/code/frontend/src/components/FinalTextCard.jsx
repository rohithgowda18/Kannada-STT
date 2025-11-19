import React from 'react'

export default function FinalTextCard({ text = '', before = '' }){
  const downloadTxt = () => {
    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'corrected.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  const copyText = async () => {
    await navigator.clipboard.writeText(text)
    alert('Copied to clipboard')
  }

  return (
    <div className="p-6 rounded-2xl shadow-xl bg-white border border-slate-200 mt-2">
      <div className="font-medium">Final Text</div>
      <div className="mt-3 grid md:grid-cols-2 gap-4">
        <div>
          <div className="text-sm text-slate-500">Before</div>
          <pre className="whitespace-pre-wrap mt-2">{before}</pre>
        </div>
        <div>
          <div className="text-sm text-slate-500">After</div>
          <pre className="whitespace-pre-wrap mt-2">{text}</pre>
        </div>
      </div>
      <div className="mt-4 flex gap-2">
        <button onClick={downloadTxt} className="btn-gradient px-3 py-1 rounded-2xl">Download .txt</button>
        <button onClick={copyText} className="px-3 py-1 rounded-2xl border">Copy</button>
      </div>
    </div>
  )
}
