# Pipelines

BioBuntu supports complex bioinformatics pipelines with dependency management and parallel execution.

## Available Pipelines

- **RNA-seq**: Complete RNA sequencing analysis pipeline
- **Variant Calling**: DNA variant detection and annotation
- **Metagenomics**: Microbial community analysis
- **QC**: Quality control and preprocessing

## Pipeline Structure

Pipelines are defined in YAML format with the following structure:

```yaml
name: Pipeline Name
description: Brief description
steps:
  - name: step_name
    tool: tool_name
    depends_on: [previous_step]  # Optional dependencies
    args:
      parameter1: value1
      parameter2: value2
```

## Advanced Features

### Dependencies
Steps can depend on previous steps using `depends_on`. BioBuntu will automatically resolve dependencies and execute steps in the correct order.

### Parallel Execution
Independent steps (no dependencies between them) are executed in parallel to maximize performance.

### Parameterization
Tools accept configurable parameters through the `args` section, allowing customization for different datasets.

## Creating Custom Pipelines

1. Create a new YAML file in the `workflows/` directory
2. Define your pipeline structure
3. Validate with: `biobuntu validate your_pipeline.yaml`
4. Run with: `biobuntu run your_pipeline.yaml --project project_name`

## Example: RNA-seq Pipeline

```yaml
name: RNA-seq Pipeline
description: Complete RNA-seq analysis
steps:
  - name: quality_control
    tool: fastqc
    args:
      input_file: raw_data/sample.fastq
      output_dir: qc/

  - name: alignment
    tool: hisat2
    depends_on: [quality_control]
    args:
      index: reference/genome
      input_fastq1: raw_data/sample.fastq
      output_sam: processed/sample.sam

  - name: quantification
    tool: featurecounts
    depends_on: [alignment]
    args:
      input_sam: processed/sample.sam
      annotation: reference/genes.gtf
      output_counts: results/gene_counts.txt
```

## Validation

Always validate your pipelines before running:

```bash
biobuntu validate workflows/rnaseq.yaml
```

This checks for:
- Required fields (name, tool)
- Valid tool names
- Dependency resolution
- Parameter validation