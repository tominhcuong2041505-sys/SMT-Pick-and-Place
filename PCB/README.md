# ⚡ LPC-PnP Custom Mainboard

![Mainboard](Images/LPC1769_LPC-PnP_v1.2.png)

This repository contains the complete hardware design files for the **LPC-PnP** custom mainboard. This board is specifically engineered as the core interface bridge between the microcontroller (running Klipper firmware) and the mechatronic actuators of the Pick and Place system.

## 🌟 Hardware Features

* **Isolated Power & Protection:** Integrates a 10A fuse and an SS56 (5A/60V) Schottky diode for high-current reverse polarity protection. The 5V logic line is strictly noise-isolated from the 24V power line using a high-efficiency LMR14030 buck converter.
* **Silent Motion Control:** Features standard sockets for **TMC2209** stepper drivers. Direct UART communication with the MCU enables high microstepping and StealthChop2 mode, effectively eliminating mechanical resonance and vibration.
* **Inductive Load Switching:** Utilizes power MOSFETs paired with flyback diodes to safely drive heavy inductive loads, including the vacuum pump, Juki nozzle solenoid valves, and vision LED lighting.
* **DFM (Design for Manufacturing) Ready:** The PCB layout is fully optimized with synchronized origin points, making it deployment-ready for automated SMT assembly.

## 📁 Repository Files & Documentation

* **Schematic:** Circuit reference for logic verification, component routing, and signal debugging.
* **Block Diagram:** High-level overview of voltage distribution and subsystem communication architecture.
* **Gerber:** Complete manufacturing files (copper, silkscreen, solder mask) compressed and ready for direct fabrication via JLCPCB, PCBWay, or similar services.
* **BOM (Bill of Materials):** Standardized component list including MPNs (Manufacturer Part Numbers) and exact quantities, immediately compatible with automated BOM tools.
* **Assembly Top:** Component placement drawing stripped of redundant values to facilitate quick orientation and component alignment during manual soldering.
* **Drill Map:** Detailed specifications of coordinates and diameters for all vias and through-holes.
* **3D PCB:** Complete 3D STEP model of the populated board, ready to be imported into 3D CAD software for mechanical enclosure design.
