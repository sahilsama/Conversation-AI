def send_whatsapp_message(contact, message):
    """Send a message to a specified WhatsApp contact."""
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import time

    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
    driver.get("https://web.whatsapp.com")

    # Wait for the user to scan the QR code
    input("Press Enter after scanning QR code")

    # Search for the contact
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(contact)
    time.sleep(2)  # Wait for the contact to appear
    search_box.send_keys(Keys.ENTER)

    # Type and send the message
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="6"]')
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)

    time.sleep(1)  # Wait a moment before closing
    driver.quit()
    return True

def manage_contacts(action, contact_name):
    """Manage contacts by adding or removing them."""
    # Placeholder for contact management logic
    if action == "add":
        # Logic to add a contact
        pass
    elif action == "remove":
        # Logic to remove a contact
        pass
    return True

def main():
    """Main function to demonstrate WhatsApp automation features."""
    # Example usage
    send_whatsapp_message("John Doe", "Hello from automation!")
    manage_contacts("add", "Jane Doe")

if __name__ == "__main__":
    main()