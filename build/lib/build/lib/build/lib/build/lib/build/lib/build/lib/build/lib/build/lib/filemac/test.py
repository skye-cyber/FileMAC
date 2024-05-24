from pdf2image import convert_from_path


def doc2image(path):
    # Convert the PDF to a list of PIL image objects
    print("Generate image objects ..")
    images = convert_from_path(path)

    # Save each image to a file
    fname = path[:-4]
    print(f"\033[93mTarget images number\033[94m {len(images)}\033[0m")
    for i, image in enumerate(images):
        image.save(f"{fname}_{i+1}.png")
    print("\033[92mOk\033[0m")


doc2image('/media/skye/Skye/FileMAC/filemac/SPC 2402 AND ECE 2422 Human Computer Interaction Year 2 Semester 1.pdf')
