import { useState } from 'react'

const RepoInput = ({ onSubmit }) => {
  const [inputValue, setInputValue] = useState('')

  const handleSubmit = () => {
    if (inputValue.trim() === '') return
    onSubmit(inputValue)
  }

  return (
    <div className="flex gap-2 w-full max-w-xl">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="https://github.com/owner/repo"
        className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Load
      </button>
    </div>
  )
}

export default RepoInput