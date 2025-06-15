# Chat Program Generation

This document outlines the process of generating a chat program.

## Objectives
1. Research project for Julia to help her get undergraduate research positions.
1. Able to be submitted in ArXiv in September 2025
1. Ready to be submitted to an AI conference in September 2025 (e.g. ICML, NeurIPS, ICLR)
1. Establish whether Graph + LLM converges to a feasible solution.
1. Esablish whether LLM, RAG, Reason, or Agent-based can achieve similar results with less domain specific structure.

## Need a sufficiently complex problem that can be explained in a few sentences, generally understood, cannot be solved by a simple prompt but could be sometimes solved by all of the advanced LLM techniques.  We will then compare the he behavior of the solutions.  Compare this to the [The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity](https://ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf).  

## Completions model
Single model, auto-regressive generation of a chat program with a standard LLM (e.g. GPT 4o, 4,1 ). Baseline.  Identify problem that can't be solve by a prompt alone even with multiple attempts.

## Reasoning model
Single model, auto-regressive generation of a chat program with a standard LLM (e.g.O3,  Deep Seek, ...). Iteration between reasoning model and completions model. Process constraints based on model training.  Ideally, the problem can be sometimes be solved ay a rasoning model.

## RAG Response
Aad retrieval-augmented generation (RAG) approach to chat program generation.  Should enable code generation if request matches a code sample in the RAG database.  Can be added to other models.  Ideally, the problem can be sometimes solved by with RAG.

## Agent-based prompt
Agents to formulate the problem structure, code generation, code execution, and code evaluation.  Ideally, the problem can be sometimes solved by with RAG.

## Graph-based prompt
Agent framework to first compose the problem into an abstract syntax graph (reference).  
1. Propose graph structureGenerate 
1. Define node expectations 
1. Create node tests  
1. Refine graph nodes into code.  
1. Run Program
1. Score results vs expected results.
1. Propose node changes based on results.
1. Propose graph changes (prune/grow) based on results

## Copilot Prompt
Create a web application named ai_chat_gpt41 that provides a real-time voice chat to the [gpt 4o realtime model](https://platform.openai.com/docs/guides/realtime/realtime-api-beta) and manages conversation history.  This web application includes is a python fastapi web server communicating using WebSocket between a html/javascript client, and OpenAI Realtime API.  Base the UI on the ChatGPT voice interface:
![](notebook/img/chat_gpt_voice.png)

References:
[How to use the GPT-4o Realtime API for speech and audio (Preview)](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/realtime-audio)
[How to use the GPT-4o Realtime API via WebSockets (Preview)](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/realtime-audio-websockets)
[The WebSocket API (WebSockets)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[GPT-4o Realtime API for speech and audio (Preview)](https://learn.microsoft.com/en-us/azure/ai-services/openai/realtime-audio-quickstart?tabs=keyless%2Cwindows&pivots=programming-language-python)
[websockets](https://websockets.readthedocs.io/en/stable/)
[fastapi](https://fastapi.tiangolo.com/)


