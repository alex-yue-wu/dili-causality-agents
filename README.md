# DILI Causality Agents (beta)

This software is a proof-of-concept implementation of agentic AI for causality assessment of drug-induced liver injury (DILI). The current version takes in a PDF file and performs a DILI causality assessment using the selected algorithm (RECAM only for now).

Four agents are used to perform the assessment:

- **DILI Informatician** – Extracts information for DILI causality assessment from the PDF file (RAG).
- **DILI Analyst** – Performs the causality assessment and gives scores.
- **DILI Writer** – Writes the report summarizing key findings and supporting evidence.
- **DILI Expert** – Reviews all the data and generate an expert review report.

**Note**: this tool is just for research purpose only and should **NOT** be used for real-world assessment before rigorous validation by domain experts.

# Usage

### setup env

```
uv venv
uv sync
```

### activate env

```
source .venv/bin/activate
```

### run causality assessment

```
python main.py \
--input-pdf ../examples/pdf/tofacitinib_case.pdf \
--algorithm RECAM \
--output-dir ../examples/results/tofacitinib/gpt_5_chat \
> ../examples/results/tofacitinib/gpt_5_chat/RECAM_assessment_with_rag_gpt_5_chat.log
```
