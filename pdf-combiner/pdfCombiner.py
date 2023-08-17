import os
import PyPDF2


def parse_page_range(page_range_str):
    # Include all pages
    page_range_str = page_range_str.lower().replace(" ", "")
    if page_range_str == 'all':
        return None
    # When there's a section in page range (Not commonly used)
    elif ',' in page_range_str:
        page_list = []
        segments = page_range_str.split(',')
        for segment in segments:
            if '-' in segment:
                start, end = map(int, segment.split('-'))
                page_list.append([start-1, end])
            else:
                page_list.append([int(segment)-1, int(segment)])
        
        page_list.append(-1)
        print(page_list)
        return page_list
    # A range
    elif '-' in page_range_str:
        start, end = map(int, page_range_str.split('-'))
        return [start-1, end]
    # A specific page
    else:
        return [int(page_range_str)-1, int(page_range_str)]


def combine_pdfs(input_folder, input_pages, output_pdf):
    pdf_merger = PyPDF2.PdfMerger()

    for pdf_file, page_range in input_pages.items():
        pdf_path = os.path.join(input_folder, pdf_file)

        with open(pdf_path, 'rb') as pdf_file:
            #pdf_merger.append(pdf_path)
            page_number = parse_page_range(page_range)
            #page_number = None
            try:
                if page_number[-1] == -1:
                    for segment in page_number:
                        if segment == -1:
                            continue
                        print(f"Appending segment: {segment}")
                        pdf_merger.append(pdf_file, pages=segment)

                else:
                    pdf_merger.append(pdf_file, pages=page_number)
            except IndexError:

                return 0
            
                # 
                '''
                
                print(f"There is a problem in the page number of file: {pdf_path}.\n")
                val = input("Please enter 1 if you want to skip that file and continue combining OR other keys if you wanna terminate the program\n")
                if val == 1:
                    continue
                else:
                    print("Program terminated.")
                    return
                '''



    output_path = os.path.join(input_folder, output_pdf)
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)

    print(f'Combined PDFs from {input_folder} into {output_path}')

    return 1


if __name__ == '__main__':
    # Input folder containing PDF files
    input_folder = "D:\PDF"

    # Dictionary of page ranges for each input PDF file in the folder
    # Format: {'input1.pdf': '1-2', 'input2.pdf': '1-2,3', ...}
    input_pages = {
        #'0.pdf': '1-2, 4-5',
        '1.pdf': '1-2,4-5',
        '2.pdf': '1,3'
    }

    # Output PDF file path
    output_pdf = 'combined_output_test.pdf'

    combine_pdfs(input_folder, input_pages, output_pdf)

    for page_number in input_pages.values():
        print(parse_page_range(page_number))
