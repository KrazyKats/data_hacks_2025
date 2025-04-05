import os

def rename_images_in_datasets(base_path):
    datasets_path = os.path.join(base_path, "../Datasets")
    for root, dirs, files in os.walk(datasets_path):
        folder_name = os.path.basename(root)
        image_counter = 1
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                old_file_path = os.path.join(root, file)
                new_file_name = f"{folder_name}_image_{image_counter}.jpeg"
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)
                image_counter += 1

if __name__ == "__main__":
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Datasets"))
    rename_images_in_datasets(base_path)