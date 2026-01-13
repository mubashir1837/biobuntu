import subprocess

def run_hisat2(index, input_fastq1, input_fastq2=None, output_sam=None):
    """
    Run HISAT2 alignment.
    """
    cmd = ['hisat2', '-x', index]
    if input_fastq2:
        cmd.extend(['-1', input_fastq1, '-2', input_fastq2])
    else:
        cmd.extend(['-U', input_fastq1])
    if output_sam:
        cmd.extend(['-S', output_sam])
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"HISAT2 failed: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("HISAT2 not found. Please install HISAT2.")