"""
Medium Transmission Line Calculator
====================================

Power Systems-II | Electrical Engineering

This program analyzes a medium transmission line using
the Nominal-T method.

Calculates:
1. Total series impedance (Z)
2. Total shunt admittance (Y)
3. ABCD parameters
4. Sending-end voltage
5. Sending-end current
6. Voltage regulation
7. Sending-end and receiving-end power
8. Transmission efficiency

Nominal-T equations:

        ZY
A = D = 1 + ---
        2

             ZY
B = Z * (1 + ---)
              4

             ZY
C = Y * (1 + ---)

Sending-end equations:

Vs = A*Vr + B*Ir
Is = C*Vr + D*Ir
"""

import cmath
import math


def polar_to_complex(magnitude, angle_degrees):
    """Convert polar form to rectangular complex form."""
    angle_radians = math.radians(angle_degrees)
    return cmath.rect(magnitude, angle_radians)


def polar_form(value):
    """Return magnitude and angle of a complex number."""
    magnitude = abs(value)
    angle = math.degrees(cmath.phase(value))
    return magnitude, angle


def calculate_parameters(length, resistance_per_km,
                         reactance_per_km, capacitance_microfarad_per_km,
                         frequency):
    """Calculate Z, Y and ABCD parameters."""

    # Total series impedance
    R = resistance_per_km * length
    X = reactance_per_km * length

    Z = complex(R, X)

    # Total capacitance
    capacitance = capacitance_microfarad_per_km * length * 1e-6

    # Shunt admittance Y = jωC
    omega = 2 * math.pi * frequency
    Y = complex(0, omega * capacitance)

    # Nominal-T ABCD parameters
    A = 1 + (Y * Z) / 2
    D = A

    B = Z * (1 + (Y * Z) / 4)

    C = Y * (1 + (Y * Z) / 4)

    return Z, Y, A, B, C, D


def calculate_sending_end(Vr, Ir, A, B, C, D):
    """Calculate sending-end voltage and current."""

    Vs = A * Vr + B * Ir
    Is = C * Vr + D * Ir

    return Vs, Is


def main():

    print("=" * 65)
    print("       MEDIUM TRANSMISSION LINE CALCULATOR")
    print("                 NOMINAL-T METHOD")
    print("                    POWER SYSTEMS-II")
    print("=" * 65)

    try:

        # ---------------- INPUT ----------------

        length = float(
            input("\nEnter transmission line length (km): ")
        )

        resistance = float(
            input("Enter resistance per km (ohm/km): ")
        )

        reactance = float(
            input("Enter reactance per km (ohm/km): ")
        )

        capacitance = float(
            input("Enter capacitance per km (microF/km): ")
        )

        frequency = float(
            input("Enter system frequency (Hz): ")
        )

        Vr_magnitude = float(
            input("Enter receiving-end voltage (V): ")
        )

        Vr_angle = float(
            input("Enter receiving-end voltage angle (degrees): ")
        )

        Ir_magnitude = float(
            input("Enter receiving-end current (A): ")
        )

        Ir_angle = float(
            input("Enter receiving-end current angle (degrees): ")
        )

        # ---------------- VALIDATION ----------------

        if length <= 0:
            raise ValueError("Line length must be greater than zero.")

        if resistance < 0:
            raise ValueError("Resistance cannot be negative.")

        if reactance < 0:
            raise ValueError("Reactance cannot be negative.")

        if capacitance < 0:
            raise ValueError("Capacitance cannot be negative.")

        if frequency <= 0:
            raise ValueError("Frequency must be greater than zero.")

        if Vr_magnitude <= 0:
            raise ValueError("Voltage must be greater than zero.")

        if Ir_magnitude < 0:
            raise ValueError("Current cannot be negative.")

        # Convert polar quantities to complex form
        Vr = polar_to_complex(
            Vr_magnitude,
            Vr_angle
        )

        Ir = polar_to_complex(
            Ir_magnitude,
            Ir_angle
        )

        # ---------------- CALCULATIONS ----------------

        Z, Y, A, B, C, D = calculate_parameters(
            length,
            resistance,
            reactance,
            capacitance,
            frequency
        )

        # Sending-end voltage and current
        Vs, Is = calculate_sending_end(
            Vr, Ir, A, B, C, D
        )

        # Polar values
        Z_mag, Z_angle = polar_form(Z)
        Y_mag, Y_angle = polar_form(Y)

        Vs_mag, Vs_angle = polar_form(Vs)
        Is_mag, Is_angle = polar_form(Is)

        # ---------------- POWER CALCULATIONS ----------------

        receiving_power = (
            3 * abs(Vr) * abs(Ir)
            * math.cos(
                math.radians(Vr_angle - Ir_angle)
            )
        )

        sending_power = (
            3 * abs(Vs) * abs(Is)
            * math.cos(
                math.radians(Vs_angle - Is_angle)
            )
        )

        # Voltage regulation
        voltage_regulation = (
            (abs(Vs) - abs(Vr))
            / abs(Vr)
        ) * 100

        # Efficiency
        efficiency = (
            receiving_power / sending_power
        ) * 100

        # ---------------- OUTPUT ----------------

        print("\n" + "=" * 65)
        print("                    RESULTS")
        print("=" * 65)

        print("\nTRANSMISSION LINE PARAMETERS")
        print("-" * 65)

        print(
            f"Total Resistance (R)       : "
            f"{Z.real:.4f} ohm"
        )

        print(
            f"Total Reactance (X)        : "
            f"{Z.imag:.4f} ohm"
        )

        print(
            f"Series Impedance (Z)       : "
            f"{Z.real:.4f} + j{Z.imag:.4f} ohm"
        )

        print(
            f"                           : "
            f"{Z_mag:.4f} ∠ {Z_angle:.2f}° ohm"
        )

        print(
            f"\nShunt Admittance (Y)       : "
            f"{Y.real:.6f} + j{Y.imag:.6f} S"
        )

        print(
            f"                           : "
            f"{Y_mag:.6f} ∠ {Y_angle:.2f}° S"
        )

        print("\nABCD PARAMETERS - NOMINAL T")
        print("-" * 65)

        print(
            f"A = {A.real:.6f} + j{A.imag:.6f}"
        )

        print(
            f"B = {B.real:.6f} + j{B.imag:.6f} ohm"
        )

        print(
            f"C = {C.real:.6f} + j{C.imag:.6f} S"
        )

        print(
            f"D = {D.real:.6f} + j{D.imag:.6f}"
        )

        print("\nSENDING-END QUANTITIES")
        print("-" * 65)

        print(
            f"Sending-End Voltage       : "
            f"{Vs_mag:.2f} ∠ {Vs_angle:.2f}° V"
        )

        print(
            f"Sending-End Current       : "
            f"{Is_mag:.2f} ∠ {Is_angle:.2f}° A"
        )

        print("\nPOWER SYSTEM PERFORMANCE")
        print("-" * 65)

        print(
            f"Receiving-End Power       : "
            f"{receiving_power:.2f} W"
        )

        print(
            f"Sending-End Power         : "
            f"{sending_power:.2f} W"
        )

        print(
            f"Voltage Regulation        : "
            f"{voltage_regulation:.2f} %"
        )

        print(
            f"Transmission Efficiency   : "
            f"{efficiency:.2f} %"
        )

        print("=" * 65)

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
