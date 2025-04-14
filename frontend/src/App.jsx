import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [formattedResponse, setFormattedResponse] = useState(null);

  const handleSubmit = async () => {
    await axios.post('http://<REQUEST-SERVICE-ENDPOINT>/submit', { text });
    setSubmitted(true);
  };

  const fetchFormattedResponse = async () => {
    const res = await axios.get('http://<FORMATTING-SERVICE-ENDPOINT>/latest');
    setFormattedResponse(res.data);
  };

  return (
    <div style={{ padding: 30 }}>
      <h2>Text Formatter</h2>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter your message"
      />
      <button onClick={handleSubmit}>Submit</button>
      {submitted && <button onClick={fetchFormattedResponse}>Fetch Response</button>}
      {formattedResponse && (
        <div>
          <strong>Formatted:</strong> {formattedResponse.formatted_response}
        </div>
      )}
    </div>
  );
}

export default App;