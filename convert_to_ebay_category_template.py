#!/usr/bin/env python3
"""
eBay Category Template Converter
Converts listing data to eBay's official category listing template format
"""

import csv
import os
from datetime import datetime, timedelta

def parse_listing_data(listing_folder):
    """Parse listing_data.txt file"""
    listing_file = os.path.join(listing_folder, 'listing_data.txt')
    
    if not os.path.exists(listing_file):
        print(f"Error: {listing_file} not found")
        return None
    
    data = {}
    with open(listing_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and ':' in line:
                key, value = line.split(':', 1)
                data[key.strip().lower()] = value.strip()
    
    return data

def get_image_urls(data, listing_folder):
    """
    Get image URLs from listing data or local files
    Priority:
    1. image_url_1, image_url_2, etc. from listing_data.txt
    2. Local file paths (for reference only - won't work in eBay upload)
    """
    images = []
    
    # First, check for image URLs in the data
    for i in range(1, 13):  # eBay allows up to 12 images
        url_key = f'image_url_{i}'
        if url_key in data and data[url_key]:
            images.append(data[url_key])
    
    # If no URLs found, list local files (for reference)
    if not images and os.path.exists(listing_folder):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        for file in sorted(os.listdir(listing_folder)):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                # Note: Local paths won't work - this is just for reference
                images.append(f"LOCAL_FILE:{file}")
    
    return images

def convert_to_ebay_category_template(listing_folder, output_file):
    """
    Convert listing data to eBay category template format
    
    Template structure for Women's Clothing (Category 53159):
    - Required: Brand, Size, Size Type, Color, Department, Type
    - Action field format: Add
    - Condition: New with tags = 1000, New without tags = 1500, Pre-owned = 3000
    """
    
    # Parse listing data
    data = parse_listing_data(listing_folder)
    if not data:
        return False
    
    # Get images
    images = get_image_urls(data, listing_folder)
    
    # Handle image URLs
    if images and not any(img.startswith('LOCAL_FILE:') for img in images):
        # We have real URLs
        pic_url = '|'.join(images[:12])
    else:
        # No URLs or only local files - leave empty for manual upload
        pic_url = ''
        if images:
            print(f"\nWARNING: Found local image files but no URLs:")
            for img in images:
                print(f"  - {img}")
            print("You'll need to upload images manually during eBay import.")
            print("See README_IMAGE_UPLOAD.md for details.\n")
    
    # Map data to eBay template fields
    # The template has a complex header row - we'll create the data row
    
    # Schedule listing for 7 days from now to give time for review
    schedule_date = datetime.now() + timedelta(days=7)
    schedule_time = schedule_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    row = {
        # Action - required (use 'Add' for scheduled listings)
        '*Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)': 'Add',
        
        # Custom Label (optional)
        'CustomLabel': data.get('sku', ''),
        
        # Category - Women's Clothing
        '*Category': '53159',
        
        # Store Category (optional)
        'StoreCategory': '',
        
        # Title - required
        '*Title': data.get('title', ''),
        
        # Subtitle (optional)
        'Subtitle': '',
        
        # Relationship fields (optional)
        'Relationship': '',
        'RelationshipDetails': '',
        
        # Schedule time - listing will go live in 7 days
        'ScheduleTime': schedule_time,
        
        # Condition - required
        '*ConditionID': '1000' if 'new' in data.get('condition', '').lower() else '3000',
        
        # REQUIRED ASPECTS for Category 53159
        '*C:Brand': data.get('brand', 'Unbranded'),
        '*C:Size': data.get('size', 'M'),
        '*C:Size Type': data.get('size_type', 'Regular'),
        '*C:Color': data.get('color', 'Multicolor'),
        '*C:Department': data.get('department', 'Women'),
        '*C:Type': data.get('type', 'T-Shirt'),
        
        # RECOMMENDED ASPECTS
        'C:Style': data.get('style', ''),
        'C:Sleeve Type': data.get('sleeve_type', ''),
        'C:Material': data.get('material', ''),
        'C:Neckline': data.get('neckline', ''),
        'C:Sleeve Length': data.get('sleeve_length', ''),
        'C:Pattern': data.get('pattern', 'Solid'),
        'C:Accents': '',
        'C:Theme': '',
        'C:Features': '',
        'C:Character': '',
        'C:Fit': data.get('fit', 'Regular'),
        'C:Vintage': 'No',
        'C:Fabric Type': data.get('fabric_type', ''),
        'C:Occasion': data.get('occasion', 'Casual'),
        'C:Closure': '',
        'C:Strap Type': '',
        'C:Country of Origin': '',
        'C:Season': data.get('season', ''),
        'C:Handmade': 'No',
        'C:Personalize': 'No',
        'C:Garment Care': data.get('care', ''),
        'C:California Prop 65 Warning': '',
        'C:MPN': data.get('mpn', ''),
        
        # Additional custom aspects (all optional)
        'C:Personalization Instructions': '',
        'C:Unit Quantity': '',
        'C:Unit Type': '',
        'C:Product Line': '',
        'C:Character Family': '',
        'C:Lining Material': '',
        'C:Performance/Activity': '',
        'C:Chest Size': '',
        'C:Compression Area': '',
        'C:Fabric Wash': '',
        'C:Model': '',
        
        # Images
        'PicURL': pic_url,
        'GalleryType': 'Gallery',
        'VideoID': '',
        
        # Description - required
        '*Description': data.get('description', ''),
        
        # Format - required (FixedPrice or Auction)
        '*Format': 'FixedPrice',
        
        # Duration - required (Days_7, Days_10, Days_30, GTC)
        '*Duration': 'GTC',
        
        # Price - required
        '*StartPrice': data.get('price', '0.00'),
        
        # Buy It Now (for auction format)
        'BuyItNowPrice': '',
        
        # Best Offer
        'BestOfferEnabled': '1' if data.get('accept_offers', '').lower() == 'yes' else '0',
        'BestOfferAutoAcceptPrice': '',
        'MinimumBestOfferPrice': '',
        
        # Quantity - required
        '*Quantity': data.get('quantity', '1'),
        
        # Payment - Don't require immediate payment if Best Offer is enabled
        'ImmediatePayRequired': '0' if data.get('accept_offers', '').lower() == 'yes' else '1',
        
        # Location - required
        '*Location': data.get('location', 'United States'),
        
        # Shipping - required
        'ShippingType': 'Flat',
        'ShippingService-1:Option': 'USPSPriority',
        'ShippingService-1:Cost': data.get('shipping_cost', '0.00'),
        'ShippingService-2:Option': '',
        'ShippingService-2:Cost': '',
        '*DispatchTimeMax': data.get('handling_time', '3'),
        
        # Shipping discount
        'PromotionalShippingDiscount': '',
        'ShippingDiscountProfileID': '',
        
        # Returns - required
        '*ReturnsAcceptedOption': 'ReturnsAccepted',
        'ReturnsWithinOption': 'Days_30',
        'RefundOption': 'MoneyBack',
        'ShippingCostPaidByOption': 'Buyer',
        'AdditionalDetails': '',
        
        # Business Policies (optional - use if you have profiles set up)
        'ShippingProfileName': '',
        'ReturnProfileName': '',
        'PaymentProfileName': '',
        
        # Product Safety (EU requirements - optional for US)
        'Product Safety Pictograms': '',
        'Product Safety Statements': '',
        'Product Safety Component': '',
        'Regulatory Document Ids': '',
        'Manufacturer Name': '',
        'Manufacturer AddressLine1': '',
        'Manufacturer AddressLine2': '',
        'Manufacturer City': '',
        'Manufacturer Country': '',
        'Manufacturer PostalCode': '',
        'Manufacturer StateOrProvince': '',
        'Manufacturer Phone': '',
        'Manufacturer Email': '',
        'Manufacturer ContactURL': '',
        'Responsible Person 1': '',
        'Responsible Person 1 Type': '',
        'Responsible Person 1 AddressLine1': '',
        'Responsible Person 1 AddressLine2': '',
        'Responsible Person 1 City': '',
        'Responsible Person 1 Country': '',
        'Responsible Person 1 PostalCode': '',
        'Responsible Person 1 StateOrProvince': '',
        'Responsible Person 1 Phone': '',
        'Responsible Person 1 Email': '',
        'Responsible Person 1 ContactURL': '',
    }
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        # First write the Info header row (from template)
        info_row = 'Info,Version=1.0.0,Template=fx_category_template_EBAY_US'
        f.write(info_row + '\n')
        
        # Write the column headers and data
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)
    
    # Calculate schedule date for display
    schedule_date = datetime.now() + timedelta(days=7)
    
    print(f"\n{'='*70}")
    print(f"SUCCESS! Created eBay SCHEDULED listing template: {output_file}")
    print(f"{'='*70}")
    
    print(f"\nSCHEDULED LISTING - Goes Live in 7 Days")
    print(f"  Scheduled for: {schedule_date.strftime('%B %d, %Y at %I:%M %p')}")
    print(f"  This gives you time to review before it goes live!")
    
    print(f"\nUpload Steps:")
    print(f"  1. Go to: https://bulksell.ebay.com/ws/eBayISAPI.dll?FileExchange")
    print(f"  2. Upload this CSV file: {output_file}")
    print(f"  3. eBay will create a SCHEDULED listing")
    
    print(f"\nReview Your Scheduled Listing:")
    print(f"  1. Go to: https://www.ebay.com/sh/lst/scheduled")
    print(f"  2. Find: {data.get('title', 'Your listing')}")
    print(f"  3. Click 'Edit' to make changes")
    print(f"  4. Click 'List now' to publish early, or 'Delete' to cancel")
    
    print(f"\nBenefits:")
    print(f"  - Listing created but NOT live yet")
    print(f"  - 7 days to review and edit")
    print(f"  - Can publish early or cancel anytime")
    print(f"  - Appears in 'Scheduled' section for easy access")
    
    print(f"\nTemplate Info:")
    print(f"  Category: Women's Clothing (53159)")
    print(f"  Images: {len(images) if images else 0} included")
    print(f"{'='*70}\n")
    
    return True

def main():
    """Main function"""
    # Check for processed folder first (where actual listings are)
    listing_folder = 'processed/lululemon_scuba_hoodie_xs'
    
    # Fall back to example if processed doesn't exist
    if not os.path.exists(listing_folder):
        listing_folder = 'listings/example_item'
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'ebay_category_upload_{timestamp}.csv'
    
    # Check if example folder exists
    if not os.path.exists(listing_folder):
        print(f"Creating example listing folder: {listing_folder}")
        os.makedirs(listing_folder, exist_ok=True)
        
        # Create example listing_data.txt
        example_data = """title: Lululemon Scuba Hoodie Gray XS
brand: Lululemon
price: 89.99
quantity: 1
condition: Pre-owned
size: XS
size_type: Regular
color: Gray
department: Women
type: Hoodie
style: Athletic
material: Cotton Blend
fit: Regular
pattern: Solid
occasion: Casual
season: Fall
description: Lululemon Scuba Hoodie in excellent pre-owned condition. Size XS. Gray color. Perfect for workouts or casual wear. No stains or damage.
location: Los Angeles, CA
shipping_cost: 5.99
handling_time: 2
accept_offers: yes
sku: LLL-SCUBA-GRY-XS-001
"""
        with open(os.path.join(listing_folder, 'listing_data.txt'), 'w') as f:
            f.write(example_data)
        
        print(f"Created example listing data file")
    
    # Convert to eBay template
    convert_to_ebay_category_template(listing_folder, output_file)

if __name__ == '__main__':
    main()

# Made with Bob
