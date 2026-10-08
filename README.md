# Parallel Web Crawler for Large-Scale Data Collection

A Python-based web crawler that demonstrates the performance improvement achieved by **parallel processing** when collecting data from multiple web pages.

The project implements both **Sequential** and **Parallel** web crawlers and compares their execution time, speedup, and efficiency.

---

## 📌 Project Overview

Web crawling involves downloading and processing information from multiple web pages. A sequential crawler processes one page at a time, which can be slow when the number of pages increases.

This project uses **Python ThreadPoolExecutor** to crawl multiple pages concurrently.

The performance of both approaches is compared using:

- Execution Time
- Speedup
- Parallel Efficiency
- Number of Workers
- Number of Pages Crawled

---

## 🎯 Objectives

- Develop a sequential web crawler.
- Develop a parallel web crawler.
- Use multithreading for concurrent web requests.
- Compare sequential and parallel execution.
- Measure speedup and parallel efficiency.
- Provide a GUI for running and monitoring the crawler.
- Store crawling and benchmark results in CSV files.

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │    User / GUI       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
   ┌────────────────────┐             ┌────────────────────┐
   │ Sequential Crawler │             │  Parallel Crawler  │
   └─────────┬──────────┘             └─────────┬──────────┘
             │                                  │
             │                                  ▼
             │                         ThreadPoolExecutor
             │                                  │
             └────────────────┬─────────────────┘
                              ▼
                    ┌────────────────────┐
                    │    Test Website    │
                    │   Local Web Pages  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   CSV Results      │
                    └────────────────────┘
