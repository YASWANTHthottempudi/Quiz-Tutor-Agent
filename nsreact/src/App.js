import React, { useState } from "react";
import axios from "axios"; // Import axios
import "./App.css";

function App() {
  const [quiz, setQuiz] = useState(null); // State to store quiz data
  const [loading, setLoading] = useState(false); // State for loading spinner
  const [error, setError] = useState(null); // State for error messages

  // Function to fetch quiz from Flask API
  const fetchQuiz = async () => {
    setLoading(true);
    setError(null); // Clear previous errors
    try {
      const response = await axios.get("http://127.0.0.1:5000/generate_quiz", {
        timeout: 120000, // Set timeout to 2 minutes (120000 ms)
      });
      setQuiz(response.data); // Set the fetched quiz data
    } catch (err) {
      setError("Failed to fetch quiz. Please try again."); // Handle errors
    } finally {
      setLoading(false); // Stop the spinner
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>Quiz Generator</h1>
          <p>Click the button below to generate a quiz!</p>
        </header>

        <div className="button-section">
          <button
            className="generate-button"
            onClick={fetchQuiz}
            disabled={loading}
          >
            {loading ? "Loading..." : "Generate Quiz"}
          </button>
        </div>

        <div className="quiz-section">
          {error && <p style={{ color: "red" }}>{error}</p>}
          {quiz ? (
            <div>
              <h2>Your Quiz</h2>
              <ol>
                {quiz.quiz.mcqs.map((mcq, index) => (
                  <li key={index}>
                    <p>
                      <strong>Q{index + 1}:</strong> {mcq.question_text}
                    </p>
                    <ul>
                      {mcq.options.map((option, i) => (
                        <li key={i}>{option}</li>
                      ))}
                    </ul>
                    <p>
                      <strong>Correct Answer:</strong> {mcq.correct_answer}
                    </p>
                  </li>
                ))}
              </ol>

              <div className="sources-section">
                <h3>Sources</h3>
                <ul>
                  {quiz.sources.map((source, index) => (
                    <li key={index}>{source}</li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            !loading && (
              <p>Your quiz will appear here after you click the button.</p>
            )
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
