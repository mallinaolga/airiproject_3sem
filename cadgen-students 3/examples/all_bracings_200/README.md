# AIRI: 200 CADGen inputs

One attempt per source, eight-type geometry-only restoration. Hard worker timeout: 600 seconds; process tree is terminated on timeout. Each model has a checkpoint; manifest and reports/results.json are updated after each result. STEP/STL remain under models/model_NNN/attempt_NNN/. Logs are in logs/.

Resume from the project directory:

powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -WorkingDirectory 'cadgen-students 3' -FilePath 'cadgen-students 3/.venv-cad/Scripts/python.exe' -ArgumentList 'run_bracings_200.py'"

No global assembly trajectory or physical strength is verified. Previous manual experiment is preserved: it lacks a supervisor manifest and reliable process/time checkpoints.
