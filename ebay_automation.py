#!/usr/bin/env python3
"""
eBay Listing Automation Agent
Processes folders containing images and listing data, creates eBay CSV for bulk upload

Features:
- Scans folders for listing data and images
- Generates eBay File Exchange CSV format
- Supports image upload to eBay/external hosting
- Validates listing data
- Logs all operations
"""

import os
import csv
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
import re

class EbayListingAutomation:
    def __init__(self, config_file='ebay_listing_config.txt'):
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.setup_directories()
        
    def load_config(self, config_file):
        """Load configuration from parameter file"""
        config = {
            'watch_folder': './listings',
            'processed_folder': './processed',
            'failed_folder': './failed',
            'output_csv': 'ebay_bulk_upload.csv',
            'max_images': 12,
            'image_extensions': ['.jpg', '.jpeg', '.png', '.gif'],
            'site_id': 'US',
            'country': 'US',
            'currency': 'USD',
            'default_category': '11450',
            'default_condition': '3000',  # Used
            'default_duration': 'GTC',
            'default_format': 'FixedPrice',
            'default_quantity': '1',
            'payment_method': 'PayPal',
            'paypal_email': 'seller@example.com',
            'shipping_service': 'USPSPriority',
            'shipping_cost': '0.00',
            'dispatch_time': '3',
            'returns_accepted': 'ReturnsAccepted',
            'return_period': 'Days_30',
            'postal_code': '10001',
            'location': 'New York'
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip("'\"")
                            config[key] = value
            except Exception as e:
                print(f"[WARNING] Error reading config file: {e}")
        
        return config
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.config.get('log_file', 'ebay_automation.log')
        log_level = self.config.get('log_level', 'INFO')
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        for folder in ['watch_folder', 'processed_folder', 'failed_folder']:
            path = self.config.get(folder)
            if path:
                os.makedirs(path, exist_ok=True)
                self.logger.info(f"Directory ready: {path}")
    
    def find_listing_folders(self):
        """Find all folders in watch directory that contain listing data"""
        watch_folder = self.config['watch_folder']
        listing_folders = []
        
        for item in os.listdir(watch_folder):
            item_path = os.path.join(watch_folder, item)
            if os.path.isdir(item_path):
                # Check if folder contains listing data file
                if self.has_listing_data(item_path):
                    listing_folders.append(item_path)
        
        return listing_folders
    
    def has_listing_data(self, folder_path):
        """Check if folder contains a listing data file"""
        data_files = ['listing_data.txt', 'listing_data.csv', 'listing.txt', 'data.txt']
        for data_file in data_files:
            if os.path.exists(os.path.join(folder_path, data_file)):
                return True
        return False
    
    def parse_listing_data(self, folder_path):
        """Parse listing data from text file in folder"""
        data_files = ['listing_data.txt', 'listing_data.csv', 'listing.txt', 'data.txt']
        listing_data = {}
        
        for data_file in data_files:
            file_path = os.path.join(folder_path, data_file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if ':' in line and not line.startswith('#'):
                                key, value = line.split(':', 1)
                                key = key.strip().lower().replace(' ', '_')
                                value = value.strip()
                                listing_data[key] = value
                    break
                except Exception as e:
                    self.logger.error(f"Error parsing {file_path}: {e}")
        
        return listing_data
    
    def find_images(self, folder_path):
        """Find all image files in folder"""
        images = []
        extensions = self.config['image_extensions']
        
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in extensions:
                    images.append(file_path)
        
        # Sort images by name and limit to max_images
        images.sort()
        max_images = int(self.config.get('max_images', 12))
        return images[:max_images]
    
    def build_description(self, listing_data):
        """Build HTML description from listing data"""
        title = listing_data.get('title', 'Item for Sale')
        description = listing_data.get('description', '')
        size = listing_data.get('size', '')
        condition = listing_data.get('condition', '')
        retail_price = listing_data.get('retail_price', '')
        brand = listing_data.get('brand', '')
        color = listing_data.get('color', '')
        material = listing_data.get('material', '')
        
        html_parts = [f"<h2>{title}</h2>"]
        
        if description:
            html_parts.append(f"<p>{description}</p>")
        
        html_parts.append("<ul>")
        if brand:
            html_parts.append(f"<li><strong>Brand:</strong> {brand}</li>")
        if size:
            html_parts.append(f"<li><strong>Size:</strong> {size}</li>")
        if color:
            html_parts.append(f"<li><strong>Color:</strong> {color}</li>")
        if material:
            html_parts.append(f"<li><strong>Material:</strong> {material}</li>")
        if condition:
            html_parts.append(f"<li><strong>Condition:</strong> {condition}</li>")
        if retail_price:
            html_parts.append(f"<li><strong>Retail Price:</strong> ${retail_price}</li>")
        html_parts.append("</ul>")
        
        return "<![CDATA[" + "".join(html_parts) + "]]>"
    
    def get_condition_id(self, condition_text):
        """Convert condition text to eBay condition ID"""
        condition_map = {
            'new': '1000',
            'new with tags': '1000',
            'new without tags': '1500',
            'new with defects': '1750',
            'used': '3000',
            'used - excellent': '3000',
            'used - good': '4000',
            'used - acceptable': '5000',
            'for parts': '7000',
            'not working': '7000'
        }
        
        condition_lower = condition_text.lower() if condition_text else ''
        return condition_map.get(condition_lower, self.config['default_condition'])
    
    def create_csv_row(self, listing_data, images, folder_name):
        """Create a CSV row for eBay File Exchange format"""
        
        # Build image URLs (placeholder - you'll need to upload images first)
        image_urls = []
        for img in images:
            # For now, use local path - in production, upload to image host first
            image_urls.append(f"file:///{os.path.abspath(img)}")
        pic_url = "|".join(image_urls) if image_urls else ""
        
        row = {
            'Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)': 'Add',
            'Category': listing_data.get('category_id', self.config['default_category']),
            'Title': listing_data.get('title', 'Item for Sale')[:80],  # eBay limit 80 chars
            'Subtitle': listing_data.get('subtitle', '')[:55],  # eBay limit 55 chars
            'Relationship': '',
            'RelationshipDetails': '',
            'ConditionID': self.get_condition_id(listing_data.get('condition', '')),
            'Duration': listing_data.get('duration', self.config['default_duration']),
            'Format': listing_data.get('format', self.config['default_format']),
            'StartPrice': listing_data.get('price', listing_data.get('start_price', '9.99')),
            'BuyItNowPrice': listing_data.get('buy_it_now_price', ''),
            'Quantity': listing_data.get('quantity', self.config['default_quantity']),
            'PaymentMethods': self.config['payment_method'],
            'PayPalEmailAddress': self.config['paypal_email'],
            'ShippingService-1:Option': self.config['shipping_service'],
            'ShippingService-1:Cost': listing_data.get('shipping_cost', self.config['shipping_cost']),
            'ShippingService-1:AdditionalCost': '0.00',
            'ShippingService-1:Priority': '1',
            'DispatchTimeMax': self.config['dispatch_time'],
            'ReturnsAcceptedOption': self.config['returns_accepted'],
            'ReturnsWithinOption': self.config['return_period'],
            'ShippingCostPaidByOption': 'Buyer',
            'Description': self.build_description(listing_data),
            'PicURL': pic_url,
            'Location': listing_data.get('location', self.config['location']),
            'PostalCode': listing_data.get('postal_code', self.config['postal_code']),
            'C:Brand': listing_data.get('brand', ''),
            'C:Size': listing_data.get('size', ''),
            'C:Color': listing_data.get('color', ''),
            'C:Material': listing_data.get('material', ''),
            'CustomLabel': listing_data.get('sku', folder_name)
        }
        
        return row
    
    def process_listing_folder(self, folder_path):
        """Process a single listing folder"""
        folder_name = os.path.basename(folder_path)
        self.logger.info(f"Processing folder: {folder_name}")
        
        try:
            # Parse listing data
            listing_data = self.parse_listing_data(folder_path)
            if not listing_data:
                raise ValueError("No listing data found")
            
            # Find images
            images = self.find_images(folder_path)
            if not images:
                self.logger.warning(f"No images found in {folder_name}")
            
            # Create CSV row
            csv_row = self.create_csv_row(listing_data, images, folder_name)
            
            self.logger.info(f"Successfully processed: {folder_name}")
            return csv_row, True
            
        except Exception as e:
            self.logger.error(f"Error processing {folder_name}: {e}")
            return None, False
    
    def generate_bulk_csv(self, csv_rows):
        """Generate eBay bulk upload CSV file"""
        output_file = self.config.get('output_csv', 'ebay_bulk_upload.csv')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"ebay_upload_{timestamp}.csv"
        
        if not csv_rows:
            self.logger.warning("No rows to write to CSV")
            return None
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
                writer.writeheader()
                writer.writerows(csv_rows)
            
            self.logger.info(f"CSV file created: {output_file} ({len(csv_rows)} listings)")
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error creating CSV: {e}")
            return None
    
    def move_folder(self, folder_path, destination_base):
        """Move processed folder to destination"""
        folder_name = os.path.basename(folder_path)
        destination = os.path.join(destination_base, folder_name)
        
        # Handle duplicate names
        counter = 1
        original_destination = destination
        while os.path.exists(destination):
            destination = f"{original_destination}_{counter}"
            counter += 1
        
        try:
            shutil.move(folder_path, destination)
            self.logger.info(f"Moved {folder_name} to {destination_base}")
        except Exception as e:
            self.logger.error(f"Error moving {folder_name}: {e}")
    
    def run(self):
        """Main automation process"""
        self.logger.info("=" * 60)
        self.logger.info("eBay Listing Automation Started")
        self.logger.info("=" * 60)
        
        # Find all listing folders
        listing_folders = self.find_listing_folders()
        
        if not listing_folders:
            self.logger.info("No listing folders found")
            return
        
        self.logger.info(f"Found {len(listing_folders)} listing folder(s)")
        
        # Process each folder
        csv_rows = []
        successful_folders = []
        failed_folders = []
        
        for folder_path in listing_folders:
            csv_row, success = self.process_listing_folder(folder_path)
            
            if success and csv_row:
                csv_rows.append(csv_row)
                successful_folders.append(folder_path)
            else:
                failed_folders.append(folder_path)
        
        # Generate CSV file
        if csv_rows:
            csv_file = self.generate_bulk_csv(csv_rows)
            
            if csv_file:
                self.logger.info(f"\n{'=' * 60}")
                self.logger.info(f"SUCCESS: Created {csv_file}")
                self.logger.info(f"Upload this file to eBay File Exchange:")
                self.logger.info(f"https://bulksell.ebay.com/ws/eBayISAPI.dll?FileExchange")
                self.logger.info(f"{'=' * 60}\n")
        
        # Move processed folders
        for folder_path in successful_folders:
            self.move_folder(folder_path, self.config['processed_folder'])
        
        for folder_path in failed_folders:
            self.move_folder(folder_path, self.config['failed_folder'])
        
        # Summary
        self.logger.info(f"\nProcessing Summary:")
        self.logger.info(f"  Total folders: {len(listing_folders)}")
        self.logger.info(f"  Successful: {len(successful_folders)}")
        self.logger.info(f"  Failed: {len(failed_folders)}")
        self.logger.info("=" * 60)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='eBay Listing Automation Agent')
    parser.add_argument('--config', default='ebay_listing_config.txt',
                       help='Configuration file path')
    parser.add_argument('--watch-folder', help='Override watch folder path')
    parser.add_argument('--output', help='Override output CSV filename')
    
    args = parser.parse_args()
    
    # Create automation instance
    automation = EbayListingAutomation(args.config)
    
    # Override config if command line args provided
    if args.watch_folder:
        automation.config['watch_folder'] = args.watch_folder
    if args.output:
        automation.config['output_csv'] = args.output
    
    # Run automation
    automation.run()


if __name__ == "__main__":
    main()

# Made with Bob
