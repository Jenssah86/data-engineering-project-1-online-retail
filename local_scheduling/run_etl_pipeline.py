import subprocess # Voor het uitvoeren van de Python scripts
import datetime # Voor het toevoegen van timestamps aan de log
import os # Voor het werken met bestanden en directories
import socket # Voor het controleren of MySQL draait door te proberen een socket te openen

# Pad naar jouw venv Python
PYTHON = r"D:\Studie\GitHub portfolio\data-engineering-project-1-online-retail\venv\Scripts\python.exe"

# Logbestand aanmaken
log_path = r"D:\Studie\GitHub portfolio\data-engineering-project-1-online-retail\local_scheduling\pipeline_log.txt"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def check_mysql_running(host="127.0.0.1", port=3306):
    """Check of MySQL draait door te proberen een socket te openen."""
    try:
        socket.create_connection((host, port), timeout=2)
        return True
    except OSError:
        return False

log("Pipeline gestart.")

try:
    # 0. Check of MySQL/XAMPP draait
    log("Controleren of MySQL draait...")
    if not check_mysql_running():
        log("FOUT: MySQL draait niet. Start XAMPP/MySQL en probeer opnieuw.")
        raise Exception("MySQL is niet bereikbaar.")

    log("MySQL draait. Pipeline gaat verder.")

    # 1. bronze_to_silver.py uitvoeren
    log("Start bronze_to_silver.py...")
    subprocess.run([PYTHON, r"D:\Studie\GitHub portfolio\data-engineering-project-1-online-retail\python\bronze_to_silver.py"], check=True)
    log("bronze_to_silver.py voltooid.")

    # 2. Alleen als bovenstaande succesvol was → incremental_load.py uitvoeren
    log("Start incremental_load.py...")
    subprocess.run([PYTHON, r"D:\Studie\GitHub portfolio\data-engineering-project-1-online-retail\python\incremental_load.py"], check=True)
    log("incremental_load.py voltooid.")

    log("ETL Pipeline succesvol afgerond.")

except subprocess.CalledProcessError as e:
    log(f"FOUT: Een subprocess is mislukt: {e}")

except Exception as e:
    log(f"ONBEKENDE FOUT: {e}")