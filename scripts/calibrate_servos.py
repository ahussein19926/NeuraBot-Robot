"""
NeuraBot Servo Calibration Script
Steps through each servo for mechanical alignment verification.
"""

import time
import yaml
import sys
from loguru import logger

def main():
    logger.info("=== NeuraBot Servo Calibration ===")

    try:
        with open("config/config.yaml") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/config.yaml not found. Run: cp config/config.example.yaml config/config.yaml")
        sys.exit(1)

    from src.control.comm_manager import CommManager
    comm = CommManager(config["comm"])
    comm.connect()

    legs   = ["FL", "FR", "RL", "RR"]
    joints = ["hip", "thigh", "knee"]
    trims  = {}

    print("\nThis script will move each servo to its neutral position (0°).")
    print("Verify the leg looks mechanically correct, then press Enter.\n")

    for leg in legs:
        trims[leg] = {}
        for joint in joints:
            print(f"  Moving {leg} {joint} to neutral (0°)...", end=" ", flush=True)

            angles = {l: {"hip": 0.0, "thigh": 0.0, "knee": 0.0} for l in legs}
            comm.send_motion(angles)
            time.sleep(0.5)

            trim = input(f"Trim offset for {leg} {joint} (0 = looks good, or enter degrees): ").strip()
            try:
                trims[leg][joint] = float(trim) if trim else 0.0
            except ValueError:
                trims[leg][joint] = 0.0

    # Save trims
    with open("config/servo_trims.yaml", "w") as f:
        yaml.dump(trims, f)

    logger.success("Servo trims saved to config/servo_trims.yaml")
    logger.info("Calibration complete!")

    comm.disconnect()

if __name__ == "__main__":
    main()
