---
title: Face recognition on low-end Android phones with TensorFlow Lite
date: 2026-11-09
summary: What mattered when an attendance app had to recognise people on-device, on cheap phones.
cover: post-3-face-recognition.jpg
tags: Android, TensorFlow Lite, On-device AI
draft: true
---
For an attendance app called Parousia, people had to be recognised by the phone, with no one touching a device. It had to run on-device, and on cheap phones. Here is what mattered.

**Pick a small model.** Large models are accurate but slow on low-end hardware. A compact face-embedding model running on TensorFlow Lite gave results fast enough for a queue of people. [Add which model you used, if you want to name it.]

**Quantize.** Converting a model to 8-bit makes it smaller and faster, usually with a small accuracy cost. Measure it on your own data before you accept the trade.

**Recognise by comparing embeddings.** The model turns a face into a vector. Enrolment stores a vector per person, and recognition finds the closest stored vector and checks it against a threshold. The threshold is a product decision: too loose and you mark the wrong person, too strict and people get rejected.

**The camera pipeline is half the work.** Cropping, rotating and resizing frames correctly, and doing it off the main thread, matters as much as the model. Most early bugs I saw were in preprocessing, not in the neural network.

**Plan for the real world.** Lighting, glasses and angles change results. I added QR code and Wi-Fi check-in as alternatives so the system still works when the camera does not. [Add one thing you learned from real use.]

**Be honest about limits.** A basic recogniser can be fooled by a photo. If the stakes are higher than attendance, you need liveness checks.

This work is one reason I went on to study AI. Running models on the device, where the user is, is the part of machine learning I enjoy most.
