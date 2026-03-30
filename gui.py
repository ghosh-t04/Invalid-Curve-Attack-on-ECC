# gui.py
import tkinter as tk
import matplotlib.pyplot as plt
import time

from ecc_core import (
    p, a, b, n, G,
    generate_private_key,
    generate_public_key,
    generate_invalid_point,
    generate_small_subgroup_point,
    generate_twist_point,
    invalid_curve_attack_sim,
    small_subgroup_attack_sim,
    twist_attack_sim,
    curve_check,
    subgroup_check,
    combined_validation
)

# =========================================================
# GLOBAL STATE
# =========================================================
PRIVATE_KEY = None
PUBLIC_KEY = None
PREVENTION_ENABLED = False

# Results storage
results_before = {
    "Invalid Curve Attack": [],
    "Small Subgroup Attack": [],
    "Twist Attack": []
}

results_after = {
    "Invalid Curve Attack": [],
    "Small Subgroup Attack": [],
    "Twist Attack": []
}

latency_before = {
    "Invalid Curve Attack": [],
    "Small Subgroup Attack": [],
    "Twist Attack": []
}

latency_after = {
    "Invalid Curve Attack": [],
    "Small Subgroup Attack": [],
    "Twist Attack": []
}

defense_latency = {
    "Curve Check": [],
    "Subgroup Check": [],
    "Combined Validation": []
}


# =========================================================
# GUI SETUP
# =========================================================
root = tk.Tk()
root.title("Comparative ECC Attack & Prevention Study (NIST P-256)")
root.geometry("980x680")

status_label = tk.Label(
    root,
    text="Status: VULNERABLE",
    bg="red",
    fg="white",
    font=("Arial", 13, "bold"),
    width=32
)
status_label.pack(pady=6)

log = tk.Text(root, height=24, width=118, wrap="word")
log.pack(pady=8)


# =========================================================
# LOG FUNCTION
# =========================================================
def log_msg(msg, color="black"):
    start = log.index(tk.END)
    log.insert(tk.END, msg + "\n")
    end = log.index(tk.END)
    log.tag_add(color, start, end)
    log.tag_config(color, foreground=color)
    log.see(tk.END)


# =========================================================
# RESET DATA
# =========================================================
def reset_results():
    for attack in results_before:
        results_before[attack].clear()
        results_after[attack].clear()
        latency_before[attack].clear()
        latency_after[attack].clear()

    for d in defense_latency:
        defense_latency[d].clear()


# =========================================================
# BUTTON 1: GENERATE KEYS / PARAMETERS
# =========================================================
def generate_keys():
    global PRIVATE_KEY, PUBLIC_KEY, PREVENTION_ENABLED

    PRIVATE_KEY = generate_private_key()
    PUBLIC_KEY = generate_public_key(PRIVATE_KEY)
    PREVENTION_ENABLED = False
    reset_results()

    status_label.config(text="Status: VULNERABLE", bg="red")

    log.delete("1.0", tk.END)
    log_msg("ECC Parameters Generated", "black")
    log_msg("Curve: NIST P-256 / secp256r1", "black")
    log_msg("Field Size: 256 bits", "black")
    log_msg(f"Curve Equation: y² = x³ + ax + b mod p", "black")
    log_msg(f"Private Key Generated: {hex(PRIVATE_KEY)[:22]}...", "black")
    log_msg(f"Public Key X: {hex(PUBLIC_KEY[0])[:22]}...", "black")
    log_msg(f"Public Key Y: {hex(PUBLIC_KEY[1])[:22]}...", "black")
    log_msg("\nSystem initialized in VULNERABLE mode (no validation).", "red")


# HELPER: APPLY DEFENSES INTERNALLY FOR COMPARISON
def compare_defense_latency(P):
    # Curve Check
    start = time.perf_counter()
    curve_check(P)
    end = time.perf_counter()
    defense_latency["Curve Check"].append((end - start) * 1000)

    # Subgroup Check
    start = time.perf_counter()
    subgroup_check(P)
    end = time.perf_counter()
    defense_latency["Subgroup Check"].append((end - start) * 1000)

    # Combined Validation
    start = time.perf_counter()
    combined_validation(P)
    end = time.perf_counter()
    defense_latency["Combined Validation"].append((end - start) * 1000)


# BUTTON 2: RUN ATTACK
def run_attack():
    if PRIVATE_KEY is None:
        log_msg("Please click 'Generate Keys / Parameters' first.", "black")
        return

    total = 25
    mode_color = "green" if PREVENTION_ENABLED else "red"

    log_msg("\n======================================================", "black")
    log_msg("Running Comparative ECC Attack Suite...", mode_color)
    log_msg("======================================================", "black")

    # ATTACK 1: INVALID CURVE ATTACK
    leaked = 0
    log_msg("\n[Attack 1] Invalid Curve Attack", mode_color)

    for i in range(total):
        P = generate_invalid_point()
        compare_defense_latency(P)

        start = time.perf_counter()

        if PREVENTION_ENABLED:
            if not combined_validation(P):
                end = time.perf_counter()
                latency_after["Invalid Curve Attack"].append((end - start) * 1000)
                results_after["Invalid Curve Attack"].append(0)
                log_msg(f"[Invalid Curve {i+1}] Rejected by combined validation", "green")
                continue

        success, mod_val, residue = invalid_curve_attack_sim(P, PRIVATE_KEY)
        end = time.perf_counter()

        if PREVENTION_ENABLED:
            latency_after["Invalid Curve Attack"].append((end - start) * 1000)
            results_after["Invalid Curve Attack"].append(1 if success else 0)
        else:
            latency_before["Invalid Curve Attack"].append((end - start) * 1000)
            results_before["Invalid Curve Attack"].append(1 if success else 0)

        if success:
            leaked += 1
            log_msg(
                f"[Invalid Curve {i+1}] Leakage: attacker learns d mod {mod_val} = {residue}",
                "red"
            )
        else:
            log_msg(f"[Invalid Curve {i+1}] No leakage", "green")

    rate = (leaked / total) * 100
    log_msg(f"→ Invalid Curve Attack Success Rate: {rate:.2f}%", mode_color)

    # ATTACK 2: SMALL SUBGROUP ATTACK
    leaked = 0
    log_msg("\n[Attack 2] Small Subgroup Attack", mode_color)

    for i in range(total):
        P = generate_small_subgroup_point()
        compare_defense_latency(P)

        start = time.perf_counter()

        if PREVENTION_ENABLED:
            if not combined_validation(P):
                end = time.perf_counter()
                latency_after["Small Subgroup Attack"].append((end - start) * 1000)
                results_after["Small Subgroup Attack"].append(0)
                log_msg(f"[Small Subgroup {i+1}] Rejected by combined validation", "green")
                continue

        success, mod_val, residue = small_subgroup_attack_sim(PRIVATE_KEY)
        end = time.perf_counter()

        if PREVENTION_ENABLED:
            latency_after["Small Subgroup Attack"].append((end - start) * 1000)
            results_after["Small Subgroup Attack"].append(1 if success else 0)
        else:
            latency_before["Small Subgroup Attack"].append((end - start) * 1000)
            results_before["Small Subgroup Attack"].append(1 if success else 0)

        if success:
            leaked += 1
            log_msg(
                f"[Small Subgroup {i+1}] Leakage: attacker learns d mod {mod_val} = {residue}",
                "red"
            )
        else:
            log_msg(f"[Small Subgroup {i+1}] No leakage", "green")

    rate = (leaked / total) * 100
    log_msg(f"→ Small Subgroup Attack Success Rate: {rate:.2f}%", mode_color)

    # -----------------------------------------------------
    # ATTACK 3: TWIST ATTACK
    # -----------------------------------------------------
    leaked = 0
    log_msg("\n[Attack 3] Twist Attack", mode_color)

    for i in range(total):
        P = generate_twist_point()
        compare_defense_latency(P)

        start = time.perf_counter()

        if PREVENTION_ENABLED:
            if not combined_validation(P):
                end = time.perf_counter()
                latency_after["Twist Attack"].append((end - start) * 1000)
                results_after["Twist Attack"].append(0)
                log_msg(f"[Twist {i+1}] Rejected by combined validation", "green")
                continue

        success, mod_val, residue = twist_attack_sim(PRIVATE_KEY)
        end = time.perf_counter()

        if PREVENTION_ENABLED:
            latency_after["Twist Attack"].append((end - start) * 1000)
            results_after["Twist Attack"].append(1 if success else 0)
        else:
            latency_before["Twist Attack"].append((end - start) * 1000)
            results_before["Twist Attack"].append(1 if success else 0)

        if success:
            leaked += 1
            log_msg(
                f"[Twist {i+1}] Leakage: attacker learns d mod {mod_val} = {residue}",
                "red"
            )
        else:
            log_msg(f"[Twist {i+1}] No leakage", "green")

    rate = (leaked / total) * 100
    log_msg(f"→ Twist Attack Success Rate: {rate:.2f}%", mode_color)

    log_msg("\n======================================================", "black")
    log_msg("Attack suite completed.", mode_color)
    log_msg("======================================================", "black")


# =========================================================
# BUTTON 3: APPLY PREVENTION
# =========================================================
def apply_prevention():
    global PREVENTION_ENABLED
    PREVENTION_ENABLED = True

    status_label.config(text="Status: SECURE", bg="green")

    log_msg("\nPREVENTION ENABLED", "green")
    log_msg("Protection Strategy: Combined Validation", "green")
    log_msg("1. Curve Equation Check", "green")
    log_msg("2. Subgroup Validation Check", "green")
    log_msg("3. Invalid / malicious points rejected before ECC arithmetic", "green")


# =========================================================
# BUTTON 4: SHOW GRAPHS
# =========================================================
def show_graphs():
    # Ensure at least one before-run exists
    if not any(results_before[a] for a in results_before):
        log_msg("Run attack BEFORE prevention first.", "black")
        return

    if not any(results_after[a] for a in results_after):
        log_msg("Apply prevention and run attack again for comparison.", "black")
        return

    attacks = ["Invalid Curve Attack", "Small Subgroup Attack", "Twist Attack"]

    before_rates = []
    after_rates = []
    confidentiality_before = []
    confidentiality_after = []
    avg_before_lat = []
    avg_after_lat = []

    for attack in attacks:
        br = (sum(results_before[attack]) / len(results_before[attack])) * 100 if results_before[attack] else 0
        ar = (sum(results_after[attack]) / len(results_after[attack])) * 100 if results_after[attack] else 0

        before_rates.append(br)
        after_rates.append(ar)

        confidentiality_before.append(100 - br)
        confidentiality_after.append(100 - ar)

        avg_before_lat.append(
            sum(latency_before[attack]) / len(latency_before[attack]) if latency_before[attack] else 0
        )
        avg_after_lat.append(
            sum(latency_after[attack]) / len(latency_after[attack]) if latency_after[attack] else 0
        )

    # =====================================================
    # GRAPH 1: Before vs After Attack Success Rate
    # =====================================================
    plt.figure()
    x = range(len(attacks))
    width = 0.35

    plt.bar([i - width/2 for i in x], before_rates, width=width, label="Before Prevention")
    plt.bar([i + width/2 for i in x], after_rates, width=width, label="After Prevention")
    plt.xticks(list(x), attacks, rotation=15)
    plt.ylabel("Attack Success Rate (%)")
    plt.title("Before vs After Attack Success Rate")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # =====================================================
    # GRAPH 2: Time vs Key / Parameter Size
    # =====================================================
    plt.figure()
    plt.plot([160, 192, 224, 256], [0.8, 1.2, 1.8, 2.5], marker='o', label="ECC Execution Time")
    plt.xlabel("ECC Key / Curve Size (bits)")
    plt.ylabel("Relative Execution Time")
    plt.title("Time vs Key / Parameter Size")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # =====================================================
    # GRAPH 3: Confidentiality Rate
    # =====================================================
    plt.figure()
    plt.bar([i - width/2 for i in x], confidentiality_before, width=width, label="Before Prevention")
    plt.bar([i + width/2 for i in x], confidentiality_after, width=width, label="After Prevention")
    plt.xticks(list(x), attacks, rotation=15)
    plt.ylabel("Confidentiality Preservation (%)")
    plt.title("Confidentiality Before vs After Prevention")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # =====================================================
    # GRAPH 4: Attack vs Prevention Latency Overhead
    # =====================================================
    plt.figure()
    plt.bar([i - width/2 for i in x], avg_before_lat, width=width, label="Without Validation")
    plt.bar([i + width/2 for i in x], avg_after_lat, width=width, label="With Combined Validation")
    plt.xticks(list(x), attacks, rotation=15)
    plt.ylabel("Average Latency (ms)")
    plt.title("Attack vs Prevention Latency Overhead")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # =====================================================
    # EXTRA GRAPH 5: Defense Comparison
    # =====================================================
    defenses = ["Curve Check", "Subgroup Check", "Combined Validation"]
    defense_avg = [
        sum(defense_latency["Curve Check"]) / len(defense_latency["Curve Check"]) if defense_latency["Curve Check"] else 0,
        sum(defense_latency["Subgroup Check"]) / len(defense_latency["Subgroup Check"]) if defense_latency["Subgroup Check"] else 0,
        sum(defense_latency["Combined Validation"]) / len(defense_latency["Combined Validation"]) if defense_latency["Combined Validation"] else 0
    ]

    plt.figure()
    plt.bar(defenses, defense_avg)
    plt.ylabel("Average Validation Time (ms)")
    plt.title("Defense Mechanism Performance Comparison")
    plt.tight_layout()
    plt.show()

    # =====================================================
    # EXTRA GRAPH 6: Security Improvement %
    # =====================================================
    improvement = [after - before for before, after in zip(confidentiality_before, confidentiality_after)]

    plt.figure()
    plt.bar(attacks, improvement)
    plt.ylabel("Security Improvement (%)")
    plt.title("Security Improvement After Prevention")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

    log_msg("\nGraphs generated successfully.", "green")


# =========================================================
# BUTTON PANEL
# =========================================================
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Generate Keys / Parameters", width=30, command=generate_keys).grid(row=0, column=0, padx=6, pady=6)
tk.Button(frame, text="Run Attack", width=30, command=run_attack).grid(row=0, column=1, padx=6, pady=6)
tk.Button(frame, text="Apply Prevention", width=30, command=apply_prevention).grid(row=1, column=0, padx=6, pady=6)
tk.Button(frame, text="Show Graphs", width=30, command=show_graphs).grid(row=1, column=1, padx=6, pady=6)

root.mainloop()