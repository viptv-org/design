# Source this file: source /path/to/viptv-org/design/scripts/android-env.sh
viptv_workspace="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
export JAVA_HOME="$viptv_workspace/.tooling/jdk-17"
export ANDROID_HOME="$viptv_workspace/.tooling/android-sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
unset viptv_workspace
