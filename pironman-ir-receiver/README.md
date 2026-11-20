# SunFounder Pironman 5 Max: standalone IR receiver for Home Assistant OS

> **Draft / experimental — not yet HAOS hardware-tested.** This contribution is
> an independently implemented feature for SunFounder's add-on repository. It
> does not require `ChristophKomenda/pironman5-homeassistant-container`, its IR
> host bridge, or its `pironman5` Home Assistant integration.

This optional add-on reads the Pironman 5 Max's **built-in IR receiver on GPIO13**
through the Linux LIRC MODE2 character device `/dev/lirc0`, and forwards raw
pulse/space frames as `sunfounder_ir_received` events using the Home Assistant
Supervisor token. An included **separate** Home Assistant integration exposes a
native `InfraredReceiverEntity`, suitable for HAIR's Sniffer.

This is **receive-only**. It does not turn the IR receiver into a transmitter.

## Requirements

- Raspberry Pi 5 with Pironman 5 Max; Home Assistant OS on aarch64.
- Home Assistant Core **2026.6+**, with the native infrared receiver platform.
- Kernel configured with `dtoverlay=gpio-ir,gpio_pin=13` and `/dev/lirc0`
  available on the host. Exact HAOS boot-overlay procedure must be verified for
  the user's installation; do not change boot partitions blindly.
- HAIR installed if learning remotes is desired.

## Install (once the PR is merged into the SunFounder add-on repository)

1. In **Settings > Add-ons / Apps > Add-on Store**, add the official SunFounder
   repository `https://github.com/sunfounder/home-assistant-addon` if needed.
2. Install **Pironman IR Receiver**. This is separate from the main Pironman 5
   Max add-on, so existing fan, RGB and display operations are unaffected.
3. Confirm `/dev/lirc0` exists. The app requires this device to start.
4. Configure `receiver_id` (e.g. `pironman5-max`) and start the app.
5. Copy `ha_custom_component/sunfounder_ir/` to Home Assistant's
   `/config/custom_components/sunfounder_ir/` and restart Home Assistant.
6. Under **Settings > Devices & Services > Add Integration**, choose
   **SunFounder IR Receiver**, using the **same** receiver ID.
7. Open HAIR > Sniffer and select the SunFounder receiver.

The custom component is an independent manually installed companion; add-on
installation **does not automatically install custom integrations**. A later
HACS listing could streamline this without adding a dependency on another
project.

## Security / behavior

- Uses `homeassistant_api: true` and the app-injected `SUPERVISOR_TOKEN`;
  users do not need to create a long-lived Home Assistant token.
- No cloud, public port, MQTT or privileged container access.
- Device access is restricted to `/dev/lirc0` instead of `full_access`.
- Signal carrier frequency is unknown on basic GPIO receivers; modulation
  is `None`. RC-5 toggle remains encoded in raw timings; no application-level
  press/release state is synthesized.
- Loss of connectivity to Home Assistant may drop frames; the bridge does not
  provide guaranteed buffering or retransmission.
- When the receiver device is absent, Supervisor may refuse to start the app
  due to the explicit device mapping; this is expected.
- Linux `/dev/lircN` enumeration can differ between systems; this first
  version intentionally supports `/dev/lirc0` only.

## Development tests

```bash
python3 -m unittest discover -s pironman-ir-receiver/tests -v
```

## Known limitations

The add-on image build, actual GPIO/LIRC device access on HAOS, Supervisor event
forwarding, and full HAIR end-to-end flow require testing on real hardware.
Please keep this PR as a **draft** until that validation succeeds.


## Diagnostics: optional debug logging

Set `debug: true` in the **Pironman IR Receiver** app options and restart the
app. The logs will include `Captured IR frame (N timings)` when the hardware
produces a complete frame and `IR event delivered (HTTP 200, ...)` when the
Supervisor event endpoint accepts it. Avoid posting unredacted logs containing
private details or access tokens. Normal operation defaults to `debug: false`.

If HAIR detects the receiver entity but does not display signals:

1. Check that the **Pironman IR Receiver** app is running (not just the custom
   integration). The custom integration alone cannot read `/dev/lirc0`.
2. With `debug: true`, press an IR remote button. If no captured frames are
   logged, check the GPIO13 overlay, `/dev/lirc0` mapping and whether another
   process is consuming the LIRC stream.
3. If captured frames appear but no delivery messages follow, check for
   Supervisor HTTP errors and confirm `homeassistant_api: true`.
4. In Home Assistant Developer Tools > Events, listen for
   `sunfounder_ir_received`. The `receiver_id` in the event must match the ID
   configured in the **SunFounder IR Receiver** custom integration.
5. If events arrive, select **SunFounder IR Receiver** in HAIR > Sniffer rather
   than a different Pironman or ESPHome receiver.

The Dockerfile uses `with-contenv` when launching Python because Home Assistant
base images run s6-overlay and environment variables injected into the app
(including `SUPERVISOR_TOKEN`) need to be restored for that process.

### Independent local smoke test (not a substitute for HAOS hardware testing)

Build with the configured `BUILD_FROM` argument and use a mock Supervisor HTTP
endpoint to validate event requests. Successful HTTP 200 responses from a mock
server prove request delivery only; they do **not** prove Supervisor
permissions or native HAIR decoding on actual Home Assistant OS.
