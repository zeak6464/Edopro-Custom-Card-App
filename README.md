# Yu-Gi-Oh! Custom Card Maker

A Python application that allows you to create custom Yu-Gi-Oh! cards with custom images and card scripts.

## Features

- Create custom cards with all standard card properties
- Support for Monster, Spell, and Trap cards
- Custom card image upload
- Card script editor
- SQLite database for card storage
- Export card scripts in .lua format

## Setup

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python card_maker.py
   ```

## Usage

1. Fill in the card details:
   - Card Name (required)
   - Card Type (required)
   - For Monster cards:
     - Attribute
     - Level
     - ATK/DEF
   - Card Effect

2. Add a custom card image:
   - Click "Select Image" to choose an image file
   - Supported formats: PNG, JPG, JPEG, GIF, BMP
   - Images will be stored in the `custom_cards/images` directory

3. Write the card script:
   - Use the script editor to write the card's Lua script
   - Scripts will be saved in the `custom_cards/scripts` directory

4. Save the card:
   - Click "Save Card" to store the card in the database
   - All card data will be saved in `custom_cards/custom_cards.db`

5. Clear the form:
   - Click "Clear Form" to reset all fields

## Directory Structure

```
custom_cards/
├── card_maker.py
├── requirements.txt
├── custom_cards.db
├── images/
└── scripts/
```

## Notes

- Card scripts should follow the EDOPro scripting format
- Images are automatically copied to the images directory
- The database and required directories are created automatically on first run 