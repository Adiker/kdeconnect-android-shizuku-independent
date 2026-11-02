# KDE Connect Android with Shizuku clipboard sync

This unofficial fork is based on KDE Connect Android 1.37.0, including upstream
master commit `4de397e2`, and builds on Shoukaku39's earlier Shizuku clipboard work.

## What this fork adds to upstream

- Automatic background clipboard sync on Android 10+ through Shizuku. When Android
  denies the app a background clipboard read, a privileged Shizuku user service
  reads the clipboard and sends it back to KDE Connect.
- AIDL interfaces connecting the clipboard monitor service to the app, plus the
  Shizuku dependencies, provider, permission handling, and startup initialization.
- Integration with upstream's Kotlin clipboard listener, including propagation of
  Android's sensitive-clipboard flag so the existing privacy preference still applies.

The normal KDE Connect features are retained. The existing READ_LOGS clipboard
path remains available as a fallback when Shizuku is unavailable or unauthorized;
the app does not need READ_LOGS permission when the Shizuku service is used.

Compared with the earlier Shizuku fork, this implementation uses a dedicated
Shizuku user service and AIDL callbacks for privileged clipboard reads.

This independent repository tracks [KDE Connect Android](https://github.com/KDE/kdeconnect-android)
as its upstream. It retains the history and credits of the earlier Shizuku fork.

## Downloads

[Download the latest signed APK](https://github.com/Adiker/kdeconnect-android-shizuku-independent/releases/latest).
This repository uses its own signing key. Android requires uninstalling a build
signed with another key before installation; this clears local settings and pairings.
Future releases signed with this repository's key can update it in place.

## Build

With a compatible JDK and Android SDK 37 installed, run:

```sh
./gradlew --no-daemon --console=plain assembleDebug assembleRelease lintDebug testDebugUnitTest
```

The release APK is generated under `build/outputs/apk/release/` and uses
`org.kde.kdeconnect_tp`. Release tags matching `v*-shizuku*` trigger GitHub Actions
to test, build, sign, verify, and publish it. The workflow requires the repository
secrets `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`,
`ANDROID_KEY_ALIAS`, and `ANDROID_KEY_PASSWORD`.

The debug APK is generated at `build/outputs/apk/debug/kdeconnect-android-debug.apk`.
It uses `org.kde.kdeconnect_tp.debug` and the repository's existing debug signing key.

## Credits

- KDE for upstream KDE Connect.
- Shoukaku39 for the original Shizuku-enabled fork.
