from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import time

from PyPDF2 import PdfFileWriter, PdfFileReader


DEFAULT_INCOMING_DIR = os.path.abspath("./")
DEFAULT_OVERLAY_FILENAME = "overlay.pdf"
DEFAULT_OUTPUT_DIR = "pseudo-anonymised - {timestamp}".format(timestamp=time.strftime("%Y-%m-%d %H%M%S"))


def anonymise_pdf(input_file, overlay_path, output_file):

    output = PdfFileWriter()
    incoming = PdfFileReader(open(input_file, "rb"))
    anon_overlay = PdfFileReader(open(overlay_path, "rb"))

    overlay_page_count = anon_overlay.getNumPages()

    # Copy all pages from incoming to output
    for i in range(incoming.getNumPages()):
        output.addPage(incoming.getPage(i))

        overlay_index = min(i, overlay_page_count - 1)
        output.getPage(i).mergePage(anon_overlay.getPage(overlay_index))

    output_stream = open(output_file, "wb")
    output.write(output_stream)
    output_stream.close()


def ensure_output_directory_exists(output_dir):

    if not os.path.exists(output_dir):
        # Make the output directory
        os.mkdir(output_dir)


def anonymise_pdfs(in_dir, overlay_path, output_dir):

    if not os.path.exists(DEFAULT_OVERLAY_FILENAME):
        print("No overlay.pdf was found. Please create one and then try running the tool again")
        return 1

    print("Anonymising incoming files...")
    start_time = time.time()

    file_count = 0
    overlay_filename = os.path.basename(overlay_path)

    for filename in os.listdir(in_dir):
        if filename.endswith(".pdf") and not filename == overlay_filename:
            ensure_output_directory_exists(output_dir)
            in_file = os.path.join(in_dir, filename)
            out_filename = filename.replace(".pdf", ".pseudo-anonymised.pdf")
            out_file = os.path.join(output_dir, out_filename)
            print("Processing '{in_file}', saving to '{out_file}'".format(in_file=filename, out_file=out_file))
            anonymise_pdf(in_file, overlay_path, out_file)
            file_count += 1

    if file_count == 0:
        print("No files were found")
    else:
        duration = (time.time() - start_time)
        print("Pseduo-anonymised {count} files, in {dur:.2f} seconds".format(count=file_count, dur=duration))
    return 0


if __name__ == "__main__":

    print("PDF Pseudo Anonymisation Tool")
    print("This tool overlays all PDFs in the current directory with the contents of overlay.pdf. These "
          "psuedo-anonymised PDFs are then saved to a folder called 'pseudo-anonymised - DATE TIME'")
    print("None of the original files are edited in anyway.")
    print("")
    result = anonymise_pdfs(DEFAULT_INCOMING_DIR, DEFAULT_OVERLAY_FILENAME, DEFAULT_OUTPUT_DIR)
    print("Finished")

    input("Press ENTER to close")
    exit(result)
