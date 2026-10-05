import { useEffect, useState } from "react";

const API = "/api";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [taskId, setTaskId] = useState(null);
  const [code, setCode] = useState("");
  const [runResult, setRunResult] = useState(null);
  const [scores, setScores] = useState({
    correctness: 4,
    efficiency: 3,
    explanation: 4,
  });
  const [justification, setJustification] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  const task = tasks.find((t) => t.id === taskId);

  useEffect(() => {
    fetch(`${API}/tasks`)
      .then((r) => r.json())
      .then((data) => {
        setTasks(data);
        if (data[0]) {
          setTaskId(data[0].id);
          setCode(data[0].sample_response || data[0].starter);
        }
      })
      .catch(() => setMessage("Cannot reach API. Start FastAPI on :8000."));
  }, []);

  function selectTask(id) {
    const t = tasks.find((x) => x.id === id);
    setTaskId(id);
    setCode(t?.sample_response || t?.starter || "");
    setRunResult(null);
    setMessage("");
  }

  async function runTests() {
    setBusy(true);
    setMessage("");
    try {
      const res = await fetch(`${API}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task_id: taskId, code }),
      });
      const data = await res.json();
      setRunResult(data);
    } catch {
      setMessage("Run failed — is the backend up?");
    } finally {
      setBusy(false);
    }
  }

  async function saveReview() {
    if (!runResult) {
      setMessage("Run tests before saving a review.");
      return;
    }
    if (justification.trim().length < 10) {
      setMessage("Justification needs at least 10 characters.");
      return;
    }
    setBusy(true);
    try {
      const res = await fetch(`${API}/reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          task_id: taskId,
          reviewer: "manalipansuriya57",
          code,
          tests_passed: runResult.passed,
          tests_total: runResult.total,
          ...scores,
          justification,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "save failed");
      setMessage(`Review saved (#${data.id}).`);
      setJustification("");
    } catch (err) {
      setMessage(String(err.message || err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>LLM Code-Response Evaluation</h1>
        <p>
          Rate coding answers for correctness, efficiency, and explanation quality.
          Reviewer: manalipansuriya57
        </p>
      </header>

      <div className="layout">
        <aside className="panel">
          <strong>Tasks</strong>
          <ul className="task-list" style={{ marginTop: "0.75rem" }}>
            {tasks.map((t) => (
              <li key={t.id}>
                <button
                  type="button"
                  className={t.id === taskId ? "active" : ""}
                  onClick={() => selectTask(t.id)}
                >
                  {t.title}
                  <div style={{ color: "var(--muted)", fontSize: "0.75rem" }}>
                    {t.test_count} tests
                  </div>
                </button>
              </li>
            ))}
          </ul>
        </aside>

        <main className="panel">
          {task && (
            <>
              <h2 style={{ marginTop: 0 }}>{task.title}</h2>
              <p className="prompt">{task.prompt}</p>

              <label htmlFor="code">Model response (code)</label>
              <textarea
                id="code"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                spellCheck={false}
              />

              <div className="actions">
                <button type="button" className="primary" disabled={busy} onClick={runTests}>
                  Run tests
                </button>
                <button
                  type="button"
                  className="ghost"
                  onClick={() => setCode(task.sample_response)}
                >
                  Load sample
                </button>
                <button
                  type="button"
                  className="ghost"
                  onClick={() => setCode(task.starter)}
                >
                  Reset starter
                </button>
              </div>

              {runResult && (
                <div className="results">
                  <div className={runResult.passed === runResult.total ? "pass" : "fail"}>
                    Tests: {runResult.passed}/{runResult.total}
                    {runResult.error ? ` — ${runResult.error}` : ""}
                  </div>
                  <ul>
                    {(runResult.results || []).map((r) => (
                      <li key={r.index} className={r.passed ? "pass" : "fail"}>
                        #{r.index}: {r.passed ? "PASS" : "FAIL"}
                        {!r.passed &&
                          ` expected=${JSON.stringify(r.expected)} got=${JSON.stringify(r.got)}${
                            r.error ? ` err=${r.error}` : ""
                          }`}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <h3>Rubric</h3>
              <div className="row">
                {["correctness", "efficiency", "explanation"].map((key) => (
                  <div key={key}>
                    <label htmlFor={key}>{key} (1–5)</label>
                    <select
                      id={key}
                      value={scores[key]}
                      onChange={(e) =>
                        setScores((s) => ({ ...s, [key]: Number(e.target.value) }))
                      }
                    >
                      {[1, 2, 3, 4, 5].map((n) => (
                        <option key={n} value={n}>
                          {n}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>

              <label htmlFor="why">Justification</label>
              <textarea
                id="why"
                value={justification}
                onChange={(e) => setJustification(e.target.value)}
                placeholder="Why these scores? Cite failed tests, complexity, or explanation gaps."
                style={{ minHeight: 100, fontFamily: "var(--font)" }}
              />

              <div className="actions">
                <button type="button" className="primary" disabled={busy} onClick={saveReview}>
                  Save review
                </button>
              </div>
              {message && <p className="msg">{message}</p>}
            </>
          )}
        </main>
      </div>
    </div>
  );
}
