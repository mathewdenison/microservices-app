import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [formattedResponse, setFormattedResponse] = useState(null);

  const handleSubmit = async () => {
    await axios.post(process.env.REACT_APP_REQUEST_SERVICE_URL, { text });
    setSubmitted(true);
  };

  const fetchFormattedResponse = async () => {
    const res = await axios.get(process.env.REACT_APP_FORMATTING_SERVICE_URL);
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