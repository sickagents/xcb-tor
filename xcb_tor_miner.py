#!/usr/bin/env python3
"""
XCB (Corecoin) Mining with Tor Proxy
Uses tor-proxy-miner-amd64 for anonymous mining through Tor network
"""

import subprocess
import random
import string
import os
import sys
import time

def generate_worker_name():
    """Generate random worker name"""
    prefix = random.choice(['compute', 'node', 'rig', 'proc', 'worker', 'cpu'])
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}{suffix}"

def check_dependencies():
    """Check if required packages are installed"""
    packages = ['git', 'cmake', 'build-essential', 'libssl-dev', 'libhwloc-dev', 'wget']
    missing = []
    
    for pkg in packages:
        result = subprocess.run(
            ['dpkg', '-l', pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode != 0:
            missing.append(pkg)
    
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.run(['apt', 'update'], check=True)
        subprocess.run(['apt', 'install', '-y'] + missing, check=True)

def download_tor_proxy_miner():
    """Download tor-proxy-miner-amd64 binary"""
    binary_path = '/usr/local/bin/tor-proxy-miner-amd64'
    
    if os.path.exists(binary_path):
        print("tor-proxy-miner-amd64 already installed. Skipping download.")
        return
    
    print("Downloading tor-proxy-miner-amd64...")
    
    # Download binary (adjust URL if needed)
    url = "https://github.com/catchthatrabbit/tor-proxy-miner/releases/latest/download/tor-proxy-miner-amd64"
    
    subprocess.run(['wget', '-O', '/tmp/tor-proxy-miner-amd64', url], check=True)
    subprocess.run(['chmod', '+x', '/tmp/tor-proxy-miner-amd64'], check=True)
    subprocess.run(['mv', '/tmp/tor-proxy-miner-amd64', binary_path], check=True)
    
    print("tor-proxy-miner-amd64 installed successfully!")

def compile_coreminer():
    """Clone and compile CoreMiner"""
    if os.path.exists('/usr/local/bin/coreminer'):
        print("CoreMiner already compiled. Skipping build.")
        return
    
    print("Cloning CoreMiner repository...")
    subprocess.run(['git', 'clone', 'https://github.com/catchthatrabbit/coreminer.git', '/tmp/coreminer'], check=True)
    
    print("Compiling CoreMiner (this may take 5-10 minutes)...")
    os.makedirs('/tmp/coreminer/build', exist_ok=True)
    os.chdir('/tmp/coreminer/build')
    
    subprocess.run(['cmake', '..'], check=True)
    subprocess.run(['make', '-j', str(os.cpu_count() or 4)], check=True)
    
    print("Installing CoreMiner to /usr/local/bin...")
    subprocess.run(['cp', '/tmp/coreminer/build/coreminer', '/usr/local/bin/'], check=True)
    subprocess.run(['chmod', '+x', '/usr/local/bin/coreminer'], check=True)
    
    print("Cleaning up build files...")
    subprocess.run(['rm', '-rf', '/tmp/coreminer'], check=True)
    
    print("CoreMiner installed successfully!")

def start_tor_proxy(local_port=9050):
    """Start Tor proxy using tor-proxy-miner-amd64"""
    print(f"\n{'='*60}")
    print(f"Starting Tor Proxy on port {local_port}")
    print(f"{'='*60}\n")
    
    # Start tor-proxy-miner in background
    tor_process = subprocess.Popen(
        ['/usr/local/bin/tor-proxy-miner-amd64', '--port', str(local_port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for Tor to bootstrap
    print("Waiting for Tor to bootstrap (30 seconds)...")
    time.sleep(30)
    
    return tor_process

def start_mining(pool_host, pool_port, wallet_address, threads=None, tor_port=9050):
    """Start mining with CoreMiner through Tor proxy"""
    if not threads:
        threads = os.cpu_count() or 4
    
    worker_name = generate_worker_name()
    pool_url = f"socks5://127.0.0.1:{tor_port}@{pool_host}:{pool_port}"
    worker_id = f"{wallet_address}.{worker_name}"
    
    print(f"\n{'='*60}")
    print(f"Starting XCB Mining via Tor")
    print(f"{'='*60}")
    print(f"Worker Name: {worker_name}")
    print(f"Pool: {pool_host}:{pool_port}")
    print(f"Tor Proxy: 127.0.0.1:{tor_port}")
    print(f"Wallet: {wallet_address}")
    print(f"Threads: {threads}")
    print(f"{'='*60}\n")
    
    try:
        subprocess.run([
            '/usr/local/bin/coreminer',
            '-o', pool_url,
            '-u', worker_id,
            '-t', str(threads)
        ])
    except KeyboardInterrupt:
        print("\n\nMining stopped by user.")
        sys.exit(0)

def main():
    """Main function"""
    # Configuration - EDIT THESE VALUES
    POOL_HOST = "dach.corecoinpool.com"  # Pool hostname
    POOL_PORT = "3333"                    # Pool port
    WALLET_ADDRESS = "CB..."              # Your Corecoin wallet address
    THREADS = None                        # None = auto-detect all cores
    TOR_PORT = 9050                       # Local Tor SOCKS5 port
    
    # Validate configuration
    if WALLET_ADDRESS == "CB...":
        print("ERROR: Please edit the script and set WALLET_ADDRESS")
        sys.exit(1)
    
    print("XCB Tor Miner Setup")
    print("=" * 60)
    
    # Setup
    print("Step 1: Checking dependencies...")
    check_dependencies()
    
    print("\nStep 2: Installing tor-proxy-miner-amd64...")
    download_tor_proxy_miner()
    
    print("\nStep 3: Compiling CoreMiner...")
    compile_coreminer()
    
    print("\nStep 4: Starting Tor proxy...")
    tor_process = start_tor_proxy(TOR_PORT)
    
    print("\nStep 5: Starting mining...")
    try:
        start_mining(POOL_HOST, POOL_PORT, WALLET_ADDRESS, THREADS, TOR_PORT)
    finally:
        # Cleanup: kill Tor process
        print("\nStopping Tor proxy...")
        tor_process.terminate()
        tor_process.wait()

if __name__ == "__main__":
    main()
