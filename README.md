# OS Algorithm Visualizer
**Scenario:** Online Examination and Result Processing System

## Modules
1. CPU Scheduling — preserved from the existing HTML/CSS/JavaScript project.
2. Producer–Consumer Synchronization — preserved from the existing Flask/threading bakery demo and reframed as an answer-submission queue.
3. Banker’s Algorithm — calculates Need = Maximum − Allocation and checks for a safe sequence.
4. Memory Management — First Fit, Best Fit and Worst Fit allocation with a per-block layout view.

## Run on Windows
1. Extract this ZIP.
2. Open the extracted folder in VS Code or PowerShell.
3. (Recommended) Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Install dependency:
   ```powershell
   pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   python app.py
   ```
6. Open http://127.0.0.1:5000

## Project layout
```
app.py  bakery.py  requirements.txt
static/  index.html  cpu-scheduling.html  producer-consumer.html  bankers.html  memory.html
         style.css  script.js  nav.js
```
All HTML, CSS and JS files must stay inside the `static/` folder.

## Notes
- Sample data is illustrative and intended for demonstrating OS concepts, not a production examination service.
- The Producer–Consumer module retains the existing bakery simulation mechanics. In the report, explain the mapping: producers = student answer submissions, bounded shelf = submission queue, consumers = evaluation workers.
- CPU Scheduling calculations remain in the existing JavaScript module.
