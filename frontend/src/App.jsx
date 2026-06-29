import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ClipboardList,
  RefreshCcw,
  RotateCcw,
  Search,
  ShieldCheck
} from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

const sampleText =
  "Officials said the public records were reviewed by independent researchers before the report was published in 2024, according to department data.";

function formatTime(value) {
  try {
    return new Intl.DateTimeFormat(undefined, {
      dateStyle: "medium",
      timeStyle: "short"
    }).format(new Date(value));
  } catch {
    return value;
  }
}

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const wordCount = useMemo(() => {
    return text.trim() ? text.trim().split(/\s+/).length : 0;
  }, [text]);

  async function loadHistory() {
    try {
      const response = await fetch(`${API_BASE}/history`);
      if (response.ok) {
        setHistory(await response.json());
      }
    } catch {
      setHistory([]);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  async function analyzeArticle(event) {
    event.preventDefault();
    const trimmed = text.trim();
    if (trimmed.length < 10) {
      setError("Enter at least 10 characters.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: trimmed })
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Prediction failed.");
      }

      setResult(payload);
      await loadHistory();
    } catch (requestError) {
      setError(requestError.message || "Prediction failed.");
    } finally {
      setLoading(false);
    }
  }

  const verdictClass = result?.prediction === "Fake" ? "danger" : "success";

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-lockup">
          <span className="brand-mark" aria-hidden="true">
            <ShieldCheck size={22} />
          </span>
          <div>
            <p className="eyebrow">NLP classifier</p>
            <h1>Fake News Detection</h1>
          </div>
        </div>
        <div className="system-status">
          <Activity size={16} />
          <span>API ready</span>
        </div>
      </header>

      <section className="workspace" aria-label="Detection workspace">
        <form className="panel compose-panel" onSubmit={analyzeArticle}>
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Article text</p>
              <h2>Analyze a claim</h2>
            </div>
            <span className="word-count">{wordCount} words</span>
          </div>

          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Paste a news article, claim, or excerpt here."
            spellCheck="true"
          />

          {error ? (
            <p className="inline-alert" role="alert">
              <AlertTriangle size={16} />
              {error}
            </p>
          ) : null}

          <div className="button-row">
            <button className="primary-button" type="submit" disabled={loading}>
              {loading ? <RefreshCcw size={18} className="spin" /> : <Search size={18} />}
              <span>{loading ? "Analyzing" : "Analyze"}</span>
            </button>
            <button className="secondary-button" type="button" onClick={() => setText(sampleText)}>
              <ClipboardList size={18} />
              <span>Sample</span>
            </button>
            <button
              className="icon-button"
              type="button"
              aria-label="Clear article text"
              title="Clear article text"
              onClick={() => {
                setText("");
                setResult(null);
                setError("");
              }}
            >
              <RotateCcw size={18} />
            </button>
          </div>
        </form>

        <section className="panel result-panel" aria-live="polite">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Verdict</p>
              <h2>Current result</h2>
            </div>
          </div>

          {result ? (
            <>
              <div className={`verdict-strip ${verdictClass}`}>
                <span>{result.prediction}</span>
                <strong>{result.confidence.toFixed(1)}%</strong>
              </div>
              <div className="confidence-track" aria-label="Confidence">
                <span style={{ width: `${Math.min(result.confidence, 100)}%` }} />
              </div>
              <dl className="metric-grid">
                <div>
                  <dt>Backend</dt>
                  <dd>{result.model_backend}</dd>
                </div>
                <div>
                  <dt>Words</dt>
                  <dd>{result.word_count}</dd>
                </div>
              </dl>
              <ul className="explanation-list">
                {result.explanation.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </>
          ) : (
            <div className="empty-result">
              <ShieldCheck size={34} />
              <p>No article analyzed yet.</p>
            </div>
          )}
        </section>
      </section>

      <section className="history-section" aria-label="Prediction history">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Recent checks</p>
            <h2>History</h2>
          </div>
          <button className="secondary-button" type="button" onClick={loadHistory}>
            <RefreshCcw size={18} />
            <span>Refresh</span>
          </button>
        </div>

        <div className="history-grid">
          {history.length ? (
            history.slice(0, 6).map((item) => (
              <article className="history-card" key={item.id}>
                <div className="history-card-top">
                  <span className={`pill ${item.prediction === "Fake" ? "danger" : "success"}`}>
                    {item.prediction}
                  </span>
                  <strong>{item.confidence.toFixed(1)}%</strong>
                </div>
                <p>{item.text_preview}</p>
                <time dateTime={item.analyzed_at}>{formatTime(item.analyzed_at)}</time>
              </article>
            ))
          ) : (
            <p className="history-empty">No saved predictions in this session.</p>
          )}
        </div>
      </section>
    </main>
  );
}

export default App;
