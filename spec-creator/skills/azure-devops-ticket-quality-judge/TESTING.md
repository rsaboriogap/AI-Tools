# Testing: Verify Results Are Saved

After running the `azure-devops-ticket-quality-judge` skill, verify that results are automatically saved to `documents/`.

## Quick Test

1. **Run the skill:**
   ```
   /azure-devops-ticket-quality-judge
   [provide evaluation input]
   ```

2. **Check that files were created:**
   ```bash
   ls -la documents/evaluation-*.json
   ls -la documents/evaluation-*.md
   ```

3. **View the markdown report:**
   ```bash
   cat documents/evaluation-*.md
   ```

## Expected Output

When the skill completes, you should see output like:
```
============================================================
Evaluation saved: eval-001
Result: ✅ PASSED | Score: 87/100
============================================================
✓ JSON evaluation:  documents/evaluation-eval-001.json
✓ Markdown report:  documents/evaluation-eval-001.md
============================================================
```

## File Structure

After running, you should have:

```
documents/
├── evaluation-eval-001.json         ← Full JSON evaluation data
└── evaluation-eval-001.md           ← Human-readable markdown report
```

## Troubleshooting

### Files not created?

1. **Check permissions:** Ensure `documents/` directory is writable
   ```bash
   ls -ld documents/
   ```

2. **Check evaluation_saver.py:** Verify it exists and is executable
   ```bash
   ls -la skills/azure-devops-ticket-quality-judge/evaluation_saver.py
   ```

3. **Check Python:** Verify Python 3 is available
   ```bash
   python3 --version
   ```

4. **Run saver manually:** Test the script directly
   ```bash
   echo '{"evaluation_id":"test-001","passed":true,"overall_score":80}' > test.json
   python3 skills/azure-devops-ticket-quality-judge/evaluation_saver.py test.json
   ```

### Skill doesn't call saver?

The skill instructions explicitly require saving results. If files aren't being created, it means:
- Claude isn't executing the save command
- There's a path issue
- The evaluation_saver.py script is failing

Check the skill output for error messages from the save attempt.

## What Gets Saved

### JSON File (`evaluation-{id}.json`)
- Complete evaluation structure
- All criterion scores
- Deterministic check results
- Failures and improvements
- Ready for programmatic processing

### Markdown File (`evaluation-{id}.md`)
- Human-readable report
- Status and score
- Criteria table
- Improvements ranked by priority
- Executive summary
- Perfect for sharing/documentation
