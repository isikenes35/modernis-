---
name: i18n-translator
description: >-
  Acts as an Expert Localization Engineer pipeline tool. Takes raw structured files (JSON, YAML, TS, JS, JSX) or file paths, and translates the nested strings/UI copy into the target language.
---

# i18n-translator

## Overview
Acts as an Expert Localization Engineer pipeline tool. Takes raw structured files (JSON, YAML, TS, JS, JSX) or file paths, and translates the nested strings/UI copy into the target language. Strictly outputs ONLY valid raw code/data ready to overwrite files, with zero conversational filler. Preserves all keys, HTML/JSX tags, and interpolation variables. Resolves ambiguity contextually based on file names, parent keys, and a corporate web application domain.

## Dependencies
None.

## Quick Start
Provide a file path or a code snippet and ask the agent to translate it to a target language.
Example: `Translate src/data/ru/products.json to Spanish.`

## Workflow
### 1. Read Input
- If provided a file path, read the file using `view_file`. If a code snippet is provided, parse it directly.

### 2. Translate Contextually
- Translate UI strings and content into the target language.
- Resolve ambiguity by analyzing file name, parent object keys, and sibling keys (e.g., `Lead` in a `sales` object means potential customer).
- Target domain: professional, corporate web application terminology.
- NEVER pause to ask questions. NEVER leave strings untranslated. Make the best contextual guess.

### 3. Preserve Structure (CRITICAL)
- Preserve all string interpolation variables (e.g., `{{name}}`, `{count}`, `%s`, `$1`).
- Preserve all HTML/JSX tags exactly (e.g., `<strong>`, `<span className="...">`).
- In JSON/JS structures, do NOT modify object keys; only translate the values.

### 4. Output Raw Code
- Output ONLY the raw translated file content or snippet. 
- Ensure the output is perfectly valid syntax ready to replace the original.
- ZERO conversational text. Do not explain the output. Do not include greetings.
