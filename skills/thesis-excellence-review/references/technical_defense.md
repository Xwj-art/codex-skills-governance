# Technical Defense Review

Use this reference when reviewing a LangGraph/RAG/Self-RAG campus QA thesis from a strict oral-defense perspective. The goal is not to make the paper sound more advanced; it is to ensure every technical claim can survive questioning.

## Core Defense Questions

### Topic Necessity

- Does the thesis explain why campus QA needs more than FAQ, keyword search, or ordinary site search?
- Are real scenarios named: policy lookup, procedure consultation, multi-source campus notices, time-sensitive information, ambiguous student wording?
- Is the system boundary clear: what campus questions are in scope and out of scope?

### RAG Necessity

- Does the thesis justify RAG over direct LLM answering, fine-tuning, database query, FAQ retrieval, or pure BM25?
- Are the reasons concrete: knowledge freshness, source grounding, controllable refusal, lower update cost?
- If knowledge coverage is weak, are claims downgraded accordingly?

### LangGraph Justification

- Does the thesis explain why graph orchestration is needed instead of a simple chain or hand-written pipeline?
- Are graph nodes, state fields, conditional edges, retries, and fallback paths mapped to actual code?
- If LangGraph is mostly used as workflow organization, describe it as engineering structure rather than theoretical innovation.

### Self-RAG And Multi-Agent Authenticity

- Does the system actually evaluate retrieval or answer quality and decide whether to retry, rewrite, refuse, or continue?
- Are "agents" real decision-making components with input, output, state, and branching rules?
- If the implementation is mainly a node pipeline, avoid overstating it as autonomous multi-agent collaboration.

### Node And State Design

For each node, identify:

- Input fields.
- Output fields.
- Decision rule.
- Failure behavior.
- Why this node should be separate instead of merged.

Check whether state fields are used consistently and whether hidden dependencies exist between nodes.

### Retrieval Validity

- Are Dense-only, Sparse/BM25-only, and Hybrid compared where retrieval benefit is claimed?
- Are chunk size, overlap, Top-K, fusion strategy, deduplication, reranking, and ranking logic explained?
- If Sparse-only wins, Hybrid must be framed as an extensibility or robustness tradeoff, not as the empirically best current strategy.
- For hash-based sparse vectors, check tokenization, IDF, collision risk, Chinese text fit, and differences from standard BM25.

### Knowledge Base And Data Legitimacy

- Are data sources, collection method, permission boundary, update time, document count, record count, and coverage categories clear?
- Are private student data, internal documents, logs, or API-transmitted content handled safely?
- Can a reader understand how new campus documents are added and indexed?

### Security And Privacy

Check whether the thesis considers:

- Prompt injection: "ignore previous rules", malicious instructions inside retrieved documents.
- Out-of-scope or unsafe questions.
- Privacy leakage from logs, memory, user IDs, API requests, or stored conversations.
- Unauthorized campus information queries.
- Content safety and refusal behavior.

Absence of full implementation is acceptable for a bachelor thesis only if the limitation is stated honestly.

### Engineering Reality

- Can each claimed module be located in code?
- Does the thesis describe startup dependencies: API keys, Qdrant, embedding model, LLM service, backend, frontend?
- Are failure paths covered: LLM timeout, vector DB unavailable, empty retrieval, malformed input, WebSocket disconnect, configuration missing?
- Are maintenance paths clear: update knowledge base, rebuild index, replace model, adjust prompts, inspect logs?

### Performance And Cost

- Are latency, concurrency, P95/P99, error rate, and resource usage measured when performance is claimed?
- Does the thesis discuss LLM API dependency, model cost, caching, retry cost, or long-term campus deployment feasibility?
- For WebSocket, does the paper explain why streaming/status events are useful compared with ordinary HTTP?

## Claim Discipline

Mark each major claim:

- **Supported**: backed by code and experiment.
- **Weak**: code exists but experiment is small or indirect.
- **Unsupported**: asserted without evidence.
- **Overstated**: wording is stronger than evidence.

Replace unsupported strong claims:

- "显著提升" -> "在当前测试集上表现更好" only if data supports it.
- "有效避免幻觉" -> "在低证据场景下倾向于给出风险提示".
- "多智能体协同" -> "基于节点化工作流的分阶段处理" if agents are not autonomous.
- "可部署到真实校园" -> "具备进一步试运行的工程基础" unless deployment was done.

## Required Output

```markdown
## Technical Defense Findings

### High-Risk Questions

1. Question:
   Current paper answer:
   Evidence:
   Risk:
   Required fix:

### Code-To-Paper Mapping

| Claim | Paper location | Code/module evidence | Status |
| ----- | -------------- | -------------------- | ------ |

### Claims To Downgrade

| Original claim | Why risky | Safer wording |
| -------------- | --------- | ------------- |
```
