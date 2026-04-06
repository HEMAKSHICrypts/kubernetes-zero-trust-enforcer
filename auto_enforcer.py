import subprocess
import time
import threading

POD_NAME = None
MARKER_FILE = "/tmp/compromised"
NAMESPACE = "default"

def get_pod_name():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", NAMESPACE, "-l", "app=web-app", "-o", "jsonpath={.items[0].metadata.name}"],
        capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None

def ensure_deployment():
    # Check if deployment exists
    result = subprocess.run(["kubectl", "get", "deployment", "web-app", "-n", NAMESPACE], capture_output=True)
    if result.returncode != 0:
        print("📦 Creating web-app deployment...")
        subprocess.run(["kubectl", "create", "deployment", "web-app", "--image=nginx", "-n", NAMESPACE])
        time.sleep(5)  # Wait for pod to start
    # Wait for pod to be ready
    for _ in range(30):
        pod = get_pod_name()
        if pod and "web-app" in pod:
            status = subprocess.run(["kubectl", "get", "pod", pod, "-n", NAMESPACE, "-o", "jsonpath={.status.phase}"], capture_output=True, text=True).stdout
            if status == "Running":
                print(f"✅ Pod {pod} is running.")
                return pod
        time.sleep(1)
    raise RuntimeError("Pod never became ready")

def simulate_attack(pod_name):
    print("\n🎭 Simulating attacker... (will create marker file in 10 seconds)")
    time.sleep(10)
    cmd = ["kubectl", "exec", pod_name, "-n", NAMESPACE, "--", "touch", MARKER_FILE]
    subprocess.run(cmd, capture_output=True)
    print(f"⚠️  Attacker created {MARKER_FILE} inside pod.")

def monitor(pod_name):
    print(f"\n🛡️ Zero‑Trust Enforcer Active – watching for {MARKER_FILE} inside {pod_name}\n")
    while True:
        cmd = ["kubectl", "exec", pod_name, "-n", NAMESPACE, "--", "test", "-f", MARKER_FILE]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            print("\n" + "="*70)
            print("🚨🚨🚨  SECURITY ALERT  🚨🚨🚨")
            print(f"Pod {pod_name} has been compromised!")
            print(f"Indicator: {MARKER_FILE} found.")
            print("Action: Pod should be isolated immediately.")
            print("="*70 + "\n")
            break
        else:
            print("[✓] Pod clean", end="\r")
        time.sleep(5)

if __name__ == "__main__":
    print("🔧 Starting Zero‑Trust Auto Enforcer...")
    pod = ensure_deployment()
    # Start attacker thread
    attacker = threading.Thread(target=simulate_attack, args=(pod,))
    attacker.daemon = True
    attacker.start()
    # Monitor in main thread
    monitor(pod)