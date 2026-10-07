# Quick Start: VBU Hackathon Plugin Installation & Usage

Get the spec-driven development plugin running in 5 minutes.

## Prerequisites

- **Claude Code** installed (CLI or IDE extension)
  - [Download Claude Code CLI](https://claude.ai/download)
  - Or use VSCode/JetBrains extension
- **Azure DevOps** access with a valid organization
- **Personal Access Token (PAT)** from Azure DevOps

## Step 1: Get Your Azure DevOps PAT

1. Go to **Azure DevOps** → your organization
2. Click **User settings** (top-right avatar) → **Personal access tokens**
3. Click **New Token**
4. Name it: `claude-code-plugin`
5. Scopes: Select **Work Items (Read)**
6. Expiration: 1 year (or your preference)
7. Click **Create** and **copy the token** immediately (you won't see it again)

## Step 2: Configure the Plugin

1. **Navigate to the plugin directory:**
   ```bash
   cd vbu-hackathon-project
   ```

2. **Create `.env` file with your PAT:**
   ```bash
   cp .env.example .env
   ```
   (If `.env.example` doesn't exist, create `.env` manually)

3. **Edit `.env` and add your PAT:**
   ```
   AZURE_DEVOPS_EXT_PAT=<paste-your-pat-here>
   AZDO_PAT=<paste-your-pat-here>
   ```

4. **Update `.mcp.json` with your Azure DevOps organization:**
   
   Open `.mcp.json` and replace `"wearegap"` with your organization name:
   ```json
   {
     "mcpServers": {
       "azure-devops": {
         "type": "stdio",
         "command": "npx",
         "args": [
           "-y",
           "@azure-devops/mcp",
           "YOUR-ORG-NAME",
           "-a",
           "env"
         ],
         "env": {
           "AZURE_DEVOPS_EXT_PAT": "${AZURE_DEVOPS_EXT_PAT}"
         }
       }
     }
   }
   ```

5. **Configure `.claude/settings.json` (optional but recommended):**
   
   Add your default Azure DevOps project to avoid specifying it each time:
   ```json
   {
     "azureDevOpsTicketQuality": {
       "defaultProject": "your-project-name"
     }
   }
   ```
   
   This lets you invoke skills with just the work item ID: `"Generate spec for ticket 12345"` instead of repeating the project name each time.

## Step 3: Install the Plugin in Claude Code

### Option A: Claude Code CLI

```bash
claude plugin install /path/to/vbu-hackathon-project
```

Then reload Claude Code.

### Option B: VSCode Extension

1. Open **Claude Code extension** in VSCode
2. Go to **Plugins** tab (or **Extensions** → find Claude Code)
3. Click **Add Plugin** → **Local Plugin**
4. Select the `vbu-hackathon-project` folder
5. Reload VSCode

### Option C: JetBrains IDE (IntelliJ, WebStorm, etc.)

1. Open **Claude Code plugin** settings
2. Go to **Plugins** section
3. Click **+** → **Add Local Plugin**
4. Navigate to `vbu-hackathon-project` folder
5. Restart IDE

## Step 4: Verify Installation

1. Open Claude Code in your IDE or terminal
2. Type `/` to see available commands
3. You should see the plugin's skills listed:
   - `/azure-devops-ticket-quality`
   - `/technical-solution-analysis`
   - `/solution-analysis-gate`
   - `/technical-spec-generator`

If you don't see them, check:
- `.env` has your PAT token
- `.mcp.json` has your org name
- Plugin installation completed without errors (check IDE logs)

## Step 5: Test the Plugin

### Test 1: Quick Token Validation

```bash
npx @azure-devops/mcp <YOUR-ORG-NAME> -a env
```

Should authenticate without errors. If it fails, your PAT or org name is wrong.

### Test 2: Analyze a Real Ticket

In Claude Code, invoke:

```
/azure-devops-ticket-quality
```

Then provide a work item ID:
```
Ticket ID: 788506
```

The skill will pull the ticket from Azure DevOps and score its quality.

### Test 3: Full Pipeline

```
/solution-analysis-gate
```

Provide a ticket ID. This will:
1. Score the ticket quality
2. Analyze your codebase (if no analysis exists)
3. Generate a technical spec

Output: `documents/technical-spec.md`

## Troubleshooting

### "Unknown command" or skills not showing

**Problem:** Skills don't appear in `/` autocomplete.

**Fix:**
- Verify plugin installed: `claude plugin list`
- Check `.env` exists and has your PAT
- Restart IDE/Claude Code
- Check IDE logs for errors

### "Authentication failed" when running a skill

**Problem:** MCP server can't authenticate to Azure DevOps.

**Fix:**
- Verify PAT in `.env` is correct (copy fresh from Azure DevOps)
- Verify org name in `.mcp.json` matches your Azure DevOps org
- Check PAT hasn't expired
- Test manually: `npx @azure-devops/mcp <YOUR-ORG> -a env`

### "Work item not found"

**Problem:** Skill can't find the ticket you referenced.

**Fix:**
- Verify work item ID exists in your org
- Check ID format (should be a number, e.g., `788506`)
- Verify your PAT has **Read** permission on Work Items

### "documents/ directory not found"

**Problem:** Skills can't write output files.

**Fix:**
- The `documents/` directory is created automatically — you don't need to create it
- Check that you have **write permission** in the project folder
- Try running a skill again; it will create the directory

### "Module '@azure-devops/mcp' not found"

**Problem:** NPM can't find the Azure DevOps MCP package.

**Fix:**
- Ensure Node.js and npm are installed globally
- Delete `node_modules/` (if present) and `.npm-cache/`
- Run: `npm install -g @azure-devops/mcp`

## Next Steps

### Run Your First Spec

1. Find a work item ID in your Azure DevOps backlog
2. In Claude Code, run:
   ```
   /solution-analysis-gate
   ```
3. Provide the work item ID
4. Wait ~2-3 minutes for analysis
5. Check `documents/technical-spec.md` in your project

### Learn the Skills

- **`azure-devops-ticket-quality`** — Evaluates ticket clarity, acceptance criteria, and completeness. Use before moving a ticket into a sprint.
- **`technical-solution-analysis`** — Understands your codebase. Run once per project, update when architecture changes.
- **`technical-spec-generator`** — Turns a ticket + codebase context into an implementation plan.

### Tips for Best Results

1. **Provide complete ticket info** — Include title, description, acceptance criteria, and any comments in the ticket.
2. **Run analysis once** — The `technical-solution-analysis` is cached. You don't need to regenerate it every time.
3. **Use for planning, not just execution** — Quality scores highlight weak tickets *before* development starts, saving time mid-sprint.

## Get Help

- **Check the detailed skill documentation:** Each skill folder has `SKILL.md` with full workflow details
- **See an example spec:** (Coming soon — `documents/example-technical-spec.md`)
- **Report issues:** Open an issue in the repo or contact the plugin maintainers

---

**Ready?** Run `/solution-analysis-gate` with a work item ID and watch the plugin generate your first spec.
