# INC-002 — Evidence pipeline failures during Windows verification

**Status:** Resolved  
**Environment:** GitHub Actions, Windows Server 2025 hosted runner  
**Successful verification run:** [36561149955](https://github.com/AC0731/enterprise-it-support-lab/actions/runs/36561149955)

## Objective

Replace generated portfolio-style evidence images with screenshots derived from a real Windows execution of the support scripts and regression tests.

## Failures found

### 1. PowerShell parser error

The first Windows verification run failed before triage could execute.

**Observed error**

```text
Variable reference is not valid. ':' was not followed by a valid variable name character.
```

**Root cause**

The summary string used `$TargetHost:`, which PowerShell parsed as an invalid variable reference.

**Fix**

Changed the interpolation to `${TargetHost}:`.

---

### 2. Evidence renderer failed after the Windows checks passed

The next run successfully completed the real Windows triage and all regression tests, but the HTML renderer failed.

**Observed error**

```text
NameError: name 'margin' is not defined
```

**Root cause**

CSS braces were embedded directly inside a Python f-string and interpreted as Python expression delimiters.

**Fix**

Reworked the template so HTML content is escaped and inserted without f-string CSS-brace evaluation.

---

### 3. Native browser screenshot invocation did not create output

The following run completed the Windows triage, test suite, metadata generation, and HTML rendering. The browser command launched without producing the expected PNG.

**Root cause**

The native browser command-line capture was not sufficiently reliable in the hosted Windows environment.

**Fix**

Replaced the direct browser invocation with Playwright/Chromium and a dedicated capture helper.

## Verification

Run **36561149955** completed successfully end-to-end:

- 5/5 Python regression tests passed.
- Windows Server 2025 system inventory collected.
- Fixed-disk threshold checks passed.
- DNS resolution of `www.microsoft.com` passed.
- TCP/443 connectivity passed.
- `Dnscache` and `Spooler` services were running.
- Playwright captured both evidence PNGs.
- GitHub Actions committed raw evidence, metadata, HTML source, and screenshots back to the repository.

## Operational takeaway

The verification path intentionally preserves failed runs and fixes. The failure history shows why support automation should be validated on the target operating system instead of relying only on static review or cross-platform tests.
