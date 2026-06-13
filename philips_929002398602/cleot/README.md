# Philips Hue Dimmer Switch v2 (929002398602) — Event Entity Controller

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fcleot%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fphilips_929002398602%2Fcleot%2Fhue_dimmer_switch_929002398602.yaml)

Customizable controller automation for the **Philips Hue Dimmer Switch gen 2 (929002398602)** via **Zigbee2MQTT**, built on Home Assistant **event entities**. Each button can run any action; button activity is visible in the logbook, history, dashboards and the mobile app.

## Requirements

- Home Assistant + Zigbee2MQTT **2.x**
- Zigbee2MQTT → **Settings → Home Assistant integration → "Experimental event entities" → ON**

## Setup

1. Enable the experimental setting above and let Zigbee2MQTT restart.
2. **Press each button once** so HA discovers the `event.*` entities (one per button, all named `<device> Action`).
3. Import this blueprint (button above) and create an automation.
4. In **Action Event Entities**, select **all** of the dimmer's "Action" entities — the automation determines the button from the entity's `button` attribute at runtime.
5. Assign actions to the buttons you want.

## Supported buttons & gestures

| Button | Pressed | Held | Released | Hold Released |
|--------|:-------:|:----:|:--------:|:-------------:|
| On     | ✅ | ✅ | ✅ | ✅ |
| Off (Hue) | ✅ | ✅ | ✅ | ✅ |
| Up     | ✅ | ✅ | ✅ | ✅ |
| Down   | ✅ | ✅ | ✅ | ✅ |

> 💡 Prefer **Released** over **Pressed**: a short tap fires both `*_press` and `*_press_release`, and `*_press` also fires at the start of a hold. The binding-mode `recall` gesture is intentionally ignored (it only fires when the dimmer is bound directly to lights, bypassing HA).

## Notes

- **No MQTT topic or device name to type** — just pick the entities. Robust against device renames.
- Requires the experimental flag; if you'd rather avoid it, the raw-MQTT-topic blueprint in the parent folder works with zero setup but does not expose the buttons as HA entities.
