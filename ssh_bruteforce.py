import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

# Global control flag
is_attacking = False

# Simulated dictionary wordlist
WORDLIST = [
    "admin", "password", "123456", "root", "qwerty", 
    "12345678", "admin123", "letmein", "cisco", "pass123", 
    "cisco123", "network", "router", "secret"
]

def simulate_attack(target_ip, username):
    global is_attacking
    text_log.config(state=tk.NORMAL)
    text_log.delete(1.0, tk.END)
    text_log.insert(tk.END, f"[*] Initializing attack module...\n")
    text_log.insert(tk.END, f"[*] Target: {target_ip} | Port: 22 (SSH)\n")
    text_log.insert(tk.END, f"[*] Loading dictionary: {len(WORDLIST)} words loaded.\n")
    text_log.insert(tk.END, "-" * 50 + "\n")
    
    # Shuffle wordlist to randomize the attack duration each time
    attack_list = WORDLIST.copy()
    random.shuffle(attack_list)
    
    # Ensure our "correct" password is in the list
    target_password = "cisco123"
    if target_password not in attack_list:
        attack_list.append(target_password)

    for pwd in attack_list:
        if not is_attacking:
            text_log.insert(tk.END, "\n[!] Attack aborted by user.\n", "warning")
            break
            
        text_log.insert(tk.END, f"[*] Trying credentials -> {username} : {pwd}\n")
        text_log.see(tk.END)
        
        # Simulate the cryptographic delay of an SSH handshake
        time.sleep(0.6) 
        
        if pwd == target_password:
            text_log.insert(tk.END, f"[+] SUCCESS: Shell access granted!\n", "success")
            text_log.insert(tk.END, f"[+] Valid Credentials: {username}:{pwd}\n", "success")
            lbl_status.config(text="VULNERABLE - Access Gained", fg="#27ae60")
            break
        else:
            text_log.insert(tk.END, f"[-] FAILED: Permission denied.\n", "error")
            
    text_log.insert(tk.END, "-" * 50 + "\n[*] Attack execution finished.\n")
    text_log.see(tk.END)
    text_log.config(state=tk.DISABLED)
    
    is_attacking = False
    btn_start.config(state=tk.NORMAL)
    btn_stop.config(state=tk.DISABLED)

def start_attack():
    global is_attacking
    target_ip = entry_ip.get().strip()
    username = entry_user.get().strip()
    
    if not target_ip or not username:
        messagebox.showerror("Input Error", "Please enter target IP and Username.")
        return
        
    if is_attacking:
        return

    is_attacking = True
    btn_start.config(state=tk.DISABLED)
    btn_stop.config(state=tk.NORMAL)
    lbl_status.config(text="ATTACK IN PROGRESS...", fg="#e67e22")
    
    # Run attack on a separate thread to keep the GUI responsive
    attack_thread = threading.Thread(target=simulate_attack, args=(target_ip, username), daemon=True)
    attack_thread.start()

def stop_attack():
    global is_attacking
    is_attacking = False
    lbl_status.config(text="ABORTED", fg="#c0392b")

# --- Tkinter GUI Layout ---
root = tk.Tk()
root.title("SOC Toolkit - SSH Brute Force Simulator")
root.geometry("500x520")
root.resizable(False, False)

frame = ttk.Frame(root, padding="15")
frame.pack(fill=tk.BOTH, expand=True)

lbl_title = tk.Label(frame, text="SSH Dictionary Attack Simulator", font=("Helvetica", 13, "bold"))
lbl_title.pack(anchor="w", pady=(0, 15))

# Target Configuration Grid
config_frame = tk.Frame(frame)
config_frame.pack(fill=tk.X, pady=(0, 15))

tk.Label(config_frame, text="Target IP:", font=("Helvetica", 9)).grid(row=0, column=0, sticky="w", pady=5)
entry_ip = ttk.Entry(config_frame, width=20)
entry_ip.grid(row=0, column=1, padx=10, pady=5)
entry_ip.insert(0, "192.168.1.100")

tk.Label(config_frame, text="Target User:", font=("Helvetica", 9)).grid(row=1, column=0, sticky="w", pady=5)
entry_user = ttk.Entry(config_frame, width=20)
entry_user.grid(row=1, column=1, padx=10, pady=5)
entry_user.insert(0, "admin")

# Controls
control_frame = tk.Frame(frame)
control_frame.pack(fill=tk.X, pady=(0, 10))

btn_start = tk.Button(control_frame, text="Launch Attack", command=start_attack, bg="#2c3e50", fg="white", font=("Helvetica", 9, "bold"), width=15)
btn_start.pack(side=tk.LEFT, padx=(0, 10))

btn_stop = tk.Button(control_frame, text="Abort", command=stop_attack, bg="#c0392b", fg="white", font=("Helvetica", 9, "bold"), width=10, state=tk.DISABLED)
btn_stop.pack(side=tk.LEFT)

lbl_status = tk.Label(control_frame, text="READY", font=("Helvetica", 9, "bold"), fg="#7f8c8d")
lbl_status.pack(side=tk.RIGHT, padx=(0, 5))

# Attack Log Output
text_frame = tk.Frame(frame)
text_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_log = tk.Text(text_frame, font=("Consolas", 9), bg="#1e1e1e", fg="#ecf0f1", yscrollcommand=scrollbar.set)
text_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_log.config(state=tk.DISABLED)

# Text Tag Configurations for Colors
text_log.tag_config("error", foreground="#e74c3c")
text_log.tag_config("success", foreground="#2ecc71", font=("Consolas", 9, "bold"))
text_log.tag_config("warning", foreground="#f1c40f")

scrollbar.config(command=text_log.yview)

root.mainloop()