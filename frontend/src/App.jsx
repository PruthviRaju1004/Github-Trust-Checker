import { useState } from 'react'
import RepoInput from './components/RepoInput'
import ChatPanel from './components/ChatPanel'

function App() {
  const [repoUrl, setRepoUrl] = useState('')

  const handleRepoSubmit = (url) => {
    setRepoUrl(url)
  }

  const handleAsk = async (url, questionText) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: url, message: questionText }),
      })
      if (!response.ok) {
        throw new Error(`Server returned status: ${response.status}`)
      }
      const data = await response.json()
      return data.answer
    } catch (error) {
      console.error('Error fetching answer from FastAPI:', error)
      throw error
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-8 gap-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Trust Checker</h1>
        <p className="text-gray-500 text-sm mt-1">
          Ask questions about a repo's docs, or check if the README matches reality
        </p>
      </div>

      <RepoInput onSubmit={handleRepoSubmit} />

      {repoUrl && (
        <>
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <span className="h-2 w-2 bg-green-500 rounded-full" />
            Active repo: <span className="font-medium text-gray-700">{repoUrl}</span>
          </div>
          <ChatPanel repoUrl={repoUrl} onAsk={handleAsk} />
        </>
      )}
    </div>
  )
}

export default App