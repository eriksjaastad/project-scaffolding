# Code Quality Standards

purpose: Hard rules for code quality (supplement to REVIEWS_AND_GOVERNANCE_PROTOCOL.md checklist)
scope: Rules here are UNIQUE to this file — governance checklist covers paths, subprocess, error handling, etc.

## Error Laundering Ban

rule: never use except: pass or except Exception: pass without logging
rule: catching an exception requires one of: (a) fix the issue, (b) log with context, (c) re-raise specific
banned: code that catches exceptions and silently continues ("error laundering")
note: governance checklist M2 covers scan; this rule defines the fix patterns

## Memory and Scaling Guards

rule: scripts processing unbounded data MUST implement size guards or map-reduce
banned: unbounded string concatenation across file collections
pattern: track token count, break/batch when exceeding MAX_TOKENS threshold
note: governance checklist S2 covers review; this rule defines the implementation pattern

## Input Sanitization

rule: all user-provided strings used in file paths MUST use safe_slug() function
require: unicodedata.normalize + regex strip + resolve() + is_relative_to() check
banned: direct slug construction from user input without traversal protection
note: governance checklist H4 covers review; this rule defines the implementation pattern

## Portable Configuration

rule: every project MUST include .env.example with all required env vars documented
rule: include check_environment() in config.py that validates required vars at startup
banned: projects that require guessing which env vars are needed
banned: absolute paths in .env — use relative paths or $HOME-based expansion

## Logging

rule: use Python logging module, not print() for debugging or error output
banned: print() for error reporting in library/scaffold code (CLI user output is acceptable)

## Type Hints

rule: all public functions must have type hints for parameters and return values
check: missing type hints on public API is a review defect

## CLI Tool Design

rule: CLI tools MUST be AI-first — see CLAUDE.md "AI-First Development Guidelines" section
require: --help on all commands, plain text default output, --json flag, batch operations
require: auto-detection of context (project, user), actionable error messages
reference: pt command is the gold standard implementation

---
version: 2.0.0
established: 2026-01-07
updated: 2026-03-26 — trimmed from 296 to atomic format, removed governance-checklist duplicates
