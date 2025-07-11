KMK-Based 10-Key Macropad

A fully custom 10-key macropad built around a Seeed Studio XIAO RP2040 and powered by KMK firmware. All electronics, PCB layouts, and enclosure parts were designed by hand in KiCad and 3D-printed for a seamless, integrated build.

🔧 Hardware Components

Microcontroller: Seeed Studio XIAO RP2040

Switches: 8 × 1U + 2 × 2U MX-compatible (with stabilizers on the 2U keys)

Diodes: 10 × 1N4148 (for full N-key rollover)

Capacitors: 0.1 µF and 1 µF (decoupling for XIAO)

Mounting: M2 screws (PCB mounts directly into the printed case)

🛠️ 3D Printing

Files: Print 3D_Model/Main.stl, 3D_Model/Plate.stl, and 3D_Model/Knob.stl.


🖨️ PCB Fabrication

Gerbers: Use PCB/hxkeysair_gerber.zip for your PCB.


🧩 Assembly

Populate PCB

Solder XIAO RP2040 header, diodes, decoupling caps.

Switches

Insert switches into PCB; add stabilizers to the two 2U keys.

Case Mount

Align PCB holes with case; secure using M2 screws.

Attach Knob

Press-fit the knob onto the encoder shaft (if applicable).


💾 Firmware & Flashing

Install KMK
pip install kmk



2. **Customize**: Edit `firmware/config.py` and `firmware/keymap.py` for your layout.  
3. **Build & Flash**  
   - Enter bootloader (press BOOT on XIAO while plugging in).  
   - Copy the generated `firmware.uf2` onto the mounted drive.


## 🚀 Usage

- Boot up your macropad; it will auto-run the KMK firmware.  
- Hold your layer key to switch layers or use macros defined in `keymap.py`.  
- To update your keymap, edit the Python files and re-flash.


📄 License

This project is licensed under the MIT License. See LICENSE for details.

© 2025 Hsinwei Hsu

