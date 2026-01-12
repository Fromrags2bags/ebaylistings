# eBay Listing Automation Agent

Automated tool to create eBay bulk upload CSV files from folders containing product images and listing data.

## 🚀 Features

- ✅ Scans folders for product images and listing data
- ✅ Generates eBay File Exchange CSV format
- ✅ Supports up to 12 images per listing
- ✅ Automatic folder organization (processed/failed)
- ✅ Detailed logging of all operations
- ✅ Validates listing data
- ✅ Builds HTML descriptions automatically
- ✅ Supports bulk processing of multiple listings

## 📁 Folder Structure

```
ebay_automation/
├── listings/                    # Place your listing folders here
│   ├── product_001/
│   │   ├── listing_data.txt    # Product information
│   │   ├── image1.jpg          # Product images
│   │   ├── image2.jpg
│   │   └── image3.jpg
│   ├── product_002/
│   │   ├── listing_data.txt
│   │   └── photo.jpg
│   └── ...
├── processed/                   # Successfully processed folders moved here
├── failed/                      # Failed folders moved here
├── ebay_automation.py          # Main script
├── ebay_listing_config.txt     # Configuration file
└── ebay_upload_YYYYMMDD_HHMMSS.csv  # Generated CSV files
```

## 🔧 Setup

### 1. Install Python Requirements

```bash
# No external dependencies required - uses Python standard library only!
python --version  # Requires Python 3.6+
```

### 2. Configure Settings

Edit `ebay_listing_config.txt`:

```
# eBay Settings
site_id = 'US'
country = 'US'
currency = 'USD'
default_category = '11450'
default_condition = '3000'

# Payment & Shipping
payment_method = 'PayPal'
paypal_email = 'your-paypal@example.com'
shipping_service = 'USPSPriority'
shipping_cost = '0.00'
postal_code = '10001'
location = 'New York'

# Folder Settings
watch_folder = './listings'
processed_folder = './processed'
failed_folder = './failed'
max_images = '12'
```

### 3. Create Listing Folders

For each product, create a folder in `listings/` with:

1. **listing_data.txt** - Product information (see format below)
2. **Images** - Product photos (JPG, PNG, GIF)

## 📝 Listing Data Format

Create a `listing_data.txt` file in each product folder:

```
title: Vintage Nike Air Jordan Sneakers Size 10
subtitle: Rare 1990s Basketball Shoes
description: Gently used vintage Nike Air Jordan sneakers in excellent condition.
brand: Nike
size: 10
color: Black/Red
material: Leather
condition: Used - Excellent
category_id: 15709
price: 89.99
quantity: 1
retail_price: 150.00
keywords: Nike, Jordan, sneakers, basketball, vintage
sku: NIKE-AJ-001
shipping_cost: 0.00
location: New York
postal_code: 10001
```

### Required Fields:
- `title` - Product title (max 80 characters)
- `price` - Starting/fixed price

### Optional Fields:
- `subtitle` - Additional title (max 55 characters)
- `description` - Product description
- `brand` - Brand name
- `size` - Size information
- `color` - Color
- `material` - Material type
- `condition` - Condition (New, Used - Excellent, Used - Good, etc.)
- `category_id` - eBay category ID
- `quantity` - Number available
- `retail_price` - Original retail price
- `keywords` - Search keywords
- `sku` - Your SKU/item number
- `shipping_cost` - Shipping cost (0.00 for free shipping)
- `location` - Item location
- `postal_code` - ZIP/postal code

## 🎯 Usage

### Run Once

```bash
python ebay_automation.py
```

### With Custom Config

```bash
python ebay_automation.py --config my_config.txt
```

### Override Watch Folder

```bash
python ebay_automation.py --watch-folder /path/to/listings
```

## 📤 Upload to eBay

After running the script:

1. **Locate the CSV file** - Look for `ebay_upload_YYYYMMDD_HHMMSS.csv`
2. **Go to eBay File Exchange** - https://bulksell.ebay.com/ws/eBayISAPI.dll?FileExchange
3. **Upload the CSV** - Click "Upload File" and select your CSV
4. **Review & Submit** - eBay will validate and create your listings

## 🖼️ Image Handling

### Current Implementation:
- Script finds all images in each folder
- Sorts images alphabetically
- Limits to first 12 images (eBay maximum)
- Includes local file paths in CSV

### For Production Use:
You need to upload images to a hosting service first. Options:

1. **eBay Picture Services (EPS)** - Upload via eBay API
2. **External Image Host** - Imgur, Photobucket, your own server
3. **eBay's Self-Hosted** - Use your own URLs

Update the `create_csv_row` method in `ebay_automation.py` to use your image URLs.

## 📊 eBay Condition IDs

| Condition | ID |
|-----------|-----|
| New | 1000 |
| New with tags | 1000 |
| New without tags | 1500 |
| New with defects | 1750 |
| Used | 3000 |
| Used - Excellent | 3000 |
| Used - Good | 4000 |
| Used - Acceptable | 5000 |
| For parts or not working | 7000 |

## 🔍 Finding eBay Category IDs

1. Go to https://www.ebay.com/
2. Browse to your product category
3. Look at the URL: `https://www.ebay.com/b/Category-Name/CATEGORY_ID`
4. Use that CATEGORY_ID in your listing_data.txt

Common Categories:
- 11450 - Clothing, Shoes & Accessories
- 15709 - Athletic Shoes
- 293 - Consumer Electronics
- 11232 - Video Games & Consoles
- 220 - Collectibles

## 📋 Example Workflow

1. **Prepare Products**
   ```
   listings/
   ├── nike_shoes_001/
   │   ├── listing_data.txt
   │   ├── front.jpg
   │   ├── side.jpg
   │   └── sole.jpg
   └── adidas_shirt_002/
       ├── listing_data.txt
       └── photo.jpg
   ```

2. **Run Script**
   ```bash
   python ebay_automation.py
   ```

3. **Check Output**
   ```
   [INFO] Found 2 listing folder(s)
   [INFO] Processing folder: nike_shoes_001
   [INFO] Successfully processed: nike_shoes_001
   [INFO] Processing folder: adidas_shirt_002
   [INFO] Successfully processed: adidas_shirt_002
   [INFO] CSV file created: ebay_upload_20260112_151500.csv (2 listings)
   [INFO] SUCCESS: Created ebay_upload_20260112_151500.csv
   ```

4. **Upload to eBay**
   - Go to eBay File Exchange
   - Upload the CSV file
   - Review and submit

5. **Check Results**
   - Processed folders moved to `processed/`
   - Failed folders moved to `failed/`
   - Check `ebay_automation.log` for details

## 🔄 Scheduled Automation

To run automatically every 5 minutes, create `run_ebay_automation_scheduler.py`:

```python
import time
import subprocess
from datetime import datetime

INTERVAL_SECONDS = 300  # 5 minutes

while True:
    print(f"\n{'='*60}")
    print(f"Running eBay Automation - {datetime.now()}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            ['python', 'ebay_automation.py'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("ERRORS:", result.stderr)
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\nNext run in {INTERVAL_SECONDS} seconds...")
    time.sleep(INTERVAL_SECONDS)
```

Run with:
```bash
python run_ebay_automation_scheduler.py
```

## 🛠️ Troubleshooting

### No Folders Found
- Check `watch_folder` path in config
- Ensure folders contain `listing_data.txt`

### Missing Images
- Check image file extensions (.jpg, .jpeg, .png, .gif)
- Verify images are in the product folder

### CSV Upload Fails on eBay
- Verify all required fields are present
- Check category IDs are valid
- Ensure condition IDs match eBay standards
- Validate image URLs are accessible

### Encoding Errors
- Ensure listing_data.txt is saved as UTF-8
- Avoid special characters in file names

## 📝 Logging

All operations are logged to `ebay_automation.log`:

```
2026-01-12 15:15:00 - INFO - eBay Listing Automation Started
2026-01-12 15:15:00 - INFO - Found 2 listing folder(s)
2026-01-12 15:15:01 - INFO - Processing folder: nike_shoes_001
2026-01-12 15:15:01 - INFO - Successfully processed: nike_shoes_001
2026-01-12 15:15:02 - INFO - CSV file created: ebay_upload_20260112_151500.csv
```

## 🔐 Security Notes

- Keep your PayPal email private
- Don't commit config files with real credentials to version control
- Use environment variables for sensitive data in production

## 📚 Additional Resources

- [eBay File Exchange Guide](https://www.ebay.com/help/selling/listings/creating-managing-listings/using-file-exchange?id=4080)
- [eBay Category IDs](https://www.ebay.com/sellercenter/resources/category-ids)
- [eBay Condition IDs](https://developer.ebay.com/devzone/finding/callref/enums/conditionIdList.html)

## 🤝 Support

For issues or questions:
1. Check the log file: `ebay_automation.log`
2. Review the failed folders in `failed/`
3. Verify your listing_data.txt format
4. Ensure images are valid and accessible

## 📄 License

This tool is provided as-is for automating eBay listing creation.