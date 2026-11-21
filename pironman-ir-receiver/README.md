# SunFounder Pironman 5 Max: standalone IR receiver for Home Assistant OS

> **Experimental / community testing — HAOS end-to-end validation pending.** This contribution is
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

## Testing the development version (v0.1.1)

The experimental Pironman IR Receiver add-on is available
for community testing before the official SunFounder release.

### Installation

1. Open the Home Assistant Add-on Store.
2. Add this repository:

   `https://github.com/ChristophKomenda/home-assistant-addon`

3. Refresh the repository.
4. Install **Pironman IR Receiver v0.1.1**.
5. Configure the add-on:

   ```yaml
   receiver_id: pironman5-max
   debug: true
   ```

6. Start the add-on and check its logs.
7. Copy the companion integration from
   `pironman-ir-receiver/ha_custom_component/sunfounder_ir/`
   into `/config/custom_components/sunfounder_ir/`.
8. Restart Home Assistant and configure the integration
   with the same `receiver_id`.
9. Open **HAIR > Sniffer** and select
   **SunFounder IR Receiver**.

If upgrading from an earlier experimental version,
refresh the repository and verify the installed version.
Back up the add-on options before reinstalling if necessary.

### Confirmed testing

Successfully tested with real IR hardware on a
Raspberry Pi 5 / Pironman 5 Max running Debian
and Home Assistant Container.

Verified signal path:

**IR remote → GPIO13 → LIRC → Docker bridge →
Home Assistant → InfraredReceiverEntity → HAIR Sniffer**

Real infrared signals appeared successfully in HAIR.

### Remaining validation

The complete Home Assistant OS workflow still requires
independent testing, particularly Supervisor authentication,
device mapping and end-to-end event delivery.

---

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

### Live end-to-end validation on Home Assistant Container (21 November 2026)

**Confirmed successful on real hardware:** Raspberry Pi 5 / Pironman 5 Max,
Debian host, and Home Assistant Container. A real IR remote was received through
GPIO13 and `/dev/lirc0`, processed by the standalone SunFounder Docker bridge,
forwarded to Home Assistant, handled by the native `InfraredReceiverEntity`,
and **displayed in the HAIR Sniffer**.

The Home Assistant custom integration was independently verified using a valid
REST API event: the receiver ID matched, 18 sample timings passed validation,
and `_handle_received_signal()` returned without error. Earlier manual events
contained empty data (`{}`), which explained their rejection; this was not
a confirmed defect in the integration.

**Important:** These tests validate Home Assistant **Container on Debian**,
**not Home Assistant OS**. Actual HAOS Supervisor proxy authentication, device
mapping, and complete HAOS-to-HAIR behavior still require confirmation by an
HAOS tester.

## Known limitations

Local Docker, real IR hardware, Home Assistant Container, and HAIR Sniffer have
now been tested successfully. HAOS Supervisor authentication, mapping, and
end-to-end HAIR functionality still require independent HAOS testing.
This contribution is open for review and community testing. Full Home Assistant OS end-to-end validation is still pending before final merge consideration.


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
