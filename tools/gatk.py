import subprocess

def run_gatk(command_args):
    """
    Run GATK with given arguments.
    """
    cmd = ['gatk'] + command_args
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"GATK failed: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("GATK not found. Please install GATK.")