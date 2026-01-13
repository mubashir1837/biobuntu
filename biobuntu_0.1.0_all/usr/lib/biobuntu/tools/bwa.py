import subprocess

def run_bwa_mem(input_fastq1, input_fastq2, reference, output_sam):
    """
    Run BWA MEM alignment.
    """
    cmd = ['bwa', 'mem', reference, input_fastq1, input_fastq2, '-o', output_sam]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"BWA failed: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("BWA not found. Please install BWA.")