# SceneValidator

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

A sophisticated tool for validating scene structure and continuity in media projects, leveraging the Gemini API for intelligent content analysis.

## Overview

SceneValidator analyzes media scene data to ensure proper structure, consistency, and continuity. It helps content creators identify potential issues before production, saving time and resources.

## Features

- **Scene Structure Validation**: Checks scene metadata against project templates
- **Continuity Checking**: Identifies continuity issues across scenes
- **Character and Prop Consistency**: Ensures characters and props remain consistent
- **Environment and Lighting Coherence**: Validates environmental elements
- **Timeline Sequence Validation**: Verifies proper scene ordering
- **Automated Issue Reporting**: Generates comprehensive validation reports
- **Gemini API Integration**: Utilizes AI for content analysis

## Documentation

Detailed documentation is available at:
[SceneValidator Documentation](https://docs.google.com/document/d/1CkWjM0SwncPw3bQnI6s13eK3pG90_6z9iqdDs-3rBHY/edit)

## Installation

### Prerequisites

- Python 3.9+
- Google Cloud SDK
- Gemini API access

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/dxaginfo/alistair-media-automation-toolkit.git
cd alistair-media-automation-toolkit/tools/scene_validator

# Install dependencies
pip install -r requirements.txt

# Configure
cp config/config.sample.json config/config.json
# Edit config.json with your API keys and settings
```

### Docker Installation

```bash
# Build the Docker image
docker build -t scene-validator .

# Run the container
docker run -v $(pwd)/data:/app/data -v $(pwd)/config:/app/config scene-validator
```

## Usage

### Command Line

```bash
# Validate a single scene
python src/validator.py path/to/scene.json output_report.html

# Run in continuous monitoring mode
python src/trigger.py
```

### API

Start the API server:

```bash
python src/api.py
```

The API will be available at http://localhost:5000

#### Endpoints

- `POST /validate/scene` - Validate a single scene
- `POST /validate/project` - Validate multiple scenes
- `GET /config` - Get current configuration
- `GET /validation-rules` - Get current validation rules

### Web UI

The web UI provides a user-friendly interface for validation:

1. Navigate to `web_ui/index.html` in your browser
2. Upload scene files for validation
3. View validation results and reports

## Integration with Other Tools

SceneValidator is designed to integrate with other tools in the Media Automation Toolkit:

- **StoryboardGen**: Validates storyboards against scenes
- **ContinuityTracker**: Shares continuity data
- **TimelineAssembler**: Validates scene ordering
- **EnvironmentTagger**: Uses environment metadata for validation

## Configuration

Configuration is stored in `config/config.json`. Key options include:

- API keys for Gemini and Google Cloud
- Validation rules and tolerance levels
- Storage settings for reports
- Trigger settings for automatic validation

Validation rules are defined in `config/validation_rules.json`.

## Development

### Project Structure

```
scene_validator/
├── config/                 # Configuration files
│   ├── config.sample.json  # Sample configuration
│   └── validation_rules.json  # Validation rules
├── data/                   # Data directory for scenes
├── reports/                # Generated reports
├── src/                    # Source code
│   ├── api.py              # REST API
│   ├── gemini_integration.py  # Gemini API integration
│   ├── trigger.py          # Automatic triggers
│   └── validator.py        # Core validation logic
├── web_ui/                 # Web user interface
│   ├── index.html          # Main UI page
│   └── api.js              # JavaScript API client
├── Dockerfile              # Docker configuration
└── requirements.txt        # Python dependencies
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_validator.py
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Released under the MIT License. See `LICENSE` file for details.

## Authors

- Media Automation Toolkit Team

## Acknowledgments

- Gemini API for content analysis capabilities
- Google Cloud for infrastructure support