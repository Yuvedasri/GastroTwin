"""
Kvasir Dataset v2 - Data Exploration Script
This script performs comprehensive analysis of the gastroenterology image dataset
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter

# Configuration
DATASET_PATH = "DATA/kvasir-dataset-v2"


def step1_list_classes():
    """Step 1: List all classes in the dataset"""
    print("="*50)
    print("STEP 1: Dataset Classes")
    print("="*50)
    
    classes = sorted(os.listdir(DATASET_PATH))
    print(f"Number of classes: {len(classes)}\n")
    print("Classes:")
    for cls in classes:
        print(f"  - {cls}")
    print()
    return classes


def step2_count_images(classes):
    """Step 2: Count images in each class"""
    print("="*50)
    print("STEP 2: Image Count per Class")
    print("="*50)
    
    print(f"{'Class':<30}{'Images':>10}")
    print("-"*45)
    
    class_counts = {}
    for cls in classes:
        cls_path = os.path.join(DATASET_PATH, cls)
        
        if os.path.isdir(cls_path):
            count = len([
                f for f in os.listdir(cls_path)
                if f.endswith((".jpg", ".jpeg", ".png"))
            ])
            class_counts[cls] = count
            print(f"{cls:<30}{count:>10}")
    
    print(f"\n{'Total Images:':<30}{sum(class_counts.values()):>10}")
    print()
    return class_counts


def step3_visualize_samples(classes):
    """Step 3: Visualize sample images from each class"""
    print("="*50)
    print("STEP 3: Visualizing Sample Images")
    print("="*50)
    
    plt.figure(figsize=(16, 10))
    
    for i, cls in enumerate(classes):
        cls_path = os.path.join(DATASET_PATH, cls)
        
        images = [
            f for f in os.listdir(cls_path)
            if f.endswith(".jpg")
        ]
        
        if images:
            img_path = os.path.join(cls_path, images[0])
            img = Image.open(img_path)
            
            plt.subplot(2, 4, i+1)
            plt.imshow(img)
            plt.title(cls, fontsize=10)
            plt.axis("off")
    
    plt.tight_layout()
    plt.savefig("sample_images.png", dpi=150, bbox_inches='tight')
    print("Sample images saved as 'sample_images.png'")
    plt.show()
    print()


def step4_get_image_sizes(classes):
    """Step 4: Get image dimensions for each class"""
    print("="*50)
    print("STEP 4: Image Dimensions")
    print("="*50)
    
    print(f"{'Class':<30}{'Size (W x H)':>15}")
    print("-"*50)
    
    sizes = {}
    for cls in classes:
        cls_path = os.path.join(DATASET_PATH, cls)
        
        if os.path.isdir(cls_path):
            images = [
                f for f in os.listdir(cls_path)
                if f.endswith(".jpg")
            ]
            
            if images:
                img = Image.open(os.path.join(cls_path, images[0]))
                sizes[cls] = img.size
                print(f"{cls:<30}{str(img.size):>15}")
    
    print()
    return sizes


def step5_create_dataframe(classes):
    """Step 5: Create a comprehensive metadata DataFrame"""
    print("="*50)
    print("STEP 5: Creating Metadata DataFrame")
    print("="*50)
    
    data = []
    
    for cls in classes:
        cls_path = os.path.join(DATASET_PATH, cls)
        
        if os.path.isdir(cls_path):
            for img in os.listdir(cls_path):
                if img.endswith(".jpg"):
                    data.append({
                        "Image_Name": img,
                        "Disease": cls,
                        "Image_Path": os.path.join(cls_path, img)
                    })
    
    df = pd.DataFrame(data)
    
    print("Sample rows:")
    print(df.head(10))
    print(f"\nTotal Images: {len(df)}")
    print(f"Total Classes: {df['Disease'].nunique()}")
    print()
    
    return df


def step6_save_metadata(df):
    """Step 6: Save metadata to CSV"""
    print("="*50)
    print("STEP 6: Saving Metadata")
    print("="*50)
    
    csv_path = "kvasir_metadata.csv"
    df.to_csv(csv_path, index=False)
    print(f"✓ Metadata saved to '{csv_path}'")
    print(f"  - Total records: {len(df)}")
    print(f"  - Columns: {list(df.columns)}")
    print()


def print_summary(class_counts, sizes):
    """Print final summary statistics"""
    print("="*50)
    print("DATASET SUMMARY")
    print("="*50)
    
    total_images = sum(class_counts.values())
    avg_images = total_images / len(class_counts)
    
    print(f"Total Classes: {len(class_counts)}")
    print(f"Total Images: {total_images}")
    print(f"Average Images per Class: {avg_images:.1f}")
    print(f"Min Images in Class: {min(class_counts.values())}")
    print(f"Max Images in Class: {max(class_counts.values())}")
    
    # Check if all images have same size
    unique_sizes = set(sizes.values())
    if len(unique_sizes) == 1:
        print(f"All images have uniform size: {list(unique_sizes)[0]}")
    else:
        print(f"Multiple image sizes detected: {len(unique_sizes)} different sizes")
    
    print("\n✓ Data exploration complete!")
    print("="*50)


def main():
    """Main execution function"""
    print("\n" + "="*50)
    print("KVASIR DATASET v2 - DATA EXPLORATION")
    print("="*50 + "\n")
    
    # Execute all steps
    classes = step1_list_classes()
    class_counts = step2_count_images(classes)
    step3_visualize_samples(classes)
    sizes = step4_get_image_sizes(classes)
    df = step5_create_dataframe(classes)
    step6_save_metadata(df)
    print_summary(class_counts, sizes)


if __name__ == "__main__":
    main()
