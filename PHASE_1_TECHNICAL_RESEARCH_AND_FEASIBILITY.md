# Ray-Ban Meta AI Data Project

## Phase 1 technical research and feasibility assessment

**Status:** Research and due diligence only  
**Prepared:** 31 July 2026, Australia/Brisbane  
**SDK baseline reviewed:** Meta Wearables Device Access Toolkit (DAT) 0.8.0, released 25 June 2026  
**Official repository snapshots reviewed:** iOS commit `2b5695d16a710f3d2d7341f88570b86d01723d50`; Android commit `4e56e1864a5e78194bababc3a68775c4196cbed0`  
**No production code, application scaffold, or irreversible architecture decision was created.**

All linked web sources were accessed on **31 July 2026** unless a different access date is stated. Hardware specifications are labelled as consumer specifications where applicable; they must not be read as developer-API capabilities.

---

## Executive assessment

### Bottom line

The technical capture concept is feasible **as a controlled prototype**, but the proposed commercial model is **not presently cleared** for use with Meta's public developer platform.

The most important finding is not a camera limitation. It is a platform-terms limitation. Meta's current Wearables Developer Terms define **Technology Data** broadly to include information or content obtained from the Technology and data derived from it. The permitted-use section is limited to operating and improving the end-user-requested integration, and the prohibited-use section expressly bars selling or licensing Technology Data. Contributor consent permits some sharing, but the text does not create an exception to the sale/licensing prohibition. The terms even state that a privacy policy cannot make a prohibited sale permissible. On an ordinary reading, packaging SDK-captured demonstrations as paid training data is likely outside the public licence. This is a strong textual inference, not legal advice. It requires written clarification from Meta and advice from qualified counsel before product investment. [Meta Wearables Developer Terms](https://wearables.developer.meta.com/terms)

The technical findings are more encouraging but narrower than the consumer marketing:

- DAT 0.8.0 is a **Developer Preview** mobile SDK. The app runs on the paired iPhone or Android phone, not as an installable third-party application on the glasses. Camera frames are delivered live to the phone. The public evidence does not establish a supported API for importing the glasses' stored consumer recordings later. [iOS repository](https://github.com/facebook/meta-wearables-dat-ios) [Android repository](https://github.com/facebook/meta-wearables-dat-android) [Meta staff answer on app execution and stored media](https://github.com/facebook/meta-wearables-dat-android/discussions/20)
- The developer camera stream is portrait **720 × 1280 maximum**, with selectable 2, 7, 15, 24, or 30 fps and adaptive degradation. That is materially below the consumer products' advertised 3K modes. [iOS integration guide](https://wearables.developer.meta.com/docs/develop/dat/build-integration-ios/) [Android integration guide](https://wearables.developer.meta.com/docs/develop/dat/build-integration-android/)
- Glasses microphone capture uses Bluetooth HFP at **8 kHz mono**. Meta says beamforming prioritises the wearer and reduces ambient speech and sound. This may help narrated instructions, but it is a poor substitute for full-fidelity environmental audio or the consumer five-microphone immersive recording. [Microphones and speakers](https://wearables.developer.meta.com/docs/develop/dat/microphones-and-speakers/)
- A/V can be muxed on the phone, but the public documentation does not promise a shared clock or bounded drift between DAT video timestamps and platform HFP audio. Reliable synchronisation remains an experiment, not a confirmed SDK feature.
- DAT exposes session/link state, stream state, thermal level, and critical battery/thermal/power errors. It does not document a developer-accessible battery percentage. Hinge position itself is explicitly not exposed. [Session lifecycle](https://wearables.developer.meta.com/docs/develop/dat/lifecycle-events/) [iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- All current DAT release channels are invite-only. iOS App Store submission is explicitly unsupported and expected to be rejected because of the SDK's current `ExternalAccessory` use, MFi, and privacy-manifest requirements. A general public Android path is not established by the reviewed documentation. [Release channels](https://wearables.developer.meta.com/docs/develop/dat/set-up-release-channels/) [iOS integration guide](https://wearables.developer.meta.com/docs/develop/dat/build-integration-ios/)

### Feasibility classification

| Question | Assessment | Why |
|---|---|---|
| Can supported glasses stream first-person video to a mobile app today? | **Yes, verified** | DAT 0.8.0 exposes live camera streaming and still capture. |
| Can wearer narration be captured? | **Yes, verified but low fidelity** | HFP provides beamformed 8 kHz mono input through mobile OS audio APIs. |
| Can video and narration be put in one file? | **Technically possible; reliability unknown** | iOS and Android have media muxing APIs, but cross-route clock alignment and drift are not guaranteed. |
| Can it run for useful work-task durations? | **Unknown** | Consumer battery claims do not measure continuous SDK streaming; thermal, compression, interruption, and dropout behavior need real-device tests. |
| Is it direct robot-action data? | **No** | RGB video lacks robot joint state, action commands, force, tactile feedback, calibrated object pose, and embodiment correspondence. |
| Can the public Meta SDK legally support a paid dataset-licensing business? | **Likely no under the current text; must be cleared** | The public terms prohibit selling or licensing Technology Data and derived data. |
| Can a public consumer app be distributed now? | **No supported path established** | Current channels are invite-only; iOS App Store publishing is explicitly unsupported. |
| Is the broader enrichment thesis viable with other capture systems? | **Plausible, unvalidated** | The market and research show demand for human demonstration data, but the space is crowded and buyer lift must be demonstrated. |

### Cofounder challenge

The project should not define its moat as “Ray-Ban footage for robots.” That proposition is exposed to three failures at once:

1. Meta may not permit the data to be licensed.
2. The SDK stream is much weaker than the consumer camera marketing suggests.
3. First-person RGB video alone is not robot control supervision.

The defensible opportunity, if one exists, is a **hardware-agnostic, rights-cleared demonstration-data system** that can prove downstream value through task design, provenance, synchronised supplementary signals, error/recovery capture, human review, and buyer-specific evaluation. Ray-Ban or Oakley glasses may be one capture endpoint only if Meta authorises the intended use.

---

## Evidence conventions

- **Verified fact** means supported by a current primary source or official repository inspected for this report.
- **Inference** means a reasoned consequence of verified facts but not a vendor guarantee.
- **Unknown** means the reviewed public material did not establish the answer.
- **Conflict** means current official sources disagree or describe different product modes.
- Company website quantities in the competitive section are **self-reported marketing claims**, not independently verified metrics.
- This is technical and commercial due diligence, not legal advice.

---

## 1. Supported hardware

### 1.1 Compatibility evidence

The DAT 0.8.0 version-dependency table names Ray-Ban Meta, Meta Glasses, Meta Ray-Ban Display, Oakley Meta HSTN, and Oakley Meta Vanguard, all at glasses firmware V125 with Meta AI app V275. The 0.8.0 repositories add mock-device models for Ray-Ban Meta, Ray-Ban Meta Optics, Oakley Meta HSTN, Oakley Meta Vanguard, and Meta Glasses. [Version dependencies](https://wearables.developer.meta.com/docs/develop/dat/version-dependencies/) [iOS 0.8.0 changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md) [Android 0.8.0 changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md)

There is a documentation inconsistency: the current Setup page lists Ray-Ban Meta Gen 1/Gen 2, Ray-Ban Meta Optics, and Meta Ray-Ban Display but omits Oakley, while the version-dependency table explicitly includes both Oakley families. The dependency table and SDK changelogs are more specific and newer evidence for Oakley support, but each intended SKU should still be verified with real hardware and current firmware before procurement. [DAT Setup](https://wearables.developer.meta.com/docs/develop/dat/getting-started-toolkit/)

### 1.2 Hardware comparison

The following camera and battery figures describe **consumer hardware**, not DAT stream output.

| Family | Consumer hardware facts | Durability / battery marketing | Capture relevance | Important caveat |
|---|---|---|---|---|
| **Ray-Ban Meta Gen 1** | 12 MP ultrawide camera, two open-ear speakers, five-microphone array; originally advertised for 1080p clips | IPX4; up to about 4 hours moderate use and about 3 hours continuous audio/voice use | Lowest-cost smoke-test device; common form factor | Shorter battery life. Consumer stored-media behavior is not a DAT API. [Meta launch](https://about.fb.com/news/2023/09/new-ray-ban-meta-smart-glasses/) [Ray-Ban FAQ](https://www.ray-ban.com/italy/c/domande-frequenti-ray-ban-meta-smart-glasses) |
| **Ray-Ban Meta Gen 2** | 12 MP camera, two open-ear speakers, five-microphone array, 32 GB consumer storage, Wi-Fi 6E, Bluetooth 5.3 | IPX4; up to 8 hours typical use; 50% charge in 20 minutes | Best baseline for indoor/everyday capture due to availability and comfort | Meta newsroom says “3K ... up to 60 fps,” while a current AU product page lists up to 2203 × 2938 at 30 fps. These are consumer-mode claims and conflict by mode/page. DAT remains capped at 720 × 1280. [Meta Gen 2 announcement](https://about.fb.com/news/2025/09/ray-ban-meta-gen-2-better-battery-life-video-capture/) [Ray-Ban AU product](https://www.ray-ban.com/australia/electronics/RW4012ray-ban%20%7C%20meta%20wayfarer%20-%20gen%202-black/8056262721391) |
| **Ray-Ban Meta Blayzer/Scriber Optics Gen 2** | Prescription-optimised frame families with overextension hinges, interchangeable nose pads, and optician-adjustable temple tips | Marketed for all-day prescription wear | Potentially better fit stability and contributor comfort | The launch page does not provide a complete capture-electronics specification. Treat parity with Gen 2 as unverified until a specific SKU page and DAT session are tested. [Meta Optics announcement](https://about.fb.com/news/2026/03/meta-ai-glasses-built-for-prescriptions/) |
| **Oakley Meta HSTN** | 12 MP camera, two open-ear speakers, five microphones, 32 GB consumer storage, Wi-Fi 6E, Bluetooth 5.3; consumer 3K recording | IPX4; up to 8 hours typical, 19 hours standby, 50% in 20 minutes | Sport styling and secure fit may help active collection | Electronics are broadly similar to Gen 2; no higher DAT stream resolution is documented. [Meta HSTN announcement](https://about.fb.com/news/2025/06/introducing-oakley-meta-glasses-a-new-category-of-performance-ai-glasses/) [Oakley product](https://www.oakley.com/en-au/l/oakley-meta) |
| **Oakley Meta Vanguard** | Centred 12 MP camera with 122-degree wide angle; two stronger open-ear speakers; five-microphone array optimised for wind | IP67; up to 9 hours typical or 6 hours continuous music; case adds up to 36 hours | Best candidate for wet, dusty, windy, or high-motion field tests; centred view may improve symmetry | A 122-degree field at only 720 stream pixels may reduce effective pixels on small tools. Consumer slow-motion, hyperlapse, stabilisation, Garmin, and autocapture are not established DAT APIs. [Meta Vanguard announcement](https://about.fb.com/news/2025/09/oakley-meta-vanguard-performance-ai-glasses-sports/) [Oakley product](https://www.oakley.com/en-au/l/oakley-meta) |
| **Meta Ray-Ban Display** | 12 MP camera plus an in-lens colour display; display content is supported by DAT 0.7+ | About 6 hours mixed-use marketing; separate Neural Band | Could provide in-view task prompts or confirmation in a future research workflow | Adds cost, weight, UI complexity, and possible behavioral bias. No Neural Band/EMG capture API was found in DAT 0.8.0. It does not solve depth or action-label gaps. [Meta Display announcement](https://about.fb.com/news/2025/09/meta-ray-ban-display-ai-glasses-emg-wristband/) [DAT changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md) |

### 1.3 Hardware conclusions

- **Recommended controlled prototype device:** Ray-Ban Meta Gen 2 for ordinary indoor tasks. It is the least specialised current baseline.
- **Second comparison device:** Oakley Meta Vanguard only if the target tasks are outdoor, dusty, wet, or high-motion, or if camera centring is a hypothesis worth testing.
- **Do not procure based on 3K marketing.** The current SDK output is the gating camera specification.
- **Consumer storage is not capture resilience for DAT.** A 32 GB glasses storage specification does not mean the developer app can record there or recover footage after a link loss.
- **Battery claims are not continuous-stream benchmarks.** “Typical use” mixes idle time and consumer operations. The project needs measured minutes per charge under DAT video + HFP audio, not catalogue hours.
- The outward-facing capture LED is a useful notice signal, but it is not informed consent and the reviewed SDK does not document developer control over it. [Oakley capture LED FAQ](https://www.oakley.com/en-au/l/oakley-meta)

---

## 2. Meta developer ecosystem

### 2.1 Toolkit and platform shape

DAT is a mobile SDK for iOS and Android. Its current public modules cover core registration/device/session functions, camera streaming and photo capture, display rendering on supported display glasses, and mock devices. Meta's current integration overview states that users start a session from the phone app and interact through the glasses. Only one device session can run on a device at a time. [Integration overview](https://wearables.developer.meta.com/docs/develop/dat/build-overview/)

**Verified:** Meta's public iOS and Android repositories are at 0.8.0 and describe the programme as Developer Preview. Their changelogs show significant API changes across every release from 0.1.0 in October 2025 to 0.8.0 in June 2026. This is high SDK churn, not a stable production dependency. [iOS repository](https://github.com/facebook/meta-wearables-dat-ios) [Android repository](https://github.com/facebook/meta-wearables-dat-android)

### 2.2 Registration, authentication, and permissions

The current flow is:

1. Create or use a Meta account and Wearables Developer Center organisation/project.
2. Pair supported glasses in the Meta AI mobile app and update to the required app/firmware versions.
3. Enable Developer Mode by tapping the Meta AI app version five times and switching the revealed toggle on.
4. Launch registration from the developer app. Registration deep-links to Meta AI and returns through the app's callback scheme.
5. Request camera permission separately. The user chooses **Allow once**, **Allow always**, or **Don't allow** in Meta AI.
6. Request mobile microphone/Bluetooth permissions through iOS or Android for HFP audio.
7. Start a device session, then its camera stream. [Setup](https://wearables.developer.meta.com/docs/develop/dat/getting-started-toolkit/) [Permissions and registration](https://wearables.developer.meta.com/docs/develop/dat/permissions-requests/)

Important constraints:

- In Developer Mode, app attestation is bypassed and placeholder application credentials may be used. Production/test-channel builds use project identifiers and client tokens from Wearables Developer Center.
- Only one third-party app can remain registered at a time in Developer Mode; registering another automatically unregisters the previous one.
- Users may link multiple glasses. The documentation says camera permission is managed per device but a permission check may return granted when any connected device is granted; the application does not get a simple permission-to-specific-device mapping.
- Users can revoke permissions or unregister the integration from Meta AI at any time.
- A firmware update may hide or disable Developer Mode, so it should be a first diagnostic check after updates. [Permissions and registration](https://wearables.developer.meta.com/docs/develop/dat/permissions-requests/) [Repository debugging guidance](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/debugging)

### 2.3 Mock and simulated devices

Mock Device Kit can simulate registration, permissions, device power/don/doff/fold state, camera streaming, still capture, and capacitive touch gestures. It accepts a phone-camera feed or an H.265 video file; the iOS sample can transcode input automatically while the Android sample requires compatible input. It supports deterministic XCTest/XCUITest or Android instrumentation testing and a local test server for iOS UI automation. [Mock Device Kit](https://wearables.developer.meta.com/docs/develop/dat/mock-device-kit/) [iOS mock testing](https://wearables.developer.meta.com/docs/develop/dat/testing-mdk-ios/) [Android mock testing](https://wearables.developer.meta.com/docs/develop/dat/testing-mdk-android/)

**Limitation:** Mock Device Kit validates application logic, not real RF bandwidth, compression artifacts, HFP route stability, battery drain, thermal behavior, physical camera placement, motion blur, or wearer comfort. Hardware testing cannot be deferred.

### 2.4 Testing and release channels

All current DAT release channels are invite-only. Testers must have Meta accounts, receive and accept email invitations, and can leave a channel; developers can revoke access. Removing a tester from a channel does not automatically unregister an already connected app. Channel and tester limits are configured per project and must be checked in Developer Center. [Release channels](https://wearables.developer.meta.com/docs/develop/dat/set-up-release-channels/)

**Public distribution restrictions:**

- iOS App Store publication is explicitly unsupported today and the official guide warns that the current SDK will be rejected.
- The reviewed Android documentation explains invite-only channels but does not establish a generally available public release path.
- Meta's terms require Integration Review before an integration can be generally released, and approval is discretionary. [iOS integration guide](https://wearables.developer.meta.com/docs/develop/dat/build-integration-ios/) [Meta Wearables Developer Terms](https://wearables.developer.meta.com/terms)

Therefore, a broad contributor marketplace cannot be a Phase 2 assumption.

### 2.5 Operational telemetry collected by Meta

DAT telemetry is enabled by default. Meta documents collection including app/package identity, SDK version, phone model/OS, glasses identifier/type/firmware, registration and attestation events, permission status, session transitions, stream configuration and duration, error data, crash grouping, and mock-device events. Apps can opt out through an iOS `Info.plist` or Android manifest setting. [DAT telemetry](https://wearables.developer.meta.com/docs/develop/dat/telemetry/)

This creates a privacy and vendor-dependency consideration even if video itself is processed locally. The project's privacy disclosures must describe Meta's SDK role and verify the actual opt-out behavior chosen for a prototype.

---

## 3. Available APIs and capabilities

### 3.1 Capability matrix

| Capability | Current evidence | Assessment |
|---|---|---|
| Live first-person camera | Portrait streams at low 360 × 640, medium 504 × 896, or high 720 × 1280; requested fps 2/7/15/24/30 | **Verified**. Adaptive bandwidth management may reduce resolution and then fps. [iOS guide](https://wearables.developer.meta.com/docs/develop/dat/build-integration-ios/) |
| Compressed video | iOS supports HEVC `hvc1`; Android exposes compressed HEVC streaming | **Verified**. iOS compressed streaming can continue in background; raw streaming pauses. [iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md) [Android changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md) |
| Raw video frames | Raw frames are available for application processing | **Verified**, but expensive for phone CPU, memory, and storage and unsuitable for background on iOS. |
| Photo capture | A still can be requested while a camera stream is active | **Verified**. This is not documented as access to the full consumer media library. |
| Glasses microphone | Mobile OS HFP route, 8 kHz mono, beamformed for wearer voice | **Verified**. Exact per-microphone channels and consumer spatial recording are not exposed. [Audio guide](https://wearables.developer.meta.com/docs/develop/dat/microphones-and-speakers/) |
| Glasses speaker | A2DP output at 44.1/48 kHz stereo; HFP output falls to 8 kHz mono while mic is active | **Verified**. A2DP and HFP are mutually exclusive modes. |
| Display output | Text, images, buttons/icons, layouts, and MP4 playback on Meta Ray-Ban Display | **Verified** since 0.7.0, but not essential to capture. |
| Device/link/session state | Device availability/link and compatibility; session started/paused/stopped; stream states | **Verified**. Session transition reason is not exposed. |
| Thermal state | `ThermalLevel` through live device state; thermal critical/emergency errors | **Verified**. |
| Battery/power | Critical battery, peak-power shutdown errors; install fails below 10% battery | **Partial**. No public battery-percentage API was found. [Known issues](https://wearables.developer.meta.com/docs/develop/dat/knownissues/) |
| Connectivity state | Link availability plus session/stream failure and pause states | **Partial**. No public RF signal strength or bandwidth metric was found. |
| Wi-Fi transport | iOS 0.8.0 changelog and guide add local-network/Wi-Fi transport for high-bandwidth features | **Verified on iOS; ambiguous across platforms**. The same camera guide still describes Bluetooth Classic bandwidth constraints, and Android does not document equivalent camera Wi-Fi setup. Test actual transport. |
| Hinge/wear state | Hinge affects connectivity and mock devices can simulate it | **Not directly exposed**. Official lifecycle docs explicitly say hinge position is not exposed. |

### 3.2 Error and lifecycle behavior

Applications must treat the device as interruptible:

- A tap, system feature, another app, removal of the glasses, closing the hinges, Bluetooth loss, permission revocation, battery/thermal protection, or Meta AI disconnection can pause or stop the session.
- During `PAUSED`, streams stop delivering data. The app must wait rather than forcing a restart.
- Closing the hinges stops the session; reopening restores availability but does not restart it. A new user-visible session is required.
- Transition reasons are not exposed, so diagnostics must record observed state, timestamps, platform errors, and local context without inventing a cause. [Session lifecycle](https://wearables.developer.meta.com/docs/develop/dat/lifecycle-events/)

Current known issues include intermittent DAT app installation, silent transfer failure with Wi-Fi off, and an Android crash when taking multiple captures in quick succession on streams running longer than a minute. [Known issues](https://wearables.developer.meta.com/docs/develop/dat/knownissues/)

### 3.3 Local, glasses-edge, and cloud processing

**Local phone processing — possible today:**

- Decode raw or HEVC frames, record/mux media, run lightweight quality checks, encrypt local segments, and queue upload.
- Run phone-capable transcription or perception models where latency, battery, and model size permit.
- Use the phone's clock and storage to create manifests, but retain the original device presentation timing.

**On-glasses custom processing — not established:**

- The reviewed DAT public surface does not provide a general custom-model runtime or file system on the glasses.
- Meta staff have stated that third-party applications do not install on the glasses OS and DAT media is delivered to the phone in real time. [Official repository discussion](https://github.com/facebook/meta-wearables-dat-android/discussions/20)
- Consumer Meta AI, Garmin integrations, display features, and consumer recording modes must not be treated as developer inference APIs.

**Cloud processing — application controlled:**

- The phone can upload captured artifacts to a cloud service selected by the developer.
- DAT does not supply a training-data cloud pipeline.
- Uploading creates additional security, privacy, cross-border, service-provider-contract, deletion, and Meta terms obligations.

### 3.4 Capabilities not found in the public DAT 0.8.0 surface

The following should be treated as **not exposed unless Meta documents otherwise in writing**:

- depth maps, stereo camera feeds, point clouds, or scene meshes;
- camera intrinsics/extrinsics and a calibrated head/camera pose;
- native DAT access to glasses IMU, accelerometer, or gyroscope data;
- eye gaze, pupil tracking, head/hand pose, hand skeletons, or object pose;
- force, torque, tactile pressure, contact state, grip aperture, or human joint angles;
- raw individual microphone channels or the consumer spatial-audio recording;
- Neural Band/EMG data;
- Garmin, heart-rate, speed, or other consumer sport telemetry;
- a general battery percentage, RF signal strength, or hinge angle;
- an API to invoke 3K/60 fps, slow motion, hyperlapse, consumer stabilisation, autocapture, or stored consumer recording;
- supported post-hoc import of media recorded to the glasses' consumer storage;
- control that disables the outward capture indicator;
- a custom on-glasses model/runtime or direct access to the consumer Meta AI model.

There is an official-document ambiguity worth recording: the generated full-document index mentions “IMU sensors,” but the actual native DAT module/API material reviewed exposes no such sensor stream. The only concrete IMU API found in current Wearables documentation is the separate Web Apps path for Meta Ray-Ban Display, which has no camera or microphone access. This report therefore classifies native camera+IMU capture as unavailable, not confirmed.

---

## 4. Real-device development workflow

### 4.1 How Codex can work with the official SDK

Once Phase 2 is explicitly approved, Codex can work from four official sources:

1. Pin the official iOS or Android repository to a reviewed DAT release rather than copying stale snippets.
2. Use the official sample application as the smallest real-device reference.
3. Install the repository's official local Codex plugin (`mwdat-ios` or `mwdat-android`) so code changes follow Meta's current SDK conventions.
4. Connect the public [Wearables documentation MCP endpoint](https://mcp.developer.meta.com/wearables) and verify exact API symbols before each SDK change. [iOS repository AI guidance](https://github.com/facebook/meta-wearables-dat-ios#ai-assisted-development) [Android repository AI guidance](https://github.com/facebook/meta-wearables-dat-android#ai-assisted-development)

The SDK is moving quickly. A Phase 2 rule should require Codex to record the SDK version, repository commit, Meta AI version, firmware version, phone OS, and tested glasses model in every experiment result.

### 4.2 Required tools and accounts

Common requirements:

- supported glasses and compatible physical phone;
- Meta account and current Meta AI app;
- Wearables Developer Center account, organisation, and project for release-channel testing;
- glasses firmware V125+ and Meta AI app V275 for DAT 0.8.0 at the time of review;
- Developer Mode for unpublished builds;
- an internet connection for account/project/registration operations and a local Bluetooth/Wi-Fi environment for device transport.

iOS:

- a Mac, current Xcode, Apple signing identity/team, and registered bundle identifier;
- Swift Package Manager access to the official repository;
- physical-device installation from Xcode; TestFlight/App Store must not be assumed.

Android:

- Android Studio, JDK, Android SDK, USB debugging/ADB, and a GitHub account;
- a classic GitHub personal access token with `read:packages` because the SDK is distributed through GitHub Packages;
- physical-device debug installation from Android Studio or Gradle.

There are prerequisite conflicts in official material. The Setup page says iOS 15.2+, Xcode 14+, Android 10+, and Android Studio Flamingo+. The repository knowledge base says Xcode 15+/iOS 16+, while the iOS sample says iOS 17+. The Android sample requires Android Studio Narwhal 2025.1.1+, JDK 17, and SDK 36. For a new prototype, use the **strictest current sample baseline**, not the lowest marketing minimum, and record the discrepancy. [Setup](https://wearables.developer.meta.com/docs/develop/dat/getting-started-toolkit/) [iOS sample](https://github.com/facebook/meta-wearables-dat-ios/tree/main/samples/CameraAccess) [Android sample](https://github.com/facebook/meta-wearables-dat-android/tree/main/samples/CameraAccess)

### 4.3 Physical installation and test flow

1. Update phone app and glasses firmware; charge glasses above 10%.
2. Pair glasses in Meta AI and enable Developer Mode.
3. Build the official CameraAccess sample for the physical phone.
4. Install from Xcode or Android Studio/ADB.
5. Register the app through the Meta AI deep-link flow.
6. Grant camera permission in Meta AI and microphone/Bluetooth/local-network permission in the mobile OS.
7. Verify the active glasses and audio route before recording.
8. Create a session, configure HFP **before starting the camera stream**, wait for the audio route to settle, then start streaming. Meta documents that reversing this order can cause the HFP route to fail silently. [Audio guide](https://wearables.developer.meta.com/docs/develop/dat/microphones-and-speakers/)
9. Exercise pause, resume, fold, permission revoke, link loss, low battery, and thermal/error paths.
10. Inspect actual files and timestamps, not only a live preview.

### 4.4 iOS versus Android starting point

**Recommendation: start the controlled technical experiment on iOS, then run an Android parity test before any product decision.**

Reasons:

- iOS 0.8.0 explicitly adds Wi-Fi transport for high-bandwidth camera/display functions.
- iOS exposes compressed `hvc1` streaming that can continue when the app is backgrounded.
- `AVAssetWriter` provides mature concurrent audio/video container writing.
- The current known-issues page specifically identifies an Android long-running-stream capture crash.

Reasons not to overcommit to iOS:

- public App Store publication is explicitly unsupported;
- Android sideloading and presentation timestamps may be easier for instrumentation;
- the iOS/Android transport descriptions are inconsistent and must be measured;
- platform parity matters if a distributed contributor workforce is ever permitted.

This is a reversible experiment choice, not an architecture commitment.

### 4.5 Suggested future repository structure

If Phase 2 is approved, keep evidence and experiments separate from any eventual product:

```text
docs/
  research/                 source register and refreshed due diligence
  legal/                    counsel questions; no legal conclusions in code
  decisions/                dated, reversible architecture decision records
  protocols/                consent, capture, privacy, safety, QA procedures
experiments/
  capture-ios/              smallest instrumented prototype
  capture-android-parity/   only after iOS evidence
  sync/                     clock, offset, and drift results
  hardware/                 battery, heat, RF, image-quality results
schemas/
  canonical/                media manifest and annotation definitions
  adapters/                 LeRobot/RLDS/COCO exports, if semantically valid
processing/
  prototypes/               offline research pipeline only
evals/
  capture-quality/
  annotation-quality/
  buyer-task-lift/
vendor-reference/
  README.md                 pinned source URLs, tags, commits; no silent forks
```

Keep consent records in a separately secured system with access controls, not casually beside media in a source repository.

---

## 5. Data-capture feasibility

### 5.1 Video and narration synchronisation

**What is verified:**

- DAT supplies timed video frames; Android explicitly exposes `presentationTimeUs`, and iOS frames use timed media buffers.
- iOS `AVAssetWriter` can interleave audio and video tracks; Android `MediaMuxer` can write encoded samples in presentation-time order. [Android changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md) [AVAssetWriter](https://developer.apple.com/documentation/avfoundation/avassetwriter) [MediaMuxer](https://developer.android.com/reference/android/media/MediaMuxer.html)
- Glasses audio is acquired through the mobile Bluetooth audio stack, not through the camera stream API.

**What is not verified:**

- that video and HFP audio share a hardware clock;
- a maximum initial offset, jitter, or drift rate;
- whether route changes preserve monotonic timing;
- whether background transitions introduce silent gaps;
- whether all devices expose the same HFP sample timing.

**Inference:** phone-side muxing is implementable, but reliable synchronisation must be measured. Each test recording should include an observable audiovisual sync event at the start and end so offset and drift can be calculated. Narration must retain its raw timestamps and must not be permanently baked into a corrected file without preserving the original.

### 5.2 Expected quality limits

- **Spatial resolution:** 720 pixels across the landscape-equivalent short dimension of a portrait frame is marginal for small tools, fast fingers, labels, fasteners, and occluded contacts.
- **Adaptive compression:** Meta warns that reported high/medium resolution can still look poor because per-frame compression adapts to bandwidth. Requesting a lower resolution or frame rate may improve per-frame quality.
- **Head view is not gaze:** a wearer can look with their eyes without turning their head. Without gaze tracking, the active object may leave the camera centre even when the wearer sees it.
- **Hands occlude objects:** first-person manipulation routinely hides contact surfaces and tool tips. A second fixed/exocentric camera may be more valuable than additional raw ego hours.
- **Narration is not environmental audio:** HFP beamforming suppresses ambient sound and other speakers. That is good for the wearer transcript, bad for machine sounds, collaborator speech, safety cues, and acoustic outcomes.
- **Narration changes behavior:** thinking aloud can slow, simplify, or alter natural task execution. “Narrated” and “natural silent” demonstrations should be separate protocol conditions.
- **No calibration:** without camera intrinsics/extrinsics or pose, metric 3D reconstruction and robot retargeting are underconstrained.

### 5.3 Duration, battery, heat, latency, and connectivity

No current official source provides a continuous DAT camera + HFP audio duration benchmark. Relevant risk signals are:

- thermal level and thermal-critical/emergency errors exist because sustained load can affect operation;
- battery-critical and peak-power shutdown errors exist;
- streaming can pause or stop for user/system events;
- the connection can degrade resolution/fps;
- Android has a documented long-stream rapid-capture crash;
- closing/folding breaks the session and does not auto-restart;
- consumer “typical use” battery values are not representative.

The prototype must measure:

- time to first frame and end-to-end preview latency;
- delivered rather than requested fps/resolution;
- timestamp gaps, duplicated/out-of-order frames, decode errors, and compression artifacts;
- initial A/V offset and drift per 10 minutes;
- glasses and phone battery percentage per minute, where available from their respective systems;
- thermal state transitions and time to stop/throttle;
- reconnection behavior and what portion of the artifact remains valid;
- storage bytes per minute for raw and compressed modes;
- behavior with Wi-Fi contention, Bluetooth interference, screen lock, foreground/background, calls, and notifications.

### 5.4 Storage, upload, and offline capture

**Recommended prototype behavior:** record short, crash-resilient segments to the phone first, write an append-only manifest, hash closed segments, then upload asynchronously. The server should never be the only copy during active capture.

Each episode should record at least:

- dataset/session/episode UUIDs;
- glasses family and pseudonymous device identifier;
- SDK version, app build, phone model/OS, Meta AI version, glasses firmware;
- requested and observed stream settings, codec, frame timing, audio route/format;
- UTC and monotonic timestamps plus clock-correction history;
- state transitions, errors, permission state, thermal level, and interruption markers;
- media hashes, byte lengths, upload parts, and transformation lineage;
- task definition, environment, contributor, consent grant/version, and withdrawal state through secure references.

**Offline:** an app can conceptually queue cloud uploads while disconnected, but fully offline DAT capture is not documented. Registration and platform checks may need Internet, live capture still needs the phone-to-glasses link, and iOS high-bandwidth streaming may use local Wi-Fi. Offline behavior is therefore an explicit test case, not a product promise.

---

## 6. AI data-processing opportunities

### 6.1 Proposed enrichment pipeline

The processing system should preserve the raw evidence and make every derived label traceable:

1. **Ingest and integrity:** verify hashes, container readability, timestamps, expected duration, consent scope, and manifest completeness.
2. **Technical QC:** detect gaps, blur, darkness, occlusion, low audio level, route changes, excessive compression, and missing task stages.
3. **Privacy pre-screen:** identify faces, voices, names, screens, documents, addresses, licence plates, badges, and confidential material before broad reviewer access.
4. **Transcription:** word/segment timestamps, confidence, non-speech markers, and reviewer corrections. At 8 kHz mono, domain vocabulary and noisy-task accuracy must be benchmarked rather than assumed.
5. **Task segmentation:** episode → phase → atomic action → interaction/event. Preserve overlapping actions and “no-op/search/hesitation” periods instead of forcing every frame into an action.
6. **Objects and tools:** class, instance, visibility, state, track, region/mask, and role such as target/tool/container/obstacle.
7. **Hand-object interaction:** left/right/unknown hand, contact state, manipulated object, tool-mediated contact, bimanual relation, and occlusion confidence.
8. **Narration alignment:** align what the wearer says, what is visible, what is inferred, and what happens later. Contradictions should be labels, not silently corrected transcripts.
9. **Mistake and recovery:** expected step, observed deviation, detection point, correction action, outcome, and whether the recovery was successful.
10. **Outcome and quality:** success/partial/failure/aborted/unknown, objective evidence, reviewer confidence, safety events, and ambiguity flags.
11. **Human review:** double-review high-value or ambiguous events, adjudicate disagreements, and record reviewer provenance.
12. **Package and evaluate:** emit the buyer's requested schema plus a canonical package; measure downstream lift, not only annotation completeness.

Existing datasets demonstrate useful annotation precedents. EPIC-KITCHENS provides narration and verb/noun action segments; Assembly101 explicitly includes mistakes and corrections; Ego-Exo4D includes timed narrations, keysteps, procedural dependencies, hand/body pose, object masks, and proficiency ratings. [EPIC-KITCHENS](https://epic-kitchens.github.io/) [Assembly101](https://assembly-101.github.io/) [Ego-Exo4D](https://docs.ego-exo4d-data.org/)

### 6.2 Opportunity and reliability table

| Enrichment | Potential value | Principal failure mode | Required validation |
|---|---|---|---|
| Transcription | Natural-language intent, steps, uncertainty, causal explanation | 8 kHz errors, specialist terms, wearer muttering, suppressed collaborators | Domain word error rate and timestamp error against reviewed clips |
| Task segmentation | Searchable episodes and skill primitives | Boundaries are subjective; overlapping actions | Written ontology, double annotation, boundary tolerance metric |
| Object/tool detection | Inventory, tracks, state changes, active-object supervision | Small/occluded tools and long-tail objects | Per-class precision/recall on buyer-domain samples |
| Hand-object interaction | Contact and manipulation cues | No depth; self-occlusion; left/right ambiguity | Hand/object visibility coverage and reviewed contact events |
| Action recognition | Verb-object sequences and procedural structure | Human action does not equal robot command | Buyer-defined action vocabulary and held-out task evaluation |
| Narration-action alignment | Links intent/reasoning to observed behavior | Speech leads/lags action; narration can be wrong | Alignment error distribution and contradiction labels |
| Mistake/recovery detection | Rare, high-value robustness supervision | “Mistake” depends on goal and expertise | Explicit expected plan, outcome evidence, expert adjudication |
| Success/failure labelling | Evaluation targets and terminal outcomes | Visual completion may not prove functional success | Instrumented or human-verifiable acceptance criteria |
| Privacy filtering | Reduces exposure before wider processing | Blurring misses reflections, screens, voices, contextual identity | Recall-first audit; human privacy review; deletion workflow |
| Quality scoring | Avoids paying for unusable footage | Proxy scores can reward the wrong behavior | Correlation with reviewer acceptance and downstream model lift |

### 6.3 Canonical dataset package

The canonical package should remain model- and buyer-neutral:

```text
episode/
  manifest.json
  media/
    video_original.mp4
    audio_original_or_extracted.wav
    preview_privacy_filtered.mp4
  annotations/
    transcript.jsonl
    segments.parquet
    objects_coco.json
    interactions.parquet
    mistakes_recoveries.jsonl
    outcomes.json
  quality/
    technical_qc.json
    semantic_qc.json
    privacy_qc.json
  provenance/
    transformations.jsonl
    source_hashes.json
```

Consent forms and directly identifying contributor records should be stored separately with controlled linkage.

### 6.4 Buyer-facing format adapters

- **MP4 + WAV/FLAC + JSONL/Parquet:** the safest canonical delivery for video-centric foundation-model work.
- **COCO-compatible JSON:** useful for object detection/segmentation, with extensions for tracks, hands, contact, and object state.
- **EPIC-KITCHENS-style action segments:** useful for verb/noun procedural tasks.
- **LeRobotDataset v3:** stores tabular state/action/timestamps in Parquet, visual data in MP4, and episode/task metadata in JSON/Parquet. It is appropriate only when the package contains semantically meaningful time-series state/action fields. [LeRobotDataset v3](https://huggingface.co/docs/lerobot/main/lerobot-dataset-v3)
- **RLDS:** represents datasets as episodes of steps with observation, action, reward/discount, and terminal metadata. Do not put human action names into robot action vectors merely to claim compatibility. [RLDS](https://github.com/google-research/rlds)
- **HDF5/Zarr/ROS bag:** reasonable buyer adapters when supplementary robot, pose, force, or sensor streams exist.

RGB demonstration video can be represented in LeRobot or RLDS containers, but the container does not make it robot-control data. Missing action/state fields must be absent or explicitly unknown, never fabricated.

---

## 7. Key limitations for robotics

### 7.1 The embodiment gap

Human first-person video supplies visual observations, task context, intent cues, and examples of outcomes. It generally does **not** supply the control target a robot policy needs. A robot must map observations to its own end-effector or joint commands under its kinematic, dynamic, latency, reach, and gripper constraints.

Recent research states the problem directly: human-object videos scale more easily, but lack explicit action labels and differ from robot embodiment. Successful systems add bridging machinery. EgoMimic used Project Aria video plus 3D hand tracking, a robot designed to reduce kinematic mismatch, cross-domain alignment, and co-training with robot data. UMI uses handheld instrumented grippers, relative 6-DoF trajectories, gripper state, and latency matching. [Human2Sim2Robot](https://proceedings.mlr.press/v305/lum25a.html) [EgoMimic](https://arxiv.org/abs/2410.24221) [UMI](https://arxiv.org/abs/2402.10329)

### 7.2 Missing signals

DAT first-person video/audio lacks:

- metric depth and scale;
- calibrated six-degree-of-freedom camera/head/hand/object trajectories;
- force, torque, tactile pressure, slip, contact and compliance;
- finger and arm joint angles;
- robot joint states, control commands, gripper aperture, reward, and safety state;
- external views that reveal occluded contact;
- precise eye gaze and attention;
- stable environment coordinates and object models.

### 7.3 Consequences

- The dataset is more defensible for **pretraining, task understanding, visual representation learning, procedural reasoning, video-language models, and error/outcome modelling** than for direct behavior cloning.
- Direct policy use will likely require a small amount of paired robot data, simulation/retargeting, or instrumented human action data.
- Claims such as “the robot sees exactly what the human sees” are false: camera placement, lens, gaze, body geometry, height, hands, and motion all differ.
- More video hours do not necessarily overcome missing action observability.

### 7.4 Additional sensors worth testing later

In increasing order of complexity:

1. a fixed exocentric phone/action camera with a sync marker;
2. phone IMU and coarse location where lawful and useful;
3. wrist/hand IMUs or optical markers;
4. instrumented tools or UMI-style grippers with 6-DoF and aperture;
5. depth camera or Project Aria-class research hardware;
6. limited robot teleoperation/paired trajectories for grounding;
7. force/torque and tactile sensors for contact-rich tasks.

Project Aria Gen 2 illustrates the sensor gap: its research hardware offers a 12 MP RGB camera, four computer-vision cameras, eye tracking, dual IMUs, seven spatial microphones, GNSS, barometer, magnetometer, PPG, calibration, on-device perception, and 6–8 hour continuous recording. Access is through a qualified research-partner programme, and commercial rights/availability require separate diligence. [Project Aria Gen 2](https://facebookresearch.github.io/projectaria_tools/gen2/) [Aria hardware specifications](https://facebookresearch.github.io/projectaria_tools/gen2/technical-specs/device/hardware)

---

## 8. Legal, privacy, and platform risks

### 8.1 Critical Meta platform-terms risk

The current Meta Wearables Developer Terms, last updated 6 October 2025, create the highest-priority go/no-go issue. Relevant provisions include:

- **Technology Data** includes information, data, or content from/about/associated with a person, device, or identifier obtained from the Technology, including derived data.
- Permitted uses are limited to running, supporting, and maintaining the integration to provide or improve the experience requested by the end user, plus legal compliance.
- Selling, licensing, purchasing, or renting Technology Data is prohibited.
- Third-party sharing requires express end-user direction/consent or a qualifying service-provider/legal basis, but the separate sale/licensing ban remains.
- Service providers need written restrictions, security/confidentiality, and deletion duties.
- User, account, Meta, or legal deletion triggers apply; the privacy policy cannot authorise a use that the terms prohibit.
- Meta may review, monitor, require attestations, inspect service-provider arrangements, and audit Technology Data handling.
- General release requires Integration Review and approval is discretionary. [Meta Wearables Developer Terms](https://wearables.developer.meta.com/terms)

**Inference:** video, audio, annotations, and derived training packages produced from DAT streams are likely Technology Data. If so, licensing those packages to AI or robotics customers is prohibited under the public terms. A contributor's consent cannot grant rights that the developer itself does not have from Meta.

**Required manual legal review:** counsel must review the full logged-in terms, linked Supplemental MPT Terms, product terms, privacy policy, Acceptable Use Policy, developer documentation, and any project-specific agreement. The public Acceptable Use Policy also prohibits unlawful/right-infringing uses, sensor/recording encouragement in sensitive locations, and certain surveillance or harmful uses. [Acceptable Use Policy](https://wearables.developer.meta.com/acceptable-use-policy)

No Phase 2 capture app should be funded beyond a minimal lab test until Meta answers in writing:

1. May DAT camera/audio be used to create datasets for commercial AI/robotics training?
2. May the developer sell or license raw or derived annotations/embeddings/models?
3. Does contributor-directed collection alter the Technology Data restriction?
4. Is there a partner/enterprise agreement that permits this use?
5. What distribution and tester scale can the project obtain?

### 8.2 Consent and bystanders

The outward LED is notice, not informed consent. A defensible collection protocol needs:

- explicit wearer/contributor consent before capture;
- clear task, duration, sensors, processing, recipients, commercial AI-training purpose, retention, deletion/withdrawal, compensation, and complaint process;
- consent or exclusion for identifiable bystanders and recorded collaborators;
- site owner/employer/customer authorisation;
- a way to stop capture immediately and mark excluded intervals;
- visible signage and a controlled capture zone where practical;
- separate treatment of children, health data, intimate spaces, safety incidents, confidential documents, screens, and trade secrets;
- auditable evidence of the consent version that governed each episode.

Automated face/plate/voice redaction reduces exposure but does not retroactively make an unlawful collection lawful, and it is not guaranteed de-identification.

### 8.3 Australian privacy and recording law

OAIC guidance says identifiable photos and videos are personal information. A dataset business may fall within the Privacy Act even below the usual AUD 3 million turnover threshold if it trades in personal information; the OAIC describes trading as providing or disclosing personal information for a benefit, service, or advantage, subject to consent and other details requiring advice. [OAIC photos and videos](https://www.oaic.gov.au/privacy/your-privacy-rights/social-media-and-online-privacy/photos-and-videos) [OAIC small business](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/small-business)

In Queensland, a party to a private conversation may fall within the party exception for making a recording, but section 45 separately restricts later communication/publication of that recorded private conversation and includes an exception for consent of all other parties. Licensing recorded private workplace or household conversations cannot safely rely on wearer consent alone. [Queensland Invasion of Privacy Act 1971, ss 43–45](https://www.legislation.qld.gov.au/view/whole/html/inforce/current/act-1971-050)

Workplace surveillance law varies by state/territory. For example, New South Wales has notice and other requirements under the Workplace Surveillance Act 2005. A national programme needs a jurisdiction-by-jurisdiction matrix and workplace-specific advice, not a single Australian consent form. [NSW Workplace Surveillance Act 2005](https://legislation.nsw.gov.au/view/html/inforce/current/act-2005-47)

### 8.4 Mobile platform rules

- Apple requires explicit user consent and a clear visual and/or audible recording indication. Its privacy rules require disclosure of collection, uses, third parties including third-party AI, retention/deletion, and consent withdrawal. [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- Google Play requires prominent disclosure and affirmative consent when collection/use of sensitive data is outside reasonable user expectation, with accurate data-safety disclosures. [Google Play User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en-GB)
- Passing store review would not resolve Meta's terms, local recording law, contributor licensing, or buyer-use rights.

### 8.5 Data ownership and contributor licensing

No source reviewed establishes that the project automatically owns captured people, places, speech, brands, documents, trade secrets, copyrighted works, or workplace processes. A contributor agreement should be drafted by counsel and address:

- authority to record the location, task, people, and materials;
- commercial collection, annotation, transformation, AI training, evaluation, and defined sublicensing;
- territories, term, compensation, withdrawal/deletion, and effect on already-trained models;
- image, voice, biometric, performance, and publicity rights;
- confidentiality and employer/customer IP;
- safety obligations and prohibited tasks;
- warranties that are realistic rather than shifting impossible risk to contributors.

These contributor rights are necessary but not sufficient: they cannot override Meta's platform restrictions.

### 8.6 Minimum privacy/security controls before any external pilot

- privacy impact assessment and threat model;
- data minimisation and controlled task zones;
- encryption in transit and at rest, separate identity vault, least-privilege access;
- reviewer access through privacy-filtered proxies where possible;
- immutable provenance/consent/deletion logs;
- service-provider agreements and subprocessor register;
- regional storage and cross-border transfer review;
- incident response and Meta incident-notification procedure;
- demonstrable deletion across raw, derived, backup, cache, annotation, and export copies;
- model-training deletion policy that honestly explains what can and cannot be unlearned.

---

## 9. Competitive and technical landscape

### 9.1 Existing first-person datasets

| Dataset | Scale and modalities | Relevance |
|---|---|---|
| **Ego4D** | 3,600 hours, 926 wearers, 74 locations in nine countries; dense narration plus portions with audio, 3D, gaze, stereo/multi-view | Establishes a large public egocentric baseline and a consent/de-identification precedent. [Ego4D](https://ego4d-data.org/docs/) |
| **Ego-Exo4D V2** | 1,286.30 total video hours, 221.26 ego-hours, 5,035 takes; synchronised ego/exo, seven-channel audio, IMU, gaze, SLAM, 3D, narrations, keysteps, procedural dependencies, pose, masks, proficiency | Much richer than DAT video and a strong schema reference. Its landing page still mentions 1,422 hours while the V2 release states 1,286.30; use the V2 number and flag the conflict. [Ego-Exo4D](https://docs.ego-exo4d-data.org/) |
| **EPIC-KITCHENS-100** | 100 hours, 45 kitchens, about 90,000 action segments, multi-language narration, verb/noun taxonomies | Strong precedent for unscripted home tasks and narration-linked action segmentation. [EPIC-KITCHENS](https://epic-kitchens.github.io/) |
| **Assembly101** | 4,321 videos, 101 assembly/disassembly toys, 8 static + 4 ego views, over 1M fine action segments, 18M 3D hand poses, mistakes/corrections | Direct precedent for procedural mistakes and recovery labels. Licence is non-commercial, so it is a research baseline rather than commercial training inventory. [Assembly101](https://assembly-101.github.io/) |
| **DROID** | 76,000 robot trajectories / 350 hours across 564 scenes and 86 tasks, with robot observations/actions | Demonstrates what robot-grounded data contains that human RGB does not. [DROID](https://droid-dataset.github.io/) |

### 9.2 Relevant research and open systems

- **EgoMimic:** uses Aria video plus 3D hand tracking and robot co-training; evidence that human data can help, but also evidence that RGB alone is insufficient. [Paper](https://arxiv.org/abs/2410.24221)
- **Universal Manipulation Interface:** portable human demonstrations with instrumented grippers, relative pose, gripper state, and latency-matched policy design. [Project](https://umi-gripper.github.io/) [Paper](https://arxiv.org/abs/2402.10329)
- **Project Aria:** substantially richer research capture with time-synchronised sensors and calibration; access and commercial rights are separate constraints. [Docs](https://facebookresearch.github.io/projectaria_tools/gen2/)
- **Open X-Embodiment/RLDS:** cross-robot datasets and episode/step semantics show the importance of embodiment-specific state/action definitions. [Open X-Embodiment](https://robotics-transformer-x.github.io/) [RLDS](https://github.com/google-research/rlds)
- **EgoScale (research preprint), EgoVerse, EgoLive, and MobileEgo Anywhere:** 2026 work indicates rapid scaling of egocentric human-data collection and processing. These recent results should be treated as emerging evidence and independently reproduced before commercial claims. [EgoScale preprint](https://arxiv.org/abs/2602.16710) [EgoVerse preprint](https://arxiv.org/abs/2604.07607) [EgoLive preprint](https://arxiv.org/abs/2604.23570) [MobileEgo Anywhere preprint](https://arxiv.org/abs/2605.05945)

### 9.3 Commercial landscape

The category is already crowded. Examples include:

- **EgoScale:** markets large-scale egocentric demonstrations and structured robotics data; its published hour/task/contributor/partner counts are self-reported. [EgoScale](https://www.egoscale.com/)
- **RoboData:** markets phone/head-mounted household demonstrations, AI processing, action/object timestamps, quality scores, and LeRobot/RLDS/HDF5/ROS-style outputs. Its scale projections and market figures are marketing claims, not verified traction. [RoboData](https://robodata.dev/)
- **Caspius:** explicitly markets first-person video, hand motion, and proprioception from wearables and phones. [Caspius](https://caspius.ai/)
- **Trillion UMI:** markets a portable rig with three synchronised cameras, two 6-DoF poses, and gripper aperture—signals DAT does not supply. [Trillion UMI](https://trillionrobotics.ai/)
- Other active egocentric-data vendors include Egosense, RoboDATA.AI, Roborecs, and specialist collection providers. Their claims need customer-reference and dataset audits before being treated as evidence of demand. [Egosense](https://egosense.ai/) [RoboDATA.AI](https://www.therobodata.ai/) [Roborecs](https://roborecs.com/)

### 9.4 Differentiation that might matter

The following are more defensible than “we collect POV video”:

1. **Provable rights and provenance:** task-, person-, site-, processing-, and buyer-specific rights; revocation and deletion traceability.
2. **Buyer-designed task packs:** ontology and acceptance criteria created with a specific robotics/model team before collection.
3. **Mistake, recovery, and outcome data:** deliberate hard negatives and recovery branches, not only clean successes.
4. **Paired grounding signals:** at least an exocentric view and, where needed, 6-DoF/gripper/contact or small robot-data anchors.
5. **Quality that predicts utility:** technical, semantic, legal, and downstream-model scores rather than raw “hours.”
6. **Evaluation as part of delivery:** a held-out benchmark showing improvement over raw footage and available public data.
7. **High-trust workplace collection:** lawful, safety-aware access to processes that public household datasets do not cover.
8. **Hardware-agnostic ingestion:** Ray-Ban/Oakley, phone, action camera, Aria-class research devices, and instrumented tools behind one evidence model.

The platform-terms finding makes hardware agnosticism a survival requirement, not a nice-to-have.

---

## 10. Feasibility assessment

### 10.1 Possible today

Subject to a lab-only legal basis and no dataset sale:

- register an invite-only iOS or Android app with supported glasses;
- stream live portrait video at up to requested 720 × 1280/30 fps;
- capture stills during a stream;
- capture beamformed wearer speech at 8 kHz mono through HFP;
- write segmented media to the phone and upload later;
- observe session, link, stream, permission, thermal, and critical power errors;
- test application logic with Mock Device Kit;
- process recorded media into transcripts, task/action/object/interaction annotations, privacy flags, outcomes, and human-reviewed quality scores;
- package video-centric data in transparent standard formats without claiming missing robot actions.

### 10.2 Possible only in a controlled prototype

- bounded A/V offset/drift across different phones/glasses;
- continuous useful-duration capture without unacceptable thermal, battery, compression, or link loss;
- safe recovery and artifact preservation after pause/fold/disconnect/background events;
- offline-first local capture and resumable upload;
- contributor onboarding through a small invite-only release channel;
- valid consent and capture in a controlled, bystander-free environment;
- buyer-validated enrichment for one task domain;
- comparison of Ray-Ban Gen 2 and Oakley Vanguard view/fit trade-offs.

### 10.3 Depends on Meta, future SDKs, or different hardware

- permission to sell/license DAT-derived data;
- general public distribution and high-scale contributor access;
- iOS App Store support;
- 3K or higher-quality developer video;
- on-glasses storage/recovery and custom model execution;
- depth, calibrated pose, gaze, IMU, raw microphone array, or Neural Band data through the native camera SDK;
- public SDK stability and long-term backward compatibility;
- direct robot-control supervision without supplementary sensing/robot data.

### 10.4 Risk register

| Risk | Severity | Evidence / uncertainty | Gate or mitigation |
|---|---|---|---|
| Meta prohibits dataset sale/licensing | **Critical** | Strong current terms text | Written Meta clearance and legal opinion before product build |
| No public distribution | **Critical** | Invite-only channels; iOS blocked | Confirm route and tester scale; do not model marketplace growth yet |
| Human video does not map to robot actions | **Critical** | Established embodiment gap | Buyer-specific task; supplementary pose/action/robot data; measure model lift |
| No buyer willingness to pay | **Critical** | Competitors and public data already exist | Buyer supplies task/schema and evaluates blind enrichment sample |
| A/V sync/drift unacceptable | **High** | Separate DAT video and HFP audio routes | Instrumented start/end sync events and multi-device measurement |
| Video too compressed/low-resolution | **High** | 720 × 1280 cap and adaptive compression | Compare settings; choose tasks with visible actions; add exocentric camera |
| HFP audio too narrow/suppressed | **High** | 8 kHz mono wearer beamforming | Benchmark ASR; optionally add separate environmental mic with consent |
| Battery/thermal duration inadequate | **High** | No continuous DAT benchmark | 5/10/20/40-minute soak matrix; segment and fail closed |
| Bystander/workplace rights failure | **Critical** | Personal information and recording laws | Controlled zones, all-party consent, site agreements, PIA, counsel |
| SDK churn/vendor discontinuation | **High** | Eight preview releases in eight months | Pin versions, isolate adapter, refresh due diligence, hardware-agnostic core |
| Interruption loses episode | **High** | Single session, device-driven stops, no glasses buffer | Phone-first short segments, manifests, integrity checks, explicit restart UX |
| Annotation looks rich but is unreliable | **High** | Subjective boundaries and outcomes | Double annotation, adjudication, ontology tests, inter-reviewer metrics |
| Privacy filtering misses identity/IP | **High** | Visual/audio/contextual re-identification | Recall-first filters plus human review and access control |

### 10.5 Biggest assumptions to test

1. Meta will permit the intended commercial data use under a written agreement.
2. A buyer values enriched egocentric demonstrations for a defined task more than public data or robot telemetry.
3. 720 × 1280 adaptive video preserves the hand/tool/object evidence needed for that task.
4. HFP narration can be synchronised and transcribed with acceptable domain accuracy.
5. At least 20 minutes of continuous real work is possible without unacceptable thermal, power, or connection failures.
6. Mistakes, recoveries, and outcomes can be labelled consistently enough to improve a model or evaluation.
7. Consent, workplace access, and data deletion can be operationalised without destroying collection economics.
8. The required embodiment bridge is small enough that human capture remains cheaper or more scalable than teleoperation/UMI/robot data.

### 10.6 Smallest experiment that validates the core thesis

The smallest useful experiment has **three sequential gates**. Passing a later technical gate cannot cure failure of an earlier legal or commercial gate.

#### Gate 0 — platform and legal clearance

- Send Meta the exact proposed data flow and revenue model.
- Obtain a written answer on commercial AI training, derivative annotations/models, third-party buyer delivery, retention/deletion, service providers, and tester scale.
- Obtain Australian privacy/recording/workplace advice and a short contributor/site consent protocol.
- **Stop condition:** no written path to commercial use. If blocked, test the broader thesis with non-DAT hardware rather than attempting to route around the terms.

#### Gate 1 — controlled capture reliability

After Phase 2 approval, use one Ray-Ban Meta Gen 2, one current iPhone, the official 0.8.0 sample as the reference, and a bystander-free controlled room. Capture approximately 30 episodes across five visible tabletop tasks, including successful execution, deliberate mistake, and recovery conditions. Use 5-, 10-, and 20-minute sessions and at least two stream settings.

Record a visible/audible sync event at the beginning and end. Measure:

- session completion and recovery rate;
- delivered fps/resolution, missing-frame time, blur/occlusion, and hand/tool visibility;
- audio route, sample format, speech intelligibility, ASR error, A/V offset and drift;
- battery drain, thermal states, storage per minute, start latency, and interruption loss;
- integrity of local segmented files after fold, link loss, screen lock, and backgrounding.

Provisional acceptance targets must be agreed with the buyer, not invented by engineering. Sensible starting gates are: at least 95% complete episodes, no unexplained media gap in accepted episodes, median absolute A/V alignment within 100 ms after correction, bounded drift across 20 minutes, and sufficient hand/tool visibility for reviewers to label the buyer's required events.

#### Gate 2 — enrichment and buyer value

- Select one task specified by a qualified robotics or embodied-AI buyer.
- Create a small canonical package with transcript, atomic actions, objects/tools, hand-object events, one mistake/recovery branch, outcome evidence, technical QC, and provenance.
- Double-annotate a subset and report disagreement rather than hiding it.
- Give the buyer a blinded comparison of raw video, automatically enriched video, and human-reviewed enrichment; where possible compare with a relevant public-data baseline.
- **Pass condition:** the buyer confirms the schema is usable and demonstrates or commits to a defined evaluation showing measurable lift or meaningful cost/time reduction.

Technical capture success without Gate 2 is not validation of a data business. Buyer enthusiasm without Gate 0 is not permission to operate.

---

## Source register

### Meta developer platform and repositories

1. [Meta Wearables Device Access Toolkit for iOS](https://github.com/facebook/meta-wearables-dat-ios) — official repository, 0.8.0 snapshot; accessed 31 July 2026.
2. [Meta Wearables Device Access Toolkit for Android](https://github.com/facebook/meta-wearables-dat-android) — official repository, 0.8.0 snapshot; accessed 31 July 2026.
3. [DAT Setup](https://wearables.developer.meta.com/docs/develop/dat/getting-started-toolkit/) — updated 17 June 2026; accessed 31 July 2026.
4. [Integration overview](https://wearables.developer.meta.com/docs/develop/dat/build-overview/) — updated 28 July 2026; accessed 31 July 2026.
5. [iOS integration guide](https://wearables.developer.meta.com/docs/develop/dat/build-integration-ios/) — updated 28 July 2026; accessed 31 July 2026.
6. [Android integration guide](https://wearables.developer.meta.com/docs/develop/dat/build-integration-android/) — updated 28 July 2026; accessed 31 July 2026.
7. [Permissions and registration](https://wearables.developer.meta.com/docs/develop/dat/permissions-requests/) — updated 28 July 2026; accessed 31 July 2026.
8. [Session lifecycle](https://wearables.developer.meta.com/docs/develop/dat/lifecycle-events/) — updated 28 July 2026; accessed 31 July 2026.
9. [Microphones and speakers](https://wearables.developer.meta.com/docs/develop/dat/microphones-and-speakers/) — updated 17 June 2026; accessed 31 July 2026.
10. [Mock Device Kit](https://wearables.developer.meta.com/docs/develop/dat/mock-device-kit/) — updated 17 June 2026; accessed 31 July 2026.
11. [Release channels](https://wearables.developer.meta.com/docs/develop/dat/set-up-release-channels/) — updated 30 June 2026; accessed 31 July 2026.
12. [Known issues](https://wearables.developer.meta.com/docs/develop/dat/knownissues/) — updated 26 June 2026; accessed 31 July 2026.
13. [Version dependencies](https://wearables.developer.meta.com/docs/develop/dat/version-dependencies/) — updated 25 June 2026; accessed 31 July 2026.
14. [DAT telemetry](https://wearables.developer.meta.com/docs/develop/dat/telemetry/) — updated 14 July 2026; accessed 31 July 2026.
15. [Meta staff discussion: third-party apps and stored media](https://github.com/facebook/meta-wearables-dat-android/discussions/20) — official repository discussion; accessed 31 July 2026.

### Meta hardware

16. [Ray-Ban Meta Gen 1 announcement](https://about.fb.com/news/2023/09/new-ray-ban-meta-smart-glasses/) — Meta, 27 September 2023, later updated; accessed 31 July 2026.
17. [Ray-Ban Meta Gen 2 announcement](https://about.fb.com/news/2025/09/ray-ban-meta-gen-2-better-battery-life-video-capture/) — Meta, 17 September 2025; accessed 31 July 2026.
18. [Ray-Ban Meta Gen 2 AU product specifications](https://www.ray-ban.com/australia/electronics/RW4012ray-ban%20%7C%20meta%20wayfarer%20-%20gen%202-black/8056262721391) — Ray-Ban; indexed official content accessed 31 July 2026; direct automated retrieval was bot-blocked and should be checked manually before procurement.
19. [Ray-Ban Meta Optics announcement](https://about.fb.com/news/2026/03/meta-ai-glasses-built-for-prescriptions/) — Meta, 31 March 2026; accessed 31 July 2026.
20. [Oakley Meta HSTN announcement](https://about.fb.com/news/2025/06/introducing-oakley-meta-glasses-a-new-category-of-performance-ai-glasses/) — Meta, 20 June 2025; accessed 31 July 2026.
21. [Oakley Meta product comparison/specifications](https://www.oakley.com/en-au/l/oakley-meta) — Oakley; indexed official content accessed 31 July 2026; direct automated retrieval was bot-blocked and should be checked manually before procurement.
22. [Oakley Meta Vanguard announcement](https://about.fb.com/news/2025/09/oakley-meta-vanguard-performance-ai-glasses-sports/) — Meta, 17 September 2025; accessed 31 July 2026.
23. [Meta Ray-Ban Display announcement](https://about.fb.com/news/2025/09/meta-ray-ban-display-ai-glasses-emg-wristband/) — Meta, 17 September 2025; accessed 31 July 2026.

**Retailer-source access note:** Ray-Ban and Oakley regional product/FAQ pages intermittently rejected direct automated requests during this review. Their indexed official content was used only for consumer specifications, cross-checked against Meta announcements, and never treated as proof of SDK capability. Recheck the exact SKU page manually before purchasing hardware.

### Platform, privacy, and law

24. [Meta Wearables Developer Terms](https://wearables.developer.meta.com/terms) — last updated 6 October 2025; accessed 31 July 2026. Page extraction may show a login interstitial; the full current text must be reviewed while authenticated before reliance.
25. [Meta Wearables Developer Acceptable Use Policy](https://wearables.developer.meta.com/acceptable-use-policy) — last updated 22 September 2025; accessed 31 July 2026. Review while authenticated.
26. [Meta Supplemental Privacy Policy](https://www.meta.com/au/legal/privacy-policy/) — effective 29 June 2026; accessed 31 July 2026.
27. [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) — last updated 8 June 2026; accessed 31 July 2026.
28. [Google Play User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en-GB) — accessed 31 July 2026.
29. [OAIC: Photos and videos](https://www.oaic.gov.au/privacy/your-privacy-rights/social-media-and-online-privacy/photos-and-videos) — accessed 31 July 2026.
30. [OAIC: Small business and trading in personal information](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/small-business) — accessed 31 July 2026.
31. [Queensland Invasion of Privacy Act 1971](https://www.legislation.qld.gov.au/view/whole/html/inforce/current/act-1971-050) — current in-force consolidation accessed 31 July 2026.
32. [NSW Workplace Surveillance Act 2005](https://legislation.nsw.gov.au/view/html/inforce/current/act-2005-47) — official current-consolidation URL; automated retrieval was blocked on 31 July 2026, so the operative text and jurisdictional application require manual legal verification.

### Mobile media APIs

33. [Apple AVAssetWriter](https://developer.apple.com/documentation/avfoundation/avassetwriter) — accessed 31 July 2026.
34. [Apple AVAudioSession preferred input](https://developer.apple.com/documentation/avfaudio/avaudiosession/preferredinput) — accessed 31 July 2026.
35. [Android AudioRecord](https://developer.android.com/reference/android/media/AudioRecord) — accessed 31 July 2026.
36. [Android MediaMuxer](https://developer.android.com/reference/android/media/MediaMuxer.html) — accessed 31 July 2026.

### Datasets, research, formats, and competitors

37. [Ego4D](https://ego4d-data.org/docs/) — official dataset documentation; accessed 31 July 2026.
38. [Ego-Exo4D](https://docs.ego-exo4d-data.org/) — official dataset documentation; accessed 31 July 2026.
39. [EPIC-KITCHENS](https://epic-kitchens.github.io/) — official project; accessed 31 July 2026.
40. [Assembly101](https://assembly-101.github.io/) — official project; accessed 31 July 2026.
41. [DROID](https://droid-dataset.github.io/) — official project; accessed 31 July 2026.
42. [EgoMimic](https://arxiv.org/abs/2410.24221) — primary research paper; accessed 31 July 2026.
43. [Universal Manipulation Interface](https://arxiv.org/abs/2402.10329) — primary research paper; accessed 31 July 2026.
44. [Human2Sim2Robot](https://proceedings.mlr.press/v305/lum25a.html) — CoRL 2025/PMLR paper; accessed 31 July 2026.
45. [Project Aria Gen 2](https://facebookresearch.github.io/projectaria_tools/gen2/) — official Meta research documentation; accessed 31 July 2026.
46. [LeRobotDataset v3](https://huggingface.co/docs/lerobot/main/lerobot-dataset-v3) — official documentation; accessed 31 July 2026.
47. [RLDS](https://github.com/google-research/rlds) — official repository; accessed 31 July 2026.
48. [Open X-Embodiment](https://robotics-transformer-x.github.io/) — official project; accessed 31 July 2026.
49. [EgoScale](https://www.egoscale.com/) — company site, self-reported claims; accessed 31 July 2026.
50. [RoboData](https://robodata.dev/) — company site, self-reported claims; accessed 31 July 2026.
51. [Caspius](https://caspius.ai/) — company site; accessed 31 July 2026.
52. [Trillion UMI](https://trillionrobotics.ai/) — company site, self-reported specifications; accessed 31 July 2026.

---

## Verified facts

- DAT 0.8.0 provides invite-only mobile access to camera streaming, still capture, HFP microphone input, speaker output, sessions, thermal state, errors, and mock devices on supported Meta glasses.
- The developer video ceiling is 720 × 1280 at a requested maximum 30 fps, not the marketed consumer 3K modes.
- Microphone capture is 8 kHz mono HFP and beamformed toward the wearer.
- Public iOS App Store distribution is not currently supported; current DAT release channels are invite-only.
- The current public terms prohibit selling or licensing Technology Data and define it to include derived data.
- First-person RGB/audio lacks the state/action/force/pose signals required for direct robot behavior cloning.

## Assumptions

- DAT-captured media and its annotations would be treated as Technology Data; this is a strong textual inference requiring legal confirmation.
- Phone-side A/V muxing can be made reliable enough after measured clock correction.
- A buyer may value rights-cleared, task-specific error/recovery/outcome enrichment even when direct robot action is absent.
- iOS is the best first technical test platform under the current SDK, not necessarily the eventual product platform.

## Open questions

- Will Meta grant written permission or a separate agreement for commercial AI-training datasets and derivative models?
- What public or enterprise distribution scale is available, on what timetable and review criteria?
- What are actual A/V drift, dropout, thermal, battery, latency, storage, and delivered-quality distributions on each glasses/phone pair?
- Which buyer task can show measurable lift from enriched human video, and what supplementary telemetry does it require?
- Can consent, workplace access, privacy filtering, withdrawal, and deletion be operated economically across target jurisdictions?
- Does any non-DAT consumer-media workflow have suitable rights and automation, or should the capture endpoint change entirely?

## Recommended next step

Do not begin production coding. Prepare a one-page data-flow and revenue-model brief for Meta and legal counsel, seeking written clearance on the Technology Data sale/licensing restriction and distribution path. In parallel, recruit one qualified robotics/model buyer to define a single evaluation task and required schema. Only after both gates have a credible path should Phase 2 authorise the small, controlled iOS capture experiment described in section 10.6.
