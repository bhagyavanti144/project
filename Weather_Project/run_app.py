# run_app.py
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    packages = [
        "streamlit",
        "pandas",
        "numpy",
        "scikit-learn",
        "plotly",
        "requests",
        "joblib"
    ]
    
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def run_app():
    """Run the Streamlit app"""
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    print("Installing requirements...")
    install_requirements()
    print("Starting the weather prediction app...")
    run_app()
