import fitz  # PyMuPDF
import pathlib
import google.generativeai as genai
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# Configure Google Gemini API
GOOGLE_API_KEY = 'AIzaSyAzAL_9-I2W2DYTt-6FeJkDyHyvXlNSAT4'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    pdf_document = fitz.open(file_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def generate_response(pdf_text, criteria):
    """Generate content based on the PDF text and user-provided criteria."""
    prompt = f"PDF Text: {pdf_text}\nCriteria: {criteria}\nTell me probability(in number 0 - 100 too) how much is this good for my criteria and some summary(in under 150 words),in this format ({'Probability': '', 'Summary': ''})"
    response = model.generate_content(prompt)

    if hasattr(response, 'content'):
        return response.content
    return str(response)
    
    # Construct JSON summary
    summary = {
        "summary": content.strip()
    }
    
    return summary


@app.post("/process-pdf")
async def generate_content(file: UploadFile = File(...), criteria: str = Form(...)):
    # Save the uploaded file temporarily
    file_location = f"./{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    
    try:
        # Extract text from the PDF
        pdf_text = extract_text_from_pdf(file_location)
        
        # Generate response based on the PDF text and criteria
        response = generate_response(pdf_text, criteria)
        
        # Return the response
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporarily saved file
        pathlib.Path(file_location).unlink()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
