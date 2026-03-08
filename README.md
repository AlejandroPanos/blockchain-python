# Python Blockchain Implementation

A simple blockchain implementation in Python demonstrating core blockchain concepts including proof-of-work consensus, cryptographic hashing, and chain validation. Built with Flask to provide a REST API for blockchain operations.

## Overview

This project implements a basic blockchain from scratch, showcasing the fundamental principles behind distributed ledger technology. It includes a proof-of-work mining algorithm, SHA-256 hashing for block integrity, and a REST API for interacting with the blockchain.

## Features

- **Proof-of-Work Mining**: Implements a computational puzzle that miners must solve to add new blocks
- **SHA-256 Hashing**: Cryptographically secure hashing for block integrity
- **Chain Validation**: Verify the entire blockchain's integrity and validity
- **Genesis Block**: Automatically creates the first block upon initialization
- **REST API**: Flask-based API for mining, viewing, and validating the blockchain
- **Ngrok Integration**: Optional tunneling for exposing local blockchain to the internet

## Technology Stack

- **Python 3.x**: Core programming language
- **Flask**: Lightweight web framework for REST API
- **hashlib**: SHA-256 cryptographic hashing
- **JSON**: Data serialization format
- **flask-ngrok**: Local server tunneling (optional)

## Prerequisites

- Python 3.7 or higher
- pip package manager

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/python-blockchain.git
   cd python-blockchain
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

Create a `requirements.txt` file with the following:

```
Flask==2.3.0
flask-ngrok==0.0.25
```

## Usage

### Running the Blockchain

Start the Flask server:

```bash
python blockchain.py
```

The server will be available at `http://localhost:5000` (or an ngrok URL if configured).

## API Endpoints

### 1. Mine a Block

**Endpoint:** `GET /mine_block`

Mines a new block using proof-of-work and adds it to the blockchain.

**Example Request:**

```bash
curl http://localhost:5000/mine_block
```

**Example Response:**

```json
{
  "message": "You have mined a new block",
  "index": 2,
  "timestamp": "2024-03-08 15:30:45.123456",
  "proof": 533,
  "previous_hash": "0000a1b2c3d4e5f6..."
}
```

### 2. Get Blockchain

**Endpoint:** `GET /get_chain`

Returns the complete blockchain with all blocks.

**Example Request:**

```bash
curl http://localhost:5000/get_chain
```

**Example Response:**

```json
{
  "chain": [
    {
      "index": 1,
      "timestamp": "2024-03-08 15:25:12.456789",
      "proof": 1,
      "previous_hash": "0"
    },
    {
      "index": 2,
      "timestamp": "2024-03-08 15:30:45.123456",
      "proof": 533,
      "previous_hash": "0000a1b2c3d4e5f6..."
    }
  ],
  "length": 2
}
```

### 3. Validate Chain

**Endpoint:** `GET /is_valid`

Validates the integrity of the entire blockchain.

**Example Request:**

```bash
curl http://localhost:5000/is_valid
```

**Example Response:**

```json
{
  "message": "Blockchain is valid"
}
```

## How It Works

### Block Structure

Each block in the chain contains:

- **Index**: Sequential position in the blockchain
- **Timestamp**: Exact time when the block was created
- **Proof**: The nonce (number used once) that satisfies the proof-of-work requirement
- **Previous Hash**: SHA-256 hash of the previous block, creating the chain link

### Proof-of-Work Algorithm

The mining process requires finding a number (proof) such that when hashed using the formula:

```
SHA256(new_proof² - previous_proof²)
```

The resulting hash starts with four leading zeros (`0000...`). This computational puzzle:

- Makes mining difficult and resource-intensive
- Prevents blockchain spam and attacks
- Ensures network security through computational work

**Example:**

```
Previous proof: 1
Try new_proof = 1: hash = "3a7f..." ❌
Try new_proof = 2: hash = "8b2c..." ❌
...
Try new_proof = 533: hash = "0000ab..." ✅
```

### Chain Validation

The blockchain validates its integrity by checking:

1. **Hash Continuity**: Each block's `previous_hash` must match the actual hash of the previous block
2. **Proof-of-Work Validity**: Each block's proof must satisfy the mining requirement (hash starts with "0000")

If any block is tampered with:

- Its hash changes
- The next block's `previous_hash` no longer matches
- Validation fails, exposing the tampering

### Genesis Block

The first block (genesis block) is special:

- Created automatically when the blockchain initializes
- Has a hardcoded `proof` of 1
- Has a `previous_hash` of "0" (no predecessor)
- Serves as the foundation for the entire chain

## Example Workflow

1. **Start the blockchain**

   ```bash
   python blockchain.py
   ```

2. **View the genesis block**

   ```bash
   curl http://localhost:5000/get_chain
   ```

3. **Mine a new block**

   ```bash
   curl http://localhost:5000/mine_block
   ```

4. **Mine another block**

   ```bash
   curl http://localhost:5000/mine_block
   ```

5. **Validate the chain**

   ```bash
   curl http://localhost:5000/is_valid
   ```

6. **View the complete blockchain**
   ```bash
   curl http://localhost:5000/get_chain
   ```

## Code Structure

```
blockchain.py
├── Blockchain Class
│   ├── __init__()              # Initialize chain with genesis block
│   ├── create_block()          # Create and append new block
│   ├── get_previous_block()    # Retrieve last block
│   ├── proof_of_work()         # Mining algorithm
│   ├── hash()                  # Calculate block hash
│   └── is_chain_valid()        # Validate entire chain
│
└── Flask API
    ├── /mine_block             # Mine new block endpoint
    ├── /get_chain              # Get blockchain endpoint
    └── /is_valid               # Validate chain endpoint
```

## Key Concepts

### Immutability

Once a block is added to the blockchain, modifying it would:

- Change its hash
- Break the chain link to the next block
- Invalidate all subsequent blocks
- Be immediately detectable through validation

### Cryptographic Security

SHA-256 hashing ensures:

- Any change to block data produces a completely different hash
- Hash functions are one-way (cannot reverse-engineer the input)
- Collision resistance (virtually impossible to find two inputs with the same hash)

### Consensus Mechanism

Proof-of-Work serves as the consensus mechanism:

- Requires computational effort to add blocks
- Makes attacks economically unfeasible
- Ensures agreement on the blockchain state

## Limitations

This is an educational implementation with the following limitations:

- **No persistence**: Blockchain resets when the server restarts
- **Single node**: No network of distributed nodes
- **No transactions**: Blocks don't contain transaction data
- **Simple PoW**: Production blockchains use more sophisticated algorithms
- **No incentives**: No cryptocurrency rewards for mining

## License

This project is open source and available under the MIT License.
