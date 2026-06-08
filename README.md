# XCB Tor Miner - Anonymous Mining via Tor Network

CPU mining for Corecoin (XCB) through Tor network using tor-proxy-miner-amd64.

## Features

- ✅ Anonymous mining via Tor SOCKS5 proxy
- ✅ Random worker names for stealth
- ✅ Auto-compile CoreMiner from source
- ✅ Easy configuration
- ✅ Multi-core support

## Files

### 1. Python Script (`xcb_tor_miner.py`)

Standalone script for terminal/SSH usage.

**Usage:**

```bash
# Edit configuration
nano xcb_tor_miner.py

# Run
python3 xcb_tor_miner.py
```

**Edit these variables:**
```python
POOL_HOST = "dach.corecoinpool.com"
POOL_PORT = "3333"
WALLET_ADDRESS = "CB...your_wallet"
THREADS = None  # Auto-detect
TOR_PORT = 9050
```

---

### 2. Interactive Notebook (`XCB_Tor_Mining.ipynb`)

Step-by-step notebook for web-based environments.

**Usage:**

1. Upload notebook to your environment
2. Edit configuration cell
3. Run cells in order
4. Mining starts in Step 6

---

## How It Works

```
Mining Server → Tor Proxy (localhost:9050) → Tor Network → XCB Pool
   (CoreMiner)    (tor-proxy-miner-amd64)      (anonymous)
```

**Benefits:**
- Pool sees Tor exit node IP, not your real IP
- New Tor circuit = new IP every 10 minutes
- Bypass datacenter IP restrictions
- Enhanced privacy

---

## System Requirements

### Minimum:
- Ubuntu 20.04+ or Debian 11+
- 4 GB RAM
- 10 GB disk space
- Internet connection (Tor-friendly)

### Dependencies (auto-installed):
- git
- cmake
- build-essential
- libssl-dev
- libhwloc-dev
- wget

---

## Performance

**Expected hashrate (per vCPU):**
- AMD EPYC: ~600-800 H/s per thread
- Intel Xeon: ~500-700 H/s per thread

**160 vCPU setup:**
- Hashrate: ~65 KH/s
- Daily: $1.99
- Monthly: $59.56

**Note:** Tor adds ~50-100ms latency but doesn't affect hashrate.

---

## Tor Considerations

### Advantages:
- Anonymous mining
- Bypass IP-based pool restrictions
- Free (no proxy subscription)

### Disadvantages:
- Slower connection (higher latency)
- Some pools block Tor exit nodes
- Tor bootstrap time (~30 seconds)

### Tor-Friendly Pools:
- DACH Pool (dach.corecoinpool.com:3333) - Recommended
- Check pool policy before mining

---

## Troubleshooting

### Tor connection fails

```bash
# Check if Tor is running
ps aux | grep tor-proxy-miner

# Test Tor proxy
curl --socks5 127.0.0.1:9050 https://check.torproject.org/api/ip
```

### Pool rejects connection

Pool may block Tor exit nodes. Try:
1. Different pool
2. Wait for new Tor circuit (10 minutes)
3. Restart Tor proxy

### Build fails

Ensure all dependencies installed:
```bash
sudo apt update
sudo apt install -y git cmake build-essential libssl-dev libhwloc-dev wget
```

### Low hashrate

- Check CPU throttling
- Verify all threads used
- Tor doesn't affect hashrate (only latency)

---

## Security

**Never share:**
- Private keys
- Wallet seed phrases
- Server credentials

**Tor privacy tips:**
- Tor hides your IP from pool
- Pool can still see wallet address
- Use different worker names per session
- Don't leak real IP in other connections

---

## Alternative Pools

Find more pools: https://miningpoolstats.stream/corecoin

**Edit in script:**
```python
POOL_HOST = "your.pool.com"
POOL_PORT = "3333"
```

---

## Corecoin Wallet

Get wallet from: https://coreblockchain.net/

Wallet format: `CB` prefix for mainnet

---

## License

MIT License - Free to use for personal and commercial mining.

---

## Related Repositories

- Direct Mining: https://github.com/sickagents/pocari-sweat
- Home Relay: https://github.com/sickagents/xcb-home-relay
- Pearl Mining: https://github.com/sickagents/yakult-h100
