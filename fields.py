from typing import Any

# b_ver_count (51210): how many of the 4 MCU version slots at b_ver_1-4
# (51211-51218) are actually valid - confirmed by BLUETTI support directly
# ("for Balco260, typically only slot 1 is valid"), not previously mapped.
AMOUNT_FIELDS = [
    "d_num_inverters",
    "d_num_battery_packs",
    "b_cycle_count",
    "b_cell_count",
    "b_ntc_count",
    "b_ver_count",
]

BATTERY_SOC = [
    "b_soc_total",
    "b_soc",
]

BATTERY_SOH = [
    "b_soh_total",
    "b_soh",
]

ENUM_FIELDS = [
    "d_inverter_status",
    "d_inverter_warning",
    "d_inverter_fault",
    "d_inverter_1_status",
    "d_inverter_2_status",
    "d_inverter_3_status",
]

# Confirmed by the official Cassandra Protocol register list (BalcoXX/EBOX sheets).
PACK_TIME_FIELDS = [
    "b_time_to_full_total",
    "b_time_to_empty_total",
    "b_time_to_full",
    "b_time_to_empty",
]

PHASE_COUNT_FIELDS = [
    "d_phase_count",
    "ac_phase_count",
    "d_inverter_phase_count",
]

# Bitmap/status registers the official sheet documents the address for but not a
# decoded bit/value meaning for - same "raw uint, decode later" treatment this
# schema already gives d_inverter_warning/d_inverter_fault.
UNDECODED_BITMAP_FIELDS = [
    "b_protect",
    "b_error",
    "b_alarm_residential",
    "b_alarm_portable",
    "d_online_component",
    "d_alarm_status",
    "d_op_mod_connect",
]

# SunSpec/DER-style status enums (EP2000's EMS/grid-export block) - addresses are
# confirmed, but the value sets are complex/model-specific enough that this schema
# doesn't attempt to name them yet, same reasoning as UNDECODED_BITMAP_FIELDS.
UNDECODED_STATUS_FIELDS = [
    "d_operational_mode_status",
    "d_connection_status",
    "d_inverter_der_status",
    "d_local_control_mode_status",
    "d_storage_mode_status",
]

# EP2000's rated-capacity/EMS-control block - diagnostic/config values, not live
# telemetry, even where they happen to share a power-like unit with a real sensor.
EP2000_DIAGNOSTIC_FIELDS = [
    "d_rated_p_max",
    "d_rated_p_max_continuous",
    "d_rated_va_max_continuous",
    "d_rated_var_max_continuous",
    "d_rated_var_max_continuous_neg",
    "d_rated_pf_min_over_excited",
    "d_rated_pf_min_under_excited",
    "d_rated_v",
    "d_rated_f",
    "d_reactive_p_total",
    "d_apparent_p_total",
]

# Register count per field, for every new field whose official register count is
# not 1 - content type alone doesn't otherwise convey this (see field.json's own
# description of "length": "Data length if not set by content type"), the same
# reason d_inverter_warning/d_inverter_fault already set it explicitly. Fields
# with content "string" already carry their own length (set inline below/in the
# match block) and aren't repeated here.
MULTI_REGISTER_FIELD_LENGTHS: dict[str, int] = {
    "g_i_p_local": 2,
    "ac_o_p_local": 2,
    "pv_i_p_local": 2,
    "pv_ac_p_local": 2,
    "g_i_e_local": 2,
    "g_o_e_local": 2,
    "ac_o_e_local": 2,
    "pv_i_e_local": 2,
    "pv_ac_e_local": 2,
    "b_serial": 4,
    "b_ver_1": 2,
    "b_ver_2": 2,
    "b_ver_3": 2,
    "b_ver_4": 2,
    "b_protect": 2,
    "b_error": 3,
    "b_alarm_portable": 2,
    "d_reactive_p_total": 2,
    "d_apparent_p_total": 2,
    "b_p": 2,
    "d_rated_p_max": 2,
    "d_rated_p_max_continuous": 2,
    "d_rated_va_max_continuous": 2,
    "d_rated_var_max_continuous": 2,
    "d_rated_var_max_continuous_neg": 2,
    "d_rated_pf_min_over_excited": 2,
    "d_rated_pf_min_under_excited": 2,
    "g_1_p_active": 2,
    "g_2_p_active": 2,
    "g_3_p_active": 2,
    "g_1_p_reactive": 2,
    "g_2_p_reactive": 2,
    "g_3_p_reactive": 2,
    "g_1_p_apparent": 2,
    "g_2_p_apparent": 2,
    "g_3_p_apparent": 2,
    "d_inverter_1_p_active_internal": 2,
    "d_inverter_2_p_active_internal": 2,
    "d_inverter_3_p_active_internal": 2,
    "d_p_active_target_l1": 2,
    "d_p_active_target_l2": 2,
    "d_p_active_target_l3": 2,
    "d_p_reactive_target_l1": 2,
    "d_p_reactive_target_l2": 2,
    "d_p_reactive_target_l3": 2,
    "d_p_apparent_target_l1": 2,
    "d_p_apparent_target_l2": 2,
    "d_p_apparent_target_l3": 2,
    "d_export_limit": 2,
    "d_storage_set_point": 2,
    "d_op_mod_gen_lim_w": 2,
    "d_op_mod_load_lim_w": 2,
}


def create_special_fields(n: str, field: dict[str, Any], com: str):
    if n in AMOUNT_FIELDS:
        field["content"] = "uint"
        field["category"] = "diagnostic"

    if n in BATTERY_SOC:
        field["content"] = "uint"
        field["unit"] = "%"
        field["num_min"] = 0
        field["num_max"] = 100
        field["state_class"] = "measurement"
        field["device_class"] = "battery"

    if n in BATTERY_SOH:
        field["content"] = "uint"
        field["unit"] = "%"
        field["num_min"] = 0
        field["num_max"] = 100
        field["category"] = "diagnostic"
        field["state_class"] = "measurement"

    if n in ENUM_FIELDS:
        field["content"] = "enum"
        field["category"] = "diagnostic"

    if n in PACK_TIME_FIELDS:
        field["content"] = "uint"
        field["unit"] = "min"
        field["category"] = "diagnostic"

    if n in PHASE_COUNT_FIELDS:
        field["content"] = "uint"
        field["category"] = "diagnostic"

    if n in UNDECODED_BITMAP_FIELDS or n in UNDECODED_STATUS_FIELDS:
        field["content"] = "uint"
        field["category"] = "diagnostic"
        # A few of these names contain "_mode_" (d_operational_mode_status,
        # d_storage_mode_status, d_local_control_mode_status), which the generic
        # suffix inference above treats as a writeable, named-options enum - not
        # right for a status register this schema leaves undecoded. Clear it back
        # out.
        field.pop("options", None)
        field.pop("writeable", None)

    if n in EP2000_DIAGNOSTIC_FIELDS:
        field["content"] = "int"
        field["category"] = "diagnostic"
        # Static ratings, not live telemetry - no state_class/device_class even
        # where the name happens to match a live sensor's suffix convention. Most
        # of this block has no unit in the official sheet either (only
        # d_rated_v/d_rated_f do - see their own cases below), so drop any unit
        # a suffix match may have guessed rather than assert one that isn't
        # actually confirmed.
        field.pop("state_class", None)
        field.pop("device_class", None)
        field.pop("unit", None)

    match (n):
        case "d_inverter_total":
            field["content"] = "uint"
            field["unit"] = "W"
            field["state_class"] = "measurement"
            field["device_class"] = "power"
        case "d_inverter_status":
            field["options"] = "inverter_status"
        case "d_inverter_warning":
            field["options"] = "inverter_warning"
        case "d_inverter_fault":
            field["options"] = "inverter_fault"
        case "d_inverter_type":
            field["content"] = "string"
            field["length"] = 6
            field["category"] = "diagnostic"
        case "b_type":
            field["content"] = "string"
            field["length"] = 6
            field["category"] = "diagnostic"
        case "b_cycle_count":
            field["state_class"] = "measurement"
        case "b_soc_low":
            field["content"] = "uint"
            field["unit"] = "%"
            field["num_min"] = 0
            field["num_max"] = 100
            field["writeable"] = True
            field["category"] = "config"
        case "b_soc_high":
            field["content"] = "uint"
            field["unit"] = "%"
            field["num_min"] = 0
            field["num_max"] = 100
            field["writeable"] = True
            field["category"] = "config"
        case "d_time_remaining":
            field["content"] = "uint"
            field["unit"] = "h"
            field["scale"] = 0.1
        case "d_power_off":
            field["content"] = "bool"
            field["writeable"] = True
        case "dc_eco_mode":
            field["options"] = "eco_mode"
        case "ac_eco_mode":
            field["options"] = "eco_mode"
        case "d_charging_mode":
            field["options"] = "charging_mode"
        case "ac_o_mode":
            field["options"] = "output_mode"
        case "ac_ups_mode":
            field["options"] = "ups_mode"
        case "d_display_mode":
            field["options"] = "display_mode"
        case "d_split_phase_mode":
            field["options"] = "split_phase_mode"
        case "d_led_mode":
            field["options"] = "led_mode"
        case "d_inverter_1_status" | "d_inverter_2_status" | "d_inverter_3_status":
            # Same options table as d_inverter_status (50022) - its [0..7] value
            # set is a superset of this per-inverter field's own [0..5] range.
            field["options"] = "inverter_status"
        case "b_status":
            field["content"] = "enum"
            field["options"] = "pack_charging_status"
            field["category"] = "diagnostic"
        case "pv_1_i_type" | "pv_2_i_type" | "pv_3_i_type" | "pv_4_i_type":
            # Reintroducing this after commit 8f5dadd reverted the same idea:
            # that attempt's PvType enum only covered 0-3 (reserve/car/
            # adapter/other) and never mapped 100/101 (DC PV/AC PV, "only
            # available on some models" per the official sheet's remark
            # column) - and every real Balco260 reports 100, so every real
            # read hit modbus_connection's "no mapping" fallback. This isn't
            # a d_ems_ctrl-style unmodeled control register (see that case
            # above) - it's exactly 6 well-defined values, just non-
            # sequential ones. bluetti-modbus-lib's hand-written PvType enum
            # class (unlike this schema's own positional enum arrays, which
            # can't cleanly represent a jump to 100) has no trouble encoding
            # arbitrary int values, so this time all 6 are covered.
            field["content"] = "enum"
            field["options"] = "pv_type"
            field["category"] = "diagnostic"
        case "pv_dc_count" | "pv_ac_count":
            # Both pack into the same register (50267, "PV connection
            # quantity per inverter") - bit0-3: number of DC PV strings,
            # bit4-7: number of AC PV strings (the official sheet's own
            # remark column) - the same "documented bits inside a register"
            # situation bit_flag() already handles for d_status on S Meter,
            # just two 4-bit counts instead of one bit. Was one undecoded
            # "pv_count" uint (UNDECODED_BITMAP_FIELDS above); split into
            # these two named fields at the same address instead. The actual
            # nibble extraction is bluetti-modbus-lib's job (import.py), not
            # this schema's - it only needs the field to exist and read as a
            # plain uint, same as every other special-decode field here
            # (b_c, d_status).
            field["content"] = "uint"
            field["category"] = "diagnostic"
        case "d_self_consumption":
            field["content"] = "uint"
            field["unit"] = "%"
            field["num_min"] = 0
            field["num_max"] = 100
            field["state_class"] = "measurement"
        case "d_iot_model":
            field["content"] = "string"
            field["length"] = 6
            field["category"] = "diagnostic"
        case "d_manufacturer":
            field["content"] = "string"
            field["length"] = 16
            field["category"] = "diagnostic"
        case "d_rated_v":
            field["content"] = "uint"
            field["unit"] = "V"
            field["category"] = "diagnostic"
        case "d_rated_f":
            field["content"] = "uint"
            field["unit"] = "Hz"
            field["scale"] = 0.01
            field["category"] = "diagnostic"
        case "d_ems_ctrl" | "d_battery_control" | "d_ramp_rate":
            # Control-mode registers with sparse/non-positional value sets (see
            # the official sheet's own remarks) - not modeled as a named enum.
            field["content"] = "uint"
            field["writeable"] = True
            field["category"] = "config"
        case "d_export_limit" | "d_storage_set_point" | "d_op_mod_gen_lim_w" | "d_op_mod_load_lim_w":
            field["content"] = "uint"
            field["unit"] = "W"
            field["writeable"] = True
            field["category"] = "config"
        case "d_hw_ver":
            # ASCII per the official sheet ("HwVer:5.0"), unlike every other
            # _ver field in this schema (which are numeric) - overrides the
            # generic _ver suffix inference below.
            field["content"] = "string"
            field["length"] = 2
            field["category"] = "diagnostic"

    # Bluetooth register
    if com == "b":
        return field

    # Modbus-TCP register

    # voltage need scaling 0.1 on modbus-tcp - except d_rated_v, whose official
    # unit is a plain "1V" (no scaling), unlike every other _v field in this
    # schema.
    if ("_v_" in n or n.endswith("_v")) and n != "d_rated_v":
        field["scale"] = 0.1

    # enums need length on modbus-tcp
    if n == "d_inverter_warning":
        field["length"] = 4
    if n == "d_inverter_fault":
        field["length"] = 5

    if n in MULTI_REGISTER_FIELD_LENGTHS:
        field["length"] = MULTI_REGISTER_FIELD_LENGTHS[n]

    # b_i_e on modbus-tcp is Wh and needs no scale
    # b_o_e on modbus-tcp is Wh and needs no scale
    if n in ["b_i_e", "b_o_e"]:
        del field["scale"]
        field["unit"] = "Wh"

    return field
