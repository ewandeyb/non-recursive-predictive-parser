# Project Documentation

This project is a non-recursive predictive parser with a GUI for loading grammars and tracing parsing. It includes a simple GUI made of panels for input, parse table visualization, productions, and parsing trace. Tests are provided for core components.

## Parts / Modules / Functions

- `main.py` — Program entry point. Initializes the application and GUI.
- `output_handling.py` — Utilities for formatting or saving program output and parse traces.
- `rules.prod`, `rules.ptbl` — Example grammar and parse table files used by the parser.
- `parsers/parse_table.py` — Builds and exposes the predictive parse table used by the parser.
- `parsers/production_rules.py` — Loads and represents production rules used by the parse table.
- `panels/` — GUI components; each panel is responsible for a part of the interface:
  - `input_panel.py` — Provides the text input UI and controls to start parsing.
  - `load_file.py` — Handles loading grammar or input files.
  - `parse_table_panel.py` — Shows the parse table to the user.
  - `parsing_trace_panel.py` — Displays step-by-step parsing trace during parse.
  - `productions_panel.py` — Shows the production rules.
- `tests/` — Unit tests for core modules:
  - `test_output_handling.py` — Tests for output utilities.
  - `test_parse_table.py` — Tests for parse table construction/behavior.
  - `test_production_rules.py` — Tests for production rules parsing.

## Control flow 

1. Program starts at `main.py`.
2. Application loads production rules from `rules.prod` (or a file chosen via `load_file`).
3. `parsers.production_rules` parses the rules into an internal representation.
4. `parsers.parse_table` builds the predictive parse table from those productions.
5. The GUI is started and panels are created (input panel, parse table panel, productions panel, trace panel).
6. The user enters or loads an input string using the input panel and triggers parsing.
7. The parser uses the parse table to process the input and emits parsing steps.
8. `parsing_trace_panel` and `output_handling` display/format the trace and final result.