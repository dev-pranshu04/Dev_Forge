---
title: Retrieval-Augmented Generation Under Domain Shift — Evaluating Embedding Faithfulness and Chunk Strategy in Specialised Knowledge Bases
authors: Pranshu Kumar
venue: Targeting ACL Findings 2026 / EMNLP 2025 workshop
year: 2025
doi: null
status: in_progress
keywords: [RAG, LLMs, Domain adaptation, SentenceTransformers, ChromaDB, Retrieval evaluation, Hallucination]
related_project: resumeiq
pdf: null
---

## Abstract

Investigates how retrieval quality degrades when RAG pipelines built on general-domain embeddings are applied to specialised knowledge bases (legal, medical, financial). Evaluates four chunking strategies and three embedding models. Preliminary findings show domain-tuned embeddings reduce hallucination rate by approximately 34% versus naive sliding-window chunking.

## Motivation

RAG is increasingly the default architecture for LLM applications requiring factual grounding. But most RAG systems are evaluated on general-domain benchmarks (Natural Questions, TriviaQA). Real-world deployments almost always involve specialised corpora where general embeddings underperform in ways that are hard to diagnose.

## Current Status

Preliminary experiments running. Dataset construction complete for legal and medical domains. Financial domain in progress. Targeting submission Q1 2026.

## Future Work

Extend to multi-hop retrieval evaluation. Explore fine-tuning embedding models on domain corpora with contrastive loss.
