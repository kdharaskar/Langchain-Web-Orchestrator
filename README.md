# Langchain-Web-Orchestrator

![Project Status](https://img.shields.io/badge/status-archived-red)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

### **Project Archived**

This project serves as a portfolio piece of integration of various technologies. Dependencies may be outdated and the application may not run without modifications.

---

## Overview

**Langchain-Web-Orchestrator** demonstrates a workflow for orchestrating web-based tasks using Python, Flask, and the Langchain framework. The core idea was to build a system that could:

1.  **Extract** information from a given webpage.
2.  **Process** that information using a Large Language Model (LLM).
3.  **Generate** new content based on the processed information.
4.  **Automate** a follow-up action.

## Key Features & Technologies

* **Backend Framework:** A simple web server and API built with **Flask**.
* **LLM Integration:** **Langchain** is used as the primary framework to structure prompts, manage chains, and interact with Large Language Models.
* **Web Data Extraction:** Utilizes Python libraries like **BeautifulSoup** and **Requests** to scrape and parse HTML content from target URLs.
* **Task Automation:** Demonstrates a simple workflow for scheduling or triggering subsequent actions based on the generated content.

### Technology Stack

* **Language:** Python
* **Web Framework:** Flask
* **LLM Framework:** Langchain
* **Core Libraries:** Requests, BeautifulSoup

---

## Setup & Installation (For Reference Only)

To run this project locally, you would typically follow these steps.

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/Langchain-Web-Orchestrator.git](https://github.com/your-username/Langchain-Web-Orchestrator.git)
cd Langchain-Web-Orchestrator

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Set up your environment variables (e.g., API keys for an LLM)
# Create a .env file and add necessary keys
# OPENAI_API_KEY="your-key-here"
