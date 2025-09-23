# msgraph Plugin for dify

## Project Overview

This project is a Microsoft Graph API-based email sending plugin designed specifically for the Dify platform. The plugin provides functionality to send emails via Microsoft Graph services, supporting both HTML and plain text formats, with built-in Markdown to HTML conversion capabilities.

### Key Features
- ✅ Send emails (supports multiple recipients)
- ✅ Support for HTML and plain text formats
- ✅ Automatic Markdown to HTML conversion
- 📋 Planned feature: Send attachments from S3 storage
- 📋 Planned feature: Send attachments from local files

## Prerequisites

### Environment Requirements
- Python 3.12
- Dify platform environment
- Microsoft Azure account with app registration

### Required Configuration
Before running, configure the following Microsoft Graph-related environment variables or credentials:
- `MICROSOFT_GRAPH_USERNAME`: Microsoft account username
- `MICROSOFT_GRAPH_TENANTID`: Azure tenant ID
- `MICROSOFT_GRAPH_CLIENTID`: Application client ID
- `MICROSOFT_GRAPH_CLIENTSECRET`: Application client secret
- `MICROSOFT_GRAPH_SCOPE_1`: Graph API permission scope (default: `https://graph.microsoft.com/.default`)

## Getting Started

### Running on Dify Platform
1. Package the plugin as a `.difypkg` file
2. Import the plugin in the Dify platform
3. Configure the required Microsoft Graph credentials
4. Use the email sending tool in your workflow

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Either through .env file or directly setting environment variables

# Run tests
python tools/sendMail.py
```

## Build Instructions

### Packaging the Plugin
Use the provided Makefile for packaging:

```bash
# Default packaging command
make

# Or manually execute
dify plugin package . -o msgraph.difypkg
```

### Build Requirements
- Dify CLI tools
- Python 3.12 environment
- All required files in the project root directory

## Project Structure

```
plugin/msgraph/
├── manifest.yaml              # Plugin manifest file
├── icon.svg                   # Plugin icon
├── makefile                   # Build script
├── README.md                  # Project documentation
├── PRIVACY.md                 # Privacy policy
├── tools/
│   ├── sendMail.yaml          # Tool definition file
│   ├── sendMail.py            # Email sending implementation
│   ├── msgraphApi.py          # Graph API wrapper
│   └── markdown_utils.py      # Markdown utilities
├── lambda-app.py.txt          # AWS Lambda sample code
└── surgery_product.sql        # Database schema (example)
```

## Tool Parameters

### sendMail Tool Parameters
- **recipients** (required): Email recipients, separate multiple recipients with commas
- **subject** (required): Email subject
- **content_type** (optional): Content format (html/text), defaults to text
- **content** (required): Email content (supports Markdown, automatically converted to HTML)

## License Information

This project does not specify a clear license. Please contact the author for usage permissions before use.

## Additional Information

### Author
- **Author**: cn00
- **Email**: cool-navy@outlook.com

### Project Repository
- **GitHub**: https://github.com/cn00/dify-plugin-msgraph.git

### Version Information
- **Current Version**: 1.0.0
- **Metadata Version**: 0.0.3
- **Supported Architectures**: amd64, arm64

### Important Notes
1. Ensure proper application permissions are configured in Azure AD
2. Email sending functionality requires a valid Microsoft 365 subscription
3. Plugin requires adequate memory configuration (recommended 256MB+)

### Changelog
- v1.0.0: Initial version with basic email sending functionality
- Planned: Add attachment sending capabilities