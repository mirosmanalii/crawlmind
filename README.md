# CRAWLMIND
A thinking crawler, not a scraper.

# PROJECT DIRECTORY 

crawlmind/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── src/
│   └── crawlergraph/
│       ├── __init__.py
│       ├── graph.py                  # LangGraph assembly
│       ├── state.py                  # CrawlState definition
│       ├── config.py                 # Tunable thresholds & limits
│       │
│       ├── nodes/
│       │   ├── __init__.py
│       │   ├── observe.py            # ObservePage node
│       │   ├── classify_page.py      # Page-type classification
│       │   ├── analyze_defects.py    # Signal → defect interpretation
│       │   ├── decide_action.py      # Next-action decision logic
│       │   ├── update_memory.py      # Loop detection & crawl memory
│       │   └── stop_conditions.py    # Explicit stop logic
│       │
│       ├── classifiers/
│       │   ├── __init__.py
│       │   ├── page_type.py          # Rule-based page classifier
│       │   └── llm_fallback.py       # Optional LLM classifier
│       │
│       ├── features/
│       │   ├── __init__.py
│       │   ├── dom_features.py       # DOM → feature extraction
│       │   └── runtime_features.py   # Console / network / perf features
│       │
│       ├── defects/
│       │   ├── __init__.py
│       │   ├── models.py             # Defect schema
│       │   ├── rules.py              # Signal → defect rules
│       │   ├── severity.py           # Severity scoring
│       │   └── priority.py           # Priority computation
│       │
│       ├── actions/
│       │   ├── __init__.py
│       │   ├── models.py             # ActionDecision schema
│       │   └── policies.py           # Page-type → action policies
│       │
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── loop_guards.py        # Infinite-loop prevention
│       │   └── visit_tracker.py      # Page fingerprint tracking
│       │
│       ├── io/
│       │   ├── __init__.py
│       │   ├── input_schema.py       # LangGraph input contract
│       │   └── output_schema.py      # LangGraph output contract
│       │
│       └── utils/
│           ├── __init__.py
│           ├── hashing.py            # DOM fingerprinting
│           ├── normalization.py      # URL / signal normalization
│           └── logging.py            # Explainable logs
│
├── tests/
│   ├── test_page_classification.py
│   ├── test_loop_detection.py
│   ├── test_defect_mapping.py
│   └── test_action_decisions.py
│
└── examples/
    ├── sample_input.json
    ├── sample_output.json
    └── replay_trace.json
