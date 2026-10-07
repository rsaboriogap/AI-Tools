# Configuration Guide

## Default Azure DevOps Project

The `azure-devops-ticket-quality` skill supports configuring a default Azure DevOps project in `.claude/settings.json` to streamline ticket analysis.

### Setup

Add the following to your `.claude/settings.json`:

```json
{
  "azureDevOpsTicketQuality": {
    "defaultProject": "your-project-name"
  }
}
```

Replace `your-project-name` with your Azure DevOps project name.

### Usage

Once configured, you can analyze tickets with just the ticket ID:

```
/azure-devops-ticket-quality
Review ticket 12345
```

The skill will automatically use the default project when fetching the ticket via Azure DevOps MCP tools.

### Override

To use a different project in a specific request, simply mention it:

```
/azure-devops-ticket-quality
Review ticket 12345 in project MyOtherProject
```

User-specified projects take precedence over the configured default.

### Technical Details

- Configuration is loaded from `.claude/settings.json` via `config_loader.py`
- The skill passes the default project to all Azure DevOps MCP tool calls
- If no project is specified and no default is configured, the skill will prompt for the project name
