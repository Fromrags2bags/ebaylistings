# Using GitHub to Host eBay Product Images

## Yes, You Can Use GitHub for Image Hosting!

GitHub can host your product images for free, and you can use the URLs directly in your eBay listings.

## How It Works

### Step 1: Create a GitHub Repository

1. Go to https://github.com
2. Click **"New repository"** (green button)
3. Name it something like: `ebay-product-images` or `store-inventory`
4. Choose **Public** (required for image URLs to work)
5. Click **"Create repository"**

### Step 2: Upload Images to GitHub

#### Option A: Via GitHub Website (Easy)
1. Go to your repository
2. Click **"Add file"** > **"Upload files"**
3. Drag and drop your product images
4. Click **"Commit changes"**

#### Option B: Via Git Command Line
```bash
git clone https://github.com/YOUR-USERNAME/ebay-product-images.git
cd ebay-product-images
mkdir products
cp /path/to/your/images/* products/
git add .
git commit -m "Add product images"
git push
```

### Step 3: Get Image URLs

After uploading, click on any image in GitHub and you'll see it displayed.

**The URL format is:**
```
https://raw.githubusercontent.com/YOUR-USERNAME/REPO-NAME/main/path/to/image.jpg
```

**Example:**
```
https://raw.githubusercontent.com/johndoe/ebay-product-images/main/products/lululemon-hoodie-1.jpg
```

### Step 4: Add URLs to listing_data.txt

```
title: Lululemon Scuba Hoodie Gray XS
brand: Lululemon
price: 89.99
size: XS
color: Gray
image_url_1: https://raw.githubusercontent.com/YOUR-USERNAME/ebay-product-images/main/products/hoodie-front.jpg
image_url_2: https://raw.githubusercontent.com/YOUR-USERNAME/ebay-product-images/main/products/hoodie-back.jpg
image_url_3: https://raw.githubusercontent.com/YOUR-USERNAME/ebay-product-images/main/products/hoodie-tag.jpg
description: Lululemon Scuba Hoodie in excellent condition...
```

### Step 5: Generate CSV and Upload to eBay

```bash
cd ebay
python convert_to_ebay_category_template.py
```

The CSV will now include your GitHub image URLs, and eBay will be able to download them!

## Organizing Your Images

### Recommended Folder Structure:
```
ebay-product-images/
├── README.md
├── lululemon/
│   ├── scuba-hoodie-gray-xs/
│   │   ├── front.jpg
│   │   ├── back.jpg
│   │   ├── tag.jpg
│   │   └── detail.jpg
│   └── align-leggings-black-m/
│       ├── front.jpg
│       └── back.jpg
├── nike/
│   └── air-max-90/
│       ├── side.jpg
│       └── sole.jpg
└── adidas/
    └── ultraboost/
        ├── main.jpg
        └── detail.jpg
```

## Automated Script to Upload Images

Here's a Python script to automate the process:

```python
#!/usr/bin/env python3
"""
Upload images to GitHub and update listing_data.txt with URLs
"""

import os
import subprocess

def upload_to_github(local_folder, github_repo, github_path):
    """
    Upload images from local folder to GitHub
    
    Args:
        local_folder: Path to folder with images
        github_repo: Your GitHub repo (username/repo-name)
        github_path: Path within repo (e.g., 'products/item1')
    """
    
    # Get list of images
    images = [f for f in os.listdir(local_folder) 
              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    if not images:
        print("No images found!")
        return []
    
    # Clone or pull repo
    repo_name = github_repo.split('/')[1]
    if not os.path.exists(repo_name):
        subprocess.run(['git', 'clone', f'https://github.com/{github_repo}.git'])
    
    os.chdir(repo_name)
    subprocess.run(['git', 'pull'])
    
    # Create directory
    os.makedirs(github_path, exist_ok=True)
    
    # Copy images
    urls = []
    for img in images:
        src = os.path.join('..', local_folder, img)
        dst = os.path.join(github_path, img)
        subprocess.run(['cp', src, dst])
        
        # Generate URL
        url = f"https://raw.githubusercontent.com/{github_repo}/main/{github_path}/{img}"
        urls.append(url)
    
    # Commit and push
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', f'Add images for {github_path}'])
    subprocess.run(['git', 'push'])
    
    os.chdir('..')
    
    return urls

# Example usage
if __name__ == '__main__':
    urls = upload_to_github(
        local_folder='listings/lululemon_scuba_hoodie_xs',
        github_repo='YOUR-USERNAME/ebay-product-images',
        github_path='products/lululemon/scuba-hoodie-xs'
    )
    
    print("\nImage URLs:")
    for i, url in enumerate(urls, 1):
        print(f"image_url_{i}: {url}")
```

## Important Notes

### ✅ Advantages:
- **Free** - No hosting costs
- **Reliable** - GitHub has excellent uptime
- **Version Control** - Track changes to images
- **Easy Management** - Simple web interface
- **Fast** - GitHub's CDN is fast worldwide

### ⚠️ Considerations:
- Repository must be **Public** (private repos won't work for image URLs)
- GitHub has file size limits (100MB per file, 1GB per repo recommended)
- Not ideal for thousands of high-res images (use dedicated image hosting for large scale)
- Images are publicly accessible (anyone with URL can view)

### 📏 Image Best Practices:
- **Size**: 1000-1600 pixels on longest side
- **Format**: JPG (best compression), PNG (if transparency needed)
- **File Size**: Keep under 5MB per image
- **Quality**: 80-90% JPEG quality is sufficient
- **Names**: Use descriptive names (e.g., `lululemon-hoodie-front.jpg`)

## Alternative: GitHub Pages

For even better performance, you can use GitHub Pages:

1. Enable GitHub Pages in repository settings
2. Images will be available at:
   ```
   https://YOUR-USERNAME.github.io/REPO-NAME/path/to/image.jpg
   ```

## Quick Start Example

1. **Create repo**: `ebay-images`
2. **Upload image**: `products/test-item.jpg`
3. **Get URL**: `https://raw.githubusercontent.com/YOUR-USERNAME/ebay-images/main/products/test-item.jpg`
4. **Add to listing_data.txt**:
   ```
   image_url_1: https://raw.githubusercontent.com/YOUR-USERNAME/ebay-images/main/products/test-item.jpg
   ```
5. **Generate CSV**: `python convert_to_ebay_category_template.py`
6. **Upload to eBay**: Works perfectly! ✅

## Security Note

Since the repository must be public:
- Don't include any sensitive information in image metadata
- Don't include personal information in filenames
- Consider watermarking images if concerned about theft
- Use generic folder names (not customer names)

## Summary

**Yes, GitHub is a great free solution for hosting eBay product images!**

Just remember:
1. Repository must be Public
2. Use the `raw.githubusercontent.com` URL format
3. Keep file sizes reasonable
4. Organize images in folders by product

This is perfect for small to medium-sized eBay stores!