import urllib.request
import os

DOCUMENTS = [
    {
        "url": "https://applications.emro.who.int/dsaf/dsa234.pdf",
        "filename": "WHO_hypertension_clinical_guidelines.pdf",
        "description": "WHO Clinical Guidelines for Management of Hypertension"
    },
    {
        "url": "https://applications.emro.who.int/dsaf/dsa509.pdf",
        "filename": "WHO_diabetes_management_standards.pdf",
        "description": "WHO Management of Diabetes Mellitus — Standards of Care"
    },
    {
        "url": "https://apps.who.int/iris/bitstream/handle/10665/204871/9789241565257_eng.pdf",
        "filename": "WHO_global_report_diabetes.pdf",
        "description": "WHO Global Report on Diabetes"
    },
    {
        "url": "https://www.who.int/docs/default-source/ncds/diabetes-training-manual.pdf",
        "filename": "WHO_diabetes_training_manual.pdf",
        "description": "WHO Diabetes Training Manual — NCD Package"
    },
    {
        "url": "https://cdn.who.int/media/docs/default-source/ncds/ncd-surveillance/guidance-on-global-monitoring-for-diabetes.pdf",
        "filename": "WHO_diabetes_monitoring_guidance.pdf",
        "description": "WHO Guidance on Global Monitoring for Diabetes Prevention"
    },
]

output_folder = "data/sample_docs"
os.makedirs(output_folder, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print("Downloading real WHO medical documents...\n")

for doc in DOCUMENTS:
    filepath = os.path.join(output_folder, doc["filename"])
    print(f"Downloading: {doc['description']}")
    try:
        req = urllib.request.Request(doc["url"], headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()
            # Verify it's actually a PDF
            if content[:4] == b'%PDF':
                with open(filepath, "wb") as f:
                    f.write(content)
                size_kb = len(content) // 1024
                print(f"  ✅ {doc['filename']} ({size_kb} KB)\n")
            else:
                print(f"  ❌ Got HTML instead of PDF — skipping\n")
    except Exception as e:
        print(f"  ❌ Failed: {e}\n")

print("\nFiles in data/sample_docs/:")
for f in os.listdir(output_folder):
    size = os.path.getsize(os.path.join(output_folder, f)) // 1024
    print(f"  {f} ({size} KB)")