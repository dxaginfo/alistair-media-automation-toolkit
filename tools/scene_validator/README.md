# SceneValidator

A tool that validates scene structure and continuity in media projects.

## Overview

SceneValidator analyzes scene metadata, content, and relationships to identify continuity issues, structural problems, and inconsistencies. It uses the Gemini API for content analysis and Google Cloud for processing.

## Features

- Scene structure validation against project templates
- Continuity checking across scenes
- Character and prop consistency validation
- Environment and lighting coherence analysis
- Timeline sequence validation
- Automated issue reporting

## Requirements

- Python 3.9+
- Google Cloud SDK
- Gemini API access
- Media metadata in compatible format (JSON, XML)

## Triggers

- New scene upload
- Scene metadata changes
- Manual validation request
- Pre-render validation check

## Outputs

- Validation report (JSON, HTML)
- Error and warning list
- Suggested fixes
- Visual representation of issues

## Integration Points

- **StoryboardGen**: Validates storyboards against scenes
- **ContinuityTracker**: Shares continuity data
- **TimelineAssembler**: Validates scene ordering
- **EnvironmentTagger**: Uses environment metadata for validation