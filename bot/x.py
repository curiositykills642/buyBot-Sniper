from telethon.sync import TelegramClient, events
import re
from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair

api_id = '22849253'
api_hash = 'eb3d7a0a5e54f47d1eda8fc93a8d6b13'
phone_number = '+916375758675'

client = TelegramClient('session_name', api_id, api_hash)

async def send_sol(receiver , amount ):
    receiver = PublicKey(receiver)
    sender = Keypair().from_private_key('5ynL86rxfPdqZpUHETusE4tdnovaHySVV9zx8dJ3jU7DAWgyXEmHCtwdNN2dxAGzUL4iS2NGGDu4Un8cgknS5P2B')
    solana_client = Client("https://api.mainnet-beta.solana.com")
    instruction = transfer(
        from_public_key=sender.public_key,
        to_public_key=receiver, 
        lamports= int(amount*(10**9))
    )
    transaction = Transaction(instructions=[instruction], signers=[sender])

    result = solana_client.send_transaction(transaction)
    print("Transaction response: ", result)

@client.on(events.NewMessage)

async def handle_new_message(event):
    # Replace 'target_bot_user_id' with the actual User ID of the bot you want to filter
    target_bot_user_id = 6501232953   # Replace with the actual bot User ID (an integer)

    # Check if the message is from the target bot
    if event.message.sender_id == target_bot_user_id:
        text = event.message.text
        # text = """
        # ⤵️ Always double check that you have entered the correct address before sending.
        # Address: **`21pB95d6PeJ6ngw63acFCCXBMhpSP232QgcUqcCMsN8j`**
        # Amount: **`0.001`** SOL
        # """

        # Define regular expressions to match the address and amount
        address_pattern = r"Address: \*\*`([^`]+)`\*\*"
        amount_pattern = r"Amount: \*\*`([0-9.]+)`\*\*"

        # Find matches using regular expressions
        address_match = re.search(address_pattern, text)
        amount_match = re.search(amount_pattern, text)

        # Extract values from matches
        if address_match:
            address = address_match.group(1)
        else:
            address = None

        if amount_match:
            amount = amount_match.group(1)
        else:
            amount = None

        # Print the extracted values
        if address != None:
            print("addy : ",address)
            print("amt : " ,amount)
        else :
            print("empty brain")

# Connect and log in
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input('Enter the code: '))

# Start the event loop
client.start()
client.run_until_disconnected()


