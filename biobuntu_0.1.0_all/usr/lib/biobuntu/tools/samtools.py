import subprocess

def run_samtools(command_args):
    """
    Run Samtools with given arguments.
    """
    cmd = ['samtools'] + command_args
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Samtools failed: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("Samtools not found. Please install Samtools.")