import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

const TRUST_PRESET = "is it actively maintained and production ready?"

export default function ChatPanel({ repoUrl, onAsk }) {
  const [mode, setMode] = useState('qa') // 'qa' | 'trust'
  const [question, setQuestion] = useState('')
  const [qaAnswer, setQaAnswer] = useState('')
  const [trustAnswer, setTrustAnswer] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const currentAnswer = mode === 'qa' ? qaAnswer : trustAnswer

  const handleSubmit = async (e) => {
    e.preventDefault()
    const messageToSend = mode === 'trust' ? TRUST_PRESET : question
    if (!messageToSend.trim() || !repoUrl || isLoading) return

    setIsLoading(true)
    setError('')

    try {
      const result = await onAsk(repoUrl, messageToSend)
      if (mode === 'trust') {
        setTrustAnswer(result)
      } else {
        setQaAnswer(result)
      }
    } catch (err) {
      setError('Something went wrong — check the backend is running and try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-md border border-zinc-200">
      {/* Mode toggle */}
      <div className="flex gap-1 mb-4 bg-zinc-100 p-1 rounded-lg w-fit">
        <button
          type="button"
          onClick={() => setMode('qa')}
          className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
            mode === 'qa' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-700'
          }`}
        >
          Ask a Question
        </button>
        <button
          type="button"
          onClick={() => setMode('trust')}
          className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
            mode === 'trust' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-700'
          }`}
        >
          Trust Check
        </button>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        {mode === 'qa' ? (
          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="How do I install this?"
              className="flex-1 px-4 py-2 bg-zinc-50 border border-zinc-300 rounded-lg text-zinc-900 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
            <button
              type="submit"
              disabled={!question.trim() || isLoading}
              className="px-5 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-zinc-300 disabled:cursor-not-allowed text-white font-medium rounded-lg shadow-sm transition-colors whitespace-nowrap"
            >
              {isLoading ? 'Thinking…' : 'Ask'}
            </button>
          </div>
        ) : (
          <button
            type="submit"
            disabled={isLoading}
            className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-zinc-300 disabled:cursor-not-allowed text-white font-medium rounded-lg shadow-sm transition-colors w-fit"
          >
            {isLoading ? 'Checking…' : 'Run Trust Check'}
          </button>
        )}
      </form>

      {isLoading && (
        <div className="mt-6 flex items-center gap-2 text-zinc-500 text-sm">
          <span className="h-2 w-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
          <span className="h-2 w-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
          <span className="h-2 w-2 bg-blue-500 rounded-full animate-bounce" />
        </div>
      )}

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {currentAnswer && !isLoading && (
        <div
          className={`mt-6 p-4 rounded-lg border ${
            mode === 'trust' ? 'bg-emerald-50 border-emerald-200' : 'bg-zinc-50 border-zinc-200'
          }`}
        >
          <h4 className="text-sm font-semibold text-zinc-500 uppercase tracking-wider mb-2">
            {mode === 'trust' ? 'Trust Report' : 'Answer'}
          </h4>
          <div className="prose prose-sm max-w-none prose-zinc prose-code:bg-zinc-200 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-code:before:content-none prose-code:after:content-none">
            <ReactMarkdown>{currentAnswer}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  )
}