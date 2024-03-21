import requests
import time
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Function to send a request to the Telegram Bot API
def send_telegram_request(method, data):
    token = "7181750288:AAEsny_8Yxefryhbe3Z5-FW3qZB4X8AFzK0"
    url = f"https://api.telegram.org/bot{token}/{method}"
    response = requests.post(url, json=data)
    return response.json()

# Function to send command to Arduino
def send_to_arduino(command):
    ser.write(command.encode())
    ser.flushInput()
    response = ser.readline().decode().strip()
    return response

# Function to handle the /mulaiBot command
def start(message):
    chat_id = message["chat"]["id"]
    send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Halo! Saya adalah bot dari TeamUno1. Bagaimana kabarmu? Sudah makan? Belum? Lapar dong."})
    send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Silahkan Ketik /mulaiUno untuk mengakses tombol"})

# Function to handle the /mulaiUno command
def opsi_uno(message):
    chat_id = message["chat"]["id"]
    keyboard = {
        "inline_keyboard": [
            [{"text": "Relay 1", "callback_data": "relay1"}],
            [{"text": "Relay 2", "callback_data": "relay2"}],
            [{"text": "Red Censor", "callback_data": "red_censor"}]
        ]
    }
    send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Pilih perangkat yang ingin diatur:", "reply_markup": keyboard})

# Function to handle button clicks
def handle_button_click(callback_query):
    button_data = callback_query["data"]
    message = callback_query["message"]
    user_id = message["chat"]["id"]

    if button_data == "relay1":
        send_to_arduino('R1\n')
    elif button_data == "relay2":
        send_to_arduino('R2\n')
    elif button_data == "red_censor":
        send_to_arduino('RS\n')

def process_message(message):
    text = message.get("text", "")
    if "/mulaiBot" in text:
        start(message)
    elif "/mulaiUno" in text:
        opsi_uno(message)
    # Add more message handling logic as needed

def main():
    offset = 0
    while True:
        try:
            response = send_telegram_request("getUpdates", {"offset": offset, "timeout": 30})
            if response["ok"]:
                for result in response["result"]:
                    process_message(result.get("message", {}))
                    if "callback_query" in result:
                        handle_button_click(result["callback_query"])
                    offset = result["update_id"] + 1
            else:
                print("Failed to get updates:", response)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred:", e)
            # Wait for a short period before retrying
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            # Handle other request-related errors as needed
            break
        except Exception as e:
            print("An unexpected error occurred:", e)
            break

if __name__ == "__main__":
    main()
