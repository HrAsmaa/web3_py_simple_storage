import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Install solc
install_solc("0.6.0")

# Compile Solidity Code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# Copy compiled code in a file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["myFirstContract"]["evm"][
    "bytecode"
]["object"]

# Get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["myFirstContract"]["abi"]

# Connect to Ganache
w3 = Web3(
    Web3.HTTPProvider("https://sepolia.infura.io/v3/19c0c7704086411e8e71daed8fbabd9c")
)
chain_id = 11155111
my_address = "0x4834441E3513D582C4487f6116F6381C7A50d3d9"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the last transaction
nonce = w3.eth.get_transaction_count(my_address)

# Submit the transaction that deploy the contract
transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Sign the transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)

# Send it
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Wait for the transaction to be mined and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with deployed contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(simple_storage.functions.getMyFavoritNumber().call())
simple_storage.functions.setMyFavoritNumber(15).call()
print(simple_storage.functions.getMyFavoritNumber().call())
first_transaction = simple_storage.functions.setMyFavoritNumber(15).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

first_signed_transaction = w3.eth.account.sign_transaction(
    first_transaction, private_key=private_key
)
first_tx_hash = w3.eth.send_raw_transaction(first_signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(first_tx_hash)

print(simple_storage.functions.getMyFavoritNumber().call())
