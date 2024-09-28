import glob

from langchain_community.document_loaders import PyPDFLoader

def get_file_list(directory_path):
    path = f"{directory_path}/*"
    return glob.glob(path)

# PDF
def load_knowledge_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return pages

def load_all_pdf_knowledges(directory_path):
    file_list = get_file_list(directory_path)
    pdf_list = [file for file in file_list if file.endswith(".pdf")]

    knwoledges = []
    for pdf in pdf_list:
        pages = load_knowledge_from_pdf(pdf)
        knwoledges.extend(pages)

    return knwoledges

# other loader types
def load_knowledge_from_txt(txt_path):
    pass

def load_all_txt_knowledges(directory_path):
    file_list = get_file_list(directory_path)
    pass
