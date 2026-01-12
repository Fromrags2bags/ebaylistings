# eBay Image Upload Guide

## The Problem
eBay requires **actual image URLs** (web links), not local file paths. When you upload a CSV, eBay needs to be able to download the images from the internet.

## Solutions

### Option 1: Use eBay's File Exchange with Image Upload (RECOMMENDED)

1. **Prepare your images**:
   - Place images in your listing folder
   - Name them clearly (e.g., `item1.jpg`, `item2.jpg`)

2. **Use eBay's Bulk Upload Tool**:
   - Go to: **Seller Hub** > **Listings** > **Create listing in bulk**
   - Choose **"Upload photos from your computer"**
   - eBay will let you upload images during the CSV import process

3. **In your CSV**:
   - Leave `PicURL` field **EMPTY** or use placeholder text like "UPLOAD_DURING_IMPORT"
   - eBay will prompt you to upload images for each listing

### Option 2: Upload Images to eBay Picture Services First

1. **Upload images to eBay**:
   - Go to: https://www.ebay.com/sh/ovw (Seller Hub)
   - Use eBay's Picture Services to upload images
   - Get the eBay-hosted URLs (format: `https://i.ebayimg.com/...`)

2. **Update your listing_data.txt**:
   ```
   image_url_1: https://i.ebayimg.com/images/g/xxxxx/s-l1600.jpg
   image_url_2: https://i.ebayimg.com/images/g/yyyyy/s-l1600.jpg
   ```

3. **Regenerate CSV** with actual URLs

### Option 3: Host Images on Your Own Server

1. **Upload images to your website**:
   - Upload to your web hosting (must be publicly accessible)
   - Example: `https://yourwebsite.com/images/product1.jpg`

2. **Update listing_data.txt**:
   ```
   image_url_1: https://yourwebsite.com/images/product1.jpg
   image_url_2: https://yourwebsite.com/images/product2.jpg
   ```

3. **Requirements**:
   - Images must be publicly accessible (no login required)
   - HTTPS is recommended
   - Images should be 500-1600 pixels on longest side
   - Max file size: 12MB per image
   - Formats: JPG, PNG, GIF

### Option 4: Use eBay API (Advanced)

For full automation, use eBay's API to upload images programmatically:

```python
# Pseudo-code example
from ebaysdk.trading import Connection

api = Connection(config_file='ebay.yaml')
response = api.execute('UploadSiteHostedPictures', {
    'PictureData': base64_encoded_image,
    'PictureName': 'product1.jpg'
})

image_url = response.dict()['SiteHostedPictureDetails']['FullURL']
```

## Modified Workflow

### Current Process (What We Have):
1. Customer creates folder with images and listing_data.txt
2. Run converter script
3. **ERROR**: CSV has local file paths, eBay can't access them

### Fixed Process (What You Need):

#### Quick Fix - Manual Upload:
1. Customer creates folder with images and listing_data.txt
2. Run converter script (generates CSV with empty PicURL)
3. Go to eBay Seller Hub > Create listing in bulk
4. Upload CSV
5. **eBay will prompt to upload images** - upload from folder
6. Complete listing creation

#### Better Solution - Pre-upload Images:
1. Customer creates folder with images
2. **Upload images to web server or eBay Picture Services**
3. Get image URLs
4. Add URLs to listing_data.txt:
   ```
   image_url_1: https://yoursite.com/img1.jpg
   image_url_2: https://yoursite.com/img2.jpg
   ```
5. Run converter script (now includes real URLs)
6. Upload CSV to eBay - works perfectly!

## Image Requirements

- **Format**: JPG, PNG, GIF, BMP
- **Size**: 500-1600 pixels (longest side)
- **File Size**: Max 12MB per image
- **Quantity**: Up to 12 images per listing (24 for some categories)
- **Quality**: Clear, well-lit, no watermarks
- **Background**: Plain white or neutral recommended

## Testing

To test without images:
1. Create a listing with just text (no images)
2. After listing is live, add images through eBay's "Revise listing" feature
3. Or use a stock photo URL for testing

## Next Steps

I'll create an updated converter that:
1. Checks for image URLs in listing_data.txt
2. Falls back to leaving PicURL empty if no URLs provided
3. Adds clear instructions in the output