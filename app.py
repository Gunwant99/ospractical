from flask import Flask, jsonify, request, send_from_directory
import bakery

app = Flask(__name__, static_folder="static")
bakery.start_all()

@app.get("/")
def home():
    return send_from_directory("static", "index.html")

@app.get("/cpu-scheduling")
def cpu_scheduling():
    return send_from_directory("static", "cpu-scheduling.html")

@app.get("/producer-consumer")
def producer_consumer():
    return send_from_directory("static", "producer-consumer.html")

@app.get("/bankers")
def bankers():
    return send_from_directory("static", "bankers.html")

@app.get("/memory")
def memory():
    return send_from_directory("static", "memory.html")

@app.get("/api/state")
def state():
    return jsonify(
        running=bakery.running,
        size=bakery.SHELF_SIZE,
        on_shelf=len(bakery.shelf),
        baked=bakery.baked,
        sold=bakery.sold,
        status=bakery.status,
        messages=bakery.messages,
        bake_time=bakery.BAKE_TIME,
        buy_time=bakery.BUY_TIME
    )

@app.post("/api/running")
def set_running():
    data = request.get_json(silent=True) or {}
    bakery.running = bool(data.get("running", False))
    return jsonify(ok=True, running=bakery.running)

@app.post("/api/speed")
def set_speed():
    data = request.get_json(silent=True) or {}
    if "bake_time" in data:
        bakery.BAKE_TIME = max(0.1, min(10, float(data["bake_time"])))
    if "buy_time" in data:
        bakery.BUY_TIME = max(0.1, min(10, float(data["buy_time"])))
    return jsonify(ok=True)

@app.post("/api/bankers")
def bankers_api():
    data = request.get_json(silent=True) or {}
    allocation = data.get("allocation", [])
    maximum = data.get("maximum", [])
    available = data.get("available", [])
    try:
        if not allocation or len(allocation) != len(maximum):
            return jsonify(error="Allocation and Maximum must have the same non-zero number of processes."), 400
        resources = len(available)
        if resources == 0 or any(len(row) != resources for row in allocation + maximum):
            return jsonify(error="Each row must have one value per resource."), 400
        if any(not isinstance(v, int) or v < 0 for row in allocation + maximum for v in row) or any(not isinstance(v, int) or v < 0 for v in available):
            return jsonify(error="Resource values must be non-negative integers."), 400
        if any(allocation[i][j] > maximum[i][j] for i in range(len(allocation)) for j in range(resources)):
            return jsonify(error="Allocation cannot be greater than Maximum."), 400

        need = [[maximum[i][j] - allocation[i][j] for j in range(resources)] for i in range(len(allocation))]
        work = available[:]
        finish = [False] * len(allocation)
        sequence = []
        steps = []
        progress = True
        while progress:
            progress = False
            for i in range(len(allocation)):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(resources)):
                    before = work[:]
                    work = [work[j] + allocation[i][j] for j in range(resources)]
                    steps.append({"process": f"P{i+1}", "work_before": before, "work_after": work[:]})
                    finish[i] = True
                    sequence.append(f"P{i+1}")
                    progress = True
        return jsonify(need=need, safe=all(finish), sequence=sequence, steps=steps, unfinished=[f"P{i+1}" for i, done in enumerate(finish) if not done])
    except (TypeError, ValueError, IndexError):
        return jsonify(error="Please enter valid integer matrices."), 400

@app.post("/api/memory")
def memory_api():
    data = request.get_json(silent=True) or {}
    blocks = data.get("blocks", [])
    processes = data.get("processes", [])
    method = data.get("method", "first")
    if method not in ("first", "best", "worst"):
        return jsonify(error="Choose First Fit, Best Fit or Worst Fit."), 400
    if not isinstance(blocks, list) or not isinstance(processes, list):
        return jsonify(error="Sizes must be lists of numbers."), 400
    if not blocks or not processes or any(not isinstance(x, int) or isinstance(x, bool) or x <= 0 for x in blocks + processes):
        return jsonify(error="Block and process sizes must be positive integers."), 400

    remaining = blocks[:]
    allocations = []
    placements = [[] for _ in blocks]
    for pi, size in enumerate(processes):
        candidates = [i for i, free in enumerate(remaining) if free >= size]
        chosen = None
        if candidates:
            if method == "first":
                chosen = candidates[0]
            elif method == "best":
                chosen = min(candidates, key=lambda i: remaining[i])
            else:
                chosen = max(candidates, key=lambda i: remaining[i])
            remaining[chosen] -= size
            placements[chosen].append({"process": f"P{pi+1}", "size": size})
        allocations.append({
            "process": f"P{pi+1}",
            "size": size,
            "block": None if chosen is None else chosen + 1,
            "remaining_in_block": None if chosen is None else remaining[chosen],
            "status": "Allocated" if chosen is not None else "Not allocated"
        })
    unallocated = [a["process"] for a in allocations if a["block"] is None]
    smallest_failed = min((a["size"] for a in allocations if a["block"] is None), default=0)
    return jsonify(allocations=allocations, remaining=remaining, total_free=sum(remaining),
                   placements=placements, unallocated=unallocated,
                   fragmentation=bool(unallocated) and sum(remaining) >= smallest_failed,
                   external_fragmentation_note="Free space is shown per block; separate free blocks cannot always be combined to satisfy one request.")

if __name__ == "__main__":
    print("Open http://127.0.0.1:5000")
    app.run(debug=True, port=5000, threaded=True, use_reloader=False)
