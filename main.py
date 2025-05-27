from flask import Flask, request, jsonify, render_template_string
import subprocess, os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>WhatsApp Pair & Sender</title>
  <style>
    body { font-family: Arial; background: #111; color: #eee; text-align: center; padding: 30px; }
    input, button { padding: 10px; margin: 10px; width: 300px; }
    .box { background: #222; padding: 20px; border-radius: 10px; display: inline-block; }
  </style>
</head>
<body>
  <h2>WhatsApp Pair Code Generator</h2>
  <div class="box">
    <form id="pairForm">
      <input name="sender" placeholder="Enter Sender Name" required><br>
      <button type="submit">Generate Pair Code</button>
    </form>
  </div>

  <h2>Send Message</h2>
  <div class="box">
    <form id="sendForm">
      <input name="sender" placeholder="Sender Name" required><br>
      <input name="target" placeholder="Target Number with +"><br>
      <input name="message" placeholder="Message Text"><br>
      <input name="delay" placeholder="Delay in Seconds"><br>
      <button type="submit">Start Sending</button>
    </form>
  </div>

  <script>
    document.getElementById('pairForm').onsubmit = async (e) => {
      e.preventDefault();
      const form = new FormData(e.target);
      const res = await fetch('/generate_paircode', { method: 'POST', body: form });
      const data = await res.json();
      alert('QR Generation Started for: ' + data.sender);
    };

    document.getElementById('sendForm').onsubmit = async (e) => {
      e.preventDefault();
      const form = new FormData(e.target);
      const res = await fetch('/send_message', { method: 'POST', body: form });
      const data = await res.json();
      alert('Message sending started...');
    };
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/generate_paircode', methods=['POST'])
def generate_paircode():
    sender = request.form.get('sender')
    if not sender:
        return jsonify({'error': 'Sender name required'}), 400

    session_dir = f"sessions/{sender}"
    os.makedirs(session_dir, exist_ok=True)
    subprocess.Popen(['node', 'generate_pair.js', sender])
    return jsonify({"status": "started", "sender": sender})

@app.route('/send_message', methods=['POST'])
def send_message():
    sender = request.form.get('sender')
    target = request.form.get('target')
    message = request.form.get('message')
    delay = request.form.get('delay')

    subprocess.Popen(['node', 'send_message.js', sender, target, message, delay])
    return jsonify({"status": "sending_started"})

if __name__ == '__main__':
    os.makedirs('sessions', exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
