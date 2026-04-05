---
name: software-development-best-practices
description: |
  Comprehensive software development knowledge foundation covering clean code
  principles, design patterns, testing strategies, version control workflows,
  and deployment practices. Use when: (1) Writing new code or refactoring
  existing code, (2) Setting up a new project structure, (3) Debugging
  software issues that may relate to code quality or architecture, (4)
  Implementing or improving CI/CD pipelines, (5) Conducting code reviews,
  (6) Making architectural decisions. Covers SOLID principles, common design
  patterns with applicability guidance, testing strategy (unit, integration,
  end-to-end), branching strategies, commit conventions, and modern deployment
  workflows including containerization and infrastructure as code.
author: Community
version: 1.0.0
date: 2026-01-15
tags: [software-engineering, best-practices, foundations, architecture, testing]
---

# Software Development Best Practices

## Problem

Software development involves numerous decisions about code structure, testing,
deployment, and maintenance. Without a systematic approach, teams and individual
developers accumulate technical debt, introduce inconsistent patterns, and spend
disproportionate time debugging issues that stem from poor foundational practices.
This skill provides a comprehensive reference for the core principles and practices
that underpin reliable, maintainable software.

## Context / Trigger Conditions

This skill applies broadly to software development tasks. It is particularly
relevant when:

- Starting a new project or feature and deciding on structure and conventions
- Refactoring existing code that has become difficult to maintain
- Setting up development infrastructure (version control, CI/CD, testing)
- Conducting code reviews and evaluating code quality
- Debugging issues that may stem from architectural or design problems
- Onboarding new developers who need to understand team conventions

## Solution

### 1. Code Quality Principles

#### SOLID Principles

- **Single Responsibility Principle (SRP):** A module, class, or function should
  have one reason to change. If a class handles both data access and email
  notification, split it into two classes. The test: can you describe what the
  class does without using "and"?

- **Open/Closed Principle (OCP):** Software entities should be open for extension
  but closed for modification. Use interfaces, abstract classes, and composition
  to add behavior without changing existing code. When you find yourself editing
  a working class to add a new feature, consider whether the feature could be
  added through extension instead.

- **Liskov Substitution Principle (LSP):** Subtypes must be substitutable for
  their base types. If a `Square` class inherits from `Rectangle` but breaks
  when `setWidth()` is called independently of `setHeight()`, the inheritance
  hierarchy is wrong. Prefer composition over inheritance when the "is-a"
  relationship does not hold strictly.

- **Interface Segregation Principle (ISP):** Clients should not be forced to
  depend on interfaces they do not use. Fat interfaces that expose methods
  irrelevant to some clients should be split into focused interfaces. A
  `Printer` interface with `print()`, `scan()`, and `fax()` should be three
  interfaces for clients that only need one capability.

- **Dependency Inversion Principle (DIP):** High-level modules should not depend
  on low-level modules. Both should depend on abstractions. This enables testing
  with mocks and swapping implementations without modifying business logic.

#### Additional Principles

- **DRY (Don't Repeat Yourself):** Every piece of knowledge should have a single,
  authoritative representation. Duplication is not just about code -- it includes
  duplicated logic, configuration, and documentation. When the same rule appears
  in three places, a change requires updating all three. Consolidate into one.

- **KISS (Keep It Simple):** Simplicity is a feature, not a sacrifice. Prefer
  straightforward solutions over clever ones. A simple solution is easier to
  understand, debug, and modify. Add complexity only when there is a measurable
  benefit.

- **YAGNI (You Aren't Gonna Need It):** Do not build functionality until it is
  needed. Speculative generality adds complexity without providing value. Build
  for today's requirements with a design that can accommodate tomorrow's, but do
  not implement tomorrow's features today.

### 2. Design Patterns

Design patterns provide tested solutions to recurring problems. Use them
judiciously -- applying a pattern where a simpler solution suffices introduces
unnecessary complexity.

| Pattern | When to Use | When to Avoid |
|---------|-------------|---------------|
| **Strategy** | Multiple algorithms for the same task; behavior selected at runtime | Only one algorithm exists and is unlikely to change |
| **Observer** | One-to-many dependency; state changes must notify multiple listeners | Tight coupling between subject and observer is acceptable |
| **Factory Method** | Creation logic is complex or varies by subclass | Object creation is straightforward with a constructor |
| **Repository** | Data access layer needs abstraction from business logic | Simple CRUD with no testing requirements |
| **Adapter** | Integrating with an interface that does not match your system's expectations | You control both sides of the interface |
| **Decorator** | Adding behavior to objects without modifying their class | Deep decorator chains become hard to debug |

#### Pattern Selection Guidance

1. Identify the problem you are trying to solve.
2. Check if a pattern addresses that specific problem.
3. Evaluate whether the pattern's complexity is justified by the problem's scope.
4. Apply the pattern minimally -- do not over-engineer the implementation.
5. Document why the pattern was chosen, not just what it does.

### 3. Testing Strategy

#### The Testing Pyramid

```
        /\
       /  \        E2E Tests (few, slow, expensive)
      /____\       - Critical user journeys only
     /      \      - Run in CI, not locally during development
    / Integration \
   /______________\  Integration Tests (moderate number)
  /                \  - Module boundaries, API contracts, database queries
 /   Unit Tests     \ - Mock external dependencies
/____________________\ Unit Tests (many, fast, cheap)
                        - Business logic, edge cases, error handling
                        - Run on every save during development
```

#### Writing Effective Tests

- **Test behavior, not implementation.** Tests that assert on internal state
  break when the implementation changes, even if the behavior is correct.
- **One assertion per concept.** A test should verify one logical outcome.
  Multiple assertions are acceptable if they collectively verify one behavior.
- **Arrange-Act-Assert pattern.** Structure every test in three phases: set up
  the preconditions, execute the action, verify the result.
- **Test edge cases explicitly.** Null values, empty collections, boundary
  values, concurrent access, and error conditions deserve dedicated tests.
- **Keep tests independent.** No test should depend on the side effects of
  another test. Each test sets up its own state and cleans up after itself.

#### Test Naming Convention

Use descriptive names that read as sentences:
- `test_user_creation_with_valid_data_succeeds()`
- `test_user_creation_with_duplicate_email_returns_conflict()`
- `test_user_creation_with_null_name_returns_validation_error()`

### 4. Version Control

#### Branching Strategy

Use a simple, consistent branching model:

- **main:** Production-ready code. Never commit directly.
- **feature/[ticket]-[description]:** New features or enhancements.
- **fix/[ticket]-[description]:** Bug fixes.
- **release/[version]:** Release preparation (if needed for complex releases).

#### Commit Conventions

Write commits as if the reader is a future developer trying to understand why
a change was made, not just what changed.

Format:
```
type(scope): imperative description

[Optional body: explain WHY the change was made]

[Optional footer: references, breaking changes]
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`

Good examples:
- `feat(auth): add JWT token refresh endpoint`
- `fix(data): handle null values in aggregation pipeline`
- `refactor(api): extract response formatting into middleware`

Bad examples:
- `update stuff`
- `fix bug`
- `wip`

#### Code Review Practices

- Review for correctness, clarity, and consistency -- not style (automate style).
- Ask questions rather than making demands: "What happens if `data` is null?"
  rather than "Add a null check."
- Approve only when you understand the change and are confident it is correct.
- Review promptly. Blocked PRs slow the entire team.

### 5. CI/CD and Deployment

#### Pipeline Design

A well-designed CI/CD pipeline provides fast feedback and reliable deployments:

1. **Lint and format** (seconds): Catch style issues and syntax errors early.
2. **Unit tests** (minutes): Verify business logic in isolation.
3. **Integration tests** (minutes): Verify module boundaries and external interfaces.
4. **Build** (minutes): Compile, package, and create deployable artifacts.
5. **Deploy to staging** (minutes): Deploy to a staging environment for validation.
6. **E2E tests** (minutes): Verify critical user journeys in a production-like environment.
7. **Deploy to production** (minutes): Promote the validated artifact to production.

#### Deployment Strategies

- **Blue/Green:** Maintain two identical environments. Deploy to the inactive one,
  switch traffic, verify, then decommission the old environment. Zero downtime.
- **Canary:** Deploy to a small percentage of traffic first. Monitor for errors.
  Gradually increase traffic if metrics are healthy.
- **Rolling:** Gradually replace instances of the old version with the new version.
  Simple but has a window where both versions are serving traffic.

#### Infrastructure as Code

Define all infrastructure in version-controlled configuration files (Terraform,
CloudFormation, Docker Compose, Kubernetes manifests). Manual infrastructure
changes are unreviewable, unreproducible, and unreliable.

### 6. Error Handling and Logging

#### Error Handling Principles

- **Fail fast.** Detect and report errors as close to their source as possible.
- **Use specific exception types.** Catch and throw exceptions that describe the
  actual problem, not generic `Exception` or `Error` classes.
- **Never swallow exceptions silently.** An empty catch block hides problems.
  At minimum, log the exception.
- **Provide context in error messages.** "Connection refused" is less useful than
  "Connection refused when connecting to database at db.example.com:5432. Verify
  the database is running and the connection string is correct."

#### Logging Best Practices

- **Log at appropriate levels:** DEBUG (development details), INFO (significant
  events), WARN (potential issues), ERROR (failures requiring attention).
- **Include correlation IDs.** Every request should have a unique ID that appears
  in all log entries related to that request. This enables tracing a request
  across multiple services.
- **Log structured data.** JSON-formatted logs are machine-parseable and enable
  powerful querying in log aggregation systems.
- **Do not log sensitive data.** Passwords, tokens, personal information, and
  credit card numbers must never appear in logs.

## Verification

After applying these practices, verify:

- [ ] Code passes linting and formatting checks without warnings
- [ ] All tests pass (unit, integration, and E2E as applicable)
- [ ] Code review approved by at least one other developer
- [ ] CI pipeline is green on the target branch
- [ ] New code has corresponding tests covering the happy path and edge cases
- [ ] Error handling covers the failure modes identified during design
- [ ] Logging provides sufficient context to diagnose issues in production

## Notes

This is a foundation skill intended to be comprehensive and serve as the base
layer for more specific domain skills. It should be reviewed and updated as
practices evolve.

- See also: `api-integration-workflow` for API-specific patterns
- See also: `python-output-buffering-background-scripts` for a specific debugging skill
- See also: `debugging-systematic-approach` for structured debugging methodology

## References

- Martin Fowler, "Refactoring: Improving the Design of Existing Code"
- Robert C. Martin, "Clean Code: A Handbook of Agile Software Craftsmanship"
- Kent Beck, "Test-Driven Development: By Example"
- The Twelve-Factor App methodology: https://12factor.net/
