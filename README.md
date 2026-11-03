# 🏭 LPC-PnP: SMT Pick and Place Machine

![PnP Machine Demo](Images/LPC-PnP.png)

## 📌 TL;DR (Project Overview)
A custom-built desktop Pick and Place (PnP) machine integrating Klipper firmware and OpenPnP computer vision for PCB assembly. 

**🔥 Latest Milestone:** Successfully achieved high-repeatability placement for **0603, 0805, and 1206 SMD packages**.

## 👨‍💻 My Core Contributions
In this 2-person mechatronics project, my partner handled 3D mechanical design while I was strictly responsible for **Firmware, Software Integration, and Hardware Testing**:

- **Firmware & OS:** Configured **Klipper** on an SKR v1.4 mainboard, establishing hardware UART communication with a Raspberry Pi.
- **Computer Vision Integration:** Configured **OpenPnP** Top/Bottom cameras for component alignment and developed custom G-code macros for vacuum/nozzle control.
- **Hardware Assembly & Validation:** Executed manual soldering (THT & basic SMD 0603/0805) for the custom mainboard. Validated power and logic circuits using a multimeter.
- **Kinematic Tuning:** Calibrated axis steps, acceleration, and endstop logic, enabling the stable placement of small 0603/0805 components.

## 🛠️ Tech Stack & Skills
- **Hardware/MCU:** Raspberry Pi 3, SKR v1.4, Custom PCB
- **Software:** Python, G-code, Klipper, OpenPnP, KiCad
- **Hands-on Skills:** Manual Soldering (THT & Basic SMD), Hardware Validation, System Integration, API Bridge

## 📊 Current Status
- ✅ **Mechanics & Framework:** Assembled and tested.
- ✅ **Firmware & API Bridge:** Stable Host-MCU communication.
- ✅ **Placement Validation:** High accuracy for 2-pad components (0603, 0805, 1206).
- 🔄 **Custom Mainboard:** Optimizing KiCad layout for final SMT manufacturing.
- 🔄 **Advanced Vision:** Upgrading recognition algorithms for multi-pad ICs.
