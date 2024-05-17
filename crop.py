import pymupdf


def crop(file, key_string, output_path):
    try:
        pages_with_key = []

        doc = pymupdf.open(file)

        for page in doc:
            areas = page.search_for(key_string)
            if len(areas) > 0:
                pages_with_key.append(page.number)

        if len(pages_with_key) > 0:
            doc.select(pages_with_key)
            doc.save(output_path)

            doc.close()
            return True
        else:
            doc.close()
            return False
    except FileNotFoundError:
        print(f"Error: the file {file} was not found")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    

    
