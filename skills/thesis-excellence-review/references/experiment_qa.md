# Experiment QA For RAG/LLM Theses

Use this reference when reviewing experiments for RAG, LLM, LangGraph, Self-RAG, or campus QA systems. The goal is to prevent weak experiments from supporting strong conclusions.

## Dataset Construction

The experiment chapter must state:

- Data source and construction time.
- Number of knowledge records/documents/chunks.
- Number of test questions.
- Topic/category distribution.
- Cleaning and deduplication rules.
- Whether test questions came from real users, manually written cases, source documents, or generated variants.
- Whether tuning/development examples overlap with test examples.

For campus QA, include factual lookup, procedure/process questions, conditional questions, ambiguous questions, out-of-scope/no-answer questions, and preferably adversarial or prompt-injection questions.

If the sample is small, the conclusion must be limited to "初步验证" or "在当前测试集上".

## Ground Truth And Annotation

- Every test case needs a reference answer, source evidence, expected document, or scoring rule.
- If using `source_file_line` or category labels as weak supervision, state the limitation.
- If author-labeled, acknowledge single-annotator bias.
- If human scoring is used, provide evaluator count, scoring dimensions, levels, examples, and disagreement handling.

## Metric Validity

Separate retrieval and generation evaluation.

Retrieval metrics may include:

- Hit@K / Recall@K.
- MRR@K.
- nDCG@K.
- AvgRelevant@K.

Generation metrics may include:

- Answer correctness.
- Completeness.
- Grounding/source consistency.
- Refusal correctness for no-answer cases.
- Risk-warning behavior.
- Human rating with rubric.

Do not use only BLEU/ROUGE for open-ended campus QA unless clearly framed as a rough text-overlap proxy.

## Baseline Fairness

Baselines must use comparable conditions:

- Same test set.
- Same knowledge base scope.
- Same Top-K or disclosed K differences.
- Same generation model and decoding parameters where possible.
- Same prompt template unless the prompt is the variable.
- Same reranker setting unless reranking is the ablated variable.

For retrieval claims, require Dense-only, Sparse/BM25-only, and Hybrid comparison when those methods are discussed. If Hybrid is retained despite lower metrics, explain engineering rationale without claiming it is empirically best.

## Statistical Reliability

- Tables must report sample count.
- For key metrics, prefer mean plus standard deviation, confidence interval, or at least absolute differences.
- Do not say "显著" without statistical support or a clearly large, repeated effect.
- If experiments are not repeated, say so.

## Ablation Coverage

If the thesis claims a module contributes to quality or stability, look for direct evidence or downgrade the claim.

Common ablation targets:

- Dense retrieval.
- BM25/sparse retrieval.
- Hybrid fusion.
- Query rewriting.
- Reranker.
- Quality evaluation.
- Retry/reflection.
- Refusal/no-answer strategy.
- Memory/context.
- WebSocket/status event layer, if UX claim is made.

## Latency And Performance Measurement

Performance results should state:

- Hardware and software environment.
- Model service/API mode.
- Number of samples.
- Cold start handling.
- Concurrency.
- Measurement endpoint: backend only, full browser, WebSocket, or API.
- Mean, median, P95/P99 or maximum latency.
- Error rate/timeouts.

For streaming systems, distinguish first visible status/first token from full-answer latency when possible.

## Failure Cases

A strong experiment chapter includes failure analysis:

- Retrieval miss.
- Wrong or weak evidence.
- Conflicting sources.
- Hallucinated answer.
- Incomplete answer.
- Wrong refusal.
- Failure to refuse.
- Prompt injection or unsafe instruction.
- Long context truncation.

Each failure case should explain cause, impact, and improvement direction.

## Reproducibility

Check whether the paper or project states:

- Evaluation script.
- Model versions.
- Embedding model.
- Vector DB and collection settings.
- Top-K.
- Prompt templates.
- Temperature/decoding settings.
- Random seed or nondeterministic factors.
- Report file paths or command examples.

## Experiment Claim Gate

Reject or downgrade when:

- Dataset source, size, or composition is missing.
- Ground truth or scoring protocol is absent.
- RAG claims use only cherry-picked examples.
- Baselines are unfair or undisclosed.
- Core modules are praised without ablation or evidence.
- Latency results omit sample count or environment.
- Human evaluation lacks rubric or evaluator description.
- Failure cases are absent while hallucination control or robustness is claimed.

## Required Output

```markdown
## Experiment QA Findings

### Dataset And Ground Truth

- Status:
- Missing details:
- Required fix:

### Metrics And Baselines

- Status:
- Fairness risks:
- Required fix:

### Claims Supported By Experiments

| Claim | Evidence | Status | Safer wording |
| ----- | -------- | ------ | ------------- |

### Missing Failure Cases

- ...
```
