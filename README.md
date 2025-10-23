# Shoe Knowledge Graph Construction

Extracts practical insights from running shoe research papers using BAML and structures them into a knowledge graph for evidence-based shoe selection guidance.

## Overview

This repository handles the **knowledge graph construction** phase of a larger running shoe recommendation system. It extracts key findings from biomechanics research papers and organizes them into a queryable graph database that connects research insights with practical shoe features.

## What This Does

1. **PDF Extraction**: Uses BAML to parse research papers and extract actionable keypoints about shoe features
2. **Knowledge Organization**: Structures findings into a Neo4j graph with topic-based connections
3. **Research Translation**: Converts academic findings into practical insights for shoe selection

This is **one component** of a multi-repo project. Other repos handle:
- Web browser agent for finding actual shoes
- Query interface for personalized recommendations
- Integration layer combining all components

## Current Focus

**Input**: PDF research papers on running shoe biomechanics  
**Output**: Structured knowledge graph with:
- Research papers → Keypoints → Topics
- Personal notes → Observations → Topics
- Topic nodes: Cushioning, CarbonPlates, HeelToeDrop, StackHeight, GaitPatterns

## Tech Stack

- **BAML**: LLM-powered structured extraction from PDFs
- **Claude (Haiku/Sonnet)**: Extraction models with fallback strategy
- **Neo4j**: Graph database for knowledge storage
- **Python**: Orchestration and batch processing

## Project Structure
```
├── baml_src/              # BAML schemas and functions
│   └── article.baml       # PDF extraction configuration
├── papers/                # Research papers (gitignored)
├── main.py               # Batch extraction script
├── extracted_articles.json # Structured keypoints output
└── README.md
```