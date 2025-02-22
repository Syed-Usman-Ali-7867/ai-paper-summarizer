from django.core.files.base import ContentFile
from django.shortcuts import render
import fitz
from transformers import pipeline
from django.core.files.storage import default_storage

# Load Huggingface summarization pipeline
summarizer = pipeline(
    "summarization",
    model="t5-small",
    revision="df1b051"
)

def home(request):
    return render(request, 'home.html')

def form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        uploaded_file = request.FILES.get('file')

        if title and uploaded_file:
            # Save file temporarily
            file_path = default_storage.save(f"uploads/{uploaded_file.name}", uploaded_file)
            full_path = default_storage.path(file_path)

            # Extract text and summarize
            extracted_text = extract_text_from_pdf(full_path)
            summary = summarize_text(extracted_text)

            # Clean up
            default_storage.delete(file_path)

            # Pass context to form.html
            return render(request, 'form.html', {
                'success': True,
                'title': title,
                'summary': summary
            })

    return render(request, 'form.html')


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def summarize_text(text):
    """Summarize the extracted text using Huggingface transformers."""
    if len(text) > 1000:
        text = text[:1000]  # Limit input size for summarization
    try:
        summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error summarizing text: {str(e)}"

