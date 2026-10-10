# Regulated and Safety-Critical Profiles

Use this reference only when the project explicitly has safety, certification, regulated coding, or assurance requirements. Generic OO work should not inherit these constraints automatically.

## Table of contents

- [Activation gate](#activation-gate)
- [Core C++ assurance sources](#core-cpp-assurance-sources)
- [Automotive](#automotive)
- [Avionics](#avionics)
- [General functional safety](#general-functional-safety)
- [Deviation and evidence discipline](#deviation-and-evidence-discipline)
- [OO-specific safety concerns](#oo-specific-safety-concerns)

## Activation gate

Before applying a regulated profile, establish:

1. governing domain and authority/customer;
2. exact standard and edition;
3. required assurance/safety level (for example ASIL, DAL, SIL) if applicable;
4. project tailoring and approved deviations;
5. permitted C++ language/version/subset;
6. qualified/approved toolchain and analysis requirements;
7. required traceability and evidence artifacts.

If any are unknown, mark them as open. Do not guess compliance obligations.

## Core C++ assurance sources

### ISO/IEC 14882:2024

Normative published C++ language standard corresponding to C++23. It defines the language; it is not a safety coding profile.

### C++ Core Guidelines

Living community guidance led by Bjarne Stroustrup and Herb Sutter. Useful for interfaces, resource management, lifetime, concurrency, and modern C++ practices. Because it is living guidance, cite a date/revision when used as controlled project evidence.

### SEI CERT C++ Coding Standard

Security/reliability-oriented C++ coding rules. Use where project policy adopts it or as a risk-oriented review source. Do not assume it is mandatory unless contract/project governance says so.

## Automotive

### MISRA C++:2023

Current MISRA C++ edition at this skill's source snapshot. It targets C++17, not C++23. Therefore:

- do not claim a C++23 codebase is MISRA C++:2023 compliant without an explicit project strategy/tool interpretation;
- apply the exact rule classification and deviation process from the authorized MISRA text/toolchain;
- keep the skill's C++23 examples educational unless the project profile permits the feature used.

Do not reproduce MISRA rule text from licensed publications; cite rule IDs/titles only when authorized context provides them.

### AUTOSAR C++14 Guidelines

The AUTOSAR C++14 guideline document Release 18-10 marks itself obsolete. Treat it as a legacy contractual profile or historical crosswalk, not the preferred baseline for a new project unless the contract requires it.

### ISO 26262:2018

Use Part 6 for software product development, together with the project's safety plan and supporting-process obligations. OO design must preserve requirements traceability, safety mechanisms, freedom-from-interference assumptions where relevant, verification evidence, configuration/change control, and project-specific method/tool qualification obligations.

Do not infer ASIL or required methods from code alone.

## Avionics

### DO-178C

Core airborne software assurance document. It is objective/evidence oriented rather than an OO style guide.

### DO-332

Use DO-332 when object-oriented technology or related techniques are used under DO-178C/DO-278A. OO concerns can include inheritance, polymorphism, dynamic binding, type consistency, local type verification, and verification of derived behavior depending on the project's use of OO features.

### DO-330

Use when software tool qualification is required. Do not equate ordinary compiler/static-analyzer use with qualified-tool credit; qualification depends on tool use, objectives, and certification context.

The RTCA software document family also includes DO-331 for model-based development and DO-333 for formal methods; activate them only when those techniques are in scope.

## General functional safety

### IEC 61508:2010 Edition 2

As of the skill's source snapshot (2026-09-20), Edition 2 remains the valid published base functional-safety series while Edition 3 is under development. For software, Part 3 is the principal software-focused part; verify the exact current edition/status when performing real compliance work.

A future revision can change obligations. Never hard-code a claim that Edition 2 remains current indefinitely.

## Deviation and evidence discipline

In regulated code, separate:

- applicable rule/objective;
- implementation/design evidence;
- verification method;
- result;
- deviation/waiver rationale;
- approval authority;
- configuration baseline/version.

Do not treat a static-analysis pass as full compliance. Some objectives require requirements, architecture, test, process, independence, configuration, or certification evidence outside source code.

## OO-specific safety concerns

Escalate review when the design uses:

- deep or multiple inheritance;
- runtime polymorphism/dynamic binding in safety-critical control paths;
- exceptions where project policy restricts them;
- dynamic memory allocation after initialization;
- shared ownership and cyclic graphs;
- RTTI or type inspection;
- concurrency/reentrancy across mutable objects;
- complex template metaprogramming that weakens analyzability;
- callbacks with unclear lifetime/ownership;
- hidden global/singleton state.

The remedy is profile-dependent. Do not ban these universally; determine what the governing standard, project plan, toolchain, and safety argument permit.
