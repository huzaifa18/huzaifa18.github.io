---
title: Moving an Android app from Java to Kotlin without freezing feature work
date: 2026-10-26
summary: How I helped move a live Java and MVP app to Kotlin, Jetpack Compose and MVVM while features kept shipping.
cover: post-1-java-to-kotlin.jpg
tags: Android, Kotlin, Compose
draft: true
---
When I joined the Arccos Golf Android app, it was written in Java and built around an MVP architecture. The goal was to move to Kotlin, introduce Jetpack Compose and end up on MVVM. The catch: the app was live and features kept shipping. Here is the approach that worked for me.

**Don't rewrite, convert along the edges.** Kotlin and Java live happily in one module, so there is no reason to stop the world. I converted files when I was already touching them for a feature or a bug fix. Every pull request left the code a little more Kotlin than before.

**Start with the leaves.** Data classes, utilities and models convert almost mechanically and give you null safety straight away. Screens and presenters come later, once the team is comfortable reading Kotlin.

**Change the architecture one screen at a time.** I did not convert MVP to MVVM in one go. New screens were written as ViewModels exposing state, and old presenters stayed until their screen needed real work. [Add: how many screens moved, or how long it took.]

**Let Compose in through new UI.** Compose can sit inside an existing View-based screen, so I used it for new components first and left stable XML screens alone. That kept risk low and let the team learn at a realistic pace.

**Use Coroutines instead of callbacks as you go.** Replacing callback chains with suspend functions removed a lot of nesting, and Retrofit supports them directly.

**What I would do again:** small pull requests, one rule per change (convert, or change behaviour, never both), and agreeing on style early. **What I would do differently:** [Add one honest lesson, for example about tests, build times or code review.]

If you are facing the same migration, the short version is: go gradually, convert what you touch, and treat architecture as a per-screen decision, not a big bang.
