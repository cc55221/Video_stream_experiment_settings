from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/decide": {"origins": "*"}})

@app.route("/decide", methods=["POST", "OPTIONS"])
def decide():
    if request.method == "OPTIONS":
        # CORS 预检
        return ("", 204)

    x = request.get_json(force=True) or {}
    buflen   = float(x.get("buffer", 0.0))
    bitrates = [int(b) for b in x.get("bitrateList", [])]  # bps
    thr_bps  = float(x.get("throughput", 0.0)) * 1000.0    # kbps -> bps

    target = 0.7 * thr_bps
    level = 0
    for i, b in enumerate(bitrates):
        if b <= target:
            level = i

    if buflen < 3 and level > 0:
        level -= 1
    elif buflen > 8 and level < len(bitrates) - 1:
        level += 1

    return jsonify({"level": int(level)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
