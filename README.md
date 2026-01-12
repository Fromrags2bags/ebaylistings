# eBay Listing Automation

Automated tool to create eBay bulk upload CSV files with GUI interface and GitHub image hosting integration.

## 🚀 Quick Start

### Option 1: GUI Application (Recommended)
```bash
python ebay_listing_gui.py
```

### Option 2: Command Line
```bash
python convert_to_ebay_category_template.py
```

## 📋 Features

- ✅ **User-Friendly GUI** - No technical knowledge required
- ✅ **GitHub Image Hosting** - Automatic image upload and URL conversion
- ✅ **Scheduled Listings** - Creates listings that go live in 7 days (review time)
- ✅ **Form-Based Input** - Easy product information entry
- ✅ **Automatic CSV Generation** - eBay File Exchange compatible
- ✅ **Image Management** - Add, remove, and organize product images
- ✅ **Configuration Management** - One-time GitHub setup

## 📁 Project Structure

```
ebay/
├── ebay_listing_gui.py              # GUI application (main)
├── convert_to_ebay_category_template.py  # CSV generator
├── ebay_automation.py               # Batch automation
├── ebay_listing_config.txt          # Configuration
├── listings/                        # Your product listings
│   └── example_item/                # Template folder
├── processed/                       # Successfully processed
├── failed/                          # Failed listings
└── README files                     # Documentation
```

## 🎯 Usage

### Using the GUI Application

1. **Run the app:**
   ```bash
   python ebay_listing_gui.py
   ```

2. **First-time setup:**
   - Enter GitHub username, repository, and personal access token
   - Or skip for manual image URL entry

3. **Create a listing:**
   - Click "Create New Listing"
   - Enter folder name
   - Fill in product details
   - Add images
   - Click "Generate CSV"

4. **Upload to eBay:**
   - Go to: https://bulksell.ebay.com/ws/eBayISAPI.dll?FileExchange
   - Upload the generated CSV file
   - Review scheduled listing at: https://www.ebay.com/sh/lst/scheduled

### Manual Method

1. **Create listing folder:**
   ```
   listings/your_product_name/
   ├── listing_data.txt
   ├── image1.jpg
   ├── image2.jpg
   └── image3.jpg
   ```

2. **Edit listing_data.txt:**
   ```
   title: Your Product Title
   brand: Brand Name
   price: 99.99
   size: M
   color: Blue
   condition: Used - Excellent
   description: Product description here
   ```

3. **Generate CSV:**
   ```bash
   python convert_to_ebay_category_template.py
   ```

## 🔧 GitHub Setup

### Why GitHub?
- Free image hosting
- Reliable and fast
- Easy to manage
- No hosting costs

### Getting a Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "eBay Image Upload"
4. Check: ☑ repo (Full control)
5. Generate and copy the token
6. Paste in GUI app or save in config

## 📝 Listing Data Format

### Required Fields:
- `title` - Product title (max 80 characters)
- `brand` - Brand name
- `price` - Price in USD
- `size` - Size (XS, S, M, L, XL, etc.)
- `color` - Color name
- `condition` - Condition (see options below)

### Optional Fields:
- `description` - Product description
- `quantity` - Number available (default: 1)
- `shipping_cost` - Shipping cost (default: 0.00 for free)
- `location` - Item location
- `sku` - Your SKU/item number
- `image_url_1`, `image_url_2`, etc. - Image URLs

### Condition Options:
- New with tags
- New without tags
- Used - Excellent
- Used - Good
- Used - Acceptable

## 📤 eBay Upload Process

1. **Generate CSV** using GUI or command line
2. **Go to eBay File Exchange:**
   - https://bulksell.ebay.com/ws/eBayISAPI.dll?FileExchange
3. **Upload CSV file**
4. **Review scheduled listing:**
   - https://www.ebay.com/sh/lst/scheduled
5. **Edit, publish early, or cancel** as needed

## 🔍 Scheduled Listings

All listings are scheduled for **7 days in the future** by default. This gives you time to:
- Review the listing details
- Edit any information
- Add or change images
- Publish early if ready
- Cancel if needed

## 📚 Documentation

- `README_EBAY_AUTOMATION.md` - Detailed automation guide
- `README_GITHUB_IMAGE_HOSTING.md` - GitHub image hosting setup
- `README_IMAGE_UPLOAD.md` - Image upload options
- `listings/example_item/README.txt` - Quick start template

## 🛠️ Requirements

- Python 3.6+
- tkinter (included with Python)
- requests library (for GitHub API)

Install dependencies:
```bash
pip install requests
```

## 🔐 Security

- GitHub tokens are stored locally in `ebay_config.json`
- Never commit `ebay_config.json` to version control
- Tokens can be revoked anytime from GitHub settings
- Use tokens instead of passwords for better security

## 📋 Troubleshooting

### GUI won't start
- Ensure Python 3.6+ is installed
- Check tkinter is available: `python -m tkinter`

### CSV upload fails
- Verify all required fields are filled
- Check image URLs are accessible
- Ensure GitHub token has correct permissions

### Images not showing
- Verify GitHub repository is public
- Check image URLs use `raw.githubusercontent.com` format
- Test URLs in browser

## 🤝 Support

For issues or questions:
1. Check the README files in the project
2. Review the example_item folder
3. Test with the GUI application first

## 📄 License

This tool is provided as-is for automating eBay listing creation.

## 🎉 Credits

Created with Python, Tkinter, and ❤️ for eBay sellers.