#!/usr/bin/env python3
import re

PREFIXES = {
    'p': 1e-12,
    'n': 1e-9,
    'u': 1e-6,
    'm': 1e-3,
    '': 1,
    'k': 1e3,
    'M': 1e6,
    'G': 1e9,
}

def parse_value(s):
    match = re.match(r'([\d.]+)\s*([pnumkMG]?)([FHL])', s, re.I)
    if not match:
        raise ValueError("Could not parse value.")
    value = float(match.group(1))
    prefix = match.group(2).lower()
    unit = match.group(3).upper()
    multiplier = PREFIXES.get(prefix, 1)
    return value * multiplier, unit

def format_impedance(z):
    abs_z = abs(z)

    if abs_z >= 1e6:
        scale = 1e6
        unit = "MΩ"
    elif abs_z >= 1e3:
        scale = 1e3
        unit = "kΩ"
    elif abs_z >= 1:
        scale = 1
        unit = "Ω"
    elif abs_z >= 1e-3:
        scale = 1e-3
        unit = "mΩ"
    elif abs_z >= 1e-6:
        scale = 1e-6
        unit = "μΩ"
    else:
        scale = 1e-9
        unit = "nΩ"

    z_scaled = z / scale

    parts = []
    if abs(z_scaled.real) > 1e-9:
        parts.append(f"{z_scaled.real:.3g}")
    if abs(z_scaled.imag) > 1e-9:
        sign = "+" if z_scaled.imag > 0 and parts else ""
        parts.append(f"{sign}{z_scaled.imag:.3g}j")
    if not parts:
        parts.append("0")

    # return " ".join(parts) + " " + unit

def main():
    try:
        omega = float(input("Enter angular frequency ω: "))
        print("Enter capacitance or inductance values.")
        while True:
            try:
                line = input("> ").strip()
                if not line:
                    continue
                value, unit = parse_value(line)
                if unit == 'F':
                    z = complex(0, -1/(omega*value))
                elif unit == 'H':
                    z = complex(0, omega*value)
                else:
                    print("Unit must be F (farads) or H (henries).")
                    continue
                print("Impedance:", format_impedance(z))
            except KeyboardInterrupt:
                print()
                break
            except Exception as e:
                print("Error:", e)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
