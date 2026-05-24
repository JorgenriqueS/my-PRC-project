from flask import Flask, request, jsonify
from calculator import add, subtract, multiply, divide

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Calculadora</title>
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Bebas+Neue&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0e0e0e;
      --surface: #1a1a1a;
      --border: #2e2e2e;
      --accent: #c8f135;
      --accent2: #ff5c5c;
      --text: #f0f0f0;
      --muted: #555;
      --btn-bg: #1f1f1f;
      --btn-hover: #2a2a2a;
      --btn-active: #c8f135;
    }

    body {
      background: var(--bg);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Share Tech Mono', monospace;
      color: var(--text);
      background-image:
        repeating-linear-gradient(0deg, transparent, transparent 39px, var(--border) 39px, var(--border) 40px),
        repeating-linear-gradient(90deg, transparent, transparent 39px, var(--border) 39px, var(--border) 40px);
    }

    .calc-wrapper {
      display: flex;
      flex-direction: column;
      gap: 8px;
      align-items: center;
    }

    .calc-label {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 11px;
      letter-spacing: 6px;
      color: var(--muted);
      text-transform: uppercase;
    }

    .calc {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 24px;
      width: 300px;
      box-shadow: 0 0 60px rgba(200, 241, 53, 0.04), 0 20px 60px rgba(0,0,0,0.6);
    }

    .display {
      background: #111;
      border: 1px solid var(--border);
      border-radius: 2px;
      padding: 16px 14px 10px;
      margin-bottom: 20px;
      min-height: 80px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }

    .display::before {
      content: '';
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(
        0deg, transparent, transparent 2px, rgba(200,241,53,0.015) 2px, rgba(200,241,53,0.015) 4px
      );
      pointer-events: none;
    }

    .display .expr {
      font-size: 12px;
      color: var(--muted);
      min-height: 18px;
      text-align: right;
      letter-spacing: 1px;
    }

    .display .result {
      font-size: 36px;
      text-align: right;
      color: var(--accent);
      letter-spacing: 2px;
      word-break: break-all;
      transition: color 0.15s;
    }

    .display .result.error { color: var(--accent2); font-size: 18px; }

    .buttons {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }

    button {
      background: var(--btn-bg);
      border: 1px solid var(--border);
      color: var(--text);
      font-family: 'Share Tech Mono', monospace;
      font-size: 16px;
      padding: 16px 0;
      border-radius: 2px;
      cursor: pointer;
      transition: background 0.1s, transform 0.08s, border-color 0.1s;
      letter-spacing: 1px;
      position: relative;
      overflow: hidden;
    }

    button:hover { background: var(--btn-hover); border-color: #444; }

    button:active {
      transform: scale(0.94);
      background: rgba(200, 241, 53, 0.12);
      border-color: var(--accent);
      color: var(--accent);
    }

    button.op {
      color: var(--accent);
      border-color: rgba(200,241,53,0.2);
      background: rgba(200,241,53,0.04);
    }
    button.op:hover { background: rgba(200,241,53,0.1); }

    button.action {
      color: var(--accent2);
      border-color: rgba(255,92,92,0.2);
      background: rgba(255,92,92,0.04);
    }
    button.action:hover { background: rgba(255,92,92,0.1); }

    button.equals {
      grid-column: span 2;
      background: var(--accent);
      color: #0e0e0e;
      border-color: var(--accent);
      font-size: 20px;
      font-family: 'Bebas Neue', sans-serif;
      letter-spacing: 3px;
    }
    button.equals:hover { background: #d4f545; }
    button.equals:active { background: #b8e020; transform: scale(0.96); }

    .status-dot {
      width: 6px; height: 6px;
      border-radius: 50%;
      background: var(--accent);
      display: inline-block;
      margin-right: 6px;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }
  </style>
</head>
<body>
<div class="calc-wrapper">
  <div class="calc-label"><span class="status-dot"></span>CALC // v1.0</div>
  <div class="calc-label" style="color:#ffffff; letter-spacing:2px; font-size:13px;">Jorge Enrique Soto Najarro &mdash; 22000612</div>
  <div class="calc">
    <div class="display">
      <div class="expr" id="expr"></div>
      <div class="result" id="result">0</div>
    </div>
    <div class="buttons">
      <button class="action" onclick="clearAll()">AC</button>
      <button class="action" onclick="toggleSign()">+/-</button>
      <button class="action" onclick="percent()">%</button>
      <button class="op" onclick="appendOp('/')">÷</button>

      <button onclick="appendNum('7')">7</button>
      <button onclick="appendNum('8')">8</button>
      <button onclick="appendNum('9')">9</button>
      <button class="op" onclick="appendOp('*')">×</button>

      <button onclick="appendNum('4')">4</button>
      <button onclick="appendNum('5')">5</button>
      <button onclick="appendNum('6')">6</button>
      <button class="op" onclick="appendOp('-')">−</button>

      <button onclick="appendNum('1')">1</button>
      <button onclick="appendNum('2')">2</button>
      <button onclick="appendNum('3')">3</button>
      <button class="op" onclick="appendOp('+')">+</button>

      <button onclick="appendNum('0')">0</button>
      <button onclick="appendDot()">.</button>
      <button class="equals" onclick="calculate()">=</button>
    </div>
  </div>
</div>

<script>
  let expr = '';
  let justCalc = false;

  const exprEl = document.getElementById('expr');
  const resultEl = document.getElementById('result');

  function updateDisplay(val, exprVal) {
    resultEl.textContent = val;
    resultEl.classList.toggle('error', val === 'Error');
    exprEl.textContent = exprVal || '';
  }

  function appendNum(n) {
    if (justCalc) { expr = ''; justCalc = false; }
    if (expr.length > 18) return;
    expr += n;
    updateDisplay(expr, '');
  }

  function appendOp(op) {
    justCalc = false;
    if (expr === '' && op !== '-') return;
    const last = expr.slice(-1);
    if (['+','-','*','/'].includes(last)) expr = expr.slice(0, -1);
    expr += op;
    updateDisplay(expr, '');
  }

  function appendDot() {
    if (justCalc) { expr = '0'; justCalc = false; }
    const parts = expr.split(/[\+\-\*\/]/);
    if (parts[parts.length - 1].includes('.')) return;
    if (parts[parts.length - 1] === '') expr += '0';
    expr += '.';
    updateDisplay(expr, '');
  }

  function clearAll() {
    expr = '';
    justCalc = false;
    updateDisplay('0', '');
  }

  function toggleSign() {
    if (!expr || expr === '0') return;
    if (expr.startsWith('-')) expr = expr.slice(1);
    else expr = '-' + expr;
    updateDisplay(expr, '');
  }

  function percent() {
    if (!expr) return;
    try { expr = String(parseFloat(expr) / 100); updateDisplay(expr, ''); } catch {}
  }

  async function calculate() {
    if (!expr) return;
    const sentExpr = expr;

    // Parse expression into a, op, b
    const match = expr.match(/^(-?[\d.]+)([+\-*/])(-?[\d.]+)$/);
    if (!match) {
      updateDisplay('Error', sentExpr);
      expr = '';
      return;
    }
    const a = parseFloat(match[1]);
    const op = match[2];
    const b = parseFloat(match[3]);

    try {
      const res = await fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ a, b, op })
      });
      const data = await res.json();
      if (data.error) {
        updateDisplay('Error', sentExpr);
        expr = '';
      } else {
        updateDisplay(data.result, sentExpr + ' =');
        expr = String(data.result);
        justCalc = true;
      }
    } catch {
      updateDisplay('Error', sentExpr);
      expr = '';
    }
  }

  document.addEventListener('keydown', e => {
    if (e.key >= '0' && e.key <= '9') appendNum(e.key);
    else if (e.key === '+') appendOp('+');
    else if (e.key === '-') appendOp('-');
    else if (e.key === '*') appendOp('*');
    else if (e.key === '/') { e.preventDefault(); appendOp('/'); }
    else if (e.key === '.') appendDot();
    else if (e.key === 'Enter' || e.key === '=') calculate();
    else if (e.key === 'Escape') clearAll();
    else if (e.key === 'Backspace') { expr = expr.slice(0, -1); updateDisplay(expr || '0', ''); }
  });
</script>
</body>
</html>"""

@app.route("/")
def index():
    return HTML

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    a = data.get("a")
    b = data.get("b")
    op = data.get("op")
    try:
        if op == "+":
            result = add(a, b)
        elif op == "-":
            result = subtract(a, b)
        elif op == "*":
            result = multiply(a, b)
        elif op == "/":
            result = divide(a, b)
        else:
            return jsonify({"error": "Operación inválida"})
        if isinstance(result, float) and result == int(result):
            result = int(result)
        return jsonify({"result": result})
    except ValueError:
        return jsonify({"error": "División entre cero"})
    except Exception:
        return jsonify({"error": "Error en la expresión"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
