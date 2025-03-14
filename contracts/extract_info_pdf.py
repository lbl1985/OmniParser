import fitz  # PyMuPDF
import re
import os
import json
import pandas as pd

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF file"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def extract_contract_info(text):
    """Extract key contract information using regex"""
    contract_info = {
        "contract_date": None,
        "machine_model": None,
        "material": None,
        "output": None,
        "fineness": None,
        "machine_price": None
    }
    
    # Extract contract date
    date_match = re.search(r"签订时间[:：\s]*(\d{4}-\d{1,2}-\d{1,2})", text)
    if date_match:
        contract_info["contract_date"] = date_match.group(1)
    
    # Extract machine model
    model_match = re.search(r"主机型号[:：\s]*(JYNU[\w\-\d]+)", text)
    if model_match:
        contract_info["machine_model"] = model_match.group(1)
    
    # Extract material to be processed
    material_match = re.search(r"粉碎物质[:：\s]*([\w\u4e00-\u9fa5]+)", text)
    if material_match:
        contract_info["material"] = material_match.group(1)
    
    # Extract output capacity (e.g., 100 公斤/小时)
    output_match = re.search(r"产量[:：\s]*(\d+)\s*公斤/小时", text)
    if output_match:
        contract_info["output"] = output_match.group(1) + " 公斤/小时"
    
    # Extract fineness (e.g., 97% 过 80-120 目)
    fineness_match = re.search(r"细度[:：\s]*(\d+%)\s*过\s*(\d+-\d+)\s*目", text)
    if fineness_match:
        contract_info["fineness"] = f"{fineness_match.group(1)} 过 {fineness_match.group(2)} 目"
    
    # Extract machine price
    price_match = re.search(r"主机价格[:：\s]*(\d{1,3}(,\d{3})*|\d+)\s*元", text)
    if price_match:
        contract_info["machine_price"] = price_match.group(1).replace(",", "") + " 元"
    
    return contract_info

def analyze_pdfs_in_folder(folder_path, output_json="contracts.json", output_csv="contracts.csv"):
    """Analyze all PDFs in a folder and save the extracted data"""
    results = []
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file_name)
            print(f"Processing: {file_name}")
            text = extract_text_from_pdf(pdf_path)
            contract_data = extract_contract_info(text)
            contract_data["file_name"] = file_name  # Add filename for reference
            results.append(contract_data)
    
    # Save results to JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    
    print(f"Results saved to {output_json} and {output_csv}")
    return results

# Example usage:
# analyze_pdfs_in_folder("./contracts")
