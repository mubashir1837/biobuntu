import subprocess
import os

def run_fastqc(input_file, output_dir=None):
    """
    Run FastQC on input file.
    """
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    
    cmd = ['fastqc', input_file, '-o', output_dir]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FastQC failed: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("FastQC not found. Please install FastQC.")