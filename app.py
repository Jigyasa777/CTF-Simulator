from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/timeline')
def timeline():
    with open('data/timeline_2024.json') as f:
        timeline_2024 = json.load(f)
    with open('data/timeline_2025.json') as f:
        timeline_2025 = json.load(f)
    return render_template('timeline.html', events_2024=timeline_2024, events_2025=timeline_2025)

@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/toolkit', methods=['GET', 'POST'])
def toolkit():
    uart_output = None
    encode_output = None

    if request.method == 'POST':
        if 'command' in request.form:
            command = request.form.get('command', '').strip()
            if command == '':
                uart_output = ""
            elif command.lower() == 'help':
                uart_output = "Available commands: help, ping, reboot, version"
            elif command.lower() == 'ping':
                uart_output = "PONG"
            elif command.lower() == 'reboot':
                uart_output = "Rebooting system...\nDone. (This is just a simulation!)"
            elif command.lower() == 'version':
                uart_output = "Device Firmware v1.2.3 (Simulated)"
            else:
                uart_output = f"Unknown command: {command}"
        elif 'text' in request.form:
            text = request.form.get('text', '')
            operation = request.form.get('operation', '')
            key = request.form.get('key', '')
            try:
                if operation == 'base64_encode':
                    import base64
                    encode_output = base64.b64encode(text.encode()).decode()
                elif operation == 'base64_decode':
                    import base64
                    encode_output = base64.b64decode(text.encode()).decode()
                elif operation == 'hex_encode':
                    encode_output = text.encode().hex()
                elif operation == 'hex_decode':
                    encode_output = bytes.fromhex(text).decode()
                elif operation == 'xor':
                    if not key:
                        encode_output = "(Error: please provide a key for XOR.)"
                    else:
                        result_chars = []
                        for i, ch in enumerate(text):
                            result_chars.append(chr(ord(ch) ^ ord(key[i % len(key)])))
                        encode_output = ''.join(result_chars)
                else:
                    encode_output = "(Unknown operation)"
            except Exception as e:
                encode_output = f"(Error: {str(e)})"
    return render_template('toolkit.html', uart_output=uart_output, encode_output=encode_output)

@app.route('/resources')
def resources():
    return render_template('resources.html')

if __name__ == '__main__':
    app.run(debug=True)
