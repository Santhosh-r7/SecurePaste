from flask import Flask, request, jsonify
from flask_cors import CORS  
from llm_guard.input_scanners import Secrets, Anonymize, Code
from llm_guard.vault import Vault

app = Flask(__name__)
CORS(app)  

vault = Vault()


secrets_scan = Secrets()
pii_scan = Anonymize(vault)
code_scan = Code(languages=["Python"], is_blocked=True)

@app.route("/scan", methods=["POST"])
def scan():
    
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    prompt = data.get("prompt", None)

    if prompt is None:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    try:
        _, secrets_issue = secrets_scan.scan(prompt)
        _, pii_issue = pii_scan.scan(prompt)
        _, code_issue = code_scan.scan(prompt)

        block = bool(secrets_issue or pii_issue or code_issue)

        
        return jsonify({
            "block": block,
            "issues": {
                "secrets": secrets_issue,
                "pii": pii_issue,
                "code": code_issue
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
