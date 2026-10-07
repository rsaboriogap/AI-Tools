# Technical Specification: DateTime Columns Display Format in Blazor DataGridView

**Work Item:** 791579  
**Title:** [Blazor][MSI] DateTime columns display time by default - DataGridView  
**Status:** Committed, Priority 2, Business Value 4/4  
**Date:** 2026-07-16  
**Related:** PR #119948, Linked items: 791407, 791408, 790224, 791403

---

## 1. Objective

Enable Blazor DataGridView DateTime columns to display date in short format (date only, e.g., "7/16/2026") instead of the current long format (including time, e.g., "7/16/2026 2:45:00 PM"), achieving parity with the legacy Windows Forms control behavior and improving migration consistency for VB.NET applications.

---

## 2. Requirements

### Functional Requirements

**FR1: Date-Only Display**
- DateTime columns in Blazor DataGridView shall render date in short format by default
- Format shall match Windows Forms short date format: MM/dd/yyyy (US locale) or locale-specific equivalent
- Time component shall not be displayed unless explicitly configured otherwise

**FR2: Format Specification**
- Default format applied to DataGridView columns of type `DateTime`
- Format must be culture-aware: respect system or configurable locale settings
- Support for custom format strings per column (future extensibility)

**FR3: WinForms Parity**
- Blazor behavior must match Windows Forms DataGridView DateTime column rendering
- Legacy applications migrating to Blazor shall see identical date presentation

### Non-Functional Requirements

**NFR1: Backward Compatibility**
- Change must not break existing Blazor applications already in production
- Consider deprecation path if existing code relies on long format
- Migration guide required for affected applications

**NFR2: Performance**
- Date formatting shall not add measurable overhead to grid rendering
- No additional API calls or external dependencies for formatting

**NFR3: Testing**
- Unit tests: Formatting logic must be covered with >90% code coverage
- Integration tests: Playwright tests must verify visual rendering before/after
- Edge cases: null dates, DateTime.MinValue, dates across different locales

---

## 3. Solution Overview

### Approach

The solution modifies the DataGridView control hierarchy to apply culture-aware date formatting at the data binding level. Rather than formatting at display time in the Razor component, formatting logic is applied in the binding layer where data type information is available.

**Key Design Decisions:**

1. **Formatting Location:** `GridViewDataAdapter` (data binding layer) rather than Razor component
   - Rationale: Keeps formatting logic centralized, reusable, and testable without Razor dependencies
   - File: `src/Gap.Blazor.Components/DataAdapters/GridViewDataAdapter.cs`

2. **Format Default:** Short date format respecting culture
   - Rationale: Aligns with WinForms behavior; cultures handle locale-specific formatting automatically
   - CultureInfo.CurrentCulture will determine format (e.g., MM/dd/yyyy for en-US, dd/MM/yyyy for en-GB)

3. **Scope:** All DateTime columns in DataGridView unless explicitly overridden
   - Rationale: Comprehensive fix for consistency; future work can add per-column configuration

4. **Configuration Level:** Application-wide default with per-column override capability
   - Rationale: Simplicity first; advanced customization available as extension point

### Architecture

```
DataGridView Control (Gap.Blazor)
  ↓
GridViewDataAdapter (Gap.Blazor.Components)
  ├─ Detects DateTime columns
  ├─ Applies short date format
  └─ Returns formatted data to Razor component
    ↓
WMDataGridViewComponent.razor (rendering)
  └─ Displays formatted values via Telerik Grid
```

### Affected Components

| Component | File | Change |
|-----------|------|--------|
| **Grid Adapter** | `src/Gap.Blazor.Components/DataAdapters/GridViewDataAdapter.cs` | Add DateTime detection and format application logic |
| **DataGridView Control** | `src/Gap.Blazor/Controls/DataGridView.cs` | Add FormatDateTime property (optional, for future per-grid configuration) |
| **Data Binding** | `src/Gap.Blazor/Controls/DataBinding/Binding.cs` | Review for interaction with format logic |
| **Razor Component** | `src/Gap.Blazor.Components/Components/DataGridViewFlex/WMDataGridViewFlexComponent.razor` | Ensure compatibility; no changes expected if binding works correctly |
| **Test Infrastructure** | `test/Gap.Blazor.Components.Test/` | Add unit tests for formatter |
| **Integration Tests** | `test/Integration.Testing/IntegrationTest/playwright-component-integration-tests/` | Add Playwright test for visual verification |

---

## 4. Implementation Steps

### Phase 1: Analysis & Design (Estimated: 2 days)

**Step 1.1: Inspect Current Implementation**
- Read `src/Gap.Blazor.Components/DataAdapters/GridViewDataAdapter.cs` to understand current data binding flow
- Identify where DateTime values are currently processed
- Verify PR #119948 to see any partial implementation
- Document current behavior (if any formatting exists)

**Step 1.2: Review Data Binding Architecture**
- Study `src/Gap.Blazor/Controls/DataBinding/Binding.cs` and `BindingContext.cs`
- Understand how column metadata is tracked
- Identify where column type information is available

**Step 1.3: Examine Telerik Grid Integration**
- Review `src/Gap.Blazor.Components/Components/DataGridViewFlex/WMDataGridViewFlexComponent.razor` and `.razor.cs`
- Understand how data is passed to Telerik Grid for rendering
- Identify Telerik Grid API for column formatting (if available)

**Step 1.4: Define Formatting Strategy**
- Determine if formatting should happen before or after Telerik Grid receives data
- Document CultureInfo handling (invariant vs. CurrentCulture)
- Define format string to use (e.g., "d" for short date, or explicit "MM/dd/yyyy")

**Deliverable:** Architecture decision document with code locations and approach confirmed

---

### Phase 2: Core Implementation (Estimated: 3-4 days)

**Step 2.1: Create Formatting Logic in GridViewDataAdapter**
- Location: `src/Gap.Blazor.Components/DataAdapters/GridViewDataAdapter.cs`
- Add method: `FormatDateTimeValue(object value, CultureInfo culture) -> string`
- Logic:
  ```csharp
  if (value is DateTime dt)
  {
      return dt.ToString("d", culture ?? CultureInfo.CurrentCulture);
  }
  return value?.ToString();
  ```
- Handle null values gracefully (return empty string or configured placeholder)
- Support both nullable and non-nullable DateTime types

**Step 2.2: Integrate Formatting in Data Binding Pipeline**
- Modify `GridViewDataAdapter.GetCellValue()` or equivalent method to apply formatting
- Ensure formatting is applied before data reaches Telerik Grid
- Preserve original DateTime value for sorting/filtering if needed
- Consider adding a `FormattedValue` vs. `OriginalValue` pattern if sorting requires unformatted data

**Step 2.3: Add Configuration Property (Optional)**
- Add `DateTimeFormatString` property to `DataGridView` control if per-grid override is desired
- Default value: `"d"` (short date format)
- Store in `GridViewDataAdapter` for use during formatting
- Allow null to indicate "use default culture format"

**Step 2.4: Handle Edge Cases**
- DateTime.MinValue and DateTime.MaxValue: ensure readable output
- Null DateTime values: display empty or configured default
- Mixed types in column: validate column assumption before formatting
- Date-only vs. DateTime: both should show date only; don't filter out DateTime with time

**Deliverable:** Formatting logic implemented and integrated; code compiles without errors

---

### Phase 3: Unit Testing (Estimated: 2 days)

**Step 3.1: Create Test Class**
- Location: `test/Gap.Blazor.Components.Test/DataAdapters/GridViewDataAdapterFormattingTests.cs`
- Framework: MSTest 3.6.3 with Moq 4.20.72
- Ensure test project targets net9.0 and net10.0

**Step 3.2: Write Test Cases**
- **TC1: Normal DateTime formatting**
  - Input: DateTime(2026, 7, 16, 14, 30, 0)
  - Expected: "7/16/2026" (US locale) or locale-specific equivalent
  - Verify format matches short date format

- **TC2: Null DateTime handling**
  - Input: null
  - Expected: Empty string or configured placeholder
  - Ensure no exceptions thrown

- **TC3: DateTime.MinValue**
  - Input: DateTime.MinValue
  - Expected: Valid formatted output (e.g., "1/1/0001")
  - Document behavior

- **TC4: DateTime.MaxValue**
  - Input: DateTime.MaxValue
  - Expected: Valid formatted output (e.g., "12/31/9999")
  - Document behavior

- **TC5: Culture-aware formatting**
  - Input: DateTime(2026, 7, 16) with CultureInfo("en-GB")
  - Expected: "16/07/2026" (DD/MM/YYYY format)
  - Verify locale-specific format applied

- **TC6: Time component ignored**
  - Input: DateTime(2026, 7, 16, 14, 30, 45)
  - Expected: "7/16/2026" (time component not shown)
  - Confirm time portion is discarded

- **TC7: Non-DateTime values pass through**
  - Input: String, int, null, or other types
  - Expected: Converted to string without DateTime formatting
  - Verify fallback behavior

**Step 3.3: Test Adapter Integration**
- Mock DataGridView with DateTime column
- Call GridViewDataAdapter with test data
- Verify formatted output matches expectations
- Ensure no side effects on original data

**Step 3.4: Code Coverage Validation**
- Run tests with coverlet (configured in `CodeCoverage.runsettings`)
- Target >90% code coverage for formatting logic
- Document any untestable paths

**Deliverable:** All tests passing; >90% code coverage; test file saved to repo

---

### Phase 4: Integration Testing (Estimated: 2 days)

**Step 4.1: Create Playwright Test**
- Location: `test/Integration.Testing/IntegrationTest/playwright-component-integration-tests/tests/`
- File: `datagridview-datetime-format.spec.ts`
- Framework: Playwright 1.20.0+

**Step 4.2: Test Scenarios**
- **TS1: Default DateTime format rendering**
  - Launch app with sample DataGridView containing DateTime column
  - Verify grid displays dates in short format (no time visible)
  - Screenshot comparison: before (with time) vs. after (date only)

- **TS2: Date-only column type**
  - Test column explicitly typed as Date (if supported)
  - Verify rendering matches DateTime behavior

- **TS3: Null date cells**
  - Verify empty cells display correctly
  - Ensure no error messages in console

- **TS4: Grid sorting with formatted dates**
  - Click column header to sort by DateTime
  - Verify sort order is correct (sorting on original DateTime, not formatted string)
  - Document if sorting requires access to unformatted data

- **TS5: Grid filtering**
  - Test filtering on DateTime column
  - Verify filter works with unformatted DateTime values

- **TS6: Locale switching** (if application supports)
  - Change CultureInfo to different locale
  - Verify date format updates to locale-specific format
  - Example: en-US (7/16/2026) vs. en-GB (16/07/2026)

**Step 4.3: Visual Regression Testing**
- Capture screenshots of rendered grid with DateTime columns
- Compare against baseline (current behavior with time)
- Confirm time component is not visible in new version
- Document any visual changes

**Step 4.4: Error Handling Tests**
- Test grid with corrupted data (invalid DateTime)
- Verify graceful fallback behavior
- Check browser console for errors

**Deliverable:** All E2E tests passing; visual regression baseline established

---

### Phase 5: Verification Against WinForms (Estimated: 1 day)

**Step 5.1: Create Comparison Test**
- Use supplied WinForms example project (from ticket supporting evidence)
- Create identical data set in Blazor app
- Side-by-side comparison of output
- Document any differences

**Step 5.2: Validate Parity**
- Verify all DateTime columns display date only
- Confirm format matches WinForms short format
- Test with multiple date values (past, present, future)
- Test with null/empty dates

**Step 5.3: Document Migration Path**
- Create guide for developers migrating from WinForms to Blazor
- Explain format behavior and customization options
- Note any differences or caveats

**Deliverable:** Parity validation report; migration guide

---

### Phase 6: Regression Testing & Documentation (Estimated: 1-2 days)

**Step 6.1: Run Full Test Suite**
- Execute all unit tests: `dotnet test Gap.Blazor.Components.Test`
- Execute integration tests: `npm test` in playwright-component-integration-tests/
- Verify no regressions in other components
- Check code coverage metrics

**Step 6.2: Code Review Preparation**
- Ensure code follows project conventions (copyright headers, naming)
- Validate against security guidelines (file: `src/Gap.Blazor.Components/...`)
- Document any breaking changes
- Update PR #119948 with implementation details

**Step 6.3: Documentation Updates**
- Update README.md with DateTime formatting behavior
- Add code examples showing:
  - Default behavior (short date format)
  - Custom format per column (if implemented)
  - Culture-aware behavior
  - Testing examples
- Document any configuration options added

**Step 6.4: Acceptance Criteria Verification**
- [ ] AC1: Date columns do not display the time by default
  - Verification: Visual inspection + Playwright assertion
- [ ] AC2: Date columns display the specified format
  - Verification: Unit tests confirm format string applied
  - **Note:** "specified format" clarified as short date (CultureInfo-aware)
- [ ] AC3: Unit testing required
  - Verification: >90% coverage in formatting logic
- [ ] AC4: Integration testing required
  - Verification: Playwright E2E tests for visual rendering

**Deliverable:** All tests passing; documentation complete; PR ready for review

---

## 5. Testing Strategy

### Unit Testing

**Framework:** MSTest 3.6.3  
**Mocking:** Moq 4.20.72  
**Location:** `test/Gap.Blazor.Components.Test/DataAdapters/GridViewDataAdapterFormattingTests.cs`  
**Coverage Target:** >90% of formatting logic  

**Test Structure:**
```csharp
[TestClass]
public class GridViewDataAdapterFormattingTests
{
    [TestMethod]
    public void FormatDateTimeValue_WithValidDateTime_ReturnsShortDateFormat() { }
    
    [TestMethod]
    public void FormatDateTimeValue_WithNull_ReturnsEmptyString() { }
    
    [TestMethod]
    [DataRow("en-US", "7/16/2026")]
    [DataRow("en-GB", "16/07/2026")]
    public void FormatDateTimeValue_CultureAware_AppliesLocaleFormat(string culture, string expected) { }
    
    // Additional test methods...
}
```

**Coverage Tools:** coverlet.collector 6.0.2 (configured in CodeCoverage.runsettings)

### Integration Testing

**Framework:** Playwright 1.20.0+ (TypeScript)  
**Location:** `test/Integration.Testing/IntegrationTest/playwright-component-integration-tests/tests/datagridview-datetime-format.spec.ts`  
**Scope:**
- Visual rendering verification (date column displays date only)
- Locale/culture switching (if applicable)
- Grid interaction (sorting, filtering with formatted display)
- Error handling (null dates, invalid data)

**Test Execution:**
```bash
cd test/Integration.Testing/IntegrationTest/playwright-component-integration-tests/
npm test
# or for specific test file:
npx playwright test tests/datagridview-datetime-format.spec.ts
```

### Acceptance Criteria Checklist

| Criterion | Test Type | Verification Method |
|-----------|-----------|---------------------|
| AC1: Date columns do not display time by default | Integration | Playwright: Query grid cell, assert time string not present |
| AC2: Date columns display specified format | Unit | MSTest: Assert output equals short date format |
| AC3: Unit testing required | Coverage | coverlet: Assert >90% coverage |
| AC4: Integration testing required | Integration | Playwright E2E test suite passes |

---

## 6. Risks & Mitigation

### Risk 1: Breaking Change to Existing Applications

**Description:** Deployed Blazor applications currently expecting long DateTime format may break visually or in business logic.

**Severity:** High  
**Mitigation:**
- Add version note in release: "Breaking change: DateTime columns now display short format by default"
- Provide configuration option for per-grid format override (future work)
- Include migration guide in documentation
- Consider phased rollout with feature flag if critical

**Owner:** Release Engineering

---

### Risk 2: Ambiguous "Specified Format" in Acceptance Criteria

**Description:** AC2 references "specified format" without defining which format exactly. Current implementation assumes short date format (e.g., "d").

**Severity:** Medium  
**Mitigation:**
- This spec clarifies format as short date format respecting CultureInfo
- Confirm with stakeholders before implementation starts
- Document clarification in spec
- Add comment in code referencing this decision

**Owner:** Product Owner

---

### Risk 3: Sorting & Filtering Issues

**Description:** If formatting is applied to display values, sorting/filtering may work on formatted strings instead of original DateTime values.

**Severity:** Medium  
**Mitigation:**
- Keep original DateTime values in model; only format for display
- Verify Telerik Grid's `ValueField` vs. `TextField` behavior
- Test sorting/filtering with unformatted DateTime values
- Document if sorting limitation exists

**Owner:** Development

---

### Risk 4: Locale/Culture Handling Complexity

**Description:** Different deployment environments may have different default cultures, leading to inconsistent formatting across instances.

**Severity:** Low  
**Mitigation:**
- Use explicit CultureInfo.InvariantCulture or configurable culture
- Document culture assumption (defaults to CultureInfo.CurrentCulture)
- Add configuration point for culture override if needed
- Test across multiple locales

**Owner:** Development

---

### Risk 5: Performance with Large Datasets

**Description:** Formatting every DateTime cell in a large grid may add overhead.

**Severity:** Low  
**Mitigation:**
- Use efficient string formatting (built-in ToString method, not custom parsing)
- No external calls or database queries during formatting
- Benchmark grid with 1000+ rows of DateTime data
- Document any performance impact findings

**Owner:** QA/Performance

---

## 7. Open Questions

| Question | Status | Notes |
|----------|--------|-------|
| What exact format should be used for "specified format"? | **CLARIFIED** | Short date format ("d") respecting CultureInfo, matching WinForms behavior. Document in acceptance. |
| Should format be configurable per column? | **DEFERRED** | Not in initial scope; can be added as future enhancement if needed. |
| Should format be configurable per grid? | **DEFERRED** | Not in initial scope; can be added as future enhancement if needed. |
| How should different locales be handled? | **CLARIFIED** | Use CultureInfo.CurrentCulture; culture-aware formatting automatic. Document in code. |
| Are the 4 related items (791407, 791408, 790224, 791403) blockers? | **UNRESOLVED** | Clarify dependencies with product owner before starting work. |
| Does PR #119948 contain partial implementation? | **UNRESOLVED** | Inspect PR before implementation; may have existing code to build on. |
| What is the MSI product line context? | **UNRESOLVED** | Does this scope apply to all Blazor or only MSI? Clarify with stakeholder. |
| Should there be a rollback capability for deployed systems? | **DEFERRED** | Not in initial scope; consider for future release strategy. |

---

## 8. Appendix

### A. File Reference Summary

| File | Purpose | Changes |
|------|---------|---------|
| `src/Gap.Blazor.Components/DataAdapters/GridViewDataAdapter.cs` | Data adapter for binding data to grid | ADD: DateTime detection and formatting logic |
| `src/Gap.Blazor/Controls/DataGridView.cs` | DataGridView control abstraction | MODIFY: Optional configuration property for format override |
| `src/Gap.Blazor/Controls/DataBinding/Binding.cs` | Data binding logic | REVIEW: Ensure compatibility with formatting layer |
| `src/Gap.Blazor.Components/Components/DataGridViewFlex/WMDataGridViewFlexComponent.razor` | Razor component rendering grid | NO CHANGES: Should work with formatted data from adapter |
| `src/Gap.Blazor.Components/Components/DataGridViewFlex/WMDataGridViewFlexComponent.razor.cs` | Code-behind for grid component | REVIEW: Verify data flow to Telerik Grid |
| `test/Gap.Blazor.Components.Test/DataAdapters/GridViewDataAdapterFormattingTests.cs` | Unit tests | CREATE: New test class with formatting test cases |
| `test/Integration.Testing/IntegrationTest/playwright-component-integration-tests/tests/datagridview-datetime-format.spec.ts` | Integration tests | CREATE: New Playwright E2E test file |
| `CodeCoverage.runsettings` | Coverage configuration | NO CHANGES: Existing configuration used |

### B. Acceptance Criteria Detail

**AC1: Date columns do not display the time by default**
- Implementation: GridViewDataAdapter applies short date format
- Verification: Playwright assertion checks grid cell does not contain time (no "PM" or "AM" or "HH:MM:SS")
- Status: Will be satisfied

**AC2: Date columns display the specified format**
- Implementation: Short date format string ("d") applied to all DateTime columns
- Verification: Unit test confirms output format matches expected pattern
- **Note:** "Specified format" clarified as short date (e.g., "7/16/2026")
- Status: Will be satisfied with clarification

**AC3: Unit testing required**
- Implementation: MSTest test class with >90% code coverage
- Verification: coverlet metrics show coverage > 90%
- Test file: `GridViewDataAdapterFormattingTests.cs`
- Status: Will be satisfied

**AC4: Integration testing required**
- Implementation: Playwright E2E tests for visual rendering
- Verification: All tests pass; screenshots demonstrate date-only display
- Test file: `datagridview-datetime-format.spec.ts`
- Status: Will be satisfied

### C. Related Work Items

The following items are linked to this ticket and may have dependencies:

- **791407:** [Unknown - requires clarification]
- **791408:** [Unknown - requires clarification]
- **790224:** [Unknown - requires clarification]
- **791403:** [Unknown - requires clarification]

**Action:** Confirm dependencies and priority with product owner before sprint start.

### D. Technology Stack Reference

From technical-solution-analysis.md:

| Component | Technology | Version | Relevance |
|-----------|-----------|---------|-----------|
| Framework | ASP.NET Core / Blazor Web | 9.0, 10.0 | Runtime environment |
| Components | Telerik UI for Blazor | 12.0.0 | Grid rendering |
| Test Framework | MSTest | 3.6.3 | Unit testing (used) |
| E2E Testing | Playwright | 1.20.0+ | Integration testing (used) |
| Mocking | Moq | 4.20.72 | Test mocking (used) |
| Coverage | coverlet | 6.0.2 | Coverage metrics (used) |

### E. Culture-Aware Formatting Examples

```csharp
// Input: DateTime(2026, 7, 16, 14, 30, 45)

// en-US Culture
dt.ToString("d", CultureInfo.GetCultureInfo("en-US"))
// Output: 7/16/2026

// en-GB Culture
dt.ToString("d", CultureInfo.GetCultureInfo("en-GB"))
// Output: 16/07/2026

// de-DE Culture
dt.ToString("d", CultureInfo.GetCultureInfo("de-DE"))
// Output: 16.07.2026

// ja-JP Culture
dt.ToString("d", CultureInfo.GetCultureInfo("ja-JP"))
// Output: 2026/07/16
```

---

## 9. Sign-Off

**Specification Status:** Ready for Implementation  
**Approved By:** [To be filled during review]  
**Implementation Owner:** [To be assigned]  
**QA Owner:** [To be assigned]

---

**Document History:**
- **2026-07-16:** Initial spec created based on work item 791579 and technical solution analysis
