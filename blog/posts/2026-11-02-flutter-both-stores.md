---
title: What shipping a Flutter app to both stores taught me
date: 2026-11-02
summary: Lessons from taking a Flutter matchmaking app to Google Play and the App Store. Mostly about process, not code.
cover: post-2-flutter-release.jpg
tags: Flutter, Release, Firebase
draft: true
---
QaboolHai, a matchmaking app, went live on Google Play and the App Store. I built features like matching, real-time chat with GetX, video calls with Agora, profile photo verification and the payment gateway, and I also looked after releases. These are the lessons that were not about Flutter code at all.

**Set up build flavors on day one.** Separate flavors for development, staging and production, each with its own Firebase project, keep test notifications and test data out of real users' hands. Adding flavors late is painful.

**Treat crash reporting as a feature.** Firebase Crashlytics told me what broke on devices I did not own. Upload debug symbols for every release or the stack traces are useless.

**Notifications need a plan.** Permissions, channels on Android, and what happens when the app is closed all behave differently on each platform. Test the full path on real devices, not only in the simulator.

**Real-time features fail in the background.** Chat and video calls look easy in a demo. The hard part is network changes, the app being backgrounded and reconnecting cleanly. [Add one concrete bug you hit and how you fixed it.]

**Store review is part of the schedule.** App Store review times and rejection reasons, especially for apps with user profiles and payments, can add days. Submit early and keep release notes and screenshots ready.

**Version numbers are a contract.** Keep one clear rule for build numbers and versions so QA, the stores and Crashlytics all agree on what is running.

The common thread: most release problems are process problems, and a small amount of setup early saves a lot of stress at launch.
