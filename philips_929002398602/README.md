# Philips Hue Dimmer Switch v2 (929002398602)

Home Assistant **controller blueprints** for the Philips Hue Dimmer Switch gen 2 (model `929002398602`), used with **Zigbee2MQTT**. Map every button (On, Off/Hue, Up, Down) and gesture (press, hold, release, hold-release) to any action.

This folder contains one recommended blueprint plus two alternatives kept as backups.

---

## ⭐ Recommended — Event Entity Controller (`cleot`)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fcleot%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fphilips_929002398602%2Fcleot%2Fhue_dimmer_switch_929002398602.yaml)

**[`cleot/hue_dimmer_switch_929002398602.yaml`](cleot/hue_dimmer_switch_929002398602.yaml)** — full docs in **[cleot/README.md](cleot/README.md)**

Built on Home Assistant **event entities** (Zigbee2MQTT 2.x). You pick the dimmer's action event entities from a dropdown — no MQTT topic or device-name strings to type — and because it uses native HA entities, button activity shows up in the **logbook, history, dashboards and the mobile app**.

- ✅ Dropdown entity picker, no topic strings
- ✅ Native HA visibility (logbook / history / app)
- ✅ All 16 button + gesture combinations
- ⚠️ Requires Zigbee2MQTT → **"Experimental event entities"** enabled (one-time setting)

---

## Alternative / backup blueprints

These work too and are kept as fallbacks — useful if you don't want to enable the experimental event-entity setting, or want the most dependency-free option.

### Raw-MQTT-topic Controller (`patpac9`)

**[`patpac9/Hue_Dimmer_Switch_Easy_Custom_Buttons.yaml`](patpac9/Hue_Dimmer_Switch_Easy_Custom_Buttons.yaml)** · [import](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fcleot%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fphilips_929002398602%2Fpatpac9%2FHue_Dimmer_Switch_Easy_Custom_Buttons.yaml)

Subscribes directly to the device's Zigbee2MQTT topic. **Zero setup** and the most robust option — it reads the raw MQTT payload, so it's immune to Home Assistant discovery/registry changes. Trade-off: you type the device's Zigbee2MQTT friendly name, and the buttons aren't exposed as HA entities.

### Hooks-compatible Controller (`EPMatt`)

**[`EPMatt-awesome-ha-blueprints-philips_929002398602/philips_929002398602.yaml`](EPMatt-awesome-ha-blueprints-philips_929002398602/philips_929002398602.yaml)** · [import](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fcleot%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fphilips_929002398602%2FEPMatt-awesome-ha-blueprints-philips_929002398602%2Fphilips_929002398602.yaml)

A patched copy of the [Awesome HA Blueprints](https://github.com/EPMatt/awesome-ha-blueprints) controller. Supports **ZHA and Zigbee2MQTT** via device triggers and integrates with the project's [Hooks](https://epmatt.github.io/awesome-ha-blueprints/docs/blueprints/hooks) ecosystem (media players, lights, covers, …). Local fixes: added `model_id` / bare-model MQTT device filters so the device shows up under Z2M 2.x, plus the missing up/down release actions.

---

## Which should I use?

| | `cleot` (event entity) | `patpac9` (MQTT topic) | `EPMatt` (device triggers) |
|---|:---:|:---:|:---:|
| Setup effort | Enable 1 Z2M flag | None | None |
| Device selection | Entity dropdown | Type Z2M name | Device dropdown |
| Visible in HA (logbook/app) | ✅ | ❌ | partial |
| Robust to HA discovery changes | ⚠️ | ✅ | ⚠️ |
| ZHA support | ❌ | ❌ | ✅ |
| Hooks ecosystem | ❌ | ❌ | ✅ |

**Most people:** start with **`cleot`**. Want zero setup or maximum robustness? Use **`patpac9`**. Need ZHA or Hooks? Use **`EPMatt`**.
