import React from 'react'
import Navbar from './components/Navbar'
import Home from './pages/Home'

export default function App(){
  return (
    <div className="min-h-screen bg-white text-slate-700">
      <Navbar />
      <main className="p-6">
        <Home />
      </main>
    </div>
  )
}
