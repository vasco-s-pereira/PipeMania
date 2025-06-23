# PipeMania AI Solver

An AI-based solver for PipeMania puzzles, developed as part of an Artificial Intelligence course project. This implementation has passed all provided unit tests, ensuring correctness and robustness of the solution.

## Table of Contents
- [Overview](#overview)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Running Tests](#running-tests)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)  

## Overview  
This repository contains a Python implementation of a PipeMania (or “Pipe Dream”) puzzle solver using informed search and heuristic techniques. Given an input puzzle description, the solver finds a valid pipe layout that satisfies end-to-end connectivity constraints.

## Features  
- **Automated Puzzle Parsing**: Reads puzzle definitions from text or PDF formats.  
- **Search Algorithms**: Implements breadth-first, depth-first, and A* search strategies.  
- **Heuristics**: Custom heuristics for guiding the search toward feasible pipe configurations.  
- **Visualization**: Renders solved puzzles graphically via the `visualizer.py` module.  
- **Robustness**: All modules have corresponding unit tests and the entire suite passes without failures :contentReference[oaicite:2]{index=2}.

## Prerequisites  
- **Python** 3.8 or higher  
- **pip** for package installation  

## Installation  
Clone the repository and install dependencies:

```bash
git clone https://github.com/vasco-s-pereira/PipeMania.git
cd PipeMania
pip install numpy matplotlib
````

## Usage

Run the solver on a puzzle file:

```bash
python pipe.py path/to/puzzle_definition.txt
```

To specify a different search strategy:

```bash
python pipe.py --strategy astar path/to/puzzle_definition.txt
```

Visualize the result:

```bash
python visualizer.py path/to/solution.json
```

## Running Tests

All unit tests are located in the `tests/` directory. To run the full test suite:

```bash
pytest
```

You should see output indicating that **all tests passed** ([github.com][1]).

## Project Structure

```
PipeMania/
├── images/                         # Example puzzle screenshots and diagrams
├── tests/                          # Unit tests for each module
├── Projeto_IA_2023_24_PIPES_23abril.pdf  
├── pipe.py                         # Main solver entry point
├── search.py                       # Search algorithm implementations
├── utils.py                        # Helper functions and data structures
├── visualizer.py                   # Puzzle solution rendering
└── README.md                       # This document
```

All modules have been tested and validated ([github.com][1]).

## Contributing

Contributions, issue reports, and pull requests are welcome! Please fork the repository, make your changes in a feature branch, and submit a PR against `main`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.


[1]: https://github.com/vasco-s-pereira/PipeMania "GitHub - vasco-s-pereira/PipeMania: Project for my Artificial Intelligence class."
